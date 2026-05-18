# Ideal Customer Profile (ICP) — DevTrace v1

> **Test ICP, S55 (2026-05-18).** Fictional product for B-1 smoke test. Substrate is written to be specific enough that Surface-Compliance citation is meaningful.

## Who you're trying to reach

**Role / title:** Solo technical founders running indie SaaS products themselves — they write the code, deploy the code, and get woken up when it breaks. No co-founder, no SRE, no team.

**Company stage / size:** $0-10K MRR, < 1000 users, solo or 1-2 people total. Pre-Series-A, often pre-revenue or just past it. Bootstrapped or indie-hacker self-funded.

**Industry / vertical:** Vertical SaaS, dev tools, content tools, productivity tools — anywhere a single technical founder can ship and run a product end-to-end. Indie-hacker adjacent.

**Geography:** No constraint, but English-speaking founders most reachable.

## What you believe they're struggling with

**Primary pain hypothesis:** When prod breaks at 2am, they're SSHing into a $5 VPS reading raw nginx logs because the observability stack is built for teams of 30.

**Secondary pain:** Datadog wants $300/month minimum and most of it is for features they won't use. Grafana means standing up Prometheus + Loki + an alertmanager and learning PromQL for a one-person operation.

**What they've probably already tried:** Cloud-provider-included dashboards (CloudWatch / DO Monitoring — too generic), Sentry for errors (covers exceptions, not infrastructure), Datadog free tier (hits the wall at 1 host), self-hosted Grafana (bounced because three services to install and they have one server).

**Why those didn't work (hypothesis):** They're all priced and designed for teams. Solo founders need the 20% of observability that catches "endpoint X just started 500ing" without the 80% of distributed tracing they don't need.

## What you offer (one paragraph, in their language)

DevTrace is observability for one-person SaaS. Single binary, drop it on your server, point it at your access log and your error log. You get a single-pane dashboard that tells you what just broke and a Discord/Telegram alert when something goes sideways. No agent forest, no time-series DB to manage, no PromQL to learn. $19/month, cancel anytime, replaces nothing complicated.

## Specific phrases B-1 should cite in drafts

- "SSH into a $5 VPS reading raw nginx logs at 2am when prod breaks"
- "the observability stack is built for teams of 30"
- "Datadog wants $300/month minimum and most of it is for features you won't use"
- "you don't need distributed tracing, you need to know which endpoint just 500ed"
- "single binary, drop on your server, point at your access log"
- "no agent forest, no time-series DB to manage, no PromQL to learn"
- "your future self at 2am will thank you for this"
- "$19/month, cancel anytime, replaces nothing complicated"

## What a great reply looks like

**Interested:** "How does it handle Postgres?" / "What's the deploy story?" / "Send me a Calendly link" / "Free trial?"

**Objection worth handling:** "I already use Sentry" → DevTrace is infra, not exceptions, complements. "I'm too small" → 100 users is exactly when 2am alerts start hurting. "Can it scale?" → not for teams of 30, that's the point.

**Hard no:** "Not a priority" / "Please remove me" / no reply after 2 follow-ups.

## What's out of scope

- Teams of 5+ engineers (they should buy Datadog)
- Enterprise SaaS (they have an SRE)
- Pre-product solo founders (no prod yet, no pain yet)

## Date / version

**Last updated:** 2026-05-18
**ICP version:** v1 (smoke test for B-1)
