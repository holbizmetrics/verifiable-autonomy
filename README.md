# verifiable-autonomy

> **Autonomous AI operations with audit trails. Falsifier per track. Operator killswitch wired before flip. Private until proof.**

## Status

**Private with invited early-access (S55, 2026-05-18).** Flips fully public when at least two tracks have demonstrated step → auto operation with cross-operator review and clean audit logs.

In the interim, repo access is by invitation, capped at 5 early-access testers. Invited testers see the same code with full audit-log access. The public read stays gated on proof; early-access exists to surface real-world friction that synthetic testing misses. Each invited tester is a falsifier-probe against the architecture's claims.

Early-access posture is reversible. Cap can be lowered, raised, or revoked at any time; no public footprint accrues. Invitation message includes a one-line don't-post-publicly clause until the proof-gate clears.

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

**What this implies for the roadmap.** v1.0 is not "when the operator-amplifier ships." v1.0 is **when the execution-layer agents catch up to the strategic-layer discipline that already runs by hand.** The path from there to "autonomous business-builder" is not adding a future layer; it is gradually shifting load from operator-exercises-strategic-discipline to S-tier-agent-exercises-strategic-discipline-with-operator-review. Same architecture, longer-horizon falsifiers, higher rungs of evidence per flip.

The product is the discipline. The agents are embodiments of it at progressively higher layers.

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

The architecture runs at two scales today. **Execution layer (this repo):** B-1 customer-interview-runner shipped at v0.2 (S55, 2026-05-19). MODE contract live; first per-agent `MODE` file in step. **Strategic layer (PCLA, the coupled research repo):** A-3 closeout-auto in `auto`, A-1 phase-transition-auto in late design review. The B-set execution-track proposal (B-2 through B-8) is gated on pre-registered strategic falsifiers in `B-PROPOSAL.md`.

This repo flips from private to public when at least two execution-tracks have flipped step → auto, demonstrated their falsifiers don't fire, and survived cross-operator review at the cross-session-same-family rung minimum.

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

*v1.1, S55 (2026-05-19). Private. Two-layer reframe added: execution layer (this repo) + strategic layer (PCLA, by-hand today). Flips public when proof lands.*
