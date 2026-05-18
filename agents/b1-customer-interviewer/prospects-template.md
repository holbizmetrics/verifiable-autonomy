# Prospects — TEMPLATE

> **Fill this in before invoking B-1 draft mode.** B-1 expects this file to contain a list of real prospects with enough substrate per row that personalization is possible. Thin rows → B-1 skips the prospect (logs `PROSPECT_THIN`) rather than fabricating context. **The agent will never invent a fact about a prospect that isn't on this page.**

## How to structure each prospect

Use markdown sections per prospect, with the headings below. B-1 parses `## prospect-<id>: <name>` as the row boundary.

Required fields: id, name, email, role, company, **one verbatim substrate snippet** (a sentence from their bio / blog / talk / job post that makes them them, not a generic role-holder).

Optional but recommended: company-stage, recent observable (funding, launch, post — only include if you have a verifiable source), the specific reason you're reaching out to THEM.

Do NOT include speculation. If you don't know what they care about, leave it blank — B-1 will skip with `PROSPECT_THIN` rather than invent.

## Example row (delete after filling in real ones)

### prospect-0001: Jane Founder

- **email:** jane@example.com
- **role:** Co-founder & CEO
- **company:** Example.co (15 employees, B2B SaaS for veterinary clinics)
- **company-stage:** ~$2M ARR, raised $1.5M seed in Q3 2025
- **substrate-snippet:** "We hired our last two engineers in 11 weeks combined — I screened every one of the 340 resumes myself because no recruiter understood our Rails 7 + Postgres + healthcare-compliance stack."
- **substrate-source:** Her Indie Hackers post 2026-03-12 (URL on file)
- **why-this-prospect:** Stated bottleneck matches our ICP's primary pain hypothesis verbatim; she has the role to buy; she's publicly looking for a solution.

## Prospect rows — fill in below

### prospect-0001: [name]

- **email:**
- **role:**
- **company:**
- **company-stage:**
- **substrate-snippet:** [verbatim quote from their public material — the more specific, the better the draft]
- **substrate-source:** [URL or document reference]
- **why-this-prospect:**

### prospect-0002: [name]

- **email:**
- **role:**
- **company:**
- **substrate-snippet:**
- **substrate-source:**
- **why-this-prospect:**

### (add more prospect-NNNN sections as needed)

## Notes for the operator

- **Sourcing.** This template is agnostic to how you found the prospects (cold-list scraping, warm intros, LinkedIn search, conference attendee list, etc.). The substrate-snippet is what matters — without it, B-1 can't personalize and will skip.
- **Snippet quality.** A 1-2 sentence verbatim quote from their public writing beats a 200-word company description. B-1 will cite the snippet in the draft; the prospect will see their own words quoted back at them. This is the load-bearing personalization.
- **Privacy.** Don't put non-public information in this file. If you have it, keep it elsewhere; B-1 only personalizes from what's here.
- **Order.** B-1 picks prospects in file order. Put highest-priority targets first.
- **Updating.** Append new prospects, don't reuse IDs. If you remove a prospect mid-campaign, B-1's log entries for them are still in `interview-log.jsonl` (which is append-only).

---

*Copy this template to `prospects.md` and fill in. B-1 reads `prospects.md`, not this template file.*
