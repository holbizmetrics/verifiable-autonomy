# Roadmap

> **Thin by design.** Sequence and gates only. Decisions live in `NEXT-3-DECISIONS.md`. Track shapes live in `B-PROPOSAL.md` + per-agent `agents/<agent>/`. This file restates nothing; it sequences. v0.3, 2026-06-23 — factory-v0.1-shipped state-sync. (v0.2, S58 2026-05-25 — factory-frame correction.)

## What we're actually building

A **verifiable business factory**: a system that, given a business spec, instantiates a deployable, auditable automated business. ("Automated" is **build-time** today — the factory builds the instance; the instance is operator-run. Run-time autonomy is a deferred layer; see `factory/SPEC.md`.) The product is the factory. Each factory output is a separate automated business instance, each itself verifiable (MODE-contract, falsifiers, audit logs, killswitch). The factory itself is mechanism-verifiable (did it deploy? are the audit logs balanced?); the business-success of each output stays dark-zone (the market verifies it, over time — that part stays with the operator forever, by design).

**What the B-tracks are.** B-1..B-8 are **business primitives** — the reusable capabilities any one instance composes (talk to customers, ship a landing page, run ads, deploy code, etc.). Shipping all 8 at autonomy gives you **one** automated business, not a factory. The factory layer (orchestration, business-spec schema, instance isolation, multi-tenant operator-attention router) is the layer **above** B-PROPOSAL that does not yet exist in this repo.

**Method: verifier-engineering, not factory-first.** "Create a business" is dark-zone (no built-in verifier, no terminal state). Building the factory abstraction before there is one working instance leaves the AI to wander through the unspecified middle. The path that does not drift is: do ONE concrete business end-to-end first, with checkable milestones at each step (each milestone IS the verifier the open-ended task is missing), THEN generalize the working instance into the factory. V-A's own go-to-market is that first instance.

## First-instance checkable milestones (the gradient)

Concrete, terminal, checkable. Each is the "done" the open-ended task lacks. Each unblocks the next.

| # | Milestone | Verifier (when is it "done") |
|---|---|---|
| M1 | Market identified | One ICP doc with ≥5 verbatim pain phrases sourced from real prospect material (not invented). **`agents/b1-customer-interviewer/icp.md` is the artifact.** State: shipped. |
| M2 | Offer defined | One paragraph + one price + one promise the offer is falsifiable against. **Artifact: a one-page offer doc in repo.** State: not started. |
| M3 | Landing page live | One URL hosting the offer; can be reached from the public internet; has a working signup/contact path. State: not started. |
| M4 | First contact made | First real prospect reached via DM or email; in `interview-log.jsonl` as `marked_sent`. State: shipped (n=1, prospect-0003). |
| M5 | First reply | One non-bot reply from a real prospect. State: not yet (0 replies). |
| M6 | First payment | One actual customer paying for the offer. State: not yet. |

Drift-detector: any work that does not advance one of M1–M6 (or one of the four hard prereqs below, or the factory-layer naming) is substrate polish. Forcing function lives on the operator side; if you (Claude) propose work that lands outside this list, the operator's job is to refuse the substitute.

## Where we are right now

- **Kernel built:** MODE-contract (per-agent `MODE` + append-only `flip-history.jsonl` + read-discipline + flip gates), repo-level `./killswitch`, `ROLLBACK.md` contract.
- **B-pattern primitives at `auto`:** 0 / 2 needed for the README's pattern-proof milestone.
- **Primitives wired:** 1 (B-1 customer-interviewer at v0.2; v0.3 amendment DRAFT 2026-05-25 awaiting cross-op review).
- **First-instance milestones cleared:** M1 (ICP), M4 partial (n=1 sent). M2, M3, M5, M6 not started.
- **Factory layer:** **factory-scaffold-v0.1 BUILT 2026-06-23** (ahead of instance-first, by explicit operator override — recorded in `factory/SPEC.md`, not the milestone). Business-spec schema (JSON) + `validate` + `build` + value→capture storefront emission live in `factory/factory.py`; per-business isolation under `businesses/` (gitignored). Still **scaffold-only**: no run-time autonomy, no auto-ideation (both deferred per SPEC). Why building it early is not the content-dark-zone drift: the scaffold is verifier-clean + content-agnostic (the operator supplies all content via the spec) — that caution applies to *what business to build*, not to *emit files from a spec*. **BUT the SPEC's base-case gate still holds for the generalization step:** you can't write the recursive step from n=1, so `factory/specs/` is **not extended** and the factory is **not declared generalizing** until a real, structurally-distinct n≥2 instance exists. Concrete evidence of that gate (2026-07-01): the n=1 (email-intake service) schema force-fit an n=2-shaped idea (styling-teacher, an app) — removed to `../Researches/styling-teacher-candidate/`. The premature schema was the root affordance for that misfit.
- **Real campaign data:** 1 marked-sent (prospect-0003 Max, 2026-05-19). 0 replies.
- **Posture:** **public** (2026-06-23); proof still owed — see README § Status. No B-track at `auto` yet (0/2).

