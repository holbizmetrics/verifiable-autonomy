# B-2 design sketch — `landing-page-deployer` (gated, not authorized)

> **Status: DESIGN-ONLY. Filed S57 (2026-05-20) to capture B-2's shape while the hard prereqs from B-PROPOSAL.md still stand. This file does NOT authorize SPEC work or implementation. Re-read § Hard prereqs before promoting any item here to a SPEC.**

## Why this file exists (and why now)

B-1 has shipped at v0.2 with the paraphrase exception. The B-PROPOSAL gate is not cleared: A-1 has not landed, hosted-infra is unfunded, and ≥2 PCLA tracks demo-stable is still 1 confirmed + 1 retroactive-provisional. So B-2 cannot start its SPEC.

What this sketch *does* is anchor B-2's shape now, so that when the gate clears, the first session does not have to reconstruct the design from B-PROPOSAL's one-line falsifier. Cost: ~30 minutes of substrate today, against ~1 session of re-derivation later.

What this sketch deliberately *does not* do: name the implementation, choose the hosted-infra stack, write the per-Pre-commit checklist, or commit to a Claude Code agent definition. Those are SPEC-time decisions and they depend on what A-1 surfaces.

## What B-2 is, in one line

The agent that takes B-1's customer-interview transcripts and emits a landing-page draft whose copy is verifiably grounded in those transcripts.

The Polsia analog is "Code & Deploy" used for marketing pages. The Polsia failure mode (from honest reviews) is generic marketing output indistinguishable from any other SaaS. B-2's differentiation is: every claim on the page maps to a verbatim or near-verbatim phrase from a real customer interview. The page is generic only if the interviews are generic.

## Falsifier register (sketch — to be expanded at SPEC time)

The B-PROPOSAL one-liner ("Copy specificity floor: <3 ICP-specific phrases from B-1 transcripts → step-flip. Generic-verb count > threshold.") is the headline falsifier. The full register at SPEC time would need ~5-7 falsifiers; here are the candidates:

