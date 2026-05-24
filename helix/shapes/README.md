# `helix/shapes/` — per-paper-type templates

A **shape** is a YAML file describing the structural template the Forge applies to a given paper. The shape-selector agent picks one (or proposes a hybrid) per brief.

## Why shapes exist

Invariant 1 of the transformation: *vary what you held fixed*. A single template forces every thesis into the same skeleton, regardless of whether the underlying argument is a multi-year compounder thesis or a 6-week catalyst short. The shape system makes the skeleton a per-paper choice.

## Shape contract

Every shape file declares:

- `name`, `slug`, `description`
- `sections` — ordered list; the paper must contain each section, in order
- `page_budget`, `chart_budget`
- `gates.required` and `gates.optional`
- `reviewer_panel` — which reviewer specialists the brief routes to
- `debate.enabled` and `debate.turns`
- `counter_construction.enabled` and `counter_construction.focus`

## Initial shape library (M0)

- `quality-compounder.yaml` — long thesis on a high-ROIC business with a multi-year reinvestment runway.
- `mean-reversion-short.yaml` — short thesis with a quantitative entry and a mechanical kill switch.
- `special-situation.yaml` — event-driven long or short (spin-off, restructuring, capital return).
- `macro-driven.yaml` — sector or thematic position predicated on a macro variable (rates, FX, commodity).

The list is not closed. Add shapes as the desk encounters thesis types that don't fit cleanly.

## Selecting a shape

The shape-selector agent reads the brief and outputs:

```yaml
shape: quality-compounder
hybrid: false
overrides:
  page_budget: 36          # under default 40
  gates.required+:
    - 17-liquidity          # tickers below $200M ADV
rationale: |
  Multi-year long on a high-ROIC business; standard compounder
  shape with a smaller page budget and liquidity gate enabled.
```

A hybrid is allowed only with explicit `rationale` and desk-lead sign-off.
