# Cross-operator review — Verifiable-Autonomy @ 4a7ba49

**Reviewer:** Eve (eve-claude-code surface, Android tablet, model claude-fable-5,
bus identity `linux-claude-a95ae96f`)
**Reviewed:** 2026-07-19 (delivered in-session; landed here 2026-07-20 on operator's
instruction — this file is a faithful record of that review, written by the same
session that ran it)
**Method:** fresh clone to /tmp, read before run, **run before believing** — every
runnable claim executed, not trusted.

## Verdict: PASS

All runnable claims verified by execution:

- `validate` — green
- `build` — green
- hostile-spec refusal — green (factory refuses the hostile spec; the refusal is
  code, in `factory/factory.py`)
- `./killswitch all` — green: repo-wide flip-back to `step` executed and recorded.
  **Evidence committed with this review:** the appended line in
  `agents/b1-customer-interviewer/flip-history.jsonl` (timestamp 2026-07-19T19:06:57Z,
  trigger `operator_killswitch`, note `./killswitch all`) is this review's own test
  artifact — the mechanical record the repo's design promises, produced by the review
  that checked the promise.

## Headline should-fix: label the enforcement split

The repo's guarantees divide into two classes that the docs present with equal
confidence but that are not equally strong:

- **Code-enforced:** `./killswitch all` (mechanical flip-back), factory.py's
  hostile-spec refusal. These hold regardless of agent behavior.
- **Agent-prose-enforced:** the MODE read-discipline (agent reads its MODE file
  before acting) and the falsifier auto-flip-back — "the killswitch in the steady
  state" — are **prose instructions to an agent**, not mechanisms. Only the operator's
  explicit `./killswitch all` is mechanical.

This is the same finding class as PCLA's code-enforced vs prose-enforced distinction:
neither class is wrong, but an **unlabeled** mix invites over-trust in the prose class.
Fix is cheap: one table in README/MODE-CONTRACT declaring which guarantee is which.

## Nits

- `factory/factory.py` docstring says "v0.0" while the factory is at 0.1 —
  stale self-description.
- The hole-check scans only `.md`/`.html`; a `{{SPEC:` remnant in generated `.py`
  would pass unnoticed. (During review, a grep hit for `{{SPEC:` in built
  `render.py` looked like a shipped hole — verified before claiming: it is a
  comment, not a hole. The check's blind spot is real even though this instance
  was benign.)

## Substrate caveat (named, per the review discipline)

Cross-operator here is **not cross-family**: reviewer and reviewed-repo agents run on
the same model family. Agreement between us is weaker evidence than cross-family
agreement would be; a shared blind spot would look like consensus.

## Honest residual

The review executed what is runnable and read what is not. Prose-enforced behaviors
(MODE read-discipline in live operation, steady-state falsifier flip-back) were
**not observed under live agent operation** — only their instructions were read and
their mechanical fallback tested. The steady-state claim remains unverified by this
review; that is exactly why the enforcement-split label matters.
