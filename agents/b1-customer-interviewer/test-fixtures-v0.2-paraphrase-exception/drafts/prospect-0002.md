# Draft for prospect-0002: Daniel Okafor

To: daniel@bookrails.test
Subject: BookRails at $6K MRR, 24/7 oncall as solo founder

Hi Daniel,

Saw your Indie Hackers post from April. The line that stayed with me: *"Last weekend the booking flow 500ed during a venue's busiest sales window. I did not see it for 6 hours because I was at a wedding."* That is exactly the failure mode DevTrace exists to prevent.

You said you cannot afford Datadog. We built DevTrace because "Datadog wants $300 a month minimum and most of it is for features you will not use." It is a single binary. Drop it on your server. Point at your access log. You get a Discord alert when an endpoint starts failing. $19 a month. Cancel anytime. Replaces nothing complicated.

Specifically for BookRails: booking-flow 500s on the venue's busiest sales window is exactly the alert-shape DevTrace surfaces (endpoint failure-rate spike on a path you mark important). The instrumentation is reading your nginx access log; no code change in BookRails required.

Free trial works the way you would expect: install, see one weekend, decide. If it does not catch the next booking-flow 500 within 90 seconds of it happening, I will refund.

Best,
[your name]

---

## Register

customer-dev

## ICP phrases cited (verbatim)

- "Datadog wants $300 a month minimum and most of it is for features you will not use"
- "single binary. Drop it on your server. Point at your access log"
- "$19 a month. Cancel anytime. Replaces nothing complicated"

## Prospect specifics cited

- "Last weekend the booking flow 500ed during a venue's busiest sales window. I did not see it for 6 hours because I was at a wedding." (verbatim)
- "I am one person. I cannot be on call 24/7 and I cannot afford Datadog." (verbatim)

Prospect-side citations are always verbatim in all registers; the paraphrase exception applies only to ICP citations and only in peer register.

## Why this prospect

Daniel is a candidate buyer with verbatim-matching pain. Stated bottleneck is the exact alert-shape DevTrace handles. Solo, under $10K MRR, has tried and bounced from team-shaped observability stack. Free-trial refund hook is a real risk-binding (operator-side commitment).

---

*Draft v1, 2026-05-19. Customer-dev register, strict verbatim per Surface-Compliance. Em-dash-free. Operator review required. Send NOT authorized (fixture).*
