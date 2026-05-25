# Amendment v0.3 (DRAFT) — falsifier spec tightening from first live-test sweep

> **Status: DRAFT, 2026-05-25. Awaiting cross-op review (windows-claude reviewed v0.2; v0.3 is the natural follow-up). Per v0.2 process: review first, integrate second. Do NOT edit `falsifier.md` until verdict in hand.**

## Why this amendment exists

`falsifier.md` v0.2 has 7 pre-registered falsifiers. None had ever been run against live artifacts until 2026-05-25, when a sweep was executed against the existing 5 drafts + 1 marked-sent + log + `icp.md` + `prospects.md`. The sweep surfaced **3 specification bugs** (F1, F3, F5 have implementation/intent divergence) **and 1 real catch** (F6 fires on timestamp non-monotonicity from retroactive logging).

Two pattern observations from the sweep:

1. **All 3 spec bugs share a root cause** — the falsifier was specified against ideal *agent behavior*, but checked against runtime *artifacts* whose shape diverges from that ideal in predictable ways (ICP evolves, drafts have versions, log shape lacks operator-correction fields).
2. **The headline falsifier (F1) silently false-positives after any ICP edit** — and would have continued to do so undetected if no one had run the sweep. This is the same pattern as the `/claim-audit` KILL-SWITCH polarity bug (PCLA `342a0d3`, 2026-05-25): structured-output → live-test → spec ambiguity surfaces.

The proof-point value of B-1 is not "the falsifier fires on agent fabrication" but **"the lab catches its own falsifier's specification bugs before any campaign hits them."** That value is realized by this amendment, not by waiting for a campaign to deliver a false-positive that derails a real prospect interaction.

## Sweep results (substrate for this amendment)

| F# | Status | Detail |
|---|---|---|
| F1 | **AMBIGUOUS — spec bug** | Bash grep against current `icp.md` fires on log record 1 (em-dash form not present in period-form current ICP); agent didn't fabricate — at log-time, ICP had em-dash form |
| F2 | PASS | No fabricated prospect context |
| F3 | **FIRES (false positive) — spec bug** | Literal: 5 drafts > 3 substrated prospects. Intent doesn't fire — count inflation is from 3 versions of prospect-0003 |
| F4 | Can't fire | n=1 sent, threshold n≥30 |
| F5 | **Can't fire — spec bug** | n=5 drafts (below n≥20), AND log shape has no operator-correction field, so threshold could never become checkable without a schema add |
| F6 | **FIRES** | Timestamps non-monotonic; line 1 dated 2026-05-19, lines 2-5 dated 2026-05-18 (earlier) → likely retroactive logging of prospect-0003 v1 on 2026-05-19 after v2/v2.1 already logged |
| F7 | Can't fire | n=5, threshold n≥10. Current rate: 1/5 = 20% (at yellow-zone *rate*; only n blocks firing) |

## Proposed amendments (4)

### Amendment A — F1 honest-to-spec implementation

**The bug.** F1 reads *"phrases are NOT verbatim present in `icp.md` at the time of that log record's timestamp."* The bash check (`grep -qF "$phrase" icp.md`) checks only **current** `icp.md`, not the version at log-time. After any ICP edit, the check false-positives on every prior record whose cited phrases were touched by the edit. The headline falsifier becomes a noise source instead of a signal.

**Why this happens.** ICP cleanups (em-dash removal in v2.1; future copy-edits) rewrite phrases. Log records persist with the at-time citation. Grep against HEAD diverges from grep at log-time. The intent ("did the agent fabricate?") and the check ("is this phrase in HEAD?") only coincide if the ICP never changes — which is unrealistic.

**Proposed fix (minimum touch — v0.3).** Change F1's bash check to git-archaeology-aware:

```bash
# For each draft_emitted log record:
jq -r 'select(.action=="draft_emitted") | "\(.timestamp)\t\(.icp_phrases_cited[])"' interview-log.jsonl \
  | while IFS=$'\t' read -r ts phrase; do
      # Find icp.md as it existed at-or-before the log record's timestamp
      commit=$(git rev-list -n 1 --before "$ts" HEAD -- icp.md)
      if [ -z "$commit" ]; then
          echo "NO-HISTORY at $ts: $phrase"
          continue
      fi
      if ! git show "$commit":./icp.md | grep -qF "$phrase"; then
          echo "MISSING at $ts (commit $commit): $phrase"
      fi
  done
```

**Cost.** One `git show` per record (cheap; bounded by record count). No new agent-side schema.

