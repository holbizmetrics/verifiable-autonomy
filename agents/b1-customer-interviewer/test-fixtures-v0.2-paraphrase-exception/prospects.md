# Prospects — v0.2 paraphrase-exception fixture

> **Synthetic prospects, S55 (2026-05-19).** Three fictional founders with substrate snippets and register classifications. Tests the operator-side register gate (HIGH 2) and the paraphrase exception flow (HIGH 3).

## prospect-0001: Naomi Larkin

- **email:** naomi@logpipe.test
- **role:** Solo builder
- **company:** LogPipe (indie observability tool, single-binary, similar product surface to DevTrace)
- **company-stage:** 80 paying users, $2K MRR, launched 6 months ago
- **register:** peer
- **substrate-snippet:** "I built LogPipe as a single binary because I refuse to maintain three services for one server. Every observability tool I tried wanted me to install Prometheus + Loki + Grafana to monitor a $5 droplet. That is not a tool for solo builders. That is a tool for teams who already have an SRE."
- **substrate-source:** Naomi's blog post 2026-02-08 'Why I Built LogPipe'
- **why-this-prospect:** Adjacent-product builder with the same ICP. Pitching her would be tone-deaf; she is not a buyer. But comparing notes on the shape of the single-binary discipline is a legitimate peer conversation.

## prospect-0002: Daniel Okafor

- **email:** daniel@bookrails.test
- **role:** Founder and sole engineer
- **company:** BookRails (booking SaaS for independent music venues)
- **company-stage:** $6K MRR, 14 paying venues, 1 person, deploys nightly
- **register:** customer-dev
- **substrate-snippet:** "Last weekend the booking flow 500ed during a venue's busiest sales window. I did not see it for 6 hours because I was at a wedding. I am one person. I cannot be on call 24/7 and I cannot afford Datadog. I need something that just tells me when an endpoint starts failing."
- **substrate-source:** Daniel's Indie Hackers post 2026-04-30
- **why-this-prospect:** Candidate buyer. Stated bottleneck is verbatim what DevTrace handles. Solo, under $10K MRR, has tried and bounced from the team-shaped observability stack.

## prospect-0003: Priscilla Vance

- **email:** priscilla@ventory.test
- **role:** Founder
- **company:** Ventory
- **register:** peer
- **substrate-snippet:**
- **substrate-source:**
- **why-this-prospect:**

(Intentionally thin substrate. B-1 should skip with `PROSPECT_THIN` regardless of register classification. The skip-vs-draft decision happens before register-driven citation discipline.)

---

*Fixture prospects v1, 2026-05-19. Two with real substrate, one thin. Each row carries the v0.2 `register:` field.*
