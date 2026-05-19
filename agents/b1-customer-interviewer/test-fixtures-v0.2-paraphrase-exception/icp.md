# Ideal Customer Profile (ICP) — DevTrace v0.2-fixture variant

> **Synthetic ICP for v0.2 paraphrase-exception fixture.** Em-dash-free. Specific phrases below are written so paraphrase-vs-verbatim tension surfaces concretely.

## Who you're trying to reach

**Role:** Solo technical founders running indie SaaS products themselves. They write the code. They deploy the code. They get woken up when it breaks.

**Company stage:** $0 to $10K MRR. Solo or two people total. Bootstrapped or indie-hacker self-funded.

**Industry:** Vertical SaaS, dev tools, indie-hacker adjacent. Anywhere a single technical founder can ship and run a product end-to-end.

## Primary pain hypothesis

When prod breaks at 2am, they SSH into a $5 VPS reading raw nginx logs because the observability stack is built for teams of 30.

## What they have already tried

Datadog free tier (hits the wall at 1 host). Self-hosted Grafana (bounced because three services to install and they have one server). Sentry (covers exceptions, not infrastructure).

## What DevTrace offers

DevTrace is observability for one-person SaaS. Single binary. Drop it on your server. Point it at your access log and your error log. You get a single-pane dashboard and a Discord alert when something goes sideways. No agent forest. No time-series DB to manage. No PromQL to learn.

## Specific phrases B-1 should cite

These are the phrases B-1 cites verbatim in `sale` and `customer-dev` drafts. Peer-register drafts may paraphrase per the v0.2 amendment, with score 0/1/2 against these sources.

- "SSH into a $5 VPS reading raw nginx logs at 2am when prod breaks"
- "the observability stack is built for teams of 30"
- "Datadog wants $300 a month minimum and most of it is for features you will not use"
- "you do not need distributed tracing. You need to know which endpoint just 500ed"
- "single binary. Drop it on your server. Point at your access log"
- "no agent forest. No time-series DB. No PromQL to learn"
- "$19 a month. Cancel anytime. Replaces nothing complicated"

## What a great reply looks like

**Interested:** "How does it handle Postgres?" / "Send me a Calendly link" / "Free trial?"

**Objection worth handling:** "I already use Sentry" or "Can it scale?" Both have ICP-aligned answers.

**Hard no:** No reply after two follow-ups. Remove from active campaign.

## Out of scope

Teams of 5+. Enterprise SaaS. Pre-product founders with no prod traffic yet.

## Version

**v0.2-fixture, 2026-05-19.** Variant of `../test-fixtures/icp.md` (v0 baseline) with em-dash hygiene applied.
