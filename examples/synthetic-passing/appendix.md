# Appendix — PRISM Diagnostics (FER-SYN-2026-Q2-PRSM)

## Source rows

| id | retrieved_at | source | reference | value |
|----|--------------|--------|-----------|-------|
| `row_revenue_fy25` | 2026-04-22 | PRSM FY25 10-K | Item 7, p.51 | $1,592.4M |
| `row_revenue_fy24` | 2026-04-22 | PRSM FY24 10-K | Item 7, p.48 | $1,448.3M |
| `row_consumables_fy25` | 2026-04-22 | PRSM FY25 10-K | Item 7, p.52 (segment) | $759.8M |
| `row_installed_base_fy25` | 2026-04-22 | PRSM FY25 Investor Day deck | Slide 14 | 18,213 platforms |
| `row_installed_base_fy24` | 2026-04-22 | PRSM FY24 10-K | Item 7, p.47 | 16,287 platforms |
| `row_consumables_per_platform_fy25` | 2026-04-22 | Computed from rows above | $759.8M / 18,213 | $41.7K |
| `row_gm_fy25` | 2026-04-22 | PRSM FY25 10-K | Item 7, p.53 | 68.9% |
| `row_gm_consumables` | 2026-04-22 | PRSM FY25 10-K | Item 7, p.53 (segment) | 88.0% |
| `row_roic_5yr` | 2026-04-22 | Compustat, computed | NOPAT / Invested Capital, FY20-FY25 | 25.3% mean |
| `row_peer_roic` | 2026-04-22 | Capital IQ peer screen | Diagnostic platforms, FY20-FY25 | Top decile threshold: 21.0% |
| `row_peer_multiples` | 2026-04-22 | FactSet | Diagnostic platforms NTM P/E, current | Median 26x, range 23-30x |
| `row_retirement_rate` | 2026-04-22 | PRSM FY25 10-K | Item 7, p.49 | 1.8% annual |
| `row_displacement_rate` | 2026-04-25 | Channel checks, 7 reference labs | Notes filed 2026-04-25 | <1% of platforms FY20-FY25 |
| `row_q2_guidance` | 2026-04-30 | PRSM Q3 FY26 earnings call | Transcript p.6 | 4,000 cumulative placements by FY28 |
| `row_assays_approved` | 2026-04-22 | FDA approval database | PRSM filings 2020-2025 | 47 new assays |
| `row_capex_fy26_fy28` | 2026-04-22 | PRSM Q1 FY26 earnings call | Transcript p.9 | ~$340M cumulative |
| `row_shares_diluted_fy25` | 2026-04-22 | PRSM FY25 10-K | Item 8, p.74 | 86.1M |
| `row_top10` | 2026-04-22 | PRSM FY25 10-K | Item 1A, p.21 | 22% of revenue |
| `row_decel_fy20_fy22` | 2026-04-25 | Historical consumables-per-platform trajectory | Internal computation | 0.4pp YoY decel observed |

## Assumptions

| id | text | body reference |
|----|------|----------------|
| `a_q2_uptake_base` | Quantum-2 placements reach 3,500 by FY28 (87.5% of management's 4,000 guidance) | Growth runway |
| `a_menu_expansion_persist` | Menu expansion contributes ~3.5% to per-platform consumables CAGR through FY28 | Economic engine |
| `a_margin_durability` | Gross margin sustains within 100bp of FY25 (68.9%) absent the Quantum-2 mix lift | Financial model |
| `a_no_payer_shock` | No discrete payer reimbursement shock in the molecular diagnostics segment through FY28 | Risks and counters |
