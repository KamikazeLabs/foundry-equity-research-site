# Gate 15 — Base-rate sanity

**Phase:** pre-publish
**Type:** hybrid (extractor LLM + deterministic check against a base-rate library)
**Owner:** automation; quant reviewer approves any overrides
**Required by shape:** all

## Purpose

Every forward-looking quantitative claim should be annotated with its historical base rate. A 35% three-year revenue CAGR sounds reasonable until you check that fewer than 8% of comparably-sized issuers in this sector have achieved it. The gate forces the paper to either (a) sit within the base-rate distribution or (b) explain explicitly why the issuer is an outlier.

## Pass condition

For every forward quantitative claim in the paper (growth rate, margin expansion, multiple re-rating, leverage delta, capex intensity):

1. The claim is extracted into a structured form (`metric`, `value`, `horizon`, `sector_anchor`).
2. The base-rate library returns a historical distribution for the same `(metric, sector_anchor, horizon)`.
3. Either:
   a. The claim is within 2σ of the historical median, OR
   b. The paper contains an explicit paragraph justifying the outlier with named differentiating factors.

## Inputs

- `paper.md`
- The forecast extraction (produced by the `forecast-extractor` agent)
- The base-rate library (`research/base-rates/` or external service)

## Outputs

```yaml
passed: bool
findings:
  - severity: error | warn
    code: OUTLIER_UNADDRESSED | NO_BASE_RATE | OTHER
    metric: "revenue_cagr_3y"
    paper_value: 0.35
    base_rate_median: 0.12
    base_rate_p90: 0.24
    z_score: 3.2
    message: "Paper forecasts a value above the 99th percentile of historical comps; the paper does not document why this issuer is the outlier."
evidence:
  forecasts_checked: int
  outliers_flagged: int
  outliers_addressed: int
```

## Failure modes the gate catches

- A growth-rate claim above the 95th percentile of historical comps without explanation.
- A margin-expansion claim that has never been achieved at the issuer's scale in the sector.
- A multiple re-rating claim ignoring the historical distribution of re-ratings in the sector.

## Failure modes the gate does NOT catch

- A claim that is *within* the base rate but still wrong for this specific issuer.
- A claim whose `sector_anchor` is misclassified (the gate trusts the extractor's mapping).

## Base-rate library

`research/base-rates/` (to be populated). One YAML file per `(metric, sector_anchor)` tuple:

```yaml
metric: revenue_cagr_3y
sector_anchor: software_application
sample_size: 412
period: 2010-2025
distribution:
  median: 0.12
  p25: 0.06
  p75: 0.22
  p90: 0.31
  p95: 0.38
  p99: 0.51
source: "Compustat North America, screened for $500M-$10B market cap at period start"
last_refreshed: 2026-Q1
```

The library refreshes annually. Source rows are cited per the constitution §II.3.
