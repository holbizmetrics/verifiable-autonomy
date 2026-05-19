# B-set: Business-Builder Track Set: PROPOSAL

> **Status: PROPOSAL. Not an active track set. Filed S55 (2026-05-18) to capture scope after Polsia competitive review. Implementation gated on A-1 landing + ≥2 PCLA tracks demo-stable + hosted-infra eng project funded. Do NOT begin B-track SPECs without re-reading hard prereqs § below.**

## Why this file exists

Polsia (https://polsia.com, launched Feb 2026, $49/mo + 20% rev-share) ships "AI that runs your company while you sleep" with the agent set: Strategic Planning, Code & Deploy, Marketing & Sales, Inbox Management, Customer Support. Built on Claude Opus 4.6 + Claude Code + MCP. Aggregate platform: 500-700 companies, $450K+ ARR claimed. Trustpilot 2.7/5 from 6 reviews; honest reviews report generic marketing output, burned credits with no output, hallucinated agent responses, "too early-stage for anything mission-critical."

The competitive opening: **autonomy without verification is what's failing in market.** PCLA's whole architecture is around audit + gates + rollback + cross-op review. That's precisely what Polsia is missing per the actual user reviews.

This file scopes a Path-B track set that would instantiate PCLA's track-and-gate architecture for the business-builder use case. The differentiation is **not the agent inventory**: it's the falsifier + audit + rollback per track.

## Track inventory (8 tracks, B-1 .. B-8)

| # | Track | Polsia analog | Pre-registered headline falsifier |
|---|---|---|---|
| **B-1** | `customer-interview-runner` | "Strategic Planning" | Agent emits "interviewed N customers, found pain X" without verifiable customer-side artifact (email thread / calendar event / recording). ≥1 = FP. **The Surface-Compliance test for soft work.** |
| **B-2** | `landing-page-deployer` | "Code & Deploy" (marketing) | Copy specificity floor: <3 ICP-specific phrases from B-1 transcripts → step-flip. Generic-verb count > threshold. *Directly targets Polsia's "marketing output is generic" review.* |
| **B-3** | `cold-outreach-runner` | "Marketing & Sales" cold email | Spam-marked rate >5% at provider level → step-flip. Reply where agent invented prospect-side context (re-derivation against scrape source) = FP. |
| **B-4** | `ads-pilot-runner` | Meta Ads agent | Budget burn past cap without statistical significance → auto-pause. ≥1 platform policy violation → step-flip. TRIAD-fail on brand consistency. |
| **B-5** | `code-deploy-runner` | "Code & Deploy" (product) | **Phantom-commit detection:** re-derive from PR diff + CI logs vs. agent's report. Mismatch = FP. Pre-deploy: ENVELOPE (scope) + BLIND-VERIFY (tests green). |
| **B-6** | `inbox-triage-runner` | Inbox Management (incl. VC) | Auto-send on flagged-high-stakes category (VC, legal, customer-escalation) without operator approval = **FATAL**, immediate step-flip + alert. |
| **B-7** | `support-triage-runner` | Customer Support | Customer-side correction rate >10% on draft replies → step-flip. ≥1 hallucinated feature claim = FP. |
| **B-8** | `metrics-watchdog` | implicit | FP rate on anomaly flags > 0.2 → step-flip. Missed-anomaly rate measurable via post-hoc review (operator marks after-the-fact). |

## Phasing (gate-cost-ordered)

- **B-α (cheap, validate pattern):** B-1 (text, low-stakes), B-8 (read-only)
- **B-β (outputs, operator-approve gate stays on):** B-2 (page), B-7 (draft support)
- **B-γ (outputs that spend money):** B-3 (email), B-4 (ads), B-5 (deploy)
- **B-δ (inbound high-stakes):** B-6 (inbox; failure mode = hallucinated VC term-sheet signed in agent's voice)

## Cross-cutting infrastructure (substrate, not tracks)

1. **Hosted infra layer**: web server + DB + email account + analytics + ad-platform OAuth, per operator. **Polsia's actual moat. PCLA does not have it.** PCLA is a research lab, not a SaaS. If Path B is real, this is the bigger engineering project than all 8 tracks combined.
2. **Audit bus**: unified `business-builder-audit.jsonl`, every track appends. Single source of truth for what happened.
3. **Operator-attention router**: step-mode notifications + diff-to-approve. SecuredChat bus (A-6) is the substrate; pattern already works.
4. **Killswitch**: one command takes all tracks back to step. ROLLBACK.md pattern, scaled.
5. **Cross-Company Learning equivalent**: MIRROR Gap Taxonomy already does this for PCLA itself. For B-tracks: anonymized failure-mode aggregation across operators, audited and opt-in (unlike Polsia's closed transfer).

## Cross-operator review burden

8 tracks × Eve-per-SPEC + Eve-per-first-impl = ~24 review cycles. Eve becomes the bottleneck.

**Recommended:** Commission ONE external reviewer (Mark / external-Claude / human pentester) for the **B-architecture meta-review first**: does the falsifier-per-track pattern actually catch the failure modes that killed Polsia's reviews? Then per-track Eve reviews only after meta-review passes. Cuts ~half the queue.

## Hard prereqs (re-read before any B-track SPEC begins)

1. **A-1 phase-transition-auto must land first.** A-1 solves exactly the Surface-Compliance detection problem that ALL 8 B-tracks depend on. The B-1 falsifier (claim "interviewed N customers" without artifact) IS a Surface-Compliance check. Without A-1's re-derivation routine as proven substrate, every B-track is built on sand.
2. **≥2 PCLA tracks flipped with demos.** Currently 1 (A-3) + 1 retroactive-provisional (A-6). Need at least one more clean step→auto with n=2 demos.
3. **Eve / Mark / external availability** for cross-op queue of ~24 review cycles.
4. **Hosted-infra eng project funded.** This is the real cost of competing with Polsia at product layer, not research layer.

## Right-sizing recommendation (load-bearing)

**Don't build all 8 tracks.** Scope B-1 first, in PCLA-research mode, as proof that the falsifier-per-track pattern catches Surface-Compliance in soft work:

- Soft outputs (text), no money spent, no users hurt if it fails
- Falsifier is the textbook Surface-Compliance test ("did the agent actually do the work it claims?")
- If B-1's falsifier catches even ONE phantom-interview during dogfooding, we have the proof point that beats Polsia on rigor
- If it doesn't catch anything, we learn the falsifier is too loose before spending money on B-3/B-4/B-5

**B-1 honest cost estimate:** ~A-1-equivalent (SPEC + Pre-commits + cross-op review + impl + n=2 demos). 3-5 sessions if A-1 is already done. 8-12 sessions if A-1 is still in flight.

## Tagline candidates (for when it's real, not now)

- "Polsia, but the agents don't lie to you."
- "Verifiable autonomy. No revenue cut."
- "Autonomous operations with audit trails."

## Honest scope of this PROPOSAL

This file is **scope-capture, not a plan**. The track titles, falsifiers, phasing, and recommended sequence are all subject to revision when (a) A-1 lands and surfaces architectural lessons that change the B-set assumptions, (b) Polsia's product evolves and the differentiation calculus shifts, (c) hosted-infra engineering surfaces costs that re-order what's tractable.

The load-bearing claims here are:
- Polsia's market vulnerability is "autonomy without verification" (sourced from honest reviews, not Polsia's marketing)
- PCLA already has the architecture (mode-toggle, falsifiers, audit, rollback, cross-op review) that addresses that vulnerability
- A B-track instantiation is feasible BUT non-trivial (hosted infra moat + cross-op review burden)
- B-1 is the right first move under load-bearing rigor (cheap, low-stakes, high signal on whether the pattern generalizes)

## Cross-references

- Polsia honest review: https://crevio.co/blog/is-polsia-legit
- Polsia $1M ARR claim (unverified): https://www.contextstudios.ai/blog/polsia-how-a-solo-founder-hit-1m-arr-in-30-days-with-ai-agents
- Polsia Product Hunt: https://www.producthunt.com/products/polsia
- PCLA mode-toggle architecture: `CLAUDE.md` § Mode toggle semantics
- A-1 SPEC (hard prereq): `tracks/06-phase-transition-auto/SPEC.md`
- A-3 SPEC (the architecture template): `tracks/08-closeout-auto/SPEC.md`
- Cross-op review template: `.prometheus/cross-operator/_TEMPLATE.md`
- A-6 SecuredChat bus (substrate for operator-attention router): `tracks/12-inter-session-bus/SPEC.md`

---

*PROPOSAL v1, S55 (2026-05-18). Filed after competitive review of Polsia. Re-read hard prereqs § before any B-track SPEC work begins. This file does NOT authorize implementation.*
