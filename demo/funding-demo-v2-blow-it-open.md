# Postdict — the 60-second "blow it wide open" script

**Audience:** investors. **Goal:** they feel the pain, see the flawed axiom crack,
watch the impossible happen live, and understand the market is *everything*.
**Format:** live terminal, one take, you talking over it. ~60s.
**Rule:** ~20s of talk. The rest is the terminal doing the impossible.

> Why NOT "X companies got hacked": it's a commodity security-FUD hook, it needs a
> stat you can't cite live (which torches your credibility — your whole moat is
> *honest + reproducible*), and it shrinks you from "every agent in production" to
> "security." Instead, open with the wound every engineer in the room has lived.

---

## THE SCRIPT (what's on screen · what you say)

### [0:00–0:12] — THE WOUND (make them feel it personally)

**On screen:** a clean dark terminal, blinking cursor. Nothing else yet.

**You say (calm, then sharper):**
> "Every engineer in this room has lost a day to this: production breaks, and the
> cause turns out to be a one-line change you made days ago and never thought
> about again. The bug looked nothing like that change — so you never connected
> them. You just *suffered* until you stumbled onto it.
>
> Now we've handed that exact job to AI agents. And here's the problem—"

---

### [0:12–0:22] — THE FLAWED AXIOM (the line they repeat to their partners)

**On screen:** type one line:
`relevance ≠ resemblance`

**You say:**
> "—every AI memory framework on Earth, every VC-backed startup, every platform
> layer, is built on one flawed assumption: that **relevance equals resemblance.**
> They search memory for what *looks similar* to the problem. But **a root cause
> never looks like the bug it creates.** The entire industry is searching in the
> one place the answer can never be."

*(Beat. Let it sit.)*

---

### [0:22–0:35] — MAKE IT CONCRETE (type it live)

**On screen:**
```
$ postdict ingest "Set API_TIMEOUT=2 in the deploy env" --ago-days 3    # the quiet cause
$ postdict ingest "500 error in the billing service" --ago-days 20      # an old lookalike
$ postdict ingest "Service crashed: 500 on the auth endpoint"           # today's crash
```

**You say:**
> "Watch it happen. A one-line config change three days ago. An old, unrelated
> 500 error weeks back. And today — the auth service crashes. Which past memory
> caused it? To a vector database, today's crash looks most like that old billing
> 500. The thing that *looks* similar is never the thing that *caused* it."

---

### [0:35–0:50] — THE PROOF (the money shot · go silent on the reveal)

**On screen:** `$ postdict backfill --contrast` →
```
── 1. SIMILARITY SEARCH · keyword (BM25) ──
   1. 500 error in the billing service          ← top match   (WRONG)
   → ranked by RESEMBLANCE. its top hit is a lookalike, not the cause.

── 2. POSTDICT (reach backward for the CAUSE) ──
   #1 Set API_TIMEOUT=2 in the deploy env
      ↩ reached back 3.0 days before the failure
      🔗 causal join: api_timeout                            (RIGHT)
```

**You say (let `↩ reached back 3.0 days` hold in dead silence for a full second):**
> "Same database. Same question. Similarity search returns the lookalike —
> confident, and wrong. Postdict reaches **backward three days** and finds the
> actual cause. Not because it's similar — because it's **causally upstream.**
> That day you lost? Gone. It's instant now."

---

### [0:50–0:58] — THE MOAT (kill "can't they just add this?")

**You say:**
> "And they can't copy it. This is a faithful port of a 2024 *Nature* result —
> the brain reaches *backward* in time to find causes, backward-only, because a
> root cause is always in the past. The incumbents can't bolt this on; their
> whole architecture **is** the flawed axiom. You have to rebuild memory from the
> cognitive science up. We already did. It runs locally, today."

---

### [0:58–1:00] — THE ASK

**On screen:** `the first memory that finds the cause, not the lookalike.`

**You say:**
> "Every agent that touches production needs this. That's the whole market, and
> it's on fire. We're raising [X] to make every AI agent debug like a senior
> engineer. The seed's in the repo — run it yourself."

---

## DELIVERY — THE 6 RULES THAT MAKE IT LAND

1. **Open with the wound, not the product.** 0:00–0:12 is about *them*, not you.
   When an investor nods because they've lived it, you've already won the room.
2. **The monologue is ~20 seconds total.** Investors fund what they *see* work.
   Get to the terminal fast; the contrast carries the weight.
3. **Two sentences, memorized cold:** the axiom — *"They believe relevance equals
   resemblance."* The detonation — *"A root cause never looks like the bug it
   creates."* Everything else can be loose.
4. **Dead silence on the reveal (0:35–0:50).** When `↩ reached back 3.0 days`
   appears, say nothing for one full second. The screen sells it.
5. **Answer the moat before they ask it.** "Can't Mem0 add this?" — no, their
   architecture is the axiom. That sentence is what turns "neat" into "fundable."
6. **End on the market (TAM), not the feature.** "Every agent that touches
   production" is the size of the prize. The demo earned you the right to say it.

## THE THREE LINES THAT DO THE WORK
- **The wound:** "Production breaks, and the cause is a change you made days ago and forgot."
- **The detonation:** "A root cause never looks like the bug it creates."
- **The category:** "We're not a better memory. We're the first memory that reasons backward."

---

## NOTE ON THE BINARY

The script types `postdict` (the new name). The shipping binary is still `vestige`
today — for recording, either (a) `alias postdict=./target/release/vestige`, or
(b) record now with `vestige` and re-record after the rename. The on-screen output
is identical; only the command word differs.
