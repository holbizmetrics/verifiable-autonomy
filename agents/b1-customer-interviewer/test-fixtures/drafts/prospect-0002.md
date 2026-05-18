# Draft for prospect-0002: Priya Subramaniam

To: priya@clinicqueue.test
Subject: One server, $19/mo, no Prometheus

Hi Priya,

Reading your 2026-03-15 thread on hitting $8K MRR and deploying to a $40 droplet — congrats. The specific bit that caught me: "I tried Grafana for a weekend and bounced — it's three services to install and I have one server." That's the exact reason DevTrace exists.

You don't need distributed tracing, you need to know which endpoint just 500ed — and DevTrace gives you that in a single binary. No agent forest, no time-series DB to manage, no PromQL to learn. Drop it on the droplet, point at the access log, done.

$19/month, cancel anytime, replaces nothing complicated. Worth 15 minutes this week?

— [your name]

---

## ICP phrases cited
- "you don't need distributed tracing, you need to know which endpoint just 500ed"
- "no agent forest, no time-series DB to manage, no PromQL to learn"
- "$19/month, cancel anytime, replaces nothing complicated"

## Prospect specifics cited
- "I tried Grafana for a weekend and bounced — it's three services to install and I have one server."

## Why this prospect
Priya hit $8K MRR solo on a single droplet, tried Grafana and bounced for the exact ICP-named reason ("three services to install, one server"). Single-server, SSH-and-grep workflow. Pre-qualified on the Grafana-rejection angle.

---

*Draft v1. Operator review required before send.*
