# AI-Agent Audit — Level-0 instance

First base-case instance of an automated business built per `factory/SPEC.md`. Hand-built (factory v0.0 only scaffolds agents, not the value→capture loop primitives — per "base case before factory" discipline).

## Status

| Step | Component | Status | Bound |
|---|---|---|---|
| 1 | Landing page template (`landing/index.html`) | written | done |
| 2 | Intake template (`intake.md`) | written | done |
| 3 | Render script (`render.py`) + configurable pattern | written; env vars or `.local/config.env` → `.local/dist/` | done |
| 4 | Operator email | set locally in `.local/config.env` (gitignored, real value never enters git) | done locally; needs GH secret for deploy |
| 5 | Report template | deferred until after audit #1 | — |
| 6 | Stripe Checkout link | not created (operator skipped per current decision) | operator |
| 7 | GH Pages deploy workflow (`.github/workflows/pages.yml`) | written; auto-renders + deploys on push | done |
| 8 | Repo Pages enabled + GH secrets configured | NO | operator |
| 9 | Test-customer loop verified | NO | operator |

## Files

- `SPEC.md` — locked 4-axis business spec
- `landing/index.html` — landing page template (uses `{{STRIPE_CHECKOUT_URL}}`)
- `intake.md` — buyer submission template (uses `{{OPERATOR_EMAIL}}`)
- `render.py` — substitutes placeholders from env / `.local/config.env` → `.local/dist/`
- `config.env.example` — example config (tracked); copy to `.local/config.env` and fill real values (gitignored)
- `OPERATOR-ACTIONS.md` — out-of-session steps for deploy + test-loop verify
- `README.md` — this file

## Configurability pattern

Real values (operator email, Stripe URL) **never enter git**. Substitution happens at render time from either env vars or `.local/config.env` (gitignored). Deploy workflow reads them as GitHub Actions secrets. Operator's local working copies live under `.local/dist/`.

## Done-condition

Per `factory/SPEC.md` and `SPEC.md`: instance is **done** when all `operator`-bound steps are complete and a test customer (you) has run the full loop end-to-end.

Real-customer acquisition = OUT-OF-SESSION, operator-bound. Berlin 2026-06-17 talk = lead-gen.
