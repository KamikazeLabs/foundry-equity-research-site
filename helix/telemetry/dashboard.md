# `helix/telemetry/` — measure the pipeline that measures the papers

Per the constitution §VI.14, the pipeline measures itself. This document specifies the dashboard the desk lead reviews each Friday alongside the ledger refresh.

## Per-paper telemetry

Captured into `helix/telemetry/runs/<paper_id>.yaml` at publish time. Schema:

```yaml
paper_id: "FER-2026-Q2-XYZ"
published_at: "2026-04-08T14:00:00Z"
shape: "quality-compounder"
constitution_sha: "..."

gate_results:
  01-number-tie: {passed: true, duration_ms: 4200, findings: 0}
  02-citation-resolver: {passed: true, ...}
  # ... all 20

argument_graph:
  node_count: 47
  edge_count: 78
  citation_count: 18
  assumption_count: 5
  min_path_length_to_conclusion: 2
  max_path_length_to_conclusion: 6

reviewer_panel:
  forensics:  {verdict: "pass", confidence: 0.91, findings: 0, model_family: "A"}
  industry:   {verdict: "concerns", confidence: 0.64, findings: 2, model_family: "B"}
  macro:      {verdict: "pass", confidence: 0.88, findings: 1, model_family: "A"}
  disagreement_pairs: 1   # industry vs forensics
  disjoint_priors_satisfied: true

debate:
  turns: 6
  bull_score: {factual: 26, responsive: 24, logical: 25, total: 75}
  bear_score: {factual: 22, responsive: 21, logical: 23, total: 66}
  external_citations_by_bear: 3
  external_citations_verified: 3
  judge_verdict: "bull"
  judge_margin: 0.62

counter_construction:
  candidates_generated: 7
  strongest_counter_strength: "weak"
  recommendation: "ship_with_appendix"
  search_space_summary: "Examined 5yr historical compounder positions in IT services, 6 macro analogs..."

funsearch:
  enabled: true
  cycles: 4
  candidates_evaluated: 78
  selected_was_top_T: true
  selected_was_analyst_first_instinct: false

prm:
  enabled: false  # M3 not complete yet
  min_edge_score: null
  edges_below_threshold: null

desk_lead_signoff:
  mechanical: true
  override_documented: null
  signoff_at: "..."

publish_outputs:
  paper_pdf_sha: "..."
  appendix_disagreement_matrix_present: true
  appendix_debate_transcript_present: true
  appendix_counter_attempt_present: true
```

## Cross-paper dashboard (refreshes every Friday)

### Throughput

- Papers shipped this quarter / target (4)
- Papers held in pre-publish (by which gate)
- Median time from `draft_complete` to `publish`

### Quality (proxy)

- % of papers where reviewer disagreement was non-zero (target ≥ 30%)
- % of debates the Judge ruled `bull` / `bear` / `inconclusive`
- % of papers where counter-construction recommended `kill` (target > 0% across a quarter — meaning the adversary is doing its job)

### FunSearch performance

- % of published papers that originated from a FunSearch candidate vs. analyst's first instinct
- Median fitness of candidates that became papers
- Mode-collapse incidents (forced diversity batches)

### PRM performance (once M3 lands)

- Calibration: PRM publish-time edge score vs. realized outcome on closed positions
- Coverage: % of historical papers with at least 60% of edges labeled

### Gate correlation

A table updated quarterly from post-mortems:

| Gate | Pass score correlation with realized outcome | Notes |
|------|---------------------------------------------|-------|
| 01-number-tie | n/a (always passes) | Catches noise; not predictive |
| 13-argument-graph | min-edge-score vs. return | Hypothesis: positive |
| 14-counter-thesis | strength-of-counter vs. inverse return | Hypothesis: positive |
| 15-base-rate | z-score vs. inverse return | Hypothesis: positive for outliers |
| ... | ... | ... |

This table is the meta-learning loop. Gates with low correlation should either be retuned, dropped, or have their thresholds revisited.

## Why publish telemetry?

Constitution §VI.14 says telemetry is auditable on request. The argument for publishing some of it:

- **Trust differentiator.** No competing desk publishes its gate-fail rates.
- **Honest selection.** Readers can see the desk holds papers, not just ships them.
- **Pre-commitment device.** Once published, the desk cannot quietly relax its own gates.

What to publish (proposed) on the public site:
- Quarterly aggregate gate-fail rate
- % of papers held in pre-publish
- % of debates where Judge ruled bear (paper rewritten)
- Reviewer disagreement rate (without specific reviewer findings)

What to keep internal:
- Per-paper telemetry runs
- Reviewer model-family choices
- PRM internals
