# AI-Agent Audit — Level-0 instance

First base-case instance of an automated business built per `factory/SPEC.md`. Hand-built (factory v0.0 only scaffolds agents, not the value→capture loop primitives — per "base case before factory" discipline).

## Status

| Step | Component | Status | Bound |
|---|---|---|---|
| 1 | Landing page (`landing/index.html`) | written; needs operator to substitute `{{STRIPE_CHECKOUT_URL}}` | in-session done / operator action pending |
| 2 | Stripe Checkout link | not created | operator |
| 3 | Intake form (`intake.md`, email-reply) | written; needs operator email substituted | in-session done / operator action pending |
| 4 | Report template | deferred until after audit #1 | — |
| 5 | Deploy | not deployed | operator |
| 6 | Test-customer loop verified | NO | operator |

## Files

- `SPEC.md` — locked 4-axis business spec
- `landing/index.html` — landing page (operator to fill Stripe URL + deploy)
- `intake.md` — what buyers submit after paying (operator to fill email)
- `OPERATOR-ACTIONS.md` — out-of-session steps for deploy + test-loop verify
- `README.md` — this file

## Done-condition

Per `factory/SPEC.md` and `SPEC.md`: instance is **done** when steps 1–3, 5, 6 above are all complete and a test customer (you) has run the full loop end-to-end.

Real-customer acquisition = OUT-OF-SESSION, operator-bound. Berlin 2026-06-17 talk = lead-gen.
