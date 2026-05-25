# verifiable-autonomy

> **Autonomous AI operations with audit trails. Falsifier per track. Operator killswitch wired before flip. Private until proof.**

## Status

**Private with invited early-access (S55, 2026-05-18).** Flips fully public when at least two tracks have demonstrated step → auto operation with cross-operator review and clean audit logs.

In the interim, repo access is by invitation, capped at 5 early-access testers. Invited testers see the same code with full audit-log access. The public read stays gated on proof; early-access exists to surface real-world friction that synthetic testing misses. Each invited tester is a falsifier-probe against the architecture's claims.

Early-access posture is reversible. Cap can be lowered, raised, or revoked at any time; no public footprint accrues. Invitation message includes a one-line don't-post-publicly clause until the proof-gate clears.

## What this is

A **verifiable business factory**: a system that, given a business spec, instantiates an automated business that runs without operator supervision and is auditable end-to-end. The product is the factory; each output is a separate automated business instance. The factory itself is mechanism-verifiable (did it deploy? are the audit logs balanced?); the business-success of each output stays dark-zone (the market verifies it, over time — that part stays with the operator, by design).

The factory does not exist yet. V-A is currently building the **first instance** (V-A's own go-to-market) as the dogfood case the factory will generalize from. The B-tracks (`B-PROPOSAL.md`, B-1..B-8) are the **primitives** any one instance composes — they are not the factory. See `ROADMAP.md` for the M1–M6 first-instance milestones and the factory-vs-pattern-proof versioning.

## The thesis

The AI-agent-runs-your-business market is currently shipping autonomy without verification. Users get generic output, hallucinated work, burned credits with nothing to show. The honest reviews (not the marketing) make this plain.

The architectural fix is not better prompts or better models. It's a discipline that operates at the substrate layer:

1. **Mode toggle per track.** Each capability has a `step` (operator-gated) and `auto` (self-firing) mode. Flips happen one track at a time. Default state is `step`. There is no "all auto" button.
2. **Pre-registered falsifier per track.** Before a track flips to `auto`, the failure mode that proves it is broken is named in writing. Falsifier fires → track flips back to `step` automatically.
3. **Audit trail per fire.** Every autonomous action emits a structured record (JSONL, append-only): what trigger fired, what artifacts were read with hash and mtime, what state was rebuilt, what was claimed and what was dropped. Operator can `tail | jq` the audit log without trusting the agent's narrative.
4. **Surface-Compliance check.** The failure mode where an agent claims "I read X, here's the plan" without reading X is treated as the headline risk. Every auto-track's gate refuses to emit a "I re-derived" record that has zero successful artifact reads behind it.
5. **Cross-operator review before flip.** Within-session self-review is the lowest rung of verification. Each flip to `auto` requires verification from a different session, ideally a different model family. Rung register is explicit; rungs not yet discharged are named, not hidden.
6. **Rollback contract.** A single command takes all tracks back to `step`. Per-track rollback triggers are pre-registered. The killswitch exists before flip, not after the first failure.

## The two layers

The discipline above is not specific to per-email tactics or per-draft choices. It operates at every layer of the work, just at different time-scales.

This repo embodies the discipline at the **execution layer**: agents drafting outreach, classifying replies, marking sends. Per-action audit records. Per-agent falsifiers. Per-agent `MODE` files. Operator-supervised by default.

The **strategic layer** is currently operated by hand. The Prometheus Crystal Lab Auto research repo (PCLA) is its audit-trail:

- **Strategic audit-trail.** PCLA mirror logs (one per session continuation, every architectural decision recorded with rationale + commit-hash citation) play the role `interview-log.jsonl` plays for execution.
- **Strategic falsifiers (pre-registered).** `B-PROPOSAL.md`'s hard prereqs ("A-1 must land, ≥2 PCLA tracks demo-stable, hosted-infra funded") are pre-registered falsifiers on the strategic move to ship B-2 through B-8. Same shape as B-1's Falsifier 1-7, longer time-scale.
- **Strategic cross-operator review.** Architectural amendments (e.g., v0.2 paraphrase exception) get reviewed by a parallel Claude session in a different environment before landing. Same shape as B-1's per-campaign cross-op, applied to architecture instead of drafts.
- **Strategic MODE contract.** PCLA's `modes.yaml` is the same primitive as B-1's per-agent `MODE` file, scoped to research tracks instead of execution agents.
- **Strategic Surface-Compliance.** Commits cite substrate (prior decisions, commit hashes, mirror-log pointers) the same direction as B-1 drafts cite verbatim from `icp.md`. Less rigorous surface; same architectural intent.

The two repos are coupled, not parallel:

- **verifiable-autonomy** = execution-layer agents
- **prometheus-crystal-lab-auto** = strategic-layer audit-trail + falsifier register + cross-op review log

**What this implies for the roadmap.** There are two distinct v1.0s, not one:

- **Pattern-proof v1.0:** ≥2 B-primitives step→auto with cross-op review + clean audit logs. The discipline holds for individual primitives. Necessary; not the product.
- **Factory v1.0:** N≥3 automated business instances produced from a business-spec; each at falsifier-clean autonomy on mechanism; cross-op review of the *factory's* instantiation discipline (not just per-instance). This is the product.

Between them sits **First-instance v1.0:** all M1–M6 milestones (`ROADMAP.md`) done; V-A's own business has paying customers and runs on the primitives. This is the dogfood case the factory generalizes from. Building the factory abstraction before this exists is the drift trap — open-ended "create a business" has no verifier, so it wanders; the M1–M6 milestones ARE the verifier the open-ended task is missing.

The path from operator-exercises-strategic-discipline to factory is therefore: discipline pattern → one whole working instance → generalize to factory. Not: discipline pattern → factory abstraction → instances. The order matters.

The product is the factory. The discipline is what makes its output trustable. The agents are how each instance does its work.

## What this repo will contain (when public)

- The track-and-gate architecture as a reference pattern
- Per-track SPECs with falsifiers
- Audit-log schema and worked examples
- Cross-operator review templates
- Rollback contract
- B-set business-builder proposal (`B-PROPOSAL.md`, already in this repo, gated on the architecture proving itself first)

## What this repo will NOT contain

- Marketing claims unbacked by demonstrated track flips
- "Agents that run your company while you sleep" without per-track audit trails
- Closed-source learning across customers without explicit opt-in
- Promises of revenue or autonomy that the audit log cannot verify

## The honest scope

The architecture runs at two scales today. **Execution layer (this repo):** B-1 customer-interview-runner shipped at v0.2 (S55, 2026-05-19); v0.3 amendment DRAFT (S58, 2026-05-25). MODE contract live; first per-agent `MODE` file in step. **Strategic layer (PCLA, the coupled research repo):** A-3 closeout-auto in `auto`, A-1 phase-transition-auto in late design review. The B-primitive proposal (B-2 through B-8) is gated on pre-registered strategic falsifiers in `B-PROPOSAL.md`.

**First-instance state (M1–M6, `ROADMAP.md`):** M1 (ICP identified) and M4 (first contact) shipped. M2 (offer), M3 (landing page), M5 (first reply), M6 (first payment) not started. The dark-zone residue at M5/M6 is operator + market work, not Claude work.

**Factory layer:** does not exist. No business-spec schema, no orchestration, no instance isolation. Naming it as the destination is not the same as designing it. The next-up factory work is M1–M6 on the dogfood instance, not a factory-design doc.

This repo flips from private to public at pattern-proof v1.0 (≥2 primitives at auto, cross-op review clean). Factory public-flip is a distinct, later decision per `NEXT-3-DECISIONS.md`.

Until then: this README is the manifesto. Early-access testers are the first real-world probe. The public proof is owed.

## License

To be determined at public-flip time. Likely a permissive license for the architecture pattern + a separate license posture for any business-builder implementation.

## Cross-references

- Quickstart for early-access testers: `QUICKSTART.md`
- Warm-reply workflow (post-send): `WARM-REPLY-WORKFLOW.md`
- Invitation message template (operator-side): `INVITATION-TEMPLATE.md`
- Active path-decision context: `NEXT-3-DECISIONS.md`
- Rollback contract: `ROLLBACK.md`
- Agents (currently shipped + pattern for B-N): `agents/README.md`
- Strategic-layer audit-trail (coupled research repo, private): `prometheus-crystal-lab-auto`
- MODE contract (per-agent execution-policy primitive): `MODE-CONTRACT.md`
- Honest review of the competing pattern (Polsia): https://crevio.co/blog/is-polsia-legit
- B-set proposal: see `B-PROPOSAL.md` in this repo

---

*v1.2, S58 (2026-05-25). Factory-frame correction: product is the factory; B-tracks are primitives; build one concrete instance first, generalize after. Private. Flips public when pattern-proof lands; factory public-flip is a distinct later decision.*