**Alternative (cleaner — v0.4 candidate).** Add `icp_sha256` to the `draft_emitted` log record. Agent computes SHA of `icp.md` content at draft-time and includes it. Falsifier check: if `icp_sha256` matches current ICP SHA → grep current; else → git-archaeology fallback (or operator-surface as drift). Catches the case where git history is missing (uncommitted changes between drafts) which the v0.3 fix doesn't.

**Falsifier of the fix.** Run the new check against the current log. It should NOT fire on records 1-2 (em-dash form was in icp.md at S55 timestamp; verify via git log). If it does fire on records 1-2 after the fix, the fix itself is broken.

### Amendment B — F3 dedupe by prospect_id

**The bug.** F3's count (`drafts_emitted > prospects_with_substrate`) doesn't dedupe by prospect_id. Multi-version drafts (legitimate — v1 / v2 / v2.1 of the same prospect, none yet sent) inflate the numerator without representing distinct prospect-coverage decisions.

**Why this happens.** The check was specified before B-1 v0.2's iteration discipline made multi-version drafts common. The intent ("agent drafted against thin substrate") tracks prospect-level decisions, not artifact-level emissions.

**Proposed fix.**

```bash
unique_drafted=$(jq -r 'select(.action=="draft_emitted") | .prospect_id' interview-log.jsonl \
  | sort -u | wc -l)
substrated_prospects=$(awk '/^## prospect-/{header=$0} /substrate-snippet:/{print header}' \
  prospects.md | sort -u | wc -l)
if [ "$unique_drafted" -gt "$substrated_prospects" ]; then
    echo "FIRE: drafted $unique_drafted unique prospects but only $substrated_prospects substrated"
fi
```

**Cost.** Drop-in replacement; no agent-side change.

**Falsifier of the fix.** Run against current log: should NOT fire (3 unique prospects drafted, 3 substrated → 3 == 3). If it fires, the dedupe logic is broken.

### Amendment C — F5 operator-correction tracking schema add

**The bug.** F5's threshold (operator rejects/rewrites >50% over n≥20 drafts) is unreachable: the log shape has no field recording operator corrections. Even at n=20+, the falsifier can't compute the rate without operator-side log entries that don't exist in the schema.

**Why this happens.** v0.1 specified F5 as a behavioral falsifier; v0.2 didn't add the schema-side machinery to make it checkable. The falsifier exists on paper only.

**Proposed fix.** Two options, both schema-light:

**Option C-1 (cheaper).** Extend the `marked_sent` record with a `correction_level` field: `none | minor | substantial | rewrite`. Operator stamps it when running `mark-sent`. F5 computes rate from `marked_sent` records.

```json
{
  "timestamp": "...",
  "mode": "operator_mark",
  "action": "marked_sent",
  "prospect_id": "...",
  "sent_at": "...",
  "correction_level": "minor"
}
```

**Option C-2 (more honest, more work).** New action: `operator_correction`. Operator appends one record per draft they edit pre-send, with `delta_words` + `correction_type` + free-text rationale.

**Recommendation.** C-1 for v0.3. C-2 is v0.4 candidate if C-1's correction_level proves too coarse to surface real drift.

**Caveat.** Either option requires the agent's `mark-sent` workflow to prompt the operator for the correction level. v0.2 `mark-sent` workflow has no such prompt; the agent definition needs an addendum.

**Falsifier of the fix.** Cannot validate without n≥20 marked-sent records carrying the new field. v0.3 ships the schema; v0.4 / first real campaign validates the threshold.

### Amendment D — F6 disambiguate event-time vs log-time

**The bug.** F6 fires on the current log because log line 1 (2026-05-19) has an earlier-timestamped record (line 2: 2026-05-18) below it. The most plausible explanation is retroactive logging: prospect-0003 v1 was drafted in S55 (2026-05-18) but its log record was appended on 2026-05-19 when the real-prospect test ran. **Append-only file discipline is preserved** (no edits to prior lines); **timestamp-ordering invariant is broken** in a way the falsifier text didn't anticipate.

**Why this happens.** The current `timestamp` field conflates event-time (when the action happened) and log-time (when the record was written). F6 assumed they coincide. Retroactive logging — a legitimate pattern when the agent re-encounters an undocumented historical action — breaks the assumption.

**Proposed fix.**

1. **Schema split.** Introduce `event_ts` (when the action happened) and `log_ts` (when the record was written). The current `timestamp` field is repurposed as `event_ts`. New `log_ts` is added.

   ```json
   {
     "event_ts": "2026-05-18T21:00:00Z",
     "log_ts":   "2026-05-19T10:00:00Z",
     "mode": "draft",
     "action": "draft_emitted",
     ...
   }
   ```

