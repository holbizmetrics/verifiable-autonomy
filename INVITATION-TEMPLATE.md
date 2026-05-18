# Early-access invitation template

> **For operator use.** Send this when inviting a tester to private-repo early access (Path B per `SCOPING-PRODUCT-READINESS.md`). Cap of 5 invited collaborators at a time. Edit the bracketed bits before sending.

## Short version (DM / one-paragraph)

> Hey [name], I'm building verifiable-autonomy: agents that draft outreach / customer-dev / follow-up with audit guarantees by construction. Operator-supervised by default. The agent drafts. You send. Every action appended to JSONL with cited sources. You can grep the audit log for the lie. Repo is private until two research tracks have proved their falsifiers don't fire. I'm running early-access with a cap of 5 testers; you'd be one of them. Interested? If yes, drop your GitHub handle and I'll add you. Quiet ask: don't post the code publicly until I unlock it.

## Longer version (email)

Subject: Early-access invite, verifiable-autonomy

Hi [name],

Quick context. I'm building verifiable-autonomy, a Claude-Code-hosted agent system where every agent ships with audit guarantees by construction:

- Operator-supervised by default. The agent drafts. You send.
- Every action appended to JSONL with cited sources.
- You can grep the audit log for the lie.
- Pre-registered failure modes per track. If a falsifier fires, the track flips back to operator-gated automatically.

[1-2 sentences about why you specifically: a line from their public writing, a problem they articulated, an adjacency to their own work. Make it not generic.]

The repo is private. The README says it flips public when at least two research tracks have proved their falsifiers don't fire, which is the current gate. Until then I'm running early-access with a cap of 5 invited testers.

What early-access means:

- You'd get repo collab access. Full code. Full audit-log visibility. Same as me.
- The only agent ready for outside use right now is B-1, customer-interview-runner. The A-track research agents (closeout-auto, phase-transition-auto) live in the research lab, not here.
- Quiet ask: don't post the code publicly until I unlock it. Talking about your experience is fine; sharing the repo URL isn't, yet.
- No NDA, no pricing. Feedback is what I'd ask in exchange.
- You can drop access at any time, and I can drop the early-access program at any time. No strings.

If you're up for it, send me your GitHub handle and I'll add you. If not the right time or wrong shape, no worries; thanks for reading either way.

Best,
[your name]

---

## Variants by relationship

**To someone who critiqued an adjacent product (e.g. Stuart on Polsia):**
Lead with their critique sentence. "You wrote [verbatim]. We started there."

**To a peer-builder (e.g. Sarkar with Overseer):**
Frame as "adjacent problems, comparing notes," not "early-access to my thing." Two-way invitation: you'd give him repo access AND ask if he'd swap access to his.

**To a strong demographic fit (e.g. Max with Flowly):**
Lead with their epistemic-frame line. Be honest that you read their post carefully.

## What to track when sending an invitation

After sending, record (in a private operator log; do NOT commit to repo):

- Date sent
- Prospect ID
- Variant used (short / long / which lead-in)
- Cap status (this would be tester N of 5)

When they accept and you `gh repo edit ... --add-collaborator <handle>`, also record:

- Their GitHub handle
- Date added
- Cap remaining

## What to track when dropping someone

If you remove a tester (their request or yours), record:

- Date removed
- Reason (one line)
- Whether the cap-of-5 has reopened a slot

## Cap-of-5 falsifier

If the cap pressures you to either (a) refuse a great tester or (b) raise the cap, that's a signal. **Raise the cap deliberately, not by drift.** Edit `SCOPING-PRODUCT-READINESS.md` to amend the number, and note why. The point is the discipline, not the number.

---

*Invitation template v1, S55 (2026-05-18). Em-dash-free. Update when the early-access posture changes or a variant proves better.*
