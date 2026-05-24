# Appendix — GLITZ Apparel (FER-SYN-2026-Q2-GLTZ)

## Source rows

| id | retrieved_at | source | reference | value |
|----|--------------|--------|-----------|-------|
| `row_revenue_fy25` | 2026-04-29 | GLTZ FY25 10-K | Item 7, p.38 | $1,597.4M |
| `row_revenue_fy24` | 2026-04-29 | GLTZ FY24 10-K | Item 7, p.36 | $1,412.6M |
| `row_eps_fy25_gaap` | 2026-04-29 | GLTZ FY25 10-K | Item 8, p.52 | $2.78 |
| `row_eps_fy26e_consensus` | 2026-05-01 | FactSet consensus, 14 analysts | as of 2026-05-01 | $3.00 |
| `row_inventory_days_q1fy24` | 2026-04-29 | GLTZ FY24 Q1 10-Q | Item 1, p.18 | 88 |
| `row_inventory_days_q1fy26` | 2026-04-29 | GLTZ FY26 Q1 10-Q | Item 1, p.21 | 142 |
| `row_sss_q3fy25` | 2026-04-29 | GLTZ FY25 Q3 earnings call | Transcript p.4 | -2.8% |
| `row_sss_q4fy25` | 2026-04-29 | GLTZ FY25 Q4 earnings call | Transcript p.4 | -3.1% |
| `row_sss_q1fy26` | 2026-04-29 | GLTZ FY26 Q1 earnings call | Transcript p.4 | -3.4% |
| `row_customer_demo_fy23` | 2026-04-29 | GLTZ FY23 Investor Day | Slide 22 | 48% under-25 |
| `row_customer_demo_fy26` | 2026-04-29 | GLTZ FY26 Q1 Investor Update | Slide 11 | 32% under-25 |
| `row_offprice_disclosure` | 2026-04-29 | GLTZ FY25 10-K | Item 1 (channels), Item 7 (segment) | ~7% of revenue (computed) |
| `row_peer_multiples` | 2026-04-29 | FactSet | Luxury/accessories peer screen | Median 18x range 15-22x |
| `row_peer_growth_match` | 2026-04-29 | Capital IQ | Peers matched on rev growth 8-12% + op margin 18-22% | Implied multiple 17-19x |
| `row_adv` | 2026-04-29 | NYSE | Trailing 20-day ADV USD | $86M / day |
| `row_borrow` | 2026-04-29 | Prime broker | Shares available to borrow | 8.3M |
| `row_borrow_rate` | 2026-04-29 | Prime broker | Borrow rate, annualized | 3.2% |
| `row_short_interest` | 2026-04-29 | Bloomberg | Short interest as % of float | 12% |

## Assumptions

| id | text | body reference |
|----|------|----------------|
| `a_consensus_revisions_lag` | Consensus EPS revisions lag actual run-rate deterioration by ~2 quarters | Thesis, Catalyst path |
| `a_multiple_compresses_to_peer_median` | Multiple compresses from 28x to peer median 18x once deterioration is visible to consensus | Thesis |
| `a_offprice_recognition` | Off-price channel placement is recognized at full wholesale rather than at off-price net realization | What we think is true |
| `a_no_takeout_squeeze` | No take-private bid materializes inside the 18-month horizon at a premium > 15% to entry | Risks and counters |
