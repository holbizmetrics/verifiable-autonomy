# Factory — DEFERRED capabilities

Items named, not built. Each is a real factory-layer extension picked per instance need *after* the factory layer exists (≥2 deployed instances per `factory/SPEC.md` § Scope decisions).

Filing here keeps them out of the in-flight work and surfaces them when the factory layer is being designed. Per SPEC § Working protocol step 4: "no in-session move is a valid answer" — filing without building is the correct response when the prerequisite (the base case) does not yet exist.

---

## Framing: business-as-DevOps

These items aren't two unrelated extensions — they're facets of one architecture. The factory is the **platform** (templates = infra-as-code, `render.py` = build, GH Actions = CI/CD, secrets = config). On top of that platform, the two deferred items add the missing operational layers:

- **CC-mode (§ 1)** = control plane. The operator drives staging + prod from one interface.
- **Simulation (§ 2)** = test environment. Two invocation modes (pre-deploy verifier + post-deploy diagnostic).

What AWS is to a web service, the factory is to a value→capture business loop: versioned, tested, deployable, rollback-able, observable. Both items earn their slot in v1 of the factory layer (post ≥2 instances), not before. DevOps tooling is a *trailing* discipline — built when the manual ops pain has been felt, not before the first prod exists.

---

## 1. CC-mode output (CC as operator-full interface, or CC-only surface for inbound businesses)

**What:** A second factory output shape, alongside the current "web-deploy" shape. Two sub-variants:

- **CC-operator-mode:** customer-facing surface is still web (landing, Stripe, email), but the operator drives everything from inside Claude Code via tool integrations — Stripe API/MCP for payments, Gmail MCP for intake reading + report sending, `gh` CLI for deploy. Operator never leaves CC.
- **CC-only surface:** for businesses where the audience is already direct (no public landing needed), the customer-facing surface is email-only. CC reads inbound, drafts quotes, processes payment links, delivers reports. No public storefront.

**Why deferred:**

- SPEC scope decision 4: base case before factory. Not at ≥2 deployed instances yet.
- This is a factory output-shape choice; picking it now would build a factory layer before the base case is done — the exact drift the SPEC was designed to stop.

**Revisit when:** factory layer is being designed (after ≥2 instances) AND a candidate instance has a business model that fits one of the sub-variants (audience-already-direct = candidate for CC-only surface).

**Tradeoffs to carry forward:**

- Credentials cross the CC boundary — needs explicit auth + secret-handling (env vars / MCP auth / OAuth).
- "Deployable without you" weakens — CC needs operator-initiated sessions to run; not a 24/7 web server. Acceptable for instance shapes where build-time automation is the value, not run-time autonomy (per SPEC § Scope decisions: "Automated = build-time").

---

## 2. Loop simulation (pre-deploy verifier + post-deploy diagnostic)

**What:** Multi-agent role-play of the full value→capture loop. Agents play customer + operator + edge cases (refund flow, no-reply-from-buyer, payment-without-intake, etc.). Two invocation modes:

- **Pre-deploy verifier:** before declaring an instance Level-0 done, run simulation to catch loop holes the single-pass test-customer verifier misses.
- **Post-deploy diagnostic:** when prod breaks (buyer complaint, dropped intake, refund-edge fires unexpectedly), spin up simulation matching prod state, reproduce the failure, fix in code, redeploy. The high-value mode — turns "prod incident" from operator-pager into "diff + replay."

Same shape as V-A's existing multi-agent verification discipline (Surface-Compliance, falsifier-per-track, MODE-contract). Becomes a factory-layer capability.

**Why deferred:**

- Overkill for low-state-machine instances (audit-consulting has 4 hops; test-customer step already covers it).
- SPEC scope decision 4: base case before factory. Not at ≥2 deployed instances yet.
- Pays off for higher-state-machine businesses (subscriptions, marketplaces, anything with churn/retries/multi-party flows) — none yet in scope.

**Revisit when:** an instance is being scoped that has more than ~5 state transitions in the value→capture loop, OR a deployed instance fails in a way the single-pass test-customer verifier missed.

**Tradeoffs to carry forward:**

- **Hard one:** even good simulation is NOT real-customer signal. Run too many sim-rounds and you build comfort instead of revenue. **Bound tightly:** pre-deploy verifier only, not a substitute for going live.
- Distinguishes sharply from market simulation ("will customers actually buy?") which SPEC explicitly forbids ("genuine-novelty parts are market-verified, out-of-session"). This entry is mechanism-simulation only.

---

## Filing protocol

Add a new entry here when:

- An architectural extension is named in dialog
- It is real (would add value when conditions allow)
- But conditions don't allow yet (usually: prerequisite step in the SPEC discipline isn't met)

Do NOT add:

- Speculation about features no one asked for
- Cleanup tasks (those go in `OPEN-WORK-*.md`)
- Things already covered by SPEC § Deferred (autonomous ideation; run-time autonomy; the factory layer itself)

Filed: 2026-05-26 (after operator decided to defer CC-mode and pre-deploy simulation until factory layer exists).
