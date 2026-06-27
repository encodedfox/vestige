# Postdict — the 60-second funding demo

**Audience:** investors. **Goal:** they see a category, a moat, and a market — not a feature.
**Thesis (say it in the first 10 seconds):** *the entire AI-memory industry is trapped in a category error.*

Format: live terminal, one take, you talking over it. ~60s. Punchy. No slides.

---

## THE SCRIPT (with what's on screen + what you say)

### [0:00–0:10] — THE CATEGORY ERROR (the hook that funds you)

**On screen:** a clean terminal, one line of text:
`Every AI memory company is solving the wrong problem.`

**You say:**
> "Every AI memory company — Mem0, Zep, all of them — is built on vector
> similarity search. They find what your problem *looks like*. But a root cause
> **never** looks like the bug it creates. So the entire industry is
> architecturally incapable of the one thing that matters most: finding *why*
> something broke. That's not a bug in their products. It's a category error in
> the whole field."

*(Pause. Let "category error" land. That's the sentence they'll repeat to their partners.)*

---

### [0:10–0:25] — THE SETUP (make the impossible concrete)

**On screen:** type these, real (this is a realistic history — a config change, an
old unrelated incident, and today's crash):
```
$ vestige ingest "Set API_TIMEOUT=2 in the deploy env" --ago-days 3            # the quiet cause
$ vestige ingest "500 error in the billing service" --ago-days 20             # an old lookalike
$ vestige ingest "Service crashed: 500 on the auth endpoint"                  # today's crash
```

**You say:**
> "Watch. Three days ago, a one-line config change — boring, forgotten. There's
> also an old 500 error in a different service, weeks back. And today, the auth
> service crashes. Now — which of those past memories caused today's crash? A
> vector database ranks by *resemblance*: today's crash *looks* most like that
> old billing 500. That's the trap. The thing that actually *looks* similar is
> never the cause."

---

### [0:25–0:45] — THE PROOF (split screen, the money shot)

**On screen:** `$ vestige backfill --contrast`  → it prints:
```
── 1. SIMILARITY SEARCH · keyword (BM25) ──
   → ranked by RESEMBLANCE. its top hit is a lookalike, not the cause.

── 2. POSTDICT (reach backward for the CAUSE) ──
   #1 Set API_TIMEOUT=2 in the deploy env
      ↩ reached back 3.0 days before the failure
      🔗 causal join: api_timeout
```

**You say (slow down here — this is the "holy shit" beat):**
> "Same query, same database. Similarity search returns the lookalike — it's
> confidently wrong. Postdict reaches **backward three days** and finds the
> actual cause. Not because it's *similar* — because it's *causally upstream*.
> This is memory with **hindsight**. The 'ohhh, *that's* why' moment — automatic."

---

### [0:45–0:55] — THE MOAT (why this isn't copyable in a weekend)

**You say:**
> "Two things make this defensible. One: it's a faithful port of a 2024 *Nature*
> result — the brain reaches backward in time to find causes, and it's
> *backward-only*, which is exactly correct because a root cause is always in the
> past. We didn't invent this. We ported the algorithm evolution already
> perfected. Two: the incumbents can't bolt this on — their entire architecture
> *is* the category error. To do this, you have to rebuild memory from the
> cognitive science up. We already did."

---

### [0:55–1:00] — THE ASK (category, market, check)

**On screen:** `the first memory that finds the cause, not the lookalike.`

**You say:**
> "Every agent that writes code, runs infra, or touches production hits root
> causes it can't explain — that's the entire agentic-AI market, and it's on
> fire. We're not a better memory. We're the first memory that *reasons backward*.
> It's local-first, running today, and the repo is reproducible. We're raising
> [X] to make every AI agent debug like a senior engineer. Run it yourself —
> the seed's in the repo."

---

## DELIVERY NOTES (the difference between "neat" and "funded")

1. **Lead with the category error, not the feature.** Investors fund categories.
   "The whole industry is wrong" is a thesis; "we reach back in time" is a feature.
   Say the thesis first, prove it with the feature.

2. **The one sentence to nail:** *"A root cause never looks like the bug it
   creates."* Memorize it. It's the entire investment thesis in nine words. It
   reframes a crowded market ("another memory startup") into an empty one ("the
   only one that finds causes").

3. **Slow down at 0:25–0:45.** The contrast is the proof. Let the
   `↩ reached back 3.0 days` line sit on screen for a full beat in silence.

4. **The moat answer is what closes.** Every investor will think "can't Mem0 just
   add this?" Answer it *before* they ask: their architecture IS the problem.
   That's why it took a from-scratch, neuroscience-grounded rebuild.

5. **End on market size, not the demo.** "Every agent that touches production" =
   the whole agentic market. The demo earns the right to say that; don't bury it.

6. **Reproducibility is the trust close.** "Run it yourself, seed's in the repo"
   is what separates you from every cherry-picked AI demo they've been burned by.

## THE THREE LINES THAT DO THE WORK

- **The hook:** "The entire AI-memory industry is trapped in a category error."
- **The thesis:** "A root cause never looks like the bug it creates."
- **The category:** "We're not a better memory. We're the first memory that reasons backward."
