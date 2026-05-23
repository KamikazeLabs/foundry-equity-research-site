# Helix Pre-Redesign Audit — 2026 Q2

**Scope:** the Helix Site Forge pipeline as currently described in `method/index.html` of this site, before any of the M1–M4 transformations land.
**Reference:** `research/2026-05-helix-transformation.md`, Parts III and IV.

This audit grades the existing pipeline against the ten invariants distilled in the transformation paper. It is the baseline against which M1–M4 deliverables will be measured.

## Existing pipeline (recap)

- Two human reviewers: one fundamental, one quantitative.
- Three independent AI reviewers; *all three must concur*.
- Twelve mechanical gates: number-tie, citation resolver, date consistency, ticker validity, chart render, font embedding, brand check, TOC parity, page budget, disclaimer, spell and grammar, AI triple-review concurrence.
- Any gate failure blocks publication.

## Grades

| # | Invariant | Status | Notes |
|---|-----------|--------|-------|
| 1 | Vary what you held fixed | **Gap** | Template, gate set, reviewer count, page budget are constants. |
| 2 | General reasoner + cheap verifier | **Partial** | 12 verifiers exist; reasoners appear to be a single class. |
| 3 | Step-level supervision | **Partial** | Gates are mostly artifact-level (cell, citation, page). No step-level claim scoring. |
| 4 | Convergence across independent paths | **Weak** | Three reviewers but no enforced disjointness of priors. |
| 5 | Adversarial structure | **Missing** | "Concurrence" is consensus, not survival of refutation. |
| 6 | Layered specialists | **Partial** | Two human roles differentiated. AI reviewers undifferentiated. |
| 7 | Cross-domain transfer | **Missing** | No architectural slot for it. |
| 8 | Wandering vs. grounding separated | **Strong** | Number-tie + citation resolver separate grounding well. |
| 9 | Written principles + self-critique | **Missing** | Implicit editorial policy only. |
| 10 | Long arguments as graphs | **Missing** | Number-tie checks cells; no argument-graph check. |

**Net:** strong on grounding, weak on diversity and adversariality, missing on cross-domain reach and self-critique.

## What the transformation must deliver

- **M0** closes invariant 9 (constitution exists) and invariant 1 (paper shapes parameterize the pipeline).
- **M1** closes invariants 3 and 10 (argument-graph gate) and invariant 4 (disjoint-priors panel).
- **M2** closes invariant 5 (adversarial debate) and adds the counter-construction adversary for invariant 7.
- **M3** completes invariant 3 (PRM for step-level supervision) and adds evolutionary thesis search.
- **M4** closes invariant 7 fully (ledger as algebraic structure) and adds the constitution gate (invariant 9 mechanical).

## Baseline metrics (to be filled in once telemetry lands)

| Metric | Last 4 papers | Target after M1–M4 |
|--------|---------------|--------------------|
| Mean gates failed per paper before resolution | — | ≤ 2 |
| Reviewer pairwise disagreement rate | — | ≥ 30% (disagreement is healthy) |
| Papers killed by counter-construction | n/a | ≥ 1 per quarter |
| Debate length (median turns) | n/a | 6–10 |
| Argument-graph minimum edge score | n/a | ≥ threshold |
| Thesis hit rate at 12 months | (see ledger) | ≥ baseline |

These rows are placeholders. The first job of the M0 + telemetry work is to populate them.
