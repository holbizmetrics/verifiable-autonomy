# Persona-Sweep Audit — operator-bound actions (out-of-session)

Everything below needs you; the builder stops at deployable + loop-verified.

1. **Calibration run #0 (before any pitch):** the warm PM contact runs with the
   one-pager. Free-for-data. Collect: which deliverable he'd pay for (doc / service /
   tool), his org's real intake artifacts' shape, and his unanticipated-gap count.
   Only after this lands, decide whether to pitch a paid sweep into his org.
2. **Config:** copy `config.env.example` → `.local/config.env`, set OPERATOR_EMAIL.
   Run `python render.py` → `.local/dist/`.
3. **Deploy:** extend the existing Pages workflow to render this instance too, or host
   `.local/dist/landing` anywhere static. (Same pattern as agent-audit-consulting.)
4. **Invoice mechanism:** same manual-invoice path as the sibling instance. Stripe
   stays deferred for sweeps 1–3.
5. **Test-customer loop:** you, as test customer — land → mail intake → receive
   invoice → confirmation. Loop verified = done-condition met.
6. **Pricing sanity:** after sweep #1, check hours against $3,000 and adjust the SPEC
   (the number is a starter, not a finding).
