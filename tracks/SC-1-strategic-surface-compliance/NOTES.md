# SC-1 — Strategic Surface-Compliance Gate (track contribution)

## What this is

A runnable `Stop`-hook that enforces **Surface-Compliance (#4) at the strategic layer**,
where the README currently marks it *"less rigorous surface; same architectural intent"*
(i.e. asked for in prose, not enforced by a gate). SC-1 makes it a gate: it refuses to let
a turn close while the turn asserts work its own tool calls did not back, and writes a
`tail | jq`-able audit record per turn (discipline #3 shape).

Provenance: extracted from a live strategic-layer instance (a Vulcan kernel, a PCLA
descendant). That instance's session audit corpus (48 mirror logs) shows the unbacked-claim
failure recurring across at least 6 named sessions, each caught by operator substitution,
never by an automatic gate. SC-1 converts that prose discipline into substrate.

## Design — the inversion

The leaky part of the naive design is detecting "a claim" in free text. So SC-1 does not
fire on every "done". It fires on a high-precision triad:

> **mutation (Edit/Write) AND success-claim AND no verification this turn → block**

plus a secondary derivation check (asserts "I read X" with no Read/Grep/Glob this turn).
Conversational "done, what's next?" has no mutation, so it never fires.

**Asymmetric loss (why precision over recall):** a false positive traps a turn → the
operator disables the gate (fatal to adoption). A false negative is backstopped by the
next-boot Mirror (tolerable). So the rule maximizes precision, accepts low recall, and
**fails open in every branch**. It is loop-guarded (`stop_hook_active`), so a block can
never trap a turn — discipline, not a cage.

## Status — proof owed (per this repo's own bar)

- **Verified now:** the mechanism. `test_surface_compliance.py` is green (8 case scenarios
  + loop guard + fail-open + audit-record assertion). Feed it a turn that edits a file and
  says "done" with no test run → it blocks; feed it one that ran pytest → it passes.
- **Owed (not done):** in-production efficacy. The build plan runs SC-1 in **shadow mode
  first** (emit audit records, do NOT block) for one campaign, measures the false-positive
  rate against the pre-registered falsifier (SPEC.md), and only then enables blocking.
- **Owed:** cross-operator review (#5). A second-session/identity review of the audit
  verdicts. Honest caveat: the available second operator may be the same model family, so
  that discharges the cross-session rung fully and the cross-family rung only partially.

This matches the repo's posture: the mechanism is verifiable today; the track-record is not
yet earned, and is named rather than claimed.

## Self-teardown (attacking the falsifier)

Per the invitation to break it, the triad was attacked directly. Three findings:

- **F3 — false positive on non-code mutations (FIXED).** The success rule fired on *any*
  mutation, so writing a doc/note and saying "done" tripped it though nothing was testable.
  That is the fatal loss class (a trapped turn gets the gate disabled). The rule is now
  scoped to code-file mutations (`CODE_EXTS`); doc/config writes no longer demand a verify
  command. New regression test: `doc mutation + success + noverify -> allow`.
- **F2 — verify command counted as present, not as passed (FIXED — the block-mode blocker).**
  The gate detected that a test/build command *ran*, never that it *passed*, so a failing
  `pytest` satisfied it (it certified the ritual, not the result). `parse_last_turn` now
  reads `tool_result` blocks (`tool_use_id -> is_error`) from the turn window, and a verify
  command backs a success claim only when its result is present and `is_error` is false.
  Fail-open held: a missing/unknown result counts as neither passed nor failed and falls
  through to `read_back`, so uncertainty never manufactures a block.
- **F1 — read-back was any read, of any file (TIGHTENED).** A `Read` of *any* file satisfied
  a derivation claim ("I read X"), even a file the claim never named. The derivation rule now
  requires a read whose basename matches a file the claim names (a path-less repo-wide search
  still counts; a claim that names no file still accepts any read). Conservative by design —
  F1 is a recall gap, so every uncertain case resolves toward backing, never toward a block.

Both were previously recorded-not-patched (a maintainer tuning call); the maintainer's PR
review requested F2 before block-mode and F1 alongside, so both are now landed with the
fail-open/precision invariants preserved and regression tests added.

## Files

- `SPEC.md` — track spec: gap, mechanism, audit schema, pre-registered falsifier, detector-gaps, build plan.
- `vulcan-surface-compliance.py` — the hook (fail-open, loop-guarded; reuses the Stop-hook skeleton already proven in the source instance).
- `test_surface_compliance.py` — end-to-end tests via real Stop payloads on stdin.

## Run the tests

```
python3 tracks/SC-1-strategic-surface-compliance/test_surface_compliance.py
```

## Placement

Filed under `tracks/` as a self-contained proposal; relocate as fits the repo's layout.
