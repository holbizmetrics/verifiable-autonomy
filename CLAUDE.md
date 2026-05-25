# verifiable-autonomy — session discipline

**Authoritative spec:** `factory/SPEC.md` (Automated Business Builder). Read it before suggesting work in this repo.

## Anti-drift gate — run EVERY turn that proposes work

Per `factory/SPEC.md` § Working protocol. These 4 steps exist because this exact repo drifted 6+ rounds in one session before the spec was written. The gate is the corrective.

1. **Session-start gate.** Name the target + blocker out loud:
   *"Today's only honest in-session moves are: build/advance a Level-0 instance, or define the factory once ≥2 instances exist. If neither applies, the move is out-of-session/operator — say so and stop."*

2. **Specify by example.** Demand a concrete business-desire + (when building) the value→capture loop it must produce. Never act on just "build a business."

3. **In-session vs out-of-session boundary.**
   - **In-session:** building the instance — product / page / payment / deploy.
   - **Out-of-session, operator-bound:** real customers, infra-funding, multi-week engineering.
   - The builder **does** the first, **names** the second, and **does not substitute** one for the other.

4. **"No in-session move" is a valid answer.** When asked "what's next" and there's no in-session move, the correct output is *"the move is yours"* — **not** substrate-polish, doc-tidying, or scaffolding more layers.

## State as of 2026-05-26

- **Level-0 instances deployed with value→capture loop:** 0 of needed 1.
- **Level-0 instance in flight:** `instances/agent-audit-consulting/` — spec locked (4 axes), landing + intake + operator-actions written in-session; deploy + Stripe link + test-loop verify = operator-bound, see `instances/agent-audit-consulting/OPERATOR-ACTIONS.md`.
- **Factory layer (`factory/`):** scaffolded prematurely (spec says don't build until ≥2 instances exist); kept as substrate, not advanced until base case done.

In-session move = advance the in-flight instance toward done-condition where steps are not operator-bound. If all remaining steps are operator-bound, the correct output is *"the move is yours"*.

## Repo map

- `factory/SPEC.md` — authoritative
- `factory/factory.py`, `factory/specs/`, `factory/README.md` — premature factory scaffold; do not advance until base case exists
- `instances/agent-audit-consulting/` — Level-0 instance in flight (AI-agent audit consulting)
- `agents/b1-customer-interviewer/` — B-1 primitive (talk-to-customer); the one primitive partially built
- `B-PROPOSAL.md`, `ROADMAP.md`, `README.md` — repo framing docs (factory-frame corrected in commit 69e0b51)
- `OPEN-WORK-doc-staleness.md` — known recurring failure mode
