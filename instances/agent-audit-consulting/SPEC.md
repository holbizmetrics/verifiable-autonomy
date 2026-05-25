# Spec — AI-Agent Audit (instance v0)

Locked 2026-05-26 per session dialog. Per `factory/SPEC.md` § Input "minimum viable business-spec." First Level-0 base-case instance of the Automated Business Builder.

## 4 axes

| Axis | Value |
|---|---|
| What's sold | Written audit of an AI-agent setup — review of prompts + tool wiring + audit logs; report names hallucination/drift/misuse risks; pre-registers failure-modes-to-grep |
| To whom | Berlin Early AI-dopters (2026-06-17 attendees) with ≥1 agent in some running state (prototype or prod) |
| How delivered | Async written report only (no call), PDF or markdown, 5 business days from intake received |
| How captured | Stripe Checkout, pay-first, $2,500 USD flat; full refund if zero auditable risks found |

## Why these starters

All four were "operator doesn't know yet" defaults at spec-lock time. Picked smallest defensible answer that lets the loop close. Refine after audits 1–3 produce real signal.

- **ICP starter:** Berlin 2026-06-17 talk = scheduled forcing function, reachable audience, gives post-talk ICP signal in ~3 weeks.
- **Scope starter:** 4 operator-hours/audit caps the deliverable + lets the $2,500 price be honestly defended (~$625/hr).
- **Delivery starter:** async-only = lowest friction; add calls only if buyers ask.
- **Payment starter:** pay-first removes invoicing/collection friction; refund-promise carries the trust.

## Deferred (named, not done)

- **Report template** — write by hand after audit #1; template after audits 2–3 produce a shape (same "base case before factory" discipline as `factory/SPEC.md`).
- **Calls in delivery** — add only if buyers ask.
- **Multi-audit packages, retainers** — add only after first paying customer.

## Done-condition (per factory/SPEC.md)

The instance deploys AND the value→capture loop works end-to-end — a test customer (operator) can land → pay → submit intake → get confirmation. **First real customer = OUT-OF-SESSION, operator-bound.** The builder stops at "deployable + loop-verified."
