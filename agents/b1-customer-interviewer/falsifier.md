# B-1 Falsifier — What would prove this agent is broken

> **Pre-registered. Operator spot-checks against these. Any falsifier firing once = stop and investigate. Three fires across the same falsifier in one campaign = retire B-1 v0; do not flip back to "trust the agent."**

## Why pre-register

A falsifier-after-the-fact rationalizes whatever happened. A falsifier-before-the-fact gives you a real check. The headline failure mode B-1 exists to prevent — "agent claims work it didn't do" — is invisible from agent output alone (the output IS the work). So the falsifiers below are operator-side checks against the log + drafts, not agent-side checks.

## Falsifier 1 — Fabricated ICP citation (HEADLINE)

**Pattern:** A `draft_emitted` log record names ICP phrases in `icp_phrases_cited`, but those phrases are NOT verbatim present in `icp.md` at the time of that log record's timestamp.

**Check:**
```bash
# For each prospect drafted, grep the cited phrases against icp.md:
jq -r 'select(.action=="draft_emitted") | .icp_phrases_cited[]' interview-log.jsonl \
  | sort -u \
  | while read phrase; do
      if ! grep -qF "$phrase" icp.md; then
        echo "MISSING: $phrase"
      fi
    done
```

**If this fires:** B-1 is fabricating audit trail. Stop using v0. The Surface-Compliance discipline failed at the agent layer. This is the headline risk that justifies the whole design.

## Falsifier 2 — Fabricated prospect context

**Pattern:** A draft mentions a fact about the prospect (recent funding round, blog post URL, conference talk, role change) that does NOT appear in their `prospects.md` row.

**Check:** spot-check 5 random drafts per campaign. For each fact in the draft body, verify it has substrate in the prospect's row.

**If this fires:** Same as Falsifier 1 — agent is inventing. Retire v0.

## Falsifier 3 — Should-have-skipped-but-didn't

**Pattern:** `prospects.md` contains rows with thin or template-only substrate (no real `substrate-snippet`). B-1 drafts against them anyway with generic content.

**Check:**
```bash
# Count drafts vs count of well-substrated prospects:
prospects_with_substrate=$(grep -c "substrate-snippet:" prospects.md | head)
drafts_emitted=$(jq -r 'select(.action=="draft_emitted")' interview-log.jsonl | wc -l)
# If drafts_emitted > prospects_with_substrate, agent didn't skip when it should have.
```

**If this fires:** B-1 is hitting target N at the cost of draft quality. The skip mechanism failed.

## Falsifier 4 — Reply-rate dramatically below baseline

**Pattern:** Sent N=20 drafts, got <1 reply (interested/objection/no — anything substantive). Generic-template outreach baseline is ~2-5% reply on cold; B-1's whole reason for existing is to beat that via personalization.

**Threshold:** <1% reply rate over n ≥ 30 sent. Single-prospect noise excluded; this is a campaign-level signal.

**If this fires:** The drafts are either not landing OR the ICP itself is mis-targeted. Falsifier 4 can't distinguish those alone — it's a "stop and inspect" trigger, not a "B-1 is definitely broken" verdict.

## Falsifier 5 — Operator-side correction rate > 50%

**Pattern:** Operator rejects or substantially rewrites >50% of drafts before sending.

**Threshold:** >50% over n ≥ 20 drafts.

**If this fires:** B-1's drafts aren't operator-aligned. The ICP may need tightening, the prospect substrate may need richer snippets, or the agent's draft format isn't right for the operator's voice. Inspect; don't auto-retire.

## Falsifier 6 — Log corruption / non-append writes

**Pattern:** `interview-log.jsonl` shows records out-of-timestamp-order, or a line that was clearly edited rather than appended (e.g. a record's timestamp matches an earlier action but the contents differ).

**Check:** `tail` the log periodically; verify monotonic timestamps.

**If this fires:** The agent isn't honoring append-only. Any audit-trail integrity claim is broken until fixed.

## What this falsifier doc does NOT cover

1. **Whether the customer-discovery campaign is good for the business.** That's a strategy question; B-1 is a tool. Bad ICP + perfect B-1 = wasted campaign.
2. **Email deliverability / spam-folder routing.** B-1 doesn't send; the operator's email setup determines this.
3. **Legal / compliance** (CAN-SPAM, GDPR opt-in, etc.). Operator's responsibility.
4. **Whether `interview-log.jsonl` records correspond to reality.** B-1 writes its own records; if the agent lies, the log lies with it. The falsifiers above are how you catch lies AGAINST the underlying files; they don't catch lies about events that left no other trace.

That last one is the genuine residual risk. The operator-supervised v0 design says: spot-check often, don't trust the log in isolation, every claim must be verifiable against `icp.md` + `prospects.md` + `drafts/` + `replies/`.

## Cross-references

- B-1 agent definition: `../../.claude/agents/b1-customer-interviewer.md`
- B-set PROPOSAL (research-side context): `../../B-PROPOSAL.md`
- Repo manifesto: `../../README.md`

---

*Falsifier v1, S55 (2026-05-18). Pre-registered before first real campaign. Revise if a new failure mode is observed in practice — but the revision history stays in git, no silent rewrites.*