2. **F6 invariant.** **`log_ts` must be monotonic non-decreasing** across file order (append-only enforces this trivially: `log_ts = now()` at write-time). `event_ts` may be earlier than the previous record's `event_ts` ONLY if a `retroactive: true` flag is present + a one-line `retroactive_reason`. Without the flag, `event_ts` must also be monotonic.

3. **Backfill (existing records).** Treat all current records as `event_ts == log_ts == timestamp` and re-stamp accordingly. Add a one-line backfill note to `falsifier.md` explaining the convention break.

**Cost.** Schema change. Existing records need a one-time rewrite (which would be a non-append edit — itself an F6 violation unless explicitly carved out as a one-time backfill commit). Carve-out language needed.

**Falsifier of the fix.** After backfill, F6 should not fire on the current log. Add a synthetic-test fixture: retroactive record without flag → must fire; retroactive record with flag + reason → must not fire.

## Open questions for cross-op review

1. **F1 v0.3 vs v0.4:** is the git-archaeology fix (Amendment A v0.3) adequate as a stopping point, or is the SHA-hash approach (v0.4 candidate) load-bearing enough to ship now? Cost-benefit: v0.3 is cheap; v0.4 catches the uncommitted-ICP-changes case that v0.3 misses.
2. **F5 schema:** Option C-1 (correction_level on marked_sent) vs C-2 (separate operator_correction action). Which fits the operator's actual review flow? Is correction_level granular enough to surface drift before n=20?
3. **F6 backfill carve-out:** is a one-time non-append rewrite of existing records acceptable, or should the schema split apply only to new records (with old records grandfathered into the old timestamp semantics)? The grandfather path is purer but means F6 has two regimes.
4. **Amendment ordering:** A is HIGH (headline falsifier is silently broken); B is MED (cosmetic; doesn't false-negative); C is HIGH (falsifier is paper-only); D is MED (real catch but legitimate cause). Should v0.3 ship all four, or A+C first and B+D as v0.4? The bundled path matches v0.2's discipline.

## Anti-pattern self-flag (drafter)

- **Same-family conflation:** this amendment is authored by the same Claude session (Opus 4.7) that ran the sweep. windows-claude (also Opus 4.7) reviewed v0.2; that's still cross-session-same-family rigor, not cross-family.
- **"Catches itself" risk:** the headline framing ("the lab catches its own falsifier's specification bugs before any campaign hits them") sounds clever and could become performative. The actual proof-point is whether the v0.3 fixes prevent at least one false-positive in the next n drafts. Pre-register that as the test, not the rhetoric.
- **No campaign data yet.** v0.2 was designed for a campaign that hasn't run; v0.3 tightens it before the campaign runs. There's a real risk that the v0.3 fixes solve the wrong problem if campaign reality differs from the sweep's assumptions. Hedge: ship v0.3 fixes as DRAFT in the falsifier doc with a revisit-after-campaign trigger, mirror the OPEN-WORK v0.2 pattern.

## Filing instructions (post-review)

When verdict is PASS / REVISE-and-PASS:

1. Edit `falsifier.md` integrating the amendments per verdict
2. Update the v0.2 dateline at the bottom to "v0.3 (S58, 2026-05-25; cross-op verdict by <reviewer> at <path>)"
3. Add v0.3 entry to a Changelog block (mirroring SPEC.md changelog convention from A-6)
4. For Amendment C: edit `.claude/agents/b1-customer-interviewer.md` workflow `mark-sent` step to prompt for `correction_level`
5. Commit + send `mark-seen`-equivalent over the bus to windows-claude

When verdict is BLOCK: revise this draft per blocker, re-send.

## Cross-references

- Sweep substrate (this conversation, PCLA termux session 2026-05-25)
- v0.2 (current): `falsifier.md` § F7 amendment
- v0.2 cross-op review (windows-claude): `prometheus-crystal-lab-auto/.prometheus/cross-operator/windows-review-b1-paraphrase-exception-2026-05-18-RESPONSE.md`
- OPEN-WORK v0.2 deferred items: `OPEN-WORK-paraphrase-exception.md`
- Yesterday's analog (the spec-bug-from-live-test pattern): PCLA `342a0d3` `/claim-audit` KILL-SWITCH polarity catch
- Pattern: PCLA auto-memory `feedback_ship_then_live_test.md`

---

*Amendment v0.3 DRAFT, 2026-05-25. Awaiting cross-op review. Do NOT integrate into `falsifier.md` until verdict in hand.*
