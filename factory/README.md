# Factory v0.1

> **The verifiable business factory.** Takes a business-spec, emits a deployable automated business: per-agent dirs wired from the `agents/` templates AND (when the spec has a `loop` block) a `storefront/` value→capture loop — landing page, intake, render script, deploy guide — with business content baked in and operator secrets left for deploy-time. Mode defaults to `step`, ready to be opened in Claude Code. v0.1 (loop emission), 2026-06-23. v0.0, S58 (2026-05-25).

## What this is

The minimum viable factory. Input: a JSON business-spec. Output: a `businesses/<name>/` directory with the spec's agents instantiated and wired, plus — when the spec carries a `loop` block — a `storefront/` containing the value→capture loop (landing page, intake, render script, deploy workflow template). No hosted infra; runs entirely on the operator's laptop. Each output business is a separate Claude Code project that inherits the V-A MODE-contract discipline.

**Two-stage substitution (how secrets stay out of git).** The factory fills *business content* (`{{SPEC:...}}` — headline, pitch, price, promise, intake fields) at **build time**. The emitted storefront's own `render.py` fills *operator secrets* (`{{OPERATOR_EMAIL}}`, `{{STRIPE_CHECKOUT_URL}}`) at **deploy time**, from env vars or a gitignored `.local/config.env`. Real values never enter git; a spec is enough to build, an operator's keys are needed only to deploy.

This is the layer **above** the B-tracks (`B-PROPOSAL.md`). The B-tracks are the primitives; the factory composes them per spec. Shipping one business instance manually was the entire repo until now; this is the generalizer.

## What this is NOT

- Not a hosted multi-tenant platform. Each output is a local directory.
- Not a real orchestrator yet — it scaffolds, it doesn't run agents on a schedule.
- Not v1.0. v0.0 dogfoods on V-A itself; v0.1 adds a second instance (different ICP, different offer); v1.0 is `ROADMAP.md` § Versioning.

## Usage

The pipeline is **desire → spec → business**:

```bash
# 1. Scaffold a spec from the interview axes (prints the questions to fill):
python factory/factory.py new my-business --desire "sell X to Y"
#    -> factory/specs/my-business.json (axes/offer/loop as TODO)
#    Interview the operator; fill the TODOs. The factory does NOT auto-ideate.

# 2. Validate before building (build also does this; this is the standalone check):
python factory/factory.py validate factory/specs/my-business.json

# 3. Build (validates first; refuses on errors):
python factory/factory.py build factory/specs/agent-audit-consulting.json   # full loop
python factory/factory.py build factory/specs/verifiable-autonomy.json      # agents-only
```

`build` outputs to `businesses/<name>/`. Open it in Claude Code and the agents are wired; if a `storefront/` was emitted, follow `storefront/OPERATOR-ACTIONS.md` to deploy the landing + intake loop.

## Commands

