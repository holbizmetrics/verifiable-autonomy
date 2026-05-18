# Rollback contract

> **Thesis principle 6 (README): "A single command takes all tracks back to `step`. Per-track rollback triggers are pre-registered. The killswitch exists before flip, not after the first failure."**

This document is the repo-level rollback contract. Per-agent rollback triggers live in each agent's `falsifier.md`.

## Current scope (v0, S55)

**Nothing in this repo is currently in `auto` mode.** B-1 is operator-supervised end-to-end. The "rollback" surface today is therefore:

- **Retire B-1 v0 entirely.** Stop using the agent. The audit log remains as historical record.
- **Retire a single campaign.** Mark `campaign_closed` in `interview-log.jsonl`. New invocations skip closed campaigns.
- **Retire the paraphrase exception** (per Falsifier 7). Restore strict verbatim; re-review prior peer-register drafts.

There is no `auto` track in this repo to flip back. The PCLA research lab has one A-track in `auto` (A-3 closeout-auto); rollback there is governed by PCLA's own rollback contract.

## What rollback means when B-1 v1 ships (future)

B-1 v1 is the candidate first `auto` track in this repo (v0 is `step`-only; v1 considers auto-mode after falsifiers hold across n ≥ 2 campaigns per the B-1 README roadmap).

When B-1 flips `step → auto`:

1. **Killswitch command (single).** A repo-level command takes B-1 back to `step` without losing audit history. Proposed shape: a file flag `agents/b1-customer-interviewer/MODE` containing `step` or `auto`. B-1 reads this on every invocation; defaults to `step` if absent or unparseable.
2. **Per-track rollback triggers (pre-registered).** B-1's `falsifier.md` already lists the failure modes. Any falsifier firing = flip back to `step` automatically. The agent itself refuses to operate in `auto` mode when its most recent campaign has a falsifier-fire on record.
3. **Audit-log preservation.** Rollback never edits the log. Append a `mode_changed` record with the trigger (`falsifier_fire | operator_killswitch | scheduled_retirement`). Past records remain readable.

## Per-agent rollback triggers (pre-registered)

Each agent's `falsifier.md` is the per-agent rollback contract. As of S55:

- **B-1:** `agents/b1-customer-interviewer/falsifier.md` (Falsifiers 1-7; any single fire = retire mode-auto if ever active; 3 fires across same falsifier = retire v0)

Future B-N agents must ship a `falsifier.md` before any `step → auto` consideration.

## What rollback never does

- **Edit the audit log.** Append-only is non-negotiable.
- **Hide a failure.** Falsifier-fire that triggered rollback is logged with the trigger, the timestamp, and the operator's call.
- **Bypass cross-operator review.** A rollback that adds back to `auto` later requires fresh cross-op review at minimum the rung from the original flip.

## Cross-references

- Repo manifesto: `README.md` (thesis principle 6)
- B-1 falsifier register: `agents/b1-customer-interviewer/falsifier.md`
- PCLA rollback patterns (research-side reference): `prometheus-crystal-lab-auto/Prometheus/KERNEL.md` + per-track SPECs
- Path-decision context: `NEXT-3-DECISIONS.md`

---

*Rollback contract v1, S55 (2026-05-18). v0 scope is retirement, not mode-flip. Updates when first `auto` track ships.*
