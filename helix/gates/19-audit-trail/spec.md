# Gate 19 — Audit trail completeness

**Phase:** pre-publish
**Type:** deterministic
**Owner:** automation
**Required by shape:** all

## Purpose

Every figure (chart, table cell, body number) traces back to `(source, transformation, timestamp)`. This is the constitution's §II.4 made mechanical, and is a strict superset of the existing number-tie gate (which only checks "did the cell come from a source row" — not "was the transformation reproducible").

## Pass condition

For every figure in the paper:

1. Source row exists in the appendix.
2. The transformation from source row to figure is either:
   - the identity (figure equals source row value), or
   - an explicit computation step in a `transformations.yaml` artifact, expressed in a constrained DSL (`sum`, `multiply`, `divide`, `growth_rate`, `cagr`, `weighted_avg`, etc.).
3. The transformation re-runs deterministically from the source row to the published figure. The gate executes the DSL and compares.
4. The source row has a `retrieved_at` timestamp.

## Inputs

- `paper.md`
- `appendix.md`
- `transformations.yaml`

## Outputs

```yaml
passed: bool
findings:
  - severity: error
    code: NO_SOURCE | NO_TRANSFORMATION | RECOMPUTE_MISMATCH | NO_TIMESTAMP
    figure_id: "fig_2_segment_revenue"
    expected: 1234.56
    actual: 1280.10
    message: "..."
```

## Failure modes the gate catches

- A figure with no source row (already caught by gate 1, but checked again here for safety).
- A figure derived by a transformation that isn't documented.
- A figure whose transformation does not reproduce when re-run.
- A source row without a `retrieved_at` timestamp.

## Failure modes the gate does NOT catch

- A figure whose underlying *source data* is wrong. The citation resolver (gate 2) is responsible for source validity.

## Transformations DSL

A small, pure subset of operations expressible in YAML:

```yaml
fig_2_segment_revenue:
  source: row_seg_rev_fy25  # appendix row id
  steps:
    - op: identity

fig_3_organic_growth:
  source: [row_seg_rev_fy25, row_seg_rev_fy24]
  steps:
    - op: growth_rate
      args: { current: row_seg_rev_fy25, prior: row_seg_rev_fy24 }

fig_4_eps_normalized:
  source: [row_gaap_eps, row_one_time_items]
  steps:
    - op: subtract
      args: { from: row_gaap_eps, value: row_one_time_items }
    - op: divide
      args: { by: row_share_count_diluted }
```

The DSL is intentionally constrained so the gate can re-execute every transformation deterministically. New ops require a desk-lead approval and addition to the DSL spec.
