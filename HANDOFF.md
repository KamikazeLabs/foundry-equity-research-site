# Helix Site Forge — Implementation Handoff

**Audience:** the KamikazeLabs Forge engineering team.
**Branch:** `claude/research-helix-application-gJVdH`
**Status:** blueprint complete; runtime integration begins here.

This document is the entry point for the engineers who will take the blueprint and turn it into Forge runtime code. The blueprint is large; this handoff is the path through it.

---

## TL;DR

The current Helix Site Forge runs 12 mechanical gates + a 3-AI concurrence check. The blueprint on this branch transforms that into a 20-gate pipeline with:

- **Disjoint-priors reviewer panel** replacing undifferentiated concurrence (Invariant 4).
- **Adversarial debate** (Bull / Bear / Judge) replacing flat consensus (Invariant 5).
- **Counter-construction agent** building publicly-verifiable counterexamples before publish (Invariant 5/7).
- **Argument-graph coherence gate** with weighted load-bearing edges (Invariant 10).
- **Constitution gate** enforcing 15 written provisions mechanically (Invariant 9).
- **FunSearch-style evolutionary thesis search** (Invariant 1) — pre-paper phase.
- **PRM (process reward model)** for step-level supervision once trained (Invariant 3).
- **Ledger-query agent** treating the ledger as algebraic structure for precedent surfacing (Invariant 7).

The first-principles derivation lives in `research/2026-05-helix-transformation.md` (Parts I–VIII). The implementation plan is Part VI.

---

## Read these in this order

1. **`research/2026-05-helix-transformation.md`** — the why. 30 minutes.
2. **`HELIX_CONSTITUTION.md`** — the live rule set (15 provisions). 5 minutes.
3. **`research/audits/2026-Q2-pre-redesign-audit.md`** — the gap analysis. 5 minutes.
4. **`helix/README.md`** — the blueprint package overview. 2 minutes.
5. **`helix/gates/README.md`** — the 20 gates. 5 minutes.
6. **`examples/synthetic-passing/`** — what a complete paper bundle looks like end-to-end. 15 minutes.
7. **`helix/gates/13-argument-graph/`** — the one runnable gate. Reference implementation. Run the tests. 10 minutes.
8. **This document** — the implementation order. 5 minutes.

Total: ~75 minutes to fully load the blueprint.

---

## File map

| Path | Purpose | Status |
|------|---------|--------|
| `HELIX_CONSTITUTION.md` | Live constitution (15 provisions, 6 sections) | Production-ready |
| `research/2026-05-helix-transformation.md` | Design paper (608 lines, Parts I–VIII) | Reference only |
| `research/audits/2026-Q2-pre-redesign-audit.md` | Baseline audit | Reference only |
| `helix/README.md` | Blueprint package overview | Reference only |
| `helix/shapes/*.yaml` | 4 paper shapes (compounder, short, special, macro) | Implementable |
| `helix/gates/13-argument-graph/check.py` + tests | **Runnable** reference implementation | Production-ready |
| `helix/gates/<N>-<slug>/spec.md` | Per-gate specs (13–20) | Implementable |
| `helix/agents/<slug>/spec.md` | Per-agent specs (8 agents) | Implementable |
| `helix/agents/README.md` | Agent inventory + "model family" definition | Reference only |
| `helix/pipelines/*.yaml` | pre-paper, pre-publish, post-mortem | Implementable |
| `helix/prm/*.md` | PRM training data schema and approach | Spec only |
| `helix/funsearch/spec.md` | Evolutionary thesis search | Spec only |
| `helix/disagreement_matrix_schema.md` | YAML schema for the disagreement artifact | Implementable |
| `helix/telemetry/dashboard.md` | Per-paper and cross-paper telemetry schema | Implementable |
| `examples/synthetic-quality-compounder/` | Held-paper example (Judge ruled bear) | Reference |
| `examples/synthetic-passing/` | Shipped-paper example (Judge ruled bull) | Reference |
| `examples/synthetic-short/` | Shipped-short example (8-turn debate) | Reference |
| `examples/VALIDATION_NOTES.md` | The eight spec gaps surfaced during validation | Resolved (commit `308fbdf`) |
| `research/base-rates/*.yaml` | Sample base-rate library file (gate 15 input) | One worked example committed |
| `research/post-mortems/GLTZ-*.md` | Sample post-mortem validating M3 PRM schema | One worked example committed |
| `Makefile` | `make test` / `make verify-all` / `make check-source-values` | Production |
| `tools/check_source_values.py` | Lints source_values.json vs transformations.yaml row refs | Production |
| `.github/workflows/helix-gates.yml` | CI for gates 13, 14, 17, 18, 19, 20 on every push | Production |

