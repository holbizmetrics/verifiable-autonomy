# Warm-reply workflow

> **What you (operator) do when a real reply lands.** Parent-level pointer; mechanics live in the agent's directory.

## The cadence

B-1 sends nothing. You send manually. So replies arrive in your normal inbox. The workflow is:

1. **Reply lands** in your email client.
2. **You decide** whether it's worth keeping in the campaign (warm signal) or dropping it (autoresponder, unsubscribe, bounce, etc.).
3. **If keeping:** save the reply text to `agents/b1-customer-interviewer/replies/<prospect_id>.md` (single message) or `replies/<prospect_id>-thread.md` (multi-message thread).
4. **Run classify in batches:** `/agents b1-customer-interviewer classify`. B-1 reads all unclassified replies in one pass, classifies each (`interested | no | call-booked | objection | unclear`), and drafts a follow-up where appropriate.
5. **Review the follow-up drafts** the same way you review initial drafts: are cited phrases real, does it sound like you, send manually.

## Reply-citation discipline (S55 amendment v0.2)

Follow-up drafts cite verbatim from the reply, NOT paraphrased. **The paraphrase exception applies ONLY to ICP citations, never to reply citations.** This holds across all registers (sale, customer-dev, peer). If the reply's tone makes verbatim citation feel awkward, the agent skips with `REGISTER_REQUIRES_REWRITE` rather than paraphrasing.

## When to run classify (cadence, not real-time)

Not every reply needs immediate classification. Reasonable cadence:

- **End of day** if you sent ≥5 emails that day
- **End of week** for low-volume campaigns
- **Immediately** only if a reply is clearly call-booked or hot-interest

Running classify after every single reply wastes context and produces fragmented follow-up drafts. Batch.

## Privacy

Replies contain real prospect text. They are gitignored by default (see `.gitignore`). Do not commit them. When the repo flips public, this directory pattern needs revisiting (see B-1 README "Privacy / data hygiene").

For early-access testers: the same applies. Your replies live in your local clone, not pushed.

## When NOT to use B-1 for the reply

If the reply is high-stakes (a call-booked, a price negotiation, a board-level introduction), respond personally. B-1's classify-mode is for triage and follow-up drafting on routine replies, not for high-judgment moments.

## Cross-references

- Full B-1 workflow: `agents/b1-customer-interviewer/README.md` (steps 7-8 cover this)
- Agent definition (workflow rules + register discipline): `.claude/agents/b1-customer-interviewer.md`
- Falsifier register: `agents/b1-customer-interviewer/falsifier.md`
- Paraphrase-exception amendment + open work: `agents/b1-customer-interviewer/OPEN-WORK-paraphrase-exception.md`

---

*Warm-reply workflow v1, S55 (2026-05-18). Pointer document; mechanics in B-1 README.*
