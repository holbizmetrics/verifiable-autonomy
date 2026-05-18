# Prospects — DevTrace smoke test

> **Test prospects, S55 (2026-05-18).** Three fictional indie founders with synthetic-but-realistic substrate snippets. **Names and companies are fictional**; substrate is written to simulate the kind of public blog/tweet material an operator would actually source. The test: does B-1 cite verbatim and refuse to draft against the thin row?

## prospect-0001: Marcus Chen

- **email:** marcus@shipreceipts.test
- **role:** Solo founder & engineer
- **company:** ShipReceipts (invoice tool for Shopify-adjacent marketplaces)
- **company-stage:** ~$3K MRR, launched 4 months ago, 1 person operation
- **substrate-snippet:** "I built ShipReceipts in 3 months and now I'm running it from my MacBook at home. Last Sunday production went down for 4 hours because I was hiking and didn't see the Discord alert. I'm not adding Datadog — that's $200/month, and I'd spend another 10 hours learning it."
- **substrate-source:** Marcus's blog post 2026-04-22 'On Being My Own SRE'
- **why-this-prospect:** Stated bottleneck matches ICP primary pain hypothesis verbatim; he's already articulated rejection of Datadog for the exact reason the ICP names; solo and runs prod himself.

## prospect-0002: Priya Subramaniam

- **email:** priya@clinicqueue.test
- **role:** Founder & sole engineer
- **company:** ClinicQueue (waitroom-management SaaS for dental practices)
- **company-stage:** $8K MRR, 22 paying customers, deploys daily, 1 person
- **substrate-snippet:** "We just hit $8K MRR. I deploy to a $40 DigitalOcean droplet every morning. When something breaks, I SSH in and grep through journalctl. I tried Grafana for a weekend and bounced — it's three services to install and I have one server."
- **substrate-source:** Priya's tweet thread 2026-03-15
- **why-this-prospect:** Articulates the Grafana-bounce path the ICP names; SSH-and-grep workflow is exactly what DevTrace replaces; under $10K MRR so still solo.

## prospect-0003: Tom Wexler

- **email:** tom@wexlerlabs.test
- **role:** Founder
- **company:** Wexler Labs
- **substrate-snippet:**
- **substrate-source:**
- **why-this-prospect:**

(Note: this prospect's row is intentionally THIN — no substrate-snippet provided. B-1 should skip with `PROSPECT_THIN` rather than draft a generic email.)
