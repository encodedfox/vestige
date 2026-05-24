import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = REPO_ROOT / "hooks" / "sanhedrin-local.py"


def load_sanhedrin():
    spec = importlib.util.spec_from_file_location("sanhedrin_local_under_test", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def patched_attr(obj, name, value):
    sentinel = object()
    old = getattr(obj, name, sentinel)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if old is sentinel:
            delattr(obj, name)
        else:
            setattr(obj, name, old)


class SanhedrinClaimModeTests(unittest.TestCase):
    def setUp(self):
        self.sanhedrin = load_sanhedrin()

    def run_main(self, draft):
        stdin = io.StringIO(draft)
        stdout = io.StringIO()
        with mock.patch.object(sys, "stdin", stdin), mock.patch.object(sys, "stdout", stdout):
            self.sanhedrin.main()
        return stdout.getvalue().strip()

    def test_plain_sam_biographical_achievement_claim_is_check_worthy(self):
        claims = self.sanhedrin.extract_check_worthy_claims(
            "Sam graduated from Example University and won the Example AI Challenge."
        )

        self.assertGreaterEqual(len(claims), 1)
        self.assertTrue(any(claim.sam_critical for claim in claims))
        self.assertTrue(
            any(claim.claim_class in {"BIOGRAPHICAL", "ACHIEVEMENT"} for claim in claims)
        )
        self.assertTrue(any("Sam" in claim.text for claim in claims))

    def test_zero_high_trust_evidence_on_sam_critical_claim_blocks(self):
        def fail_if_judge_is_called(_claim, _evidence):
            self.fail("zero-evidence absence decisions should not require model judgment")

        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ), patched_attr(self.sanhedrin, "judge_claim_with_model", fail_if_judge_is_called):
            out = self.run_main("Sam won first place at the Example AI Challenge.")

        result = json.loads(out)
        self.assertFalse(result["passed"])
        self.assertTrue(result["legacy_verdict"].startswith("no - "), result)
        self.assertEqual(result["verdicts"][0]["status"], "REFUTED_BY_ABSENCE")

    def test_vague_user_positive_claim_fails_closed(self):
        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ):
            out = self.run_main("Sam won a few competitions and earned some prize money.")

        result = json.loads(out)
        self.assertFalse(result["passed"], result)
        self.assertEqual(result["verdicts"][0]["claim"]["claim_class"], "VAGUE-QUANTIFIER")
        self.assertEqual(result["verdicts"][0]["status"], "REFUTED_BY_ABSENCE")

    def test_retrieval_failure_on_sam_critical_claim_fails_open(self):
        def fail_if_judge_is_called(_claim, _evidence):
            self.fail("retrieval failures should fail open before model judgment")

        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], False)
        ), patched_attr(self.sanhedrin, "judge_claim_with_model", fail_if_judge_is_called):
            out = self.run_main("Sam won first place at the Example AI Challenge.")

        result = json.loads(out)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["legacy_verdict"], "yes")
        self.assertEqual(result["verdicts"][0]["status"], "NEI")
        self.assertIn("retrieval unavailable", result["verdicts"][0]["reason"])

    def test_current_turn_attribution_discourse_is_not_absence_blocked(self):
        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ):
            out = self.run_main(
                "You asked me to audit the Sanhedrin hook, and I reviewed your requested changes."
            )

        result = json.loads(out)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["legacy_verdict"], "yes")
        self.assertEqual(result["claims_extracted"], 0)

    def test_discourse_framing_does_not_hide_embedded_sam_claim(self):
        examples = [
            "Per your request, Sam won first place at the Example AI Challenge.",
            "Sam won first place at the Example AI Challenge, which would be impressive.",
        ]
        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        for example in examples:
            with self.subTest(example=example), mock.patch.dict(os.environ, env, clear=False), patched_attr(
                self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
            ):
                out = self.run_main(example)

            result = json.loads(out)
            self.assertFalse(result["passed"], result)
            self.assertEqual(result["verdicts"][0]["status"], "REFUTED_BY_ABSENCE")
            self.assertIn("Sam won", result["verdicts"][0]["claim"]["text"])

    def test_leading_hypothetical_still_skips_embedded_claim(self):
        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ):
            out = self.run_main("If Sam wins first place next time, he could claim the prize.")

        result = json.loads(out)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["claims_extracted"], 0)

    def test_subject_modal_prefix_skips_without_hiding_asserted_claim(self):
        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ):
            nonassertive = self.run_main("Sam could win first place next time.")
            asserted = self.run_main(
                "Sam won first place at the Example AI Challenge and could collect prize money."
            )

        nonassertive_result = json.loads(nonassertive)
        asserted_result = json.loads(asserted)
        self.assertTrue(nonassertive_result["passed"], nonassertive_result)
        self.assertEqual(nonassertive_result["claims_extracted"], 0)
        self.assertFalse(asserted_result["passed"], asserted_result)
        self.assertEqual(asserted_result["verdicts"][0]["status"], "REFUTED_BY_ABSENCE")

    def test_malformed_deep_reference_response_fails_open(self):
        def fail_if_judge_is_called(_claim, _evidence):
            self.fail("malformed retrieval responses should fail open before model judgment")

        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        for response in ({}, {"status": "error"}, {"errors": ["timeout"]}):
            with self.subTest(response=response):
                def fake_post_json(_url, _body, _timeout):
                    return response

                with mock.patch.dict(os.environ, env, clear=False), patched_attr(
                    self.sanhedrin, "post_json", fake_post_json
                ), patched_attr(self.sanhedrin, "judge_claim_with_model", fail_if_judge_is_called):
                    out = self.run_main("Sam won first place at the Example AI Challenge.")

                result = json.loads(out)
                self.assertTrue(result["passed"], result)
                self.assertEqual(result["verdicts"][0]["status"], "NEI")
                self.assertIn("retrieval unavailable", result["verdicts"][0]["reason"])

    def test_non_critical_technical_zero_evidence_does_not_block(self):
        def fail_if_judge_is_called(_claim, _evidence):
            self.fail("zero-evidence technical claims should fail open without model judgment")

        env = {"VESTIGE_SANHEDRIN_CLAIM_MODE": "1", "VESTIGE_SANHEDRIN_OUTPUT": "json"}
        with mock.patch.dict(os.environ, env, clear=False), patched_attr(
            self.sanhedrin, "fetch_claim_evidence", lambda _claim: ([], True)
        ), patched_attr(self.sanhedrin, "judge_claim_with_model", fail_if_judge_is_called):
            out = self.run_main(
                "Qwen3.6-35B can be served through an OpenAI-compatible chat endpoint."
            )

        result = json.loads(out)
        self.assertTrue(result["passed"])
        self.assertEqual(result["legacy_verdict"], "yes")
        self.assertEqual(result["verdicts"][0]["status"], "NEI")
        self.assertEqual(result["verdicts"][0]["claim"]["claim_class"], "TECHNICAL")

    def test_fetch_evidence_truncates_on_python_character_boundary(self):
        emoji_out = self.sanhedrin.truncate_chars(("a" * 4) + "🙂" + "tail", 8)
        combining_out = self.sanhedrin.truncate_chars("Cafe\u0301 tail", 8)

        self.assertEqual(emoji_out, "aaaa🙂...")
        self.assertEqual(combining_out, "Cafe...")
        self.assertNotIn("\ufffd", emoji_out + combining_out)
        self.assertFalse(self.sanhedrin.unicodedata.combining(combining_out[-4]))
        (emoji_out + combining_out).encode("utf-8")

    def test_staged_evidence_is_used_without_smart_ingest_or_durable_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged_path = Path(tmp) / "sanhedrin-staged-evidence.json"
            staged = [
                {
                    "id": "samstage2",
                    "role": "memory",
                    "trust": 0.89,
                    "preview": "Sam's final result was second place with no payout.",
                }
            ]
            staged_path.write_text(json.dumps(staged), encoding="utf-8")

            post_urls = []

            def fake_post_json(url, body, _timeout):
                post_urls.append(url)
                if "smart_ingest" in url or "/api/memories" in url:
                    self.fail(f"staged evidence path attempted durable write to {url}: {body}")
                self.assertEqual(url, "http://127.0.0.1:3927/api/deep_reference")
                return {"confidence": 0.0, "evidence": []}

            env = {
                "VESTIGE_SANHEDRIN_CLAIM_MODE": "1",
                "VESTIGE_SANHEDRIN_OUTPUT": "json",
                "VESTIGE_SANHEDRIN_STAGE_FILE": str(staged_path),
            }
            with mock.patch.dict(os.environ, env, clear=False), patched_attr(
                self.sanhedrin, "post_json", fake_post_json
            ), patched_attr(self.sanhedrin, "VESTIGE_ENDPOINT", "http://127.0.0.1:3927/api/deep_reference"):
                out = self.run_main("Sam won first place and earned prize money.")

        result = json.loads(out)
        verdict = result["verdicts"][0]
        self.assertFalse(result["passed"], result)
        self.assertEqual(result["staged_evidence_count"], 1)
        self.assertEqual(verdict["status"], "REFUTED_BY_ABSENCE")
        self.assertEqual(verdict["durable_evidence_count"], 0)
        self.assertEqual(verdict["high_trust_evidence_count"], 1)
        self.assertEqual(post_urls, ["http://127.0.0.1:3927/api/deep_reference"])

    def test_staged_only_refuted_verdict_is_downgraded_without_durable_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged_path = Path(tmp) / "sanhedrin-staged-evidence.json"
            staged_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "stage-tech",
                            "trust": 0.95,
                            "preview": "Qwen3.6-35B cannot be served through a chat endpoint.",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            def fake_post_json(url, _body, _timeout):
                if url == self.sanhedrin.VESTIGE_ENDPOINT:
                    return {"confidence": 0.0, "evidence": []}
                if url == self.sanhedrin.SANHEDRIN_ENDPOINT:
                    return {
                        "choices": [
                            {
                                "message": {
                                    "content": json.dumps(
                                        {
                                            "status": "REFUTED",
                                            "class": "TECHNICAL",
                                            "reason": "Staged evidence contradicts the claim.",
                                            "evidence_ids": ["stage-tech"],
                                        }
                                    )
                                }
                            }
                        ]
                    }
                self.fail(f"unexpected post_json URL: {url}")

            env = {
                "VESTIGE_SANHEDRIN_CLAIM_MODE": "1",
                "VESTIGE_SANHEDRIN_OUTPUT": "json",
                "VESTIGE_SANHEDRIN_STAGE_FILE": str(staged_path),
            }
            with mock.patch.dict(os.environ, env, clear=False), patched_attr(
                self.sanhedrin, "post_json", fake_post_json
            ):
                out = self.run_main(
                    "Qwen3.6-35B can be served through an OpenAI-compatible chat endpoint."
                )

        result = json.loads(out)
        verdict = result["verdicts"][0]
        self.assertTrue(result["passed"], result)
        self.assertEqual(verdict["status"], "NEI")
        self.assertEqual(verdict["durable_evidence_count"], 0)
        self.assertIn("Durable evidence required", verdict["reason"])

    def test_staged_only_legacy_refuted_line_is_downgraded_without_durable_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged_path = Path(tmp) / "sanhedrin-staged-evidence.json"
            staged_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "stage-tech",
                            "trust": 0.95,
                            "preview": "Qwen3.6-35B cannot be served through a chat endpoint.",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            def fake_post_json(url, _body, _timeout):
                if url == self.sanhedrin.VESTIGE_ENDPOINT:
                    return {"confidence": 0.0, "evidence": []}
                if url == self.sanhedrin.SANHEDRIN_ENDPOINT:
                    return {
                        "choices": [
                            {
                                "message": {
                                    "content": (
                                        "no - [Sanhedrin Veto] [TECHNICAL]: "
                                        "Staged evidence contradicts the claim."
                                    )
                                }
                            }
                        ]
                    }
                self.fail(f"unexpected post_json URL: {url}")

            env = {
                "VESTIGE_SANHEDRIN_CLAIM_MODE": "1",
                "VESTIGE_SANHEDRIN_OUTPUT": "json",
                "VESTIGE_SANHEDRIN_STAGE_FILE": str(staged_path),
            }
            with mock.patch.dict(os.environ, env, clear=False), patched_attr(
                self.sanhedrin, "post_json", fake_post_json
            ):
                out = self.run_main(
                    "Qwen3.6-35B can be served through an OpenAI-compatible chat endpoint."
                )

        result = json.loads(out)
        verdict = result["verdicts"][0]
        self.assertTrue(result["passed"], result)
        self.assertEqual(verdict["status"], "NEI")
        self.assertEqual(verdict["durable_evidence_count"], 0)
        self.assertIn("Durable evidence required", verdict["reason"])

    def test_current_turn_discourse_patterns_are_not_claims(self):
        examples = [
            "You asked for maximum subagents, so I audited the hook.",
            "Your request was to verify the installer env preservation.",
            "Per your request, I reviewed the Sanhedrin stop hook.",
            "Sam asked me to go all in on the Sanhedrin patch.",
            "The user requested maximum subagents for this implementation.",
        ]
        for example in examples:
            with self.subTest(example=example):
                self.assertEqual(self.sanhedrin.extract_check_worthy_claims(example), [])


if __name__ == "__main__":
    unittest.main()
