# Product-readiness gate scoping

> **What blocks B-1 from sending a real email to a real prospect?** Surfaced S55 (2026-05-18) during the Max draft test (1+2 only, send not authorized).

## The structural finding

The README's own manifesto names the gate (L11):

> *"flips public when at least two tracks have flipped step → auto."*

Current state: **1 track flipped** (A-3 closeout-auto, per PCLA). So the literal precondition for "send Max a real email and link the repo" is either:

- One more A-track flip, or
- A manifesto amendment.

The downstream stuff (landing page, install docs, warm-reply workflow) is small. The upstream question is which path through the self-gate.

## Three paths

### Path A: Wait for second flip

- **What it requires:** A-1 phase-transition-auto reaches `mode: auto` per PCLA flip contract (cross-operator review + falsifier + n≥2 demos).
- **Cost:** Time. A-1 is in late-stage design but not yet flipped. Estimated weeks, not days.
- **Benefit:** Cleanest. No manifesto change. Real customer-dev waits, but ICP discipline holds when it starts.
- **Risk:** B-1's draft pipeline goes stale without real-world feedback. ICP shapes itself in a vacuum.

### Path B: Early-access amendment (LEAN)

- **What it requires:** README amendment allowing N≤5 invited collaborators on the private repo while still gated. Wording: *"Until two tracks have flipped step → auto, repo access is by invitation to early-access testers. The public read is gated on proof. Early-access testers see the same code with full audit-log access."*
- **Cost:** One README edit + one collab-invite workflow (operator manually invites via `gh`).
- **Benefit:** B-1 can run real customer-dev now. Each invited tester is a falsifier-probe against real-world conditions.
- **Risk:** "Early-access" can drift into "soft public" if uncontrolled. Cap-of-5 + named list mitigates.

### Path C: Split (public stub + private impl)

- **What it requires:** A new public repo (`verifiable-autonomy-public` or similar) with the manifesto + architecture writeup + waitlist form. Implementation stays private.
- **Cost:** New repo, simple static site or markdown, waitlist mechanism.
- **Benefit:** B-1 can link to *something* in cold mail. Discoverable. Builds public substrate before public code.
- **Risk:** Two repos to maintain. Drift between public manifesto and private implementation. Marketing-shaped, not product-shaped.

## Lean: Path B

**Why:**
- Honors "private until proof" for the world (Path A's spirit).
- Gives operator real-customer-dev pipeline (Path A's missing piece).
- Doesn't compromise the architectural claim because invited collaborators aren't the public (Path C's worry).
- Reversible: drop early-access at any time, no public footprint to manage.

**Failure mode that would flip the lean:**
- If invited testers turn around and post the code publicly, Path B has leaked. Mitigation: collaborator agreement is a one-line "don't post publicly until I unlock" in the invite message. Cap-of-5 keeps it tractable.
- If real customer-dev surfaces that the product isn't ready (e.g. agent fails on a real ICP that wasn't synthetic), Path B reveals it earlier than Path A. That's a benefit framed as a falsifier.

## What Path B actually requires (the scoping work)

If operator authorizes Path B, the work splits into 5 small items:

1. **README amendment.** One-paragraph insertion in the Status section allowing early-access. Operator-authored, not agent-drafted.
2. **Invite workflow.** `gh repo edit holbizmetrics/verifiable-autonomy --add-collaborator <username>` per invited tester. No tooling needed; manual `gh` is fine for N≤5.
3. **Quickstart at repo root.** A QUICKSTART.md (or section in README) covering: clone, Claude Code already installed, cd in, `/agents b1-customer-interviewer draft 5`. ~30 lines.
4. **Warm-reply workflow doc.** What operator does when a reply lands. Already partially in B-1's README ("Drop replies + classify"). Needs a parent-level pointer.
5. **Invitation message template.** What you send when offering early-access. ~5 sentences. Includes the don't-post-publicly clause.

Estimated total work: 1-2 hours, mostly writing.

**Not required for Path B:**
- Landing page (private repo, no public face needed)
- Installer (Claude Code is the installer)
- Pricing page (early-access is free / feedback-traded)
- Onboarding video / docs site / dashboard

## Falsifier (for this scoping document itself)

This scoping is **wrong** if:

- A-1 turns out to be closer to flip than estimated (Path A becomes cheap, lean shifts to A).
- The operator's customer-dev cadence wants more than 5 testers in the next month (cap is too tight, lean shifts toward C).
- The first invited tester reports the product isn't actually ready for their use case (Path B revealed a real readiness gap; back to A-track work before more invites).

## Decision owed

**Operator picks one of A / B / C before next real-prospect send is authorized.**

Until then: B-1 keeps drafting against the real ICP + real prospects for review, but no send. v1, v2, v2.1 of Max all live in `drafts/` as A/B/C-of-tone candidates.

---

*Scoping document. v1, S55 (2026-05-18). Operator authorization required for any path-selection or amendment.*
