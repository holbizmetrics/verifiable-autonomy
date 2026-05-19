# agents/

> **Operator-supervised AI agents.** One subdirectory per agent. Each agent is self-contained: definition, falsifier, templates, runtime artifacts.

## Currently shipped

| Agent | Status | Purpose |
|---|---|---|
| `b1-customer-interviewer/` | v0 (S55) | Drafts personalized customer-discovery outreach grounded in real ICP + real prospect substrate. Classifies replies. Never sends. |

## Pattern (for future B-N agents)

Each agent directory follows the same shape:

```
agents/<agent-name>/
  README.md                 # operator-facing quickstart + workflow
  falsifier.md              # pre-registered failure modes (load-bearing)
  *-template.md             # blank operator-fillable substrate templates
  *.md                      # operator-filled real substrate (gitignored)
  drafts/                   # agent output (gitignored)
  replies/                  # operator-collected inputs (gitignored)
  test-fixtures/            # frozen self-vs-self smoke-test (committed)
  OPEN-WORK-*.md            # tracked open work from cross-op reviews
  interview-log.jsonl       # append-only audit log (gitignored, contains real prospect data)
```

The agent's runtime contract lives one level up at `.claude/agents/<agent-name>.md` (Claude Code reads it from there).

## Discipline that every agent must satisfy

From the repo manifesto (`../README.md`) + B-set proposal (`../B-PROPOSAL.md`):

1. **Pre-registered falsifier.** `falsifier.md` exists before any real use. Failure modes named, not discovered after harm.
2. **Surface-Compliance.** Every claim the agent makes is verifiable against substrate the operator can read directly. No paraphrase, no synthesis, no "I reviewed X" without grep-able evidence.
3. **Audit trail (append-only).** Every action emits a JSONL record. Operator can `tail | jq` the log without trusting the agent's narrative.
4. **No autonomous send / no autonomous external action.** v0 is operator-supervised end-to-end. Auto-mode considered only after falsifiers hold across n ≥ 2 real campaigns + cross-operator review.
5. **Operator-side classification gates.** Where the agent could grant itself permissive license (e.g. peer-register paraphrase exception), the gate lives in operator-curated substrate, not in agent self-classification. See B-1's `register:` field on prospect rows for the canonical pattern (S55 amendment v0.2).
6. **Open work tracked, not hidden.** Cross-op review items that don't land in v0.N are written to `OPEN-WORK-*.md` with explicit revisit triggers, not deferred to memory.

## When B-2 (or any future B-N) ships

Copy `b1-customer-interviewer/`'s shape. Adapt the falsifier to that agent's failure surface. Decide per-amendment whether B-1's paraphrase exception generalizes (current stance: B-1-specific; see `b1-customer-interviewer/OPEN-WORK-paraphrase-exception.md` item 6).

Do NOT copy the runtime substrate (icp.md, prospects.md, drafts/, replies/, log); those are operator-filled per-agent.

## Cross-references

- Repo manifesto: `../README.md`
- B-set proposal (B-2 through B-8 design context): `../B-PROPOSAL.md`
- Rollback contract: `../ROLLBACK.md`
- Path-decision context: `../NEXT-3-DECISIONS.md`
- Research lab (track-and-gate origin): `../../prometheus-crystal-lab-auto/` (separate repo)

---

*v1, S55 (2026-05-18). One agent shipped. Pattern document for future B-N.*
