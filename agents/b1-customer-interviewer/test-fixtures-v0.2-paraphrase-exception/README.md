# Test fixture: paraphrase-exception (v0.2 amendment)

> **What this fixture validates:** the three HIGH-severity catches landed in v0.2 (verifiable-autonomy commit `2c8b3b8`), against synthetic substrate built to exercise each one.

This fixture is a **sibling** to `test-fixtures/` (which remains frozen as the v0 baseline). The v0 fixtures predate the v0.2 amendment and do not have `register:` fields on prospect rows; running the current agent against them would STOP on missing-register (which is correct v0.2 behavior).

## Substrate

- **`icp.md`** — variant of the DevTrace ICP focused on phrases that surface the paraphrase-vs-verbatim tension in peer-register outreach. Em-dash-free per outgoing-mail discipline.
- **`prospects.md`** — three prospects: one `peer` (eligible for paraphrase exception), one `customer-dev` (verbatim required), one `peer` with thin substrate (should skip with `PROSPECT_THIN`).
- **`drafts/`** — one peer-register draft with scored paraphrased citations + one customer-dev draft with strict verbatim.
- **`refused/`** — describes what a score-0 refusal looks like (no draft file emitted; log entry only).
- **`interview-log.jsonl`** — sample records showing the v0.2 audit log shape (`register` field + `icp_phrases_paraphrased[].score`).

## What each test case exercises

| Test case | Validates |
|---|---|
| `prospects.md` → all rows have `register:` field | **HIGH 2** — operator-side gate; agent reads, does not classify |
| `drafts/prospect-0001.md` (peer, scored paraphrase) | **HIGH 3** — semantic-preservation score 0/1/2 visible in metadata |
| `drafts/prospect-0002.md` (customer-dev, verbatim) | v0 Surface-Compliance still holds in non-peer registers |
| `refused/NOTES.md` (score-0 refusal scenario) | **HIGH 3 reject path** — `SEMANTIC_LOSS_IN_PARAPHRASE` skip-record shape |
| `interview-log.jsonl` paraphrase-rate count | **HIGH 1** — Falsifier 7 yellow (>20%) / red (>35%) computable from log |

## How to read this fixture (no run required)

The fixture is documentation-shaped, not auto-runnable. To verify the amendment:

1. Read the drafts; verify each paraphrased citation has `| score: N` in the metadata block.
2. Grep `interview-log.jsonl` for `register=peer` records vs total; the rate here is computed below for the Falsifier 7 check.
3. Read `refused/NOTES.md` for the score-0 refusal pattern.

Computed paraphrase rate for this fixture: 1 peer / 2 total = 50%. **This exceeds Falsifier 7 yellow (20%) and red (35%) thresholds**, which is expected for a fixture (deliberately demonstrating the exception). A real campaign would not.

## What this fixture does NOT cover

- B-set generalization (OPEN-WORK item 6 — B-1-specific stance)
- Register transitions across follow-up chain (OPEN-WORK item 7)
- Metadata-body register mismatch detection (OPEN-WORK item 4)
- Em-dash + paraphrase tell-surface (OPEN-WORK item 8)

Those need their own fixtures when triggers fire per the OPEN-WORK queue.

## Cross-references

- v0.2 amendment commit: `2c8b3b8` in `holbizmetrics/verifiable-autonomy`
- Cross-review response: PCLA `.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-RESPONSE.md`
- OPEN-WORK queue: `../OPEN-WORK-paraphrase-exception.md`
- Agent definition: `../../../.claude/agents/b1-customer-interviewer.md`
- Falsifier: `../falsifier.md`

---

*Fixture v1, S55 (2026-05-19). Documentation-shaped; not auto-run. Add fixtures here as OPEN-WORK items close.*
