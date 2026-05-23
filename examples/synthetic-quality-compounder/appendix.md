# Appendix — ACME Industries (FER-SYN-2026-Q2-ACME)

## Source rows

Each row is named by `id` and referenced from the body and from `transformations.yaml`.

| id | retrieved_at | source | reference | value |
|----|--------------|--------|-----------|-------|
| `row_revenue_fy25` | 2026-04-22 | ACME FY25 10-K | Item 7, p.42 | $1,340.2M |
| `row_revenue_fy24` | 2026-04-22 | ACME FY24 10-K | Item 7, p.39 | $1,189.6M |
| `row_revenue_fy23` | 2026-04-22 | ACME FY23 10-K | Item 7, p.38 | $1,054.8M |
| `row_gm_fy25` | 2026-04-22 | ACME FY25 10-K | Item 7, p.43 | 37.1% |
| `row_gm_fy24` | 2026-04-22 | ACME FY24 10-K | Item 7, p.40 | 36.4% |
| `row_opm_fy25` | 2026-04-22 | ACME FY25 10-K | Item 7, p.43 | 19.8% |
| `row_roic_5yr` | 2026-04-22 | Compustat, computed | NOPAT / Invested Capital, FY20-FY25 | 24.1% mean |
| `row_peer_roic` | 2026-04-22 | Capital IQ peer screen | Industrial Components, FY20-FY25 | Top decile threshold: 21.4% |
| `row_ev_tam_2028` | 2026-04-23 | IHS Markit / EV power-electronics outlook | Q1 2026 report p.18 | $4.2B |
| `row_ev_tam_2025` | 2026-04-23 | IHS Markit / EV power-electronics outlook | Q1 2026 report p.18 | $1.9B |
| `row_ev_platforms_qualified` | 2026-04-15 | Channel check, 3 EV platform suppliers | Notes filed 2026-04-15 | 3 of top 5 |
| `row_channel_attrition` | 2026-04-29 | Channel check, 9 distributors | Notes filed 2026-04-29 | 0 attrition signals |
| `row_capex_plan_fy26_fy28` | 2026-04-22 | ACME Q1 FY26 earnings call transcript | p.7 | ~$240M cumulative |
| `row_ma_history_fy18_fy25` | 2026-04-23 | ACME 10-K filings, three tuck-ins | various | 3 acquisitions, avg 7x EBITDA |
| `row_shares_diluted_fy25` | 2026-04-22 | ACME FY25 10-K | Item 8, p.61 | 92.4M |
| `row_aerospace_seg_pct` | 2026-04-22 | ACME FY25 10-K | Item 7, p.42 | 15% of revenue |
| `row_top10_concentration` | 2026-04-22 | ACME FY25 10-K | Item 1A, p.18 | 38% of revenue |

## Assumptions

Every assumption is referenced from the body (constitution §III.6).

| id | text | body reference |
|----|------|----------------|
| `a_margin_persist` | Gross margin sustains within 100bp of FY25 (37.1%) through FY28 at constant mix. | "Financial model" section |
| `a_ev_qualified_to_share` | Qualified position with EV platforms converts to 12–15% market share at maturity. | "Growth runway" section |
| `a_capex_self_funded` | Capex plan ($240M FY26–FY28) is fully fundable from operating cash flow. | "Growth runway" section |
| `a_capital_allocation_consistency` | Management continues current capital allocation mix (~62% reinvestment, ~23% M&A, ~15% buybacks). | "Management and capital allocation" |
| `a_no_disruption` | No regulatory or technology disruption invalidates the precision-machining moat through FY28. | "Durability" section |

## Disagreement matrix

(Per constitution §III.8; consumed by the constitution gate.)

| Reviewer | Verdict | Confidence | Findings | Material disagreement with others? |
|----------|---------|-----------|----------|-------------------------------------|
| forensics | pass | 0.86 | 0 errors, 1 warn (working-capital noise FY25) | no |
| industry | pass | 0.78 | 0 errors, 1 warn (top-10 concentration on watchlist) | no |
| macro | concerns | 0.71 | 0 errors, 1 warn (refi risk: $180M maturing FY27, paper assumes refi at +75bp; current market suggests +130bp) | yes, vs forensics + industry |

The macro reviewer's `concerns` verdict is addressed in the appendix: FY28 EPS sensitivity to refi at +130bp is a $0.15 EPS hit, leaving base-case EPS at $5.50 (within model band). Paper proceeds; sensitivity disclosed in body.
