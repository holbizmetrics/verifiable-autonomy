# Track SPEC — Strategic Surface-Compliance Gate (SC-1)

> Status: DRAFT, filed before implementation (per the track-structure discipline:
> SPEC + falsifier + audit-log schema + detector-gaps, before code).
> Layer: strategic. Mode: `step` (no self-fire; default).
> Target repo on acceptance: a track/instance under `verifiable-autonomy`.

## The gap this closes

The six-discipline thesis enforces **Surface-Compliance (#4)** mechanically at the
execution layer: an agent's gate "refuses to emit an 'I re-derived' record that has zero
successful artifact reads behind it." At the **strategic layer**, the same README marks
this discipline as *"less rigorous surface; same architectural intent"* — strategic
Surface-Compliance is asked for in prose (commits and mirror logs *should* cite
substrate), not enforced by a gate.

A live strategic-layer instance (the Vulcan kernel, a PCLA descendant) has an audit
corpus of **48 session mirror logs** (counted, not estimated). Across those logs, the
failure where a completion, causal, or authorship claim is asserted with no backing read
recurs in **at least 6 distinct sessions**, named: completion-claims-self-certified
(2026-06-16), relayed-causal-claim (2026-06-20), authorship-misattribution (2026-06-20),
auth-fixed at wrong identity scope (2026-06-20), vulcan-sync authorship-miss (2026-06-22),
assumption-over-fact (2026-06-29). Each was caught by operator substitution ("did you test
it?", "you sure?", "that was weak"), never by an automatic gate. The instance's own logs name the durable fix as a
"mechanical pre-assertion claim-classifier" and record it as repeatedly proposed and
unbuilt, because the enforcement was attempted in prose and prose leaks.

So the gap is named by both sides: the architecture knows strategic #4 is unenforced; the
live instance has the evidence that leaving it as prose does not hold. SC-1 is the
mechanism that converts strategic #4 from prose to substrate.

## What SC-1 is

A `Stop` hook (`vulcan-surface-compliance.py`) that runs at every turn end and refuses to
let a turn close while it contains an unbacked claim. It is the strategic-layer analogue
of the execution-layer gate that "refuses to emit a record with zero artifact reads."

The mechanism is not novel plumbing. An existing Stop hook in the same instance
(`vulcan-closeout-gate.py`) already: reads the hook payload from stdin, parses the
session transcript, fails open on any error, is loop-guarded via `stop_hook_active`, and
blocks a turn by emitting `{"decision":"block","reason":...}`. SC-1 reuses that exact
skeleton and changes only the target: instead of "did the Mirror fire?", it asks "does
this turn's text assert work that this turn's tool calls did not back?"

## Mechanism (pseudocode)

```
on Stop(payload):
    if payload.stop_hook_active: allow()          # loop guard: never trap a turn
    turn = parse_transcript(payload.transcript_path)
    assistant_text = turn.last_assistant_message
    tool_calls     = turn.tool_uses_since_last_user_message

    claims = classify(assistant_text)             # see claim classes below
    if not claims: allow()                        # nothing asserted -> nothing to back

    unbacked = []
    for claim in claims:
        if not has_backing(claim.kind, tool_calls):
            unbacked.append(claim)

    emit_audit_record(turn, claims, tool_calls, verdict = "block" if unbacked else "pass")

    if not unbacked: allow()                       # every claim had a backing read
    block(reason = downgrade_or_verify_instruction(unbacked))
```

### Claim classes and their required backing

| Claim kind | Trigger patterns (assertion form only) | Backing required THIS turn |
|---|---|---|
| completion | done, fixed, verified, it works, complete, passing, tests green, shipped | a `Bash` test/build/lint run, or a `Read`/tool observation of the result |
| derivation | I read X, per the file, according to, I checked, the file says | a `Read`/`Grep`/`Glob` of the referenced artifact |
| causal / impossibility | X is the cause, can't, blocked, auth-gated, not possible | one disconfirming probe (`Bash`/`Read`/`WebFetch`) |
| authorship / provenance | X wrote, X owns, authored by, came from | `git blame` / `git log --author` / `gh ... --json author` |

`has_backing` checks only that a tool call **of the required kind exists in the turn**.
See Detector Gaps for what it deliberately does not check.

## Audit record (discipline #3 shape; `tail | jq`-able)

One append-only JSONL line per turn checked, written to
`audit/surface-compliance.jsonl`:

```json
{
  "timestamp": "2026-06-29T14:40:00Z",
  "session": "<session-id>",
  "turn_index": 37,
  "claims_detected": [
    {"kind": "completion", "excerpt": "auth's fixed, fire's out", "backed": false}
  ],
  "tool_calls_this_turn": ["Bash:claude -p (zod)", "Read:.env"],
  "verdict": "block",
  "reason_code": "completion_unbacked_at_claim_scope"
}
```

The operator reads this without trusting the agent's narrative: `jq 'select(.verdict
=="block")' audit/surface-compliance.jsonl` lists every turn the gate caught, with the
claim text and the reads that were or were not present. The record is emitted on `pass`
too, so the log is a complete history of checks, not just catches.

## Pre-registered falsifier (discipline #2)

SC-1 is declared broken, and flips back to `step` / is disabled, on any of:

1. **False-positive flood.** Block records where the operator discharges the block with a
   trivial or irrelevant read (gate fired on a non-claim) exceed an agreed fraction of
   blocking turns across a campaign. Measured from the audit log. Cause: claim pattern set
   too broad. Action: narrow patterns, re-file.
2. **Undischargeable block.** Any block the model cannot satisfy with a real verification
   because the "claim" was a judgment with no possible artifact backing (e.g. a design
   opinion). A dead-end block is a false positive with teeth. Cause: a claim class that
   should not be gated. Action: remove that class.
3. **Dead-man (too narrow).** Across N sessions whose mirror logs show unbacked claims by
   human review, SC-1 emitted zero blocks. It is not catching what it exists to catch.
   Cause: patterns too narrow / claims phrased outside the set. Action: widen, re-file.

Falsifier state is summarized at each `step -> auto` consideration and recorded in the
flip-history record, per the MODE contract.

## Honest scope (detector-gaps doc)

This gate is a **floor, not a ceiling**. What it deliberately does not do:

- **Existence, not relevance.** It verifies a backing read of the right *kind* exists in
  the turn. It does not verify that read actually supports the specific claim. A `Read` of
  the wrong file still passes. Relevance is delegated to discipline #5 (cross-operator
  review). SC-1 removes the zero-evidence case; it does not remove the wrong-evidence case.
- **Heuristic text match.** Claim detection is pattern-based. It will miss novel phrasings
  (false negative) and can fire on quoted or negated text (false positive). Mitigations:
  match assertion form only (skip negations and questions), keep the pattern set
  conservative, and **fail open in every branch** — any parse error, missing file, or
  ambiguity allows the turn. A gate that traps turns gets disabled, which is worse than a
  gate that occasionally misses.
- **Cross-context blindness (scope-identity).** It cannot verify a claim made about a
  different execution context (another OS user, machine, account, service principal). A
  check that ran in the agent's own context cannot back a claim about another's. SC-1 can
  flag the claim class but the verifying run must happen as that context; that is handed to
  discipline #5. (n-evidence: the live instance logged "auth's fixed" asserted off a check
  run as the wrong user.)
