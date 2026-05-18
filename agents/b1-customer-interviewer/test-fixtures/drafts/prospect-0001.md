# Draft for prospect-0001: Marcus Chen

To: marcus@shipreceipts.test
Subject: 4 hours down on a Sunday — there's a $19/mo fix

Hi Marcus,

Saw your "On Being My Own SRE" post — specifically: "Last Sunday production went down for 4 hours because I was hiking and didn't see the Discord alert." That hit, because that's exactly the bracket DevTrace is built for.

Datadog wants $300/month minimum and most of it is for features you won't use. DevTrace is the opposite end: single binary, drop on your server, point at your access log. You get one dashboard plus Discord alerts the second your error rate ticks up — so the Sunday-hiking-version of you actually finds out before the user does.

Your future self at 2am will thank you for this. $19/month, ~10 minutes to deploy.

Worth a 15-min call this week?

— [your name]

---

## ICP phrases cited
- "Datadog wants $300/month minimum and most of it is for features you won't use"
- "single binary, drop on your server, point at your access log"
- "your future self at 2am will thank you for this"

## Prospect specifics cited
- "Last Sunday production went down for 4 hours because I was hiking and didn't see the Discord alert."

## Why this prospect
Marcus's "On Being My Own SRE" post articulates a 4-hour outage caused by missing a Discord alert while hiking — that's the exact "alert-blind-spot for solo founder" scenario DevTrace addresses. He's already publicly rejected Datadog ("$200/month and 10 hours to learn") for the reason DevTrace exists. Pre-qualified.

---

*Draft v1. Operator review required before send.*