---

## Milestone-by-milestone ticket breakdown

Tickets are sequenced in implementation order. Each ticket includes (a) what to build, (b) what to reference, (c) acceptance criterion.

### M0 — Foundation (mostly complete on branch)

- **M0-T1.** Adopt `HELIX_CONSTITUTION.md` v1.0 as live policy. *Acceptance:* desk lead signs off; document is treated as binding by gate 20.
- **M0-T2.** Integrate the shape-selector agent. Spec: pick one of 4 shapes from the brief. *Acceptance:* Q3 2026 paper produced under the selected shape, not the legacy template.
- **M0-T3.** Add `research/audits/<quarter>-audit.md` to the quarterly cadence. *Acceptance:* one audit per quarter, scored against the ten invariants.

### M1 — Argument graph + reviewer panel (4–6 weeks)

- **M1-T1.** Implement the **argument-graph extractor** (LLM call). Reference: `helix/gates/13-argument-graph/extractor_prompt.md`. Output: `graph.json`. *Acceptance:* the extractor reproduces one of the three example graphs from the corresponding paper bundle within 10% structural similarity (node/edge counts).
- **M1-T2.** Wire the **deterministic checker** into the pre-publish pipeline. *No new code needed;* import `check_graph` from `helix/gates/13-argument-graph/check.py`. *Acceptance:* failing graph (orphan, cycle, unjustified, single-sourced load-bearing) blocks publish.
- **M1-T3.** Deploy the **three reviewer agents**: `reviewer-forensics`, `reviewer-industry`, `reviewer-macro`. Model-family diversity enforced — see "Open decision points" §1.
- **M1-T4.** Build the **disagreement matrix aggregator** per `helix/disagreement_matrix_schema.md`. *Acceptance:* every paper bundle ships with both `disagreement_matrix.yaml` and a derived `disagreement_matrix.md`.
- **M1-T5.** Post-mortem template for the analyst's **step-localization labels** (feeds M3-T3). *Acceptance:* one closed position is fully labeled per the schema in `helix/prm/data_format.md`.

### M2 — Adversarial debate + counter-construction (6–8 weeks)

- **M2-T1.** **Debate orchestrator.** Bull/Bear turn loop, 400-word limit per turn, citation verification per turn. Output: `debate_transcript.md`. *Acceptance:* debate runs against the synthetic-passing PRSM paper and reproduces the transcript structure (Bull score outpaces Bear in turn-by-turn factual grounding).
- **M2-T2.** **Debate judge.** Consume transcript + appendix + constitution; produce `judge_verdict.yaml`. *Acceptance:* judge applies §III.7 + §II.5 + §III.6 by section ID, not by vibes.
- **M2-T3.** **Counter-construction agent** with retrieval tooling (SEC EDGAR, ledger, primary-source index). Produce `counter_attempt.md` with provenance per entry. *Acceptance:* the agent kills at least one candidate paper before M2 closes (constitutional requirement from `helix/agents/counter-construction/spec.md`).
- **M2-T4.** Gates **14–19** runtime. The deterministic ones (17, 18, 19) can mirror the gate-13 pattern in `check.py`. *Acceptance:* each gate has a runnable check + a test file + a passing example.
- **M2-T5.** **Appendix coupling.** Every published paper bundle includes the disagreement matrix, debate transcript, counter-attempt, and argument-graph render as appendix items. *Acceptance:* Q4 2026 paper ships with all four.

### M3 — Evolutionary thesis search + PRM (8–12 weeks)

- **M3-T1.** **Thesis generator** agent + cheap-gate evaluator harness.
- **M3-T2.** **FunSearch loop driver** per `helix/funsearch/spec.md`.
- **M3-T3.** **PRM data collection** pipeline. Start now; PRM training waits until data accumulates. Schema: `helix/prm/data_format.md`. *Acceptance:* one quarter of newly-shipped papers labeled at step level by the analysts.
- **M3-T4.** **PRM training** script + cross-validation against historical outcomes. *Acceptance:* PRM's publish-time edge score correlates non-trivially (Spearman ρ > 0.2) with realized 12-month outcomes on held-out papers.