| # | Failure mode | Detection | Severity |
|---|---|---|---|
| 1 | Page copy with <3 phrases verbatim-from-substrate (B-1 transcript pool) | grep-able trace: each copy block annotated with source `interview-log.jsonl` row | step-flip |
| 2 | Generic-verb density above threshold (e.g. "leverage", "empower", "unlock") on hero block | regex count over a curated jargon list, normalized by word count | step-flip |
| 3 | Claim on page that has no source row in `interview-log.jsonl` at all (fabrication) | Surface-Compliance check: every claim block has a `cited-from:` field; agent refuses to emit blocks without it | FATAL on deploy |
| 4 | Deployed page diverges from the draft the operator approved (phantom-deploy) | re-derive from deploy log + DOM snapshot vs. approved draft; mismatch = fail | step-flip + alert |
| 5 | ICP segment claimed on page does not match the segment the cited interviews actually came from | row-level segment field on transcripts; per-block segment match | step-flip |
| 6 | A/B variant generation invents a claim not present in either source pool | same Surface-Compliance check as #3, applied per-variant | FATAL on deploy |
| 7 | Page references a customer-permission scope the operator did not grant (e.g. names a logo'd customer in a "trusted by" block without an opt-in row) | per-customer `marketing-permission:` field; refuse if missing | FATAL |

Falsifier 1 is the headline. Falsifier 3 + 6 are the Surface-Compliance backbone — same shape as B-1's "no paraphrase, no synthesis, no I-reviewed-X-without-grep-able-evidence" rule from agents/README.md.

## Substrate the agent consumes

- **B-1's `interview-log.jsonl`** — the primary source of cited phrases. B-2 cannot run until B-1 has produced ≥N transcripts (N TBD at SPEC time; sketch: N=5 minimum for non-fabricated specificity).
- **B-1's `icp.md`** — the ICP definition. Page must claim only segments named there.
- **A new `marketing-permissions.md`** — per-customer/logo opt-in registry. Empty until operator fills it.
- **A new `page-templates/`** — structural templates the agent fills, not generates. Layout decisions are operator-side; copy decisions are agent-side from substrate.

## Substrate the agent produces

- `drafts/page-NNNN-v1.html` (or .md) — draft with per-block `cited-from:` annotations.
- `drafts/page-NNNN-v1.surface-compliance.json` — per-block trace: which substrate row each claim cites, generic-verb scan, segment match.
- `deploy-log.jsonl` — append-only on deploy attempt: target URL, hash of approved draft, post-deploy DOM snapshot hash, mismatch flag.

## Mode contract (per MODE-CONTRACT.md, no exceptions)

- Default: `step`. Operator triggers each draft + each deploy explicitly.
- `step → auto` gate: ≥2 deployed pages where Falsifiers 1-7 all stayed clean across the campaign + cross-operator review on the architecture + operator confirmation.
- `auto`-mode behavior: agent self-fires on a fresh batch of B-1 transcripts (e.g. weekly), emits a draft, opens a "review-and-deploy" review for the operator. Auto-fire on *draft*, never on *deploy*. Deploy stays operator-gated even in auto, because Falsifier 4 + 7 are FATAL-on-deploy.

## Dependencies the gate surfaces

| Hard prereq from B-PROPOSAL | B-2-specific shape |
|---|---|
| A-1 phase-transition-auto must land | A-1's re-derivation routine is the substrate Falsifier 1, 3, 5, 6 all run on. Without it, the per-claim citation check is hand-implementation, not architecture. |
| ≥2 PCLA tracks flipped with demos | Establishes that the falsifier-per-track pattern survives the step→auto transition under real load. B-2 is a step→auto candidate in the execution-layer repo; we want evidence from the strategic-layer repo that the pattern holds. |
| Hosted-infra eng project funded | B-2's deploy target. The "moat" line in B-PROPOSAL: without somewhere to deploy to, B-2 is a draft generator with no audit-trail closure on Falsifier 4. |
| Eve / Mark / external availability | B-architecture meta-review per B-PROPOSAL § Cross-operator review burden. B-2 specifically: meta-review on whether Falsifier 1's threshold (3 phrases) catches Polsia-style generic output in practice. |

The B-1 corollary: B-2 cannot ship until B-1 has produced N≥5 real transcripts. N=0 today. This is a *substrate* gate, not a code gate, and it ticks up only when operator-sent prospects actually reply and the conversation actually happens.

## What B-2 is NOT, deliberately

- Not a copywriting agent. The agent does not generate marketing language; it composes phrases from substrate. If the substrate is bland, the page is bland (and that is the correct signal — Polsia's failure was hiding bland substrate behind LM-generated wrapper text).
- Not an A/B testing platform. Variants are allowed (see Falsifier 6), but the optimization loop is operator-side, not agent-side, until the gate clears. Statistical-significance gates are B-4 territory.
- Not a CMS integration. The deploy target at SPEC time is a single hosted page per draft; CMS integration is a hosted-infra question, not an agent question.
- Not a SEO agent. Keyword density, metadata, structured data are all stretch — out of scope until B-2 v0 ships clean.

## Open questions the SPEC will need to resolve

1. **The "near-verbatim" boundary.** B-1's v0.2 paraphrase exception was scored 0/1/2 in `peer` register. Does B-2 inherit that score machinery, or does landing-page copy require strict verbatim only? Sketch position: strict verbatim by default; per-block paraphrase exception possible but only with a per-block score ≥1 and operator review per amendment.
2. **Threshold tuning for Falsifier 2 (generic-verb count).** What's the jargon list? Operator-curated, or seeded from a published list? Sketch position: operator-curated, in `b2-landing-page-deployer/generic-verbs.md`, version-pinned at SPEC time.
3. **Falsifier 4 mechanics.** "DOM snapshot hash vs. approved-draft hash" is naive (whitespace / framework wrapping breaks it). Real check: structural diff over claim-bearing nodes. Defer detail to SPEC.
4. **Multi-segment pages.** If B-1's transcripts span 3 ICP segments, does B-2 emit 3 pages or one page with 3 sections? Sketch position: one page per segment until the operator has substrate volume to justify a multi-segment landing page.
5. **Inheritance from B-1's OPEN-WORK items.** Specifically the sibling-second-pass-wiring item from windows v0.2 verdict — if B-2 inherits B-1's paraphrase machinery, does it inherit the second-pass gate too? Sketch position: yes if paraphrase is allowed; no if strict verbatim is the call.

## Cross-references

- B-set proposal (parent, with B-2 row): `B-PROPOSAL.md`
- B-1 agent (the substrate producer): `agents/b1-customer-interviewer/`
- MODE contract (the execution-policy substrate): `MODE-CONTRACT.md`
- Killswitch (repo-level convenience layer): `./killswitch all`
- Agents pattern (the directory shape B-2 will copy): `agents/README.md`
- PCLA research-side parallel: `../prometheus-crystal-lab-auto/` (strategic-layer audit-trail; B-track flip evidence)

---

*Design sketch v1, S57 (2026-05-20). Captures B-2 shape against the gate. Not a SPEC. Promotion to SPEC requires B-PROPOSAL hard prereqs cleared + operator confirmation. Re-read this file at that time, not implement directly from it.*
