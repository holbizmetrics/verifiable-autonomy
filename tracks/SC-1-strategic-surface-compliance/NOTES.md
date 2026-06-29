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
