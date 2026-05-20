# MODE contract

> **Thesis principle 1 (README): "Mode-toggle (`step | auto`) is per-agent, not per-repo." Principle 6: "A single command takes all tracks back to `step`."**

This document is the repo-level contract for how an agent's execution mode is recorded, read, and changed. It is the kernel piece that makes `step → auto` a real architectural transition, not a narrative one.

## What the contract says

Every agent has two runtime files:

| File | Role | Mutability |
|---|---|---|
| `agents/<agent>/MODE` | Current mode. One word: `step`, `auto`, or `paused`. | Overwritten on flip. |
| `agents/<agent>/flip-history.jsonl` | Append-only audit of every mode transition. | Append-only. Never edit, never rewrite. |

The two files are coupled. `MODE` is the cheap-read source of truth at agent boot. `flip-history.jsonl` is the journal that proves the current value of `MODE` is one the operator authorized.

If the two ever disagree (latest flip-history record's `to_mode` != current `MODE` file content), the agent must refuse to operate and report the discrepancy. This is the load-bearing invariant.

## What each mode means

| Mode | Agent behavior |
|---|---|
| `step` | Operator-supervised. The agent runs invocations the operator triggers explicitly (`/agents <name> <mode> ...`). Never self-fires. Default for v0 of every agent. |
| `auto` | The agent may self-fire on its pre-registered triggers (defined in the agent's own SPEC / agent definition). Subject to falsifier-fire automatic flip-back to `step`. |
| `paused` | The agent refuses all invocations except `status`, `inspect`, and `flip-mode`. Used when an agent is under investigation or a campaign is closed but the agent isn't retired. |

`step` is the default. An agent with no `MODE` file is treated as `step`, but the agent must immediately surface the missing file to the operator and refuse work until it is created (this prevents silent-default-to-step from masking a corruption).

## The flip-history.jsonl record shape

Every transition appends one line:

```json
{
  "timestamp": "2026-05-19T20:18:49Z",
  "agent": "b1-customer-interviewer",
  "from_mode": "step",
  "to_mode": "auto",
  "trigger": "falsifier_clean | operator_killswitch | falsifier_fire | scheduled_retirement | initialization",
  "authorized_by": "operator | falsifier-N-fire | system",
  "falsifier_status": "summary of pre-registered falsifier state at flip time",
  "cross_op_review": "summary or pointer to the review artifact, if required by this transition",
  "note": "free-form context"
}
```

Initialization records use `from_mode: null` and `trigger: initialization`.

## Read discipline (every agent invocation)

At the start of every invocation, the agent must:

1. Read `agents/<self>/MODE`. If missing or unparseable: refuse work, tell operator.
2. Read the LAST record of `agents/<self>/flip-history.jsonl`. If missing or unparseable: refuse work.
3. Verify `MODE` content == last flip-history record's `to_mode`. If mismatch: refuse work, surface both values.
4. If `MODE == paused` and the invocation is not `status | inspect | flip-mode`: refuse with one-line explanation pointing at the most recent flip-history record.
5. If `MODE == step` and the invocation is one of the agent's pre-registered self-fire triggers (not operator-explicit): refuse. Self-fire requires `auto`.
6. Otherwise proceed.

The read is cheap (two small files); skipping it is the failure mode this contract exists to prevent.

## Flip discipline (the `flip-mode` invocation)

Every agent exposes a `flip-mode <target>` invocation. The transition rules:

| From | To | Allowed? | Preconditions |
|---|---|---|---|
| any | `step` | always | none beyond operator confirmation |
| any | `paused` | always | none beyond operator confirmation |
| `step` | `auto` | conditional | (a) agent's falsifier.md is clean across the most recent n campaigns (n defined per agent, typically ≥2); (b) cross-operator review artifact exists; (c) operator confirms |
| `paused` | `auto` | conditional | same as `step → auto` plus an explicit reason for un-pausing |
| `auto` | `auto` | refused | no-op; agent surfaces "already in auto" |

The agent itself enforces these gates. The agent refuses to flip to `auto` if it cannot find evidence of the preconditions. Evidence pointers (paths to falsifier-clean summaries + cross-op review files) are recorded in the new flip-history record.

`flip-mode` itself does two writes:
1. Append the new record to `flip-history.jsonl`.
2. Overwrite `MODE` with the new value.

If either write fails, the agent must refuse all further invocations until the operator resolves the inconsistency. The append-then-overwrite order means a crash between writes leaves `MODE` stale (still showing the old value) but the history shows the intent. The read-discipline check (step 3 above) catches this.

## Falsifier-fire automatic flip-back

When an agent in `auto` detects one of its own pre-registered falsifier-fire conditions, it must:

1. Immediately flip to `step` via the same flip-mode mechanism. `authorized_by: falsifier-N-fire`.
2. Surface a one-line summary to the operator (or the next operator who reads the log).
3. Refuse further work until the operator acknowledges and either repairs the substrate or retires the agent.

The flip-back is the killswitch in the steady state. The repo-level "single command" killswitch (`./killswitch all`) is a convenience layer over the same primitive: it iterates every agent and, for any agent not already in `step`, appends one flip-history record and overwrites `MODE` to `step`.

## Cross-references

- Repo manifesto: `README.md` (thesis principles 1, 6, and the `step → auto` discipline)
- Rollback contract: `ROLLBACK.md`
- B-1 agent definition: `.claude/agents/b1-customer-interviewer.md`
- B-1 falsifier register: `agents/b1-customer-interviewer/falsifier.md`
- Pattern doc: `agents/README.md`
- PCLA research-side parallel: `prometheus-crystal-lab-auto/modes.yaml` (per-track mode, repo-wide config rather than per-agent files; PCLA is research, this repo is execution-runtime)

## Why this exists as a contract, not just a convention

A convention can drift. A contract is enforced at every invocation. Three things would break the audit-trail discipline of this repo if MODE were a convention:

1. **Silent flip.** An agent that "feels ready" for `auto` could narrate the flip in chat without recording it. The flip-history journal forecloses this: no record = no flip.
2. **Mode-drift across sessions.** An agent that read MODE once at session start and held it in memory could keep operating in stale `auto` after the operator killed it elsewhere. Read-on-every-invocation forecloses this.
3. **MODE/history skew.** A direct edit to `MODE` (operator running `echo auto > MODE`) without a history record would bypass the precondition gate. The MODE-vs-history match check forecloses this: the agent refuses to operate when the two disagree.

The contract is small (two files per agent + 6 read-steps + 1 flip primitive). The discipline it enforces is the architectural difference between "we say we're operator-supervised" and "every action is audit-checkable."

---

*MODE-contract v1, S55 (2026-05-19). First per-agent MODE file lives at `agents/b1-customer-interviewer/MODE`. Future agents copy the pattern.*
