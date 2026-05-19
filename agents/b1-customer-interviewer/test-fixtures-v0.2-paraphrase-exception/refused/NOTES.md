# Refused draft: score-0 paraphrase rejection (HIGH 3 reject path)

> **What this directory documents:** the agent-side refusal pattern when a paraphrase would drop the verbatim source's claim. No draft file is emitted; only a `draft_skipped` record is appended to `interview-log.jsonl`.

## Scenario

Imagine a fourth prospect, `prospect-0004: Vera Tomasic`, peer-register, adjacent observability product. The agent attempts a peer-register draft. One of the paraphrases B-1 is about to emit:

```
[paraphrased: "we keep humans in the loop on alerts" ← "single binary. Drop it on your server. Point at your access log"]
```

**Score evaluation:** the paraphrase drops the load-bearing semantic content. The verbatim source says: deploy mechanics (binary, drop, log path). The paraphrase says: human-supervision pattern (humans in the loop). These are not the same claim. Score = 0.

## Agent behavior on score-0

Per the v0.2 amendment, B-1 MUST refuse to emit the draft. The agent appends a skip record to `interview-log.jsonl`:

```json
{
  "timestamp": "2026-05-19T14:32:11Z",
  "mode": "draft",
  "action": "draft_skipped",
  "prospect_id": "prospect-0004",
  "reason": "SEMANTIC_LOSS_IN_PARAPHRASE",
  "detail": "paraphrase 'we keep humans in the loop on alerts' drops verbatim source's deploy-mechanics semantic; scored 0. Refusing to emit draft. Operator should reclassify prospect or rewrite ICP phrase to peer-register-compatible verbatim."
}
```

## Why this matters

This is the path windows-claude's Attack 3 named as the largest unenforced boundary in v0.1. Before v0.2, an agent could emit a draft with a claim-diluted paraphrase, log a `draft_emitted` record, pass Falsifier 7's audit cross-check (source still exists in `icp.md`), and contaminate the campaign with a soft-shaped pitch that the falsifier register would never catch.

With v0.2: score-0 is a hard refusal. No draft file. No `draft_emitted` record. A `draft_skipped` record with explicit `SEMANTIC_LOSS_IN_PARAPHRASE` reason. Operator-visible. Auditable.

## What this does NOT prove

This fixture documents the refusal pattern; it does not by itself prove the agent will correctly identify score-0 cases. That validation requires real-campaign data + spot-check across edge cases. The residual blind-spot risk (B-1 self-scoring inherits Claude-family pattern) is acknowledged in `../README.md` and tracked under `../../OPEN-WORK-paraphrase-exception.md`.

## Cross-references

- v0.2 amendment commit: `2c8b3b8`
- Windows-claude Attack 3 (the catch this closes): PCLA `.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-RESPONSE.md` Section 2 "Attack 3"
- B-1 ACK on the residual risk: PCLA `.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-ACK-v0.2.md` HIGH 3 section

---

*Refusal documentation v1, 2026-05-19. No draft file emitted for this scenario by design.*
