# Open work: paraphrase-exception amendment (S55 v0.2 → forward)

> Items deferred from the v0.2 amendment per windows-claude cross-review (PCLA `.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-RESPONSE.md`). All MED/LOW; revisit triggers below.

## Status

- **v0.1 (commit `b83a4e1`):** initial amendment. Verdict: REVISE (HIGH on items 1-3).
- **v0.2 (this commit):** HIGH 1-3 landed. Verdict-target: ACCEPT-WITH-CAVEAT (caveats = items below).
- **v0.3 trigger:** first real-campaign data, or any single item below becoming load-bearing in practice.

## Deferred items

### MED-HIGH 4 — Metadata-body register mismatch unchecked

windows-claude's catch: a non-peer draft body could contain paraphrased ICP-source-material that isn't in the verbatim-citation block. Falsifier 7 only counts records where `register=peer`; Falsifier 1 only checks declared verbatim citations. The undeclared paraphrase floats unverified.

**Why deferred:** detection requires semantic-similarity heuristic on the draft body vs `icp.md`. Tooling cost is real; benefit-per-event is unclear until we have campaign data on whether this actually fires.

**Revisit when:** first real campaign emits ≥10 non-peer drafts. Spot-check 3 for undeclared paraphrase. If any caught, build the heuristic.

### MED 5 — "2 transformations" rule is undefined

The `REGISTER_REQUIRES_REWRITE` skip-condition uses "would require >2 transformations" without defining a transformation. Lexical / syntactic / register-shift / claim-rewording / structural are all candidates; the agent currently decides what counts.

**Why deferred:** v0.2 lowers stakes here — the score-0 reject (HIGH 3) catches the worst case (claim drop) before the transformation-count question matters. The 2-transformation rule is now a secondary skip-condition behind score-0.

**Revisit when:** B-1 invokes `REGISTER_REQUIRES_REWRITE` in a campaign and the operator finds the skip-vs-emit boundary unclear. Define the unit then with substrate.

### MED 6 — Cross-application to B-2, B-3 not specified

The amendment doesn't say whether the paraphrase exception generalizes to other B-set agents.

**Stance (v0.2):** the exception is **B-1-specific**. Future B-N agents that need a paraphrase exception must file their own amendment with their own falsifier rates appropriate to their register mix. B-set canonical Surface-Compliance discipline (in `B-PROPOSAL.md`) is strict verbatim by default; per-agent exceptions are amendments, not inheritance.

**Why this stance:** generalizing the exception inherits all five attack-surfaces across the B-set, compounding technical debt. Per-agent amendments keep each Falsifier 7 calibrated to that agent's register-mix reality.

**Revisit when:** B-2 design starts. Decide whether to copy the v0.2 amendment pattern (register field in prospects.md + score 0/1/2) or design something different.

### MED 7 — Register transitions across the outreach chain

If a peer-classified prospect's reply shows buyer-signal, who flips the register? Agent or operator?

**Stance (v0.2):** **register persists per prospect-chain.** Follow-up drafts use the register declared in the original prospect row. If the operator decides the relationship has shifted, they edit the prospect row to flip the register; B-1 reads the new register on the next follow-up.

**Why this stance:** keeps operator-as-classifier (HIGH 2's whole point) consistent across the chain. B-1 doesn't get to reclassify mid-conversation; that would re-introduce the agent-self-classification incentive at a new level.

**Revisit when:** first follow-up sequence has 5+ rounds, OR operator hits a case where row-flip feels wrong.

### MED-LOW 8 — Em-dash + paraphrase tell-surface interaction

The verbatim-citation discipline had a hidden second function: cited chunks were in a different voice (operator-manifesto) than B-1's surrounding draft. Voice-shift on quotation is a tell-removal — humans cite in different voice; AI templates have uniform voice throughout. Paraphrasing brings the citation into the agent's voice, removing the voice-shift.

**Stance (v0.2):** acknowledged trade-off. Peer-register drafts trade voice-shift-tell-prevention for tone-match. Operators reviewing peer-register drafts should specifically check for uniform-voice tells.

**Revisit when:** any reply suggests "this reads as AI-written" or operator's first peer-register sent draft feels uniform-voice-templated.

**Optional fix (not in v0.2):** peer-register drafts could use an inline lead-in like "you've written that..." prefixing paraphrases, preserving structural voice-shift. Defer until needed.

### LOW-MED 9 — Reply-citation paraphrase policy

The paraphrase exception applies to ICP citations. What about reply citations in follow-up drafts?

**Stance (v0.2):** **reply citations remain verbatim in all registers.** Already encoded in the v0.2 amendment body. No further work.

## Triggers summary

| Item | Trigger | Action |
|---|---|---|
| 4 | First real campaign emits ≥10 non-peer drafts | Spot-check 3 for undeclared paraphrase |
| 5 | `REGISTER_REQUIRES_REWRITE` skip with unclear boundary | Define transformation unit with substrate |
| 6 | B-2 design starts | Decide inherit-vs-amend |
| 7 | Follow-up chain ≥5 rounds OR row-flip feels wrong | Revise register-transition rule |
| 8 | Peer-register draft feels uniform-voice OR reply flags AI-text | Add inline lead-in prefix |
| 9 | n/a (already encoded) | n/a |

## Cross-references

- v0.1 amendment: commit `b83a4e1`
- v0.2 amendment: this commit (HIGH 1-3 landed)
- windows-claude review: PCLA `.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-RESPONSE.md`
- Falsifier 7: `falsifier.md`
- Agent definition: `../../.claude/agents/b1-customer-interviewer.md`

---

*Open-work queue v1, S55 (2026-05-18). Delete this file if all items close.*
