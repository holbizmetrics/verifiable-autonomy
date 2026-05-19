# Rollback contract

> **Thesis principle 6 (README): "A single command takes all tracks back to `step`. Per-track rollback triggers are pre-registered. The killswitch exists before flip, not after the first failure."**

This document is the repo-level rollback contract. Per-agent rollback triggers live in each agent's `falsifier.md`.

## Current scope (v0.2, S55)

**Nothing in this repo is currently in `auto` mode.** B-1 is in `step` (operator-supervised). The MODE contract (`MODE-CONTRACT.md`) is live as of 2026-05-19; B-1's `MODE` file + `flip-history.jsonl` are the killswitch primitive. The rollback surface today:

- **Flip B-1 to `paused`.** `/agents b1-customer-interviewer flip-mode paused`. Refuses all invocations except `status | inspect | flip-mode`. Audit log preserved.
- **Retire B-1 entirely.** Stop using the agent. MODE + history + audit-log remain as historical record.
- **Retire a single campaign.** Mark `campaign_closed` in `interview-log.jsonl`. New invocations skip closed campaigns.
- **Retire the paraphrase exception** (per Falsifier 7). Restore strict verbatim; re-review prior peer-register drafts.

There is no `auto` track in this repo to flip back yet. The PCLA research lab has one A-track in `auto` (A-3 closeout-auto); rollback there is governed by PCLA's own rollback contract.

## What rollback means when B-1 v1 ships (future)

B-1 v1 is the candidate first `auto` track in this repo (v0.2 is `step`; v1 considers `auto` after falsifiers hold across n ≥ 2 campaigns per the B-1 README roadmap).

When B-1 flips `step → auto`:

1. **Killswitch primitive (LIVE since v0.2).** `MODE-CONTRACT.md` defines the per-agent `MODE` file + `flip-history.jsonl` journal. `/agents b1-customer-interviewer flip-mode step` (or `paused`) is the single command. Audit-log untouched.
2. **Per-track rollback triggers (pre-registered).** B-1's `falsifier.md` lists the failure modes. Any falsifier-fire = automatic flip-back to `step` via the same MODE primitive. The agent refuses to operate in `auto` when its most recent campaign has a falsifier-fire on record.
3. **Audit-log preservation.** Rollback appends to `flip-history.jsonl` and (separately) does not touch `interview-log.jsonl`. Both journals are append-only. Past records remain readable.

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

*Rollback contract v1.1, S55 (2026-05-19). MODE primitive live; v0.2 scope is `step | paused | retire`. `auto` arrives with B-1 v1.*