| Command | What it does |
|---|---|
| `new <slug> [--desire ...]` | Scaffold `factory/specs/<slug>.json` from the four minimum-viable axes; print the interview. Refuses to overwrite. |
| `validate <spec>` | Report errors (block a build) + warnings (don't). Exit 1 if any error. |
| `build <spec>` | Validate, then emit `businesses/<name>/`. **Refuses to build an invalid spec** — no broken business ships silently. |

## Validation rules

**Errors (block the build):** missing/bad `name` (must be an `[a-z0-9-]` slug); no `agents`, or an agent whose template is absent; invalid `mode`; a `loop` with an unknown `type`, no headline/title, no intake, or whose `offer` lacks `price`/`promise` (the landing renders those).

**Warnings (don't block):** no `axes` block; unfilled `offer.paragraph`; agents-only spec with no offer; any straggler `"TODO"` left anywhere (so a half-filled scaffold is loud).

## The interview axes (the minimum-viable business-spec)

`new` scaffolds these four; the operator/agent fills them. Per `factory/SPEC.md` § Input — the factory **interviews to clarify, it does not invent** (autonomous ideation is deferred):

- `axes.what_is_sold` — the product/offer in one phrase
- `axes.to_whom` — the ICP
- `axes.how_value_delivered` — storefront / written report / flow
- `axes.how_money_captured` — payment mechanism + price

## Spec format

```json
{
  "name": "<business-slug>",
  "agents": ["b1-customer-interviewer", "..."],
  "icp_source": "agents/b1-customer-interviewer/icp.md",
  "mode": "step",
  "axes": {
    "what_is_sold": "...",
    "to_whom": "...",
    "how_value_delivered": "...",
    "how_money_captured": "..."
  },
  "offer": {
    "paragraph": "...",
    "price": "...",
    "promise": "..."
  },
  "loop": {
    "type": "email-intake",
    "title": "Display title",
    "headline": "Landing <h1>",
    "pitch": "Landing lead paragraph (falls back to offer.paragraph)",
    "cta_label": "Request an audit",
    "cta_subject": "AI-Agent Audit — Request",
    "turnaround": "5 business days from intake received.",
    "footer": "Delivered async (written, no call).",
    "what_you_send": ["...", "..."],
    "what_you_get": ["...", "..."],
    "intake_fields": [
      { "heading": "Prompts", "items": ["...", "..."] }
    ]
  }
}
```

Fields:
- `name` — directory slug. Refuses to overwrite an existing `businesses/<name>/`.
- `agents` — list of agent IDs from `agents/` to scaffold into the business.
- `icp_source` — repo-relative path to the ICP markdown to copy into each agent dir.
- `mode` — default MODE for all agents in this instance. Defaults to `step`.
- `offer` — paragraph + price + promise. Renders to `OFFER.md` in the output.
- `loop` — **optional.** When present, emits a `storefront/` value→capture loop. Omit it for an agents-only scaffold (no customer-facing surface). Sub-fields:
  - `type` — loop shape (currently `email-intake`; Stripe path stubbed in `render.py`/config). Recorded in `manifest.json`.
  - `title`, `headline`, `pitch`, `cta_label`, `cta_subject`, `turnaround`, `footer` — landing-page content (`pitch` defaults to `offer.paragraph`; price/promise come from `offer`).
  - `what_you_send`, `what_you_get` — bullet lists on the landing page.
  - `intake_fields` — structured intake sections (`[{heading, items:[...]}]`); falls back to `what_you_send` as a flat list if omitted.
- `repo_url` — **optional.** Substrate link in the landing footer (defaults to the V-A repo).

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

## What gets emitted (the storefront, when `loop` is present)

Into `businesses/<name>/storefront/`, from `factory/templates/loop/`:
- `landing/index.html` — landing page; `{{SPEC:...}}` content baked in, `{{OPERATOR_EMAIL}}` left for deploy-time
- `intake.md` — intake form (structured from `intake_fields`)
- `render.py` — deploy-time renderer; fills operator secrets from env / `.local/config.env` → `.local/dist/`
- `config.env.example` — copy to `.local/config.env` (gitignored) and fill
- `deploy-pages.yml.tmpl` — GitHub Pages workflow to drop into the business's own repo
- `OPERATOR-ACTIONS.md` — the deploy + test-loop-verify guide

`build` warns (non-fatal) if any `{{SPEC:...}}` placeholder is left unfilled — a malformed spec is loud, not silently shipped with a hole. The count + any unfilled placeholders are recorded under `manifest.json` → `loop`.

## Falsifier (for the factory itself)

The factory is **doing its job** if:
- `python factory/factory.py build factory/specs/verifiable-autonomy.json` produces `businesses/verifiable-autonomy/` with a runnable B-1 agent inside.
- A second spec (different name, different ICP) produces a second, isolated business directory.
- Opening `businesses/<name>/` in Claude Code lets the operator run B-1 (or whatever was scaffolded) without manual wiring.
- A spec with a `loop` block emits a `storefront/` whose `render.py` produces a complete landing page (CTA wired to the operator email, no unfilled placeholders) — i.e. the value→capture loop is deployable, not just scaffolded. Verify: `python factory/factory.py build factory/specs/agent-audit-consulting.json && OPERATOR_EMAIL=test@example.com python businesses/agent-audit-consulting/storefront/render.py && grep -c '{{SPEC:' businesses/agent-audit-consulting/storefront/.local/dist/landing/index.html` → `0`.
- A spec **without** a `loop` block emits **no** `storefront/` (agents-only scaffold).

The factory has **failed** if:
- It needs hand-fixing after every build (= it's not actually a factory, it's a sketch).
- Two builds from different specs produce overlapping state (= no isolation).
- It silently overwrites operator edits in `businesses/<name>/` (= it destroys work).

## Roadmap

- **v0.0**: single-agent scaffold; JSON spec; B-1 only; dogfood on V-A itself.
- **v0.1** (now): value→capture loop emission (`storefront/` from a spec `loop` block) — landing + intake + render + deploy guide, two-stage substitution, utf-8 pinned. The factory now builds a *deployable* business, not just an agent scaffold. Dogfooded on `agent-audit-consulting` (reproduces the hand-built `instances/` storefront from spec).
- **v0.2**: multi-agent scaffold; spec validation; MODE-contract wiring (per-instance flip-history; killswitch propagation).
- **v0.3+**: agent-template versioning (so the factory can produce instances at older B-1 versions deliberately); spec inheritance.
- **v1.0** per `ROADMAP.md` § Versioning: N≥3 instances from spec; falsifier-clean autonomy on mechanism; cross-op review of the factory's instantiation discipline (not just per-instance).

The hosted-infra layer (`B-PROPOSAL.md` § Cross-cutting infrastructure #1) is the substrate every factory output beyond v0.0 will eventually deploy onto. v0.0 deliberately runs without it: prove the compiler first, host later.
