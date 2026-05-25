# B-1: Customer Interview Runner

> **Operator-supervised customer-discovery agent.** Drafts personalized outreach grounded in a real ICP + real prospect substrate. Classifies replies. Maintains append-only audit log. Never sends email. Never invents prospects. Refuses to draft against thin substrate.

## Status

**v0.2 (S55–S57); v0.3 amendment DRAFT (S58, 2026-05-25).** v0.1 added `mark-sent`; v0.2 added the paraphrase exception for `peer` register (Falsifier 7). v0.3 draft tightens F1 (git-archaeology-aware ICP grep), F3 (dedupe by prospect_id), F5 (correction_level field), F6 (event_ts vs log_ts) — surfaced by the 2026-05-25 falsifier sweep; awaiting cross-op review. Still operator-supervised end-to-end. No SMTP, no auto-send, no cron, no autonomous fire. The agent drafts; you send.

## Quickstart

### 1. Copy the templates

```bash
cd agents/b1-customer-interviewer/
cp icp-template.md icp.md
cp prospects-template.md prospects.md
```

### 2. Fill in your ICP

Edit `icp.md`. Replace every `[fill this in]` with real substrate. Specifically:
- 5-10 concrete phrases B-1 will cite verbatim in drafts
- Falsifiable pain hypotheses, not platitudes
- Their words, not yours

The agent's draft quality is upper-bounded by this file. Vague ICP → generic drafts → no replies.

### 3. Fill in your prospects

Edit `prospects.md`. For each prospect, include **one verbatim substrate snippet**: a sentence from their public material (blog, bio, post, talk) that makes them specifically them. Generic role descriptions are not enough; the agent will skip those rows.

### 4. Invoke B-1

From the repo root, with Claude Code in this directory:

```
/agents b1-customer-interviewer draft 5
```

Or via the Task tool from a parent conversation:

```
Use the b1-customer-interviewer subagent. Prompt: "draft 5"
```

B-1 will:
1. Read `icp.md` + `prospects.md` + `interview-log.jsonl`
2. Pick the next 5 prospects that haven't been drafted yet
3. Write each draft to `drafts/<prospect_id>.md`
4. Append a `draft_emitted` (or `draft_skipped`) record to `interview-log.jsonl`
5. Print a summary

### 5. Review drafts

Read each draft in `drafts/`. Check:
- Does it cite real ICP phrases? (Listed in `## ICP phrases cited` block.)
- Does it cite the prospect's own substrate? (Listed in `## Prospect specifics cited`.)
- Does it sound like you wrote it?
- Approve, edit, or reject.

### 6. Send manually + mark sent

Send approved drafts from your own email client. For each sent, mark it in the log:

```
/agents b1-customer-interviewer mark-sent prospect-0007
```

B-1 refuses if there's no `draft_emitted` for that prospect, or if a `marked_sent` already exists (append-only discipline). The manual `echo '{...}' >> interview-log.jsonl` fallback still works if you need it, but `mark-sent` is the preferred path as of v0.1.

### 7. Drop replies + classify

When a reply lands in your inbox, save it as a text file to `replies/<prospect_id>.md` (or `replies/<prospect_id>-thread.md` for multi-message threads). Then:

```
/agents b1-customer-interviewer classify
```

B-1 will classify each new reply (`interested | no | call-booked | objection | unclear`) and draft a follow-up if appropriate.

### 8. Check status

```
/agents b1-customer-interviewer status
```

Prints campaign stats: drafts emitted, sent, replies, bucket counts, conversion rates.

## Files in this directory