## Versioning, factory-honest

The earlier "v1.0 = ≥2 tracks step→auto" was implicit B-pattern proof — the discipline holds for individual primitives. It is **not** factory-v1.0. Re-stated:

| Layer | Milestone | Meaning |
|---|---|---|
| **B-pattern proof** | ≥2 B-tracks step→auto with cross-op review + clean audit logs | The discipline holds for individual primitives. (Inherited from README.) |
| **First instance** | M1–M6 all "done"; V-A's own business has paying customers and runs on the primitives | One whole automated business exists, end-to-end. Dogfood case. |
| **Factory v0.1** | Business-spec schema defined; factory can instantiate primitives against a spec; produces a second *structurally-distinct* business instance (not V-A itself) | The factory exists as a thing, however rough. Two instances ≠ a product, but ≠ one-off either. **STATE 2026-07-01: schema + instantiate-against-spec + storefront emission DONE as scaffold (`factory.py`), by operator override — NOT the milestone (milestone still gates on a real n≥2). n=1 base = agent-audit-consulting; `pitch-deck-review` is a SAME-shape second (content-parameterization, not the axis-inverting generalization test). The real n=1→n=2 test — a structurally-distinct instance that STRESSES the n=1 schema — is still owed.** |
| **Factory v1.0** | N≥3 instances produced from spec; each at falsifier-clean autonomy on mechanism; cross-op review of the factory's instantiation discipline (not just per-instance) | The factory is what's shipping, not a particular business. |

Public-flip is per-layer operator-judgment (`NEXT-3-DECISIONS.md` Decision 3). Pattern-proof public-flip and factory public-flip are distinct decisions.

## Prereq ladder (from `B-PROPOSAL.md` § Hard prereqs)

These gate factory-v0.1, not the first instance. The first instance can proceed against M1–M6 without them; the factory cannot.

| # | Prereq | Where it lives | Cost shape |
|---|---|---|---|
| 1 | ≥2 PCLA tracks demo-stable | PCLA repo (`modes.yaml`) | Currently 1 (A-3) + 1 retroactive-provisional (A-6); cheapest lift = discharge A-6 cross-op review by 2026-05-31 deadline |
| 2 | Eve / Mark / external availability | Operator outreach | Days |
| 3 | A-1 phase-transition-auto lands | PCLA (`tracks/06-phase-transition-auto/`) | Engineering weeks; provides Surface-Compliance substrate every primitive depends on |
| 4 | Hosted-infra eng project funded | External (money + months) | The factory's actual substrate: the layer the factory deploys each instance onto. Bigger than all 8 primitives combined. |

**Substrate-vs-checkbox honesty.** Prereq #1 is checkbox; #2 is logistics; #3 is engineering-weeks; #4 is months + money and is **load-bearing for the factory specifically** (you cannot deploy N instances without hosted infra). Prereqs #3 and #4 are the real cost of the factory; #1 and #2 unblock review queue capacity, not product.

## Track ladder (primitives for the first instance — from `B-PROPOSAL.md` § Phasing)

The 8 B-tracks group by gate cost. Each phase is authorized only after the prior demonstrates the falsifier-per-track pattern catches what it's supposed to catch. **All 8 are primitives for one instance**; the factory layer is separate.

| Phase | Tracks | Why these together |
|---|---|---|
| **B-α** (cheap, validate pattern) | B-1 customer-interview-runner, B-8 metrics-watchdog | Text/read-only; low-stakes; falsifier-pattern proof |
| **B-β** (outputs, operator-approve) | B-2 landing-page-deployer, B-7 support-triage | Visible outputs; operator-supervised; no money spent |
| **B-γ** (outputs that spend money) | B-3 cold-outreach, B-4 ads-pilot, B-5 code-deploy | Real-world consequences if falsifiers fail |
| **B-δ** (inbound high-stakes) | B-6 inbox-triage | Worst-case = hallucinated VC term-sheet signed in agent's voice |

