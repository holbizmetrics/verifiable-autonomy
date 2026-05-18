# Next 3 decisions

> **Not a Gantt. Not a roadmap.** Three calls that unblock everything downstream. When one resolves, this file updates. v1, S55 (2026-05-18).

## Decision 1: Path A / B / C (early-access posture)

**The call:** Does the repo stay fully private until 2 A-tracks flip (A), accept N≤5 invited early-access testers now (B), or split into public-manifesto + private-impl (C)?

**Owner:** operator.

**Info needed:**
- How soon you want real customer-dev pipeline. Days → B. Weeks-to-months → A. Want public discoverability without code → C.
- Risk tolerance for early-access drift (B's failure mode).

**What it unblocks:** any real-prospect send. Until Decision 1 is made, B-1 stays in draft-only mode regardless of draft quality.

**Substrate:** `SCOPING-PRODUCT-READINESS.md`. Agent lean: B.

---

## Decision 2: First real send (which prospect, when)

**The call:** Of the 3 current prospects (Stuart, Sarkar, Max), which gets the first real send, and what authorization threshold is met before send?

**Owner:** operator.

**Info needed (preconditions):**
- Decision 1 resolved (so the repo-link target exists).
- Draft chosen from `drafts/prospect-0003.md` v1 / v2 / v2.1 — or rewrite. Stuart + Sarkar not yet drafted.
- Contact actually found (Substack DM, DEV profile, IH DM, or flowly.run contact).
- Operator-side warm-reply workflow ready (replies go where, who classifies).

**What it unblocks:** first real-reply data. Falsifier 4 (reply rate <1% over n≥30) gets its first data point. ICP gets first real-world correction signal.

**Substrate:** `agents/b1-customer-interviewer/prospects.md` + drafts. Agent lean: Max v2.1, but only after Decision 1.

---

## Decision 3: Public-flip trigger

**The call:** At what evidence threshold does the repo flip private → public? Stricter than the current manifesto ("2 tracks flipped"), looser, or unchanged?

**Owner:** operator (with cross-operator review owed before any amendment).

**Info needed:**
- A-1 phase-transition-auto flip status (in PCLA — currently late-stage design).
- B-1 campaign data: n≥2 real campaigns ran, falsifiers did not fire.
- Cross-operator review verdict on B-1's discipline (currently only self-review).

**What it unblocks:** public launch. README rewrite from manifesto to product page. Discoverability. Open source license decision.

**Substrate:** `README.md` L11 (current trigger), PCLA `modes.yaml`, B-1 `falsifier.md`, `interview-log.jsonl`.

---

## Falsifier (for this document)

This file is **doing its job** if:
- Each decision resolves with a single operator call + a one-line update here.
- New ideas surfacing in conversation get parked against these 3 slots, not added as #4, #5, #6.

This file has **failed** if:
- It accumulates more than 3 slots (we're back to roadmap-shaped thinking, which is the failure mode we're avoiding).
- A real decision happens without being reflected here within one session.
- It survives unchanged for more than 2 sessions without any decision resolving (the work isn't actually waiting on these calls; the file is fictional).

---

*Next-3-decisions list. Update when one resolves. Delete the file if it stops being load-bearing.*