| File | What it is | Who writes it |
|---|---|---|
| `icp-template.md` | Blank ICP template | Operator copies to `icp.md` |
| `prospects-template.md` | Blank prospect-list template | Operator copies to `prospects.md` |
| `icp.md` | Your real ICP | Operator |
| `prospects.md` | Your real prospect list | Operator |
| `interview-log.jsonl` | Append-only audit log | Agent writes; operator can append `marked_sent` |
| `drafts/<prospect_id>.md` | Drafted outreach | Agent |
| `replies/<prospect_id>.md` | Reply text from operator's inbox | Operator |
| `falsifier.md` | Pre-registered failure modes | Pre-existing |
| `README.md` | This file | Pre-existing |
| `test-fixtures/` | Self-vs-self smoke-test archive (DevTrace ICP + Marcus/Priya/Tom prospects + drafts + reply + log) | S55 smoke-test (frozen, v0 baseline) |
| `test-fixtures-v0.2-paraphrase-exception/` | Validation substrate for v0.2 amendment (register-from-prospects, score 0/1/2, Falsifier 7) | S55 v0.2 amendment fixture |
| `OPEN-WORK-paraphrase-exception.md` | MED/LOW items deferred from v0.2 cross-review with per-item revisit triggers | S55 v0.2 amendment open work |

## What B-1 will refuse to do

- **Send email.** No SMTP integration in v0.
- **Draft against an empty ICP.** If `icp.md` still has `[fill this in]` placeholders, agent stops.
- **Draft against thin prospect rows.** No verbatim `substrate-snippet`? Skipped with `PROSPECT_THIN`.
- **Invent prospect context.** Anything not in `prospects.md` doesn't appear in the draft.
- **Hit a target N at the cost of quality.** Agent will skip rather than fabricate.
- **Rewrite the log.** Append-only. Mistakes get correction records, not edits.

## What you (operator) should do periodically

1. **Spot-check drafts against substrate.** Pick 3 random drafts. Open `icp.md` + the prospect row. Are the cited phrases actually present verbatim? (See Falsifier 1.)
2. **Watch reply rates.** If <1% over n ≥ 30 sent, stop the campaign: either ICP is mis-targeted or drafts aren't landing. (See Falsifier 4.)
3. **Watch your own edit rate.** Rewriting >50% of drafts means the ICP needs sharpening or the agent's voice isn't yours. (See Falsifier 5.)

Full falsifier list: `falsifier.md`.

## Privacy / data hygiene

- `icp.md`, `prospects.md`, `replies/*`, `interview-log.jsonl`, `drafts/*` may contain identifying information about real prospects. **Do not commit personal data to a public repo.** When `verifiable-autonomy` flips public, these files should be gitignored or the directory restructured (e.g. real data lives in a sibling private repo; this directory has only templates + agent definition).
- For now (private repo), commit decisions are operator's. The agent doesn't push.

## Roadmap (v0.x → v1)

v0: operator-supervised draft + classify + status; manual send + manual reply ingestion.

**Shipped:**
- v0.1: `mark-sent` mode (agent appends the record for you given a prospect ID).
- v0.2: paraphrase exception for `peer` register — Falsifier 7 (paraphrase-rate drift) + `register` field on `draft_emitted` + per-register paraphrase tolerances.

**In flight:**
- v0.3 (DRAFT, awaiting cross-op review): falsifier spec tightening — A (F1 git-archaeology-aware ICP grep), B (F3 dedupe by prospect_id), C (F5 correction_level field on `marked_sent`), D (F6 event_ts vs log_ts split with `retroactive` flag). Spec at `AMENDMENT-v0.3-DRAFT-falsifier-spec-tightening.md`.

**Candidates (unranked):**
- Reply ingestion from IMAP folder (operator-approved per-fetch).
- Per-campaign metrics dashboard (operator dashboard, not agent autonomy).
- Multi-campaign support (per-ICP subdirectories).

**v1:** when falsifiers haven't fired across n ≥ 2 campaigns AND the falsifier-per-track audit log proves the discipline holds, consider auto-mode flip — per the MODE-contract gates in `../../MODE-CONTRACT.md`, not this README.

The v1 flip mirrors the PCLA mode-toggle contract (research-lab discipline): `mode: step` until proven; never auto-send without explicit operator authorization per fire.

## Cross-references

- Agent definition: `../../.claude/agents/b1-customer-interviewer.md`
- Falsifier register: `falsifier.md`
- B-set proposal context: `../../B-PROPOSAL.md`
- Repo manifesto: `../../README.md`

---

*v0.2 shipped S55–S57; v0.3 amendment DRAFT S58 (2026-05-25). First B-track shipped. Operator-supervised. No autonomy claims that the audit log cannot verify.*
