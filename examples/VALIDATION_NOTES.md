# Validation notes from the worked example

Building the synthetic ACME paper bundle and running it through the schemas surfaced the following spec gaps. Each is a real ambiguity a Forge engineer would hit on day one.

The example itself is in `synthetic-quality-compounder/`. Gate 13 passes on the extracted graph (verified by re-running `helix/gates/13-argument-graph/check.py`).

## A. Spec gaps to fix in the M0–M4 deliverables

### A.1 The argument-graph extractor's body coverage is unspecified

**Problem:** during the debate, the Bull cited "88–92% conversion rate in industrial-automation work" — a figure not in the paper body and not in the appendix. The argument-graph extractor only operates on the paper *body*, so the figure is invisible to gate 13. The constitution gate (§II.3) caught it via the Judge's review, but the argument-graph gate should have caught it directly.

**Fix:** the extractor's spec (`helix/gates/13-argument-graph/extractor_prompt.md`) should explicitly include the debate transcript and the counter-attempt as additional input documents, with all extracted claims joined into a single graph. This means a quantitative claim that lives only in a debate turn must also have a source row, or it fails gate 13.

**Severity:** material. Without this fix, the debate becomes a place where unsourced claims can survive.

### A.2 Kill-switch scope is under-specified

**Problem:** ACME's published kill switch covers EV revenue growth and gross margin. The debate exposed multiple-compression risk that is also a thesis-breaking variable. The constitution (§II.5) requires forecasts to have a quantitative kill switch but does not require the kill switch to cover *all* load-bearing variables.

**Fix:** update `HELIX_CONSTITUTION.md` §II.5 to read: "Every forecast discloses its kill switch — a quantitative condition that, if met, invalidates the thesis. The kill switch must cover every load-bearing variable identified in the argument graph as having more than one inbound edge to the conclusion." Add a deterministic check inside gate 20 that cross-references the argument-graph's heavy nodes against the kill-switch section.

**Severity:** material. This is the single most actionable change surfaced.

### A.3 Transformation DSL op `irr_simple` is not in the spec

**Problem:** `transformations.yaml` for the example uses `irr_simple` to compute the 3-year IRR from start / end price. The gate 19 spec lists ops `sum, multiply, divide, growth_rate, cagr, weighted_avg` but not IRR.

**Fix:** extend the DSL in `helix/gates/19-audit-trail/spec.md` to include: `irr_simple` (no cash flows in between), `irr` (with explicit cash flow schedule), `npv`, `multiple_apply` (price = EPS × multiple). Add unit tests to a future `gates/19-audit-trail/check.py`.

**Severity:** moderate. Easy to fix; will recur immediately for any DCF-based thesis.

### A.4 Reviewer panel — what is "model family"?

**Problem:** the disjoint-priors requirement says "at least one of the three reviewers must run on a different model family than the other two." But "model family" is not defined. Are Opus and Sonnet the same family? Are GPT-5 and o4 the same family?

**Fix:** add a definition to `helix/agents/README.md`. Proposed: a "model family" is a published base-model lineage (e.g., Claude 4, GPT-5, Gemini 3). Different sizes within a family count as the *same* family. Different fine-tunes count as the same family. Genuinely different *families* are required for disjointness.

**Severity:** moderate. Without this, "disjoint priors" is decorative.

### A.5 Counter-construction agent — what counts as "at least 5 distinct candidates"?

**Problem:** the counter-construction spec requires `all_attempts` ≥ 5. In the synthetic example, we had 6 candidates, but one (refi/macro) was a passthrough from the macro reviewer rather than a fresh discovery. Does that count?

**Fix:** add a `provenance` field to each candidate in `all_attempts`: `fresh` (discovered by counter-construction), `delegated` (passthrough from a reviewer, not counted toward the minimum), `ledger` (from the ledger-query agent). The minimum 5 applies to `fresh` and `ledger` only.

**Severity:** moderate. Without this, the minimum-5 requirement is gameable.

### A.6 The argument graph has no place for "the load-bearing edge"

**Problem:** gate 13 catches structural issues (orphans, cycles, dangling edges) but does not surface *which* edges are load-bearing. The Judge in the debate identified two load-bearing nodes (`claim_ev_revenue_500_650m` and `claim_rerate_22x`) that broke under Bear's pressure. The graph doesn't distinguish these from incidental claims.

**Fix:** add an optional `weight` field on edges (0.0–1.0). Edges to the conclusion with weight ≥ a threshold are "load-bearing." Extend gate 13 to validate that every load-bearing edge has ≥ 2 inbound nodes of `kind: citation` (i.e., is multiply sourced). Defer to M3: the PRM's edge scores can populate `weight` automatically once trained.

**Severity:** moderate. Without weights, gate 13 is structurally sound but blind to materiality.

### A.7 Disagreement matrix format is unspecified

**Problem:** the constitution §III.8 requires publishing the disagreement matrix. We built one (in `appendix.md` and a separate `disagreement_matrix.md`). The format is plausible but not defined anywhere as a schema. Different Forge engineers will produce different formats.

**Fix:** add `helix/agents/reviewer-forensics/spec.md` (and the other two reviewers) a section "Output schema" that includes the matrix row format. Or define a standalone schema file at `helix/disagreement_matrix_schema.md`.

**Severity:** low. Cosmetic but unifies the published artifact.

### A.8 Telemetry schema includes counters that aren't yet populated

**Problem:** the example `telemetry.yaml` has `funsearch` and `prm` sections set to null because those milestones haven't shipped. That's fine, but the schema doesn't distinguish "milestone not enabled" from "milestone failed."

**Fix:** add a `milestones_enabled` block at the top of the telemetry schema:

```yaml
milestones_enabled:
  M0: true
  M1: true
  M2: true
  M3: false
  M4: false
```

Then `null` values inside sections are *expected* when the enclosing milestone is disabled.

**Severity:** low.

## B. What worked well

- **Gate 13 catches the structural issues it claims to.** The synthetic graph passes; deliberate breakage (tested in `test_check.py`) fails predictably.
- **The shape system is genuinely useful.** The quality-compounder shape made the section list, gate set, and reviewer panel a per-paper choice without overhead.
- **The Judge spec produces a publishable rationale.** The `judge_verdict.yaml` for this example is the kind of artifact an institutional reader can read and audit.
- **Counter-construction + debate are partially complementary.** Both surfaced the conversion-rate risk independently. That convergence is the unit-distance proof's "independent paths" principle made operational.

## C. What this example doesn't cover (yet)

- A paper that passes all 20 gates and ships. The synthetic example was tuned so the Bear wins, which exercises the failure path. A `synthetic-passing/` example should follow.
- A short thesis (`mean-reversion-short` shape). The asymmetric-risk debate (8 turns vs. 6) and forensics-priority routing aren't exercised here.
- A FunSearch-originated thesis (M3). Once M3 lands, an example bundle with non-trivial `funsearch` telemetry would test that pipeline.
- The PRM (M3). No edge scoring in this example.
- The post-mortem pipeline. Once a position closes, the example bundle should be replayed against the `post-mortem.yaml` pipeline to surface schema gaps in PRM data formatting.

## D. Suggested next deliverables

1. Apply the A.1–A.8 fixes back into the spec docs. (Small edits, mostly clarifications.)
2. Build a `synthetic-passing/` companion example where Bear loses and the paper ships.
3. Build a `synthetic-short/` example exercising the `mean-reversion-short` shape.
4. Wire gate 13 into a CI hook so every committed example graph is verified automatically.