**Current primitive state:**

| Track | State | Notes |
|---|---|---|
| B-1 | v0.2 shipped; v0.3 amendment DRAFT | MODE=step; 1 real send; 5 drafts in log; falsifier sweep run 2026-05-25 |
| B-2 | DESIGN-SKETCH | Gated on hard prereqs; do NOT promote to SPEC |
| B-3..B-8 | one-line in B-PROPOSAL | Paper-only |

## Suggested sequencing (operator's call; not authorization)

Three coherent orderings, each grounded in a different binding constraint:

1. **First-instance-first:** Advance M1–M6 with the primitives that exist (B-1 for outreach; B-2 for landing page when prereqs lift). Real prospect cadence → real replies → real customers. The dark-zone residue gets verified by the market, not by us. Substance moves; factory layer can wait.
2. **Pattern-proof-first:** B-pattern proof milestone (≥2 primitives at auto, cross-op review clean). Discharge A-6 review (PCLA prereq #1). Generates artifacts but does not move M1–M6.
3. **Factory-substrate-first:** Begin hosted-infra scoping (prereq #4) and A-1 work (prereq #3). Largest cost, longest horizon, only path to factory-v0.1.

Tradeoff: #1 produces real evidence but stalls on operator outreach cadence; #2 moves the checkbox count without moving the product; #3 unblocks factory but takes months. **The forcing function refuses any fourth option** (= substrate polish dressed as progress).

## What this roadmap is NOT

- **Not a Gantt.** No dates beyond hard deadlines already in source documents (A-6 provisional → 2026-05-31).
- **Not authorization.** Track promotions (sketch → SPEC, SPEC → impl, step → auto) require their own gates per `B-PROPOSAL.md`, `MODE-CONTRACT.md`, and `README.md`.
- **Not a decision list.** Decisions live in `NEXT-3-DECISIONS.md`; this file follows them.
- **Not substrate.** Track shapes live in `B-PROPOSAL.md` + per-agent dirs; this file points, doesn't restate.
- **Not the factory spec.** The factory's actual SPEC does not exist yet. Naming it as the destination is not the same as designing it. The next-up factory work is M1–M6 (build one instance first), not a factory-design doc.
- **Forecasting boundary.** VA never ships prediction of outcomes — market/economic success is dark-zone, unforecastable; the market verifies it over time. Forecasting enters VA ONLY as calibration: not "will this succeed" (unverifiable) but "is this predictor well-calibrated" (verifiable via proper scoring rules / backtest). A calibration harness is buildable; a crystal ball is the anti-pattern. This is the dark-zone split stated at the outcome level.

## Falsifier (for this document)

This file is **doing its job** if a new session can read it once and pick up the work without re-reading every adjacent doc — AND if the named work in any given session is one of: a hard prereq, an M1–M6 milestone, or naming/speccing the factory layer.

This file has **failed** if:
- It accumulates phases beyond B-α / β / γ / δ (5th phase = scope creep, not roadmap completion).
- It survives more than 3 sessions without any state field updating (current-state block goes stale → fictional roadmap).
- Track-shape detail starts leaking back into this file (we're rebuilding `B-PROPOSAL.md` here = duplication; delete this file before that happens).
- It tries to predict when a prereq will lift (timing prediction is Gantt-thinking — and the general form: banking any OUTCOME claim ahead of its verifier. The verifiable object is the mechanism now + calibration over time, never the forecast).
- **A session lands a commit that doesn't advance a hard prereq, an M1–M6 milestone, or factory-layer naming** (= right-repo-wrong-work drift, the failure mode this version of the roadmap was written to catch).

## Cross-references

- v1.0 framings (pattern-proof + factory): `README.md`
- Hard prereqs + primitive shapes + phasing: `B-PROPOSAL.md`
- Active decisions: `NEXT-3-DECISIONS.md`
- Mode-toggle kernel: `MODE-CONTRACT.md`
- Rollback contract: `ROLLBACK.md`
- B-1 agent: `agents/b1-customer-interviewer/README.md`
- B-2 staged: `B-2-DESIGN-SKETCH.md`
- PCLA strategic-layer side: `../prometheus-crystal-lab-auto/ROADMAP.md`

---

*Roadmap v0.3, 2026-06-23. Factory-v0.1-shipped state-sync (state block + versioning row updated to ground truth; run-without-supervision overclaim softened to build-time). v0.2, S58 (2026-05-25): factory-frame correction. Thin by design. Delete if it fails the falsifier above.*
