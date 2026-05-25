# Factory v0.0

> **The verifiable business factory.** Takes a business-spec, emits a scaffolded automated business: per-agent dirs wired from the `agents/` templates, configured to the spec's ICP + offer, mode defaulting to `step`, ready to be opened in Claude Code. v0.0, S58 (2026-05-25).

## What this is

The minimum viable factory. Input: a JSON business-spec. Output: a `businesses/<name>/` directory with the spec's agents instantiated and wired. No hosted infra; runs entirely on the operator's laptop. Each output business is a separate Claude Code project that inherits the V-A MODE-contract discipline.

This is the layer **above** the B-tracks (`B-PROPOSAL.md`). The B-tracks are the primitives; the factory composes them per spec. Shipping one business instance manually was the entire repo until now; this is the generalizer.

## What this is NOT

- Not a hosted multi-tenant platform. Each output is a local directory.
- Not a real orchestrator yet — it scaffolds, it doesn't run agents on a schedule.
- Not v1.0. v0.0 dogfoods on V-A itself; v0.1 adds a second instance (different ICP, different offer); v1.0 is `ROADMAP.md` § Versioning.

## Usage

```bash
python factory/factory.py build factory/specs/verifiable-autonomy.json
```

Outputs to `businesses/verifiable-autonomy/`. Open that directory in Claude Code and the agents are wired.

## Spec format (v0.0)

```json
{
  "name": "<business-slug>",
  "agents": ["b1-customer-interviewer", "..."],
  "icp_source": "agents/b1-customer-interviewer/icp.md",
  "mode": "step",
  "offer": {
    "paragraph": "...",
    "price": "...",
    "promise": "..."
  }
}
```

Fields:
- `name` — directory slug. Refuses to overwrite an existing `businesses/<name>/`.
- `agents` — list of agent IDs from `agents/` to scaffold into the business.
- `icp_source` — repo-relative path to the ICP markdown to copy into each agent dir.
- `mode` — default MODE for all agents in this instance. Defaults to `step`.
- `offer` — paragraph + price + promise. Renders to `OFFER.md` in the output.

## What gets scaffolded (per agent)

From the template at `agents/<agent_id>/`:
- `README.md`, `falsifier.md`, `icp-template.md`, `prospects-template.md` — copied
- `MODE` — written from spec (default `step`)
- `icp.md` — copied from `icp_source` if present, else from template
- `prospects.md` — from `prospects-template.md` (operator fills per business)
- `interview-log.jsonl`, `flip-history.jsonl` — empty
- `drafts/`, `replies/` — empty dirs

Skipped (per-instance state that should not be copied across businesses):
- existing `icp.md`, `prospects.md`, `interview-log.jsonl`, `drafts/`, `replies/`, `flip-history.jsonl`, `MODE` from the template dir
- `test-fixtures*/`, `OPEN-WORK-*.md`, `AMENDMENT-*.md` (template-dir housekeeping)

## Falsifier (for the factory itself)

The factory is **doing its job** if:
- `python factory/factory.py build factory/specs/verifiable-autonomy.json` produces `businesses/verifiable-autonomy/` with a runnable B-1 agent inside.
- A second spec (different name, different ICP) produces a second, isolated business directory.
- Opening `businesses/<name>/` in Claude Code lets the operator run B-1 (or whatever was scaffolded) without manual wiring.

The factory has **failed** if:
- It needs hand-fixing after every build (= it's not actually a factory, it's a sketch).
- Two builds from different specs produce overlapping state (= no isolation).
- It silently overwrites operator edits in `businesses/<name>/` (= it destroys work).

## Roadmap

- **v0.0** (now): single-agent scaffold; JSON spec; B-1 only; dogfood on V-A itself.
- **v0.1**: multi-agent scaffold; spec validation; second-instance proof (different ICP + offer).
- **v0.2**: MODE-contract wiring (per-instance flip-history; killswitch propagation).
- **v0.3+**: agent-template versioning (so the factory can produce instances at older B-1 versions deliberately); spec inheritance.
- **v1.0** per `ROADMAP.md` § Versioning: N≥3 instances from spec; falsifier-clean autonomy on mechanism; cross-op review of the factory's instantiation discipline (not just per-instance).

The hosted-infra layer (`B-PROPOSAL.md` § Cross-cutting infrastructure #1) is the substrate every factory output beyond v0.0 will eventually deploy onto. v0.0 deliberately runs without it: prove the compiler first, host later.