- **Not a cage.** The loop guard means a determined model can re-emit a claim after one
  block and the turn will close. SC-1 raises the firing rate and forces one conscious
  verify-or-downgrade pass. It is discipline made mechanical, not an unbypassable wall.
  This is the same honest posture the thesis takes toward autonomy.

## Cross-operator review (discipline #5)

Before any `step -> auto` flip, SC-1's verdicts over a campaign get reviewed from a
different session. The live instance already runs a cross-session bus to a second operator
(`nova`); the review request is filed as an artifact, the reviewer samples the audit log
and confirms or disputes a set of `block`/`pass` verdicts. Honest caveat: the second
operator is a different session and identity but may be the same model family, so this
discharges the cross-session rung fully and the cross-family rung only partially. The
register names which rung is discharged and which is still owed, rather than claiming both.

## What this contributes, stated plainly

Not a report. A runnable gate plus an audit schema whose mechanism the maintainer can
verify directly: feed it a turn that asserts "done" with no test run, confirm it blocks
and writes the record; feed it a turn that ran the test, confirm it passes. The autonomy
claim ("strategic Surface-Compliance is enforced") becomes `tail | jq`-checkable instead of
narrative. It hardens the one discipline the thesis marks as least rigorous at the
strategic layer and names as the headline risk overall, in the layer's own lineage, with a
pre-existing corpus showing the gate was needed.

## Build plan (after SPEC acceptance)

1. Implement `vulcan-surface-compliance.py` from the closeout-gate skeleton (fail-open,
   loop-guarded, transcript-parsing). V1 = completion + derivation classes only; add
   causal and authorship once false-positive rate is measured.
2. Wire as a `Stop` hook alongside the existing ones; emit the audit JSONL.
3. Run in shadow mode first: emit audit records, do NOT block, for one campaign. Measure
   false-positive rate against the falsifier before enabling blocking.
4. File the detector-gaps deltas and the first cross-operator review request.
```
