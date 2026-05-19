# Draft for prospect-0001: Naomi Larkin

To: naomi@logpipe.test
Subject: Adjacent product, comparing notes on single-binary observability?

Hi Naomi,

Read your "Why I Built LogPipe" post from February. The line that stuck: *"That is not a tool for solo builders. That is a tool for teams who already have an SRE."* Same observation pushed us to build DevTrace.

Not pitching. We are adjacent products and probably overlap on a real subset of the ICP. A few questions if you are up for comparing notes:

1. How are you handling endpoint-level failure visibility? We currently watch nginx access-log status-codes on a tick rather than instrumenting application code. Curious if you found a lighter approach.

2. Single-binary discipline: did you write LogPipe as one Go binary or did you split data-collection from web UI? We bundled into one and the dev loop is faster but distribution gets weirder.

3. If you ever want to swap notes on user-feedback patterns from solo founders, happy to share what we have heard so far. Yours is the substrate I would want to read.

Best,
[your name]

PS: The LogPipe pricing page is unusually clean. Whoever wrote "every solo builder pays the same" got it right.

---

## Register

peer

## ICP phrases cited (verbatim)

(none verbatim in this draft; see paraphrased citations below per S55 v0.2 amendment)

## Paraphrased citations (peer register only)

- [paraphrased: "single binary observability for solo builders" ← "single binary. Drop it on your server. Point at your access log" | score: 1]
- [paraphrased: "endpoint-level failure visibility" ← "you do not need distributed tracing. You need to know which endpoint just 500ed" | score: 1]

**Why paraphrase here:** verbatim citation of declarative DevTrace product copy ("single binary. Drop it on your server. Point at your access log") would tip a peer-builder conversation into pitch register. Naomi has shipped the same shape; quoting our marketing at her would be tone-deaf. Both paraphrases preserve the load-bearing semantic claim (single-binary discipline + endpoint-level monitoring) with looser surface fit for peer-to-peer dialogue. Sources verified in `icp.md` at draft-time.

## Prospect specifics cited

- "That is not a tool for solo builders. That is a tool for teams who already have an SRE." (verbatim)
- "Why I Built LogPipe" (article title, verbatim)
- LogPipe single-binary discipline (paraphrased from her article)

## Why this prospect

Naomi is an adjacent-product builder with overlapping ICP. The draft is built as peer outreach because pitching her would waste a real founder-friend relationship. The PS recognizes a specific feature of her product (pricing-page clarity) without being patronizing.

---

*Draft v1, 2026-05-19. Peer-register fixture for v0.2 paraphrase-exception. Em-dash-free. Operator review required. Send NOT authorized (fixture, fictional prospect).*
