# Open work — doc-staleness as a falsifier-shaped failure mode

> **Filed 2026-05-25 (S58)** after a sweep found B-1's `README.md` still claimed `v0.1` status while v0.2 had shipped and v0.3 was in draft. Same shape as the spec-vs-implementation bugs the 2026-05-25 falsifier sweep caught (F1/F3/F5/F6) — just in a different artifact pair.

## The observation

The B-1 falsifier register watches **code-vs-spec** divergence: does the implementation actually do what the falsifier text says, on the real audit-log shape. The 2026-05-25 sweep found three falsifier text bugs (F1 missed git history, F3 over-counted, F5 had no field to check) and one real anomaly (F6 timestamp non-monotonicity) — all instances of "the text and the artifact have drifted apart and nobody noticed because no automated check was watching the gap."

`README.md` is the same shape. The spec-vs-impl pair is just **doc-vs-impl**:

| Pair | What can drift | What catches drift today |
|---|---|---|
| Falsifier text ↔ live data | Spec assumes a field/shape that doesn't exist | Falsifier sweep (manual, ad-hoc) |
| Doc ("status: v0.1") ↔ live state (v0.2 shipped, v0.3 drafted) | Doc names a version that no longer matches reality | Nothing — discovered by reading |
| Roadmap ("v0.2 = IMAP") ↔ actual v0.2 (paraphrase exception) | Roadmap predicts a path the project didn't take | Nothing — discovered by reading |

Three instances of the same failure pattern. The discipline that watches one pair should watch all three.

## Why it matters here (not in general)

Most projects let docs drift; it's a known tax. **In a verifiable-autonomy repo it's worse**, because:

1. **Docs are the substrate for cross-op review.** If `README.md` says v0.1 and the agent ships v0.2 behavior, an external reviewer reads the wrong thing and reviews the wrong artifact. Same-family reviewers (Opus-4.7-to-Opus-4.7) are likely to silently fix the gap in their heads; external-family reviewers are exactly the ones who *won't* — they will review what the doc says.
2. **Docs are gate substrate.** `ROLLBACK.md` line 20 says "B-1 v1 considers auto after falsifiers hold across n ≥ 2 campaigns per the B-1 README roadmap." If that roadmap is stale, the rollback contract is pointing at a phantom criterion.
3. **The falsifier-per-track pattern claims it catches Surface-Compliance.** Doc-vs-impl drift is a particularly clean Surface-Compliance failure: the doc claims a state that isn't true; nothing about the underlying work changed because of the doc; the falsehood persists silently. If our discipline doesn't catch this in our own repo, the discipline isn't generalizing.

## What a discipline for this would look like

Rough sketch — not committed, not designed, just shape:

- **Reference-graph check.** Every `README.md` / `ROLLBACK.md` / `OPEN-WORK-*.md` that names a version or a file should be checkable: does the named version match the latest amendment file? does the named file exist? An automated pass over the doc set with grep + `git log` could catch most of it.
- **Doc-touch falsifier.** "If `agents/<X>/falsifier.md` was modified in the last N commits, and `agents/<X>/README.md` was not, flag it." Same for amendments. Cheap, catches the common case.
- **Version-string single source.** Status lines that get out of sync with reality are status lines that have no canonical source. Put the version in one place; everything else references it.

All three are deferrable. None should land before B-1 has real campaign data — the cost of doc-drift at n=1 sent is zero. The point of filing now is so the next sweep doesn't re-discover the same shape and treat it as a one-off README bug.

## Trigger to revisit

- **Second instance of doc-vs-impl drift discovered manually** → escalate to "design the discipline."
- **First external-family review where reviewer demonstrably read a stale doc** → escalate to BLOCKER.
- **B-1 hits n≥10 sends** and the v0.3 amendment lands → expect the README to drift again; that's the moment to wire the reference-graph check, not before.

## Anti-pattern self-flag

- **Risk: turning this into busywork.** Every doc-drift catch suggests "let's automate doc checking." Three caught manually in one session is data; one would be noise. Don't pre-build the discipline; let the pattern accumulate so the design is grounded in real failures.
- **Risk: scope creep.** This note exists so the next sweep recognizes the pattern, not so we ship a doc-linter this sprint. If a future operator reads this and reaches for the linter before there are 5+ instances, they're skipping the falsifier-per-track substrate.
- **Risk: hiding behind the rule.** "We have an open-work note about doc-staleness" is not the same as "docs are fresh." The note is a memory aid, not a fix.

## Cross-references

- The originating sweep + amendment: `agents/b1-customer-interviewer/AMENDMENT-v0.3-DRAFT-falsifier-spec-tightening.md`
- The stale doc that prompted this: `agents/b1-customer-interviewer/README.md` (patched 2026-05-25)
- Pointer that depended on the stale roadmap: `ROLLBACK.md` line 20
- Surface-Compliance discipline this is an instance of: `MODE-CONTRACT.md`, `agents/README.md`

---

*v0.1, S58 (2026-05-25). File or delete based on whether the pattern recurs.*