### M4 — Constitution gate + ledger-as-structure (4–6 weeks)

- **M4-T1.** **Gate 20 constitution-conformance** check. Mostly deterministic over upstream gate results; some classifier sub-checks (e.g., §II.5 kill-switch quantitativeness).
- **M4-T2.** **Ledger-query agent** + **ledger structural refactor**. The current ledger displays aggregate stats; we need per-position structured records (entry_date, exit_date, kill_switch_triggered, named_sources, etc.).
- **M4-T3.** **Per-paper telemetry write** to `helix/telemetry/runs/<paper_id>.yaml`. Schema is fixed; implementation is mechanical.
- **M4-T4.** **Cross-paper Friday dashboard** per `helix/telemetry/dashboard.md`. Publish aggregate gate-fail rate, % held, debate-bear rate, reviewer disagreement rate.

---

## Open decision points (need product / desk-lead resolution)

1. **Model-family assignment.** Spec requires ≥2 distinct families across the three reviewers. Concrete picks (which family for forensics / industry / macro) are not made. Decision before M1-T3.
2. **PRM base model.** Fine-tune what — GPT, Claude, open-weights? Decision before M3-T4.
3. **Public telemetry scope.** What fraction of `helix/telemetry/` becomes public on the site vs. internal? Decision before M4-T4.
4. **Counter-construction retrieval cost.** Five candidates per paper × 4 papers per quarter × the EDGAR / primary-source query volume = a meaningful API cost. Budget decision before M2-T3.
5. **Debate transcript publication.** Constitution §III.8 publishes disagreement; less clear whether the full debate transcript publishes too. Recommended: yes, but the desk should explicitly opt in. Decision before M2-T5.

---

## What's deliberately not in the blueprint

These are tracked as next-up but out of scope for the M0–M4 work:

- **Formal verification (Lean-style) of the quantitative spine of papers.** Inspired by AlphaProof. Tractable once gate 19's DSL stabilizes.
- **Cryptographic source-row commitment.** Hash every source row at draft time; later edits to the source flag the paper. Defensive measure; useful once volumes grow.
- **Vision-model chart-vs-text consistency check.** Extension of the chart-render gate; defer until v2 of the gate stack.

---

## How to verify your install

```bash
# from the repo root
python3 helix/gates/13-argument-graph/test_check.py          # 15/15 should pass
python3 helix/gates/13-argument-graph/check.py helix/gates/13-argument-graph/example_graph.json
python3 helix/gates/13-argument-graph/check.py examples/synthetic-quality-compounder/argument_graph.json
python3 helix/gates/13-argument-graph/check.py examples/synthetic-passing/argument_graph.json
python3 helix/gates/13-argument-graph/check.py examples/synthetic-short/argument_graph.json
```

All four graphs should pass. The CI workflow `.github/workflows/helix-gates.yml` runs all of these on every push and PR touching `helix/` or `examples/`.

---

## Commit map of this branch

```
0fa6587  ci: GitHub Actions workflow for gate 13
3f93bec  examples: synthetic-short (GLITZ mean-reversion short, paper ships)
0970157  examples: synthetic-passing companion (PRISM Diagnostics, paper ships)
308fbdf  spec fixes: apply A.1-A.8 findings from worked-example validation
3177f48  examples: end-to-end worked-example validation of the Helix blueprint
8565d4f  helix M4: constitution gate, ledger-as-structure, pipelines, telemetry
92d041f  helix M3: evolutionary thesis search (FunSearch-for-theses) + PRM spec
f505cf2  helix M2: adversarial debate + counter-construction + gates 14-19
bf59d78  helix: gitignore python cache; drop accidentally committed .pyc
2851ccb  helix M1: argument-graph gate (runnable) + disjoint-priors reviewer panel
11cdc43  helix M0: constitution, audit, shape system
d2536fe  research: add Helix transformation paper from unit-distance disproof
```

---

## Where to start tomorrow morning

1. Verify the install (above).
2. Pick **M1-T1** or **M1-T2**, whichever has the engineer available.
3. Open a follow-up PR per ticket, branched off `main` after this branch lands.
4. The blueprint will get refined based on what M1 surfaces — that's expected. Treat this document as living.

Questions: open an issue, or comment on the PR.
