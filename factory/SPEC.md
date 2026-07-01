# Automated Business Builder — spec (verifiable-autonomy)

*Shaped via TRIAD (standpoint review) + a KG-substrate pass. Deliberately bounded so it's
groundable and drift-resistant: a defined input, a defined **checkable output**, and a
built-in stop condition.*

*Filed authoritative 2026-05-25. The "v1" in the source filename
(`automatedbusinessbuilderv1spec.md`) was a typo — this is the **current** target, not a
future version. Source: operator-authored, dropped into Android Downloads.*

## What it is
An **orchestrator** that turns a *business-desire* into a **deployed, revenue-capable
business instance**, by assembling reusable primitives (the B-tracks). It is **not** the
parts (B-1..B-8) — it's the **assembler** that wires them for a given desire. (This factory/
assembler layer is what the current ROADMAP / README / B-PROPOSAL were missing.)

## Scope decisions — pin these; they are what stop the drift
- **"Automated" = build-time.** The *building* is automated; the instance is **yours to run**.
  Run-time autonomy (a business that runs *itself*) = a later layer, explicitly deferred.
- **Clarify, don't auto-ideate.** Under-specified input → **interview to clarify**.
  Autonomous ideation-from-nothing = deferred (the dark-zone, most drift-prone branch).
- **Level cap.** The businesses it builds do **not** build businesses. One meta-level only.
- **Base case before factory.** Build **one** instance end-to-end first; the "factory" = the
  *generalized procedure* extracted from **2–3 worked instances**. No factory layer before
  instances exist. (You can't write the recursive step without a base case.)

## Input — the business-desire (abstract → specified)
A desire on a spectrum: *"I need an automated business"* (abstract) … *"…to sell AI art"*
(specified). If under-specified, **interview** to a **minimum viable business-spec**:

    { what's sold · to whom · how value is delivered · how money is captured }

## Output — what a "built automated business" IS (the checkable deliverable)
A **deployed instance** with a working **value→capture loop**:
1. a **product / offer**,
2. a **way for a customer to get it** (storefront / page / flow),
3. a **payment mechanism**,
4. **deployable without you** (no secrets in source; deploy steps documented).

## Done-condition (the verifier — this is the thing whose absence caused the drift)
The instance **deploys** AND the **value→capture loop works end-to-end** — a *test* customer
can get the product and pay. **First *real* customer = OUT-OF-SESSION, yours.** The builder
stops at "deployable + loop-verified" and hands real-customer acquisition to the operator.

## Relationship to the B-tracks
B-1..B-8 are the **primitives** (talk-to-customer, landing, ads, deploy, …). The **factory =
the assembler** of those primitives for a given spec.

## Working protocol — the anti-drift gate (run EVERY session, ideally in CLAUDE.md so it's read each turn)
1. **Session-start gate.** Name the target + blocker out loud: *"Today's only honest
   in-session moves are: build/advance a Level-0 instance, or define the factory once ≥2
   instances exist. If neither applies, the move is out-of-session/operator — say so and stop."*
2. **Specify by example.** Hand it a concrete desire + (when building) the value→capture loop
   it must produce. Never just "build a business."
3. **In-session vs out-of-session boundary.** Building the instance (product / page / payment
   / deploy) = in-session. Real customers / infra-funding / multi-week engineering =
   out-of-session, operator-bound. The builder **does** the first, **names** the second, and
   **does not substitute** one for the other.
4. **"No in-session move" is a valid answer.** When asked "what's next" and there's no
   in-session move, the correct output is *"the move is yours"* — **not** substrate-polish.

## Deferred (named, not done)
- Autonomous ideation (factory invents the business idea).
- Run-time autonomy (the business runs itself).
- The factory / generalization layer (until ≥2 worked instances exist).

## Amendment 2026-07-01 — operator override on the scaffold layer (recorded, not hidden)

By explicit operator decision (2026-06-23), a **content-agnostic scaffold** of the factory layer was
built ahead of the ≥2-instance gate: business-spec schema + `validate` + `build` + value→capture
storefront emission (`factory/factory.py`). This amendment records that override so SPEC (law),
`ROADMAP.md` (practice), and `CLAUDE.md` (state) agree on one source of truth.

**What the override does NOT relax — the base-case gate still holds for the generalization step.**
"Base case before factory" (above) bars building the *generalization* layer from n=1 for a reason:
*you can't write the recursive step without a base case* — from zero completed instances you build the
**wrong** generalization. Building a *content-agnostic emitter* early doesn't wander the content
dark-zone (the operator supplies all content via the spec), so that half is safe — but it does **not**
license extending `factory/specs/` or declaring the factory *generalizing* before a real,
structurally-distinct **n≥2** instance exists.

**Concrete evidence the gate is real (2026-07-01):** a differently-shaped idea (styling-teacher, an
*app*) was force-fit into the n=1 (email-intake *service*) schema — the predicted "wrong recursive
step from no base case." It was removed to `../Researches/styling-teacher-candidate/`. The premature
schema was the root affordance for that misfit. So: scaffold — allowed and recorded; extension of
`factory/specs/` with new business shapes — **gated on real n≥2**; `pitch-deck-review` is a same-shape
second (content-parameterization), not that generalization test.

---
*Honest scope: TRIAD here was a genuine standpoint review; the KG-substrate pass was
single-agent (one model playing the substrates) = the weaker form — good for shaping a spec,
not a true independent-multi-agent run. This is build-time/reach work, not novelty — the
genuine-novelty parts (will a business succeed?) are market-verified, out-of-session.*
