# Roadmap

> **Thin by design.** Sequence and gates only. Decisions live in `NEXT-3-DECISIONS.md`. Track shapes live in `B-PROPOSAL.md` + per-agent `agents/<agent>/`. This file restates nothing; it sequences. v0.1, S58 (2026-05-25).

## Where we are right now

- **Kernel built:** MODE-contract (per-agent `MODE` + append-only `flip-history.jsonl` + read-discipline + flip gates), repo-level `./killswitch`, `ROLLBACK.md` contract.
- **Tracks at `auto`:** 0 / 2 needed for v1.0.
- **Agents wired:** 1 (B-1 customer-interviewer at v0.2; sweep 2026-05-25 surfaced 3 falsifier spec bugs + 1 timestamp anomaly → v0.3 amendment drafted, awaiting cross-op review).
- **Real campaign data:** 1 marked-sent (prospect-0003 Max, 2026-05-19). 0 replies. n far below any falsifier threshold.
- **Posture:** private + invited early-access (≤5 testers).

## The trigger that ends v0 (from `README.md`)

v1.0 = **≥2 tracks step→auto with cross-operator review + clean audit logs.** Public-flip then becomes operator-judgment per `NEXT-3-DECISIONS.md` Decision 3.

## Prereq ladder (from `B-PROPOSAL.md` § Hard prereqs)

The B-track set (the actual automated-business-builder) is gated on four prereqs. Lift order is operator's call; cheapest-first listed:

| # | Prereq | Where it lives | Cost shape |
|---|---|---|---|
| 1 | ≥2 PCLA tracks demo-stable | PCLA repo (`modes.yaml`) | Currently 1 (A-3) + 1 retroactive-provisional (A-6); cheapest lift = discharge A-6 cross-op review by 2026-05-31 deadline |
| 2 | Eve / Mark / external availability | Operator outreach | Days |
| 3 | A-1 phase-transition-auto lands | PCLA (`tracks/06-phase-transition-auto/`) | Engineering weeks; provides Surface-Compliance substrate every B-track depends on |
| 4 | Hosted-infra eng project funded | External (money + months) | Polsia's actual moat; bigger than all 8 B-tracks combined |

**Note on prereq-vs-substance.** Discharging #1 (A-6 graduation) is a checkbox lift that doesn't move V-A behavior. #3 (A-1) is the only PCLA-side prereq that's substantively load-bearing for B-tracks. Track checkbox lifts in PCLA, not here.

## Track ladder (from `B-PROPOSAL.md` § Phasing — DO NOT begin without re-reading hard prereqs)

The 8 B-tracks group by gate cost. Each phase is authorized only after prior phase demonstrates the falsifier-per-track pattern catches what it's supposed to catch.

| Phase | Tracks | Why these together |
|---|---|---|
| **B-α** (cheap, validate pattern) | B-1 customer-interview-runner, B-8 metrics-watchdog | Text/read-only; low-stakes; falsifier-pattern proof |
| **B-β** (outputs, operator-approve) | B-2 landing-page-deployer, B-7 support-triage | Visible outputs; operator-supervised; no money spent |
| **B-γ** (outputs that spend money) | B-3 cold-outreach, B-4 ads-pilot, B-5 code-deploy | Real-world consequences if falsifiers fail |
| **B-δ** (inbound high-stakes) | B-6 inbox-triage | Worst-case = hallucinated VC term-sheet signed in agent's voice |

**Current track state:**

| Track | State | Notes |
|---|---|---|
| B-1 | v0.2 shipped; v0.3 amendment DRAFT | MODE=step; 1 real send; 5 drafts in log; falsifier sweep run 2026-05-25 |
| B-2 | DESIGN-SKETCH | Gated on hard prereqs; do NOT promote to SPEC |
| B-3..B-8 | one-line in B-PROPOSAL | Paper-only |

## Suggested sequencing (operator's call; not authorization)

The lift sequence isn't fixed; it depends on which gates are cheapest to lift in any given week. Plausible orderings:

1. **Substance-first:** B-1 campaign run to falsifier-evaluable n (≥10 sends; needs operator outreach cadence) → real evidence the discipline catches Surface-Compliance → second track (B-8 or B-2-when-gated) → v1.0 trigger met.
2. **Checkbox-first:** PCLA prereq #1 discharged via A-6 cross-op review → PCLA flipped-track count 1→2 → one B-PROPOSAL hard prereq ticked → A-1 work begins → eventual B-track unlock.
3. **External-leverage-first:** Prereq #2 (commission Eve/Mark) → cross-op queue capacity for whichever artifact comes next.

Tradeoff: substance-first generates real evidence but stalls on operator outreach cadence; checkbox-first moves the count without moving the product; external-leverage-first amplifies whichever path is chosen next.

## What this roadmap is NOT

- **Not a Gantt.** No dates beyond hard deadlines already in source documents (A-6 provisional → 2026-05-31).
- **Not authorization.** Track promotions (sketch → SPEC, SPEC → impl, step → auto) require their own gates per `B-PROPOSAL.md`, `MODE-CONTRACT.md`, and `README.md`.
- **Not a decision list.** Decisions live in `NEXT-3-DECISIONS.md`; this file follows them.
- **Not substrate.** Track shapes live in `B-PROPOSAL.md` + per-agent dirs; this file points, doesn't restate.

## Falsifier (for this document)

This file is **doing its job** if a new session can read it once and pick up the work without re-reading every adjacent doc.

This file has **failed** if:
- It accumulates phases beyond B-α / β / γ / δ (we have a 5th phase = scope creep, not roadmap completion).
- It survives more than 3 sessions without any state field updating (current-state block goes stale → fictional roadmap).
- Track-shape detail starts leaking back into this file (we're rebuilding `B-PROPOSAL.md` here = duplication; delete this file before that happens).
- It tries to predict when a prereq will lift (timing prediction is Gantt-thinking; we don't do that).

## Cross-references

- v1.0 trigger: `README.md`
- Hard prereqs + B-track shapes + phasing: `B-PROPOSAL.md`
- Active decisions: `NEXT-3-DECISIONS.md`
- Mode-toggle kernel: `MODE-CONTRACT.md`
- Rollback contract: `ROLLBACK.md`
- B-1 agent: `agents/b1-customer-interviewer/README.md`
- B-2 staged: `B-2-DESIGN-SKETCH.md`
- PCLA strategic-layer side: `../prometheus-crystal-lab-auto/ROADMAP.md` (the discipline this layer is catching up to)

---

*Roadmap v0.1, S58 (2026-05-25). Thin by design. Delete if it fails the falsifier above.*
