# GLITZ Apparel (GLTZ): The Premium Has Expired

**Foundry Equity Research — Synthetic example (not investment research)**
**Shape:** mean-reversion-short
**Paper ID:** FER-SYN-2026-Q2-GLTZ
**Date:** 2026-05-23

---

## One-page summary

GLTZ trades at 28× FY26E EPS ($84.20 / $3.00) versus a peer median of 18× for similar growth and margin profiles (`row_peer_multiples`). Underneath the multiple, three deteriorating fundamentals are visible: inventory days have expanded from 88 (FY24 Q1) to 142 (FY26 Q1), same-store sales have declined -3% in each of the last three quarters, and the under-25 customer cohort has shrunk from 48% to 32% of revenue over three years (`row_customer_demo`). At the same time, the revenue line shows aggressive off-price channel inventory placement that the company recognizes at full wholesale (`row_offprice_disclosure`). The thesis: the multiple compresses to 16× FY26E EPS as the deterioration becomes visible to consensus by Q3 FY26 results, with a near-term price of $48.

**Entry:** short above $84 (current $84.20).
**Exit:** $48 (16× FY26E EPS of $3.00).
**Kill switch (quantitative):** thesis invalidates if any of:
- inventory days fall below 100 for two consecutive quarters
- same-store sales return to ≥ +2% YoY for two consecutive quarters
- multiple compression stalls above 22× for two consecutive quarters
- off-price channel disclosure changes such that the recognized revenue per unit at off-price equals or exceeds the per-unit recognition reduces below 50% of full-channel recognition

**Horizon:** 18 months. **Expected return (base):** -43% on the stock, ~24% on the short position before borrow cost.

## Thesis

The multiple anchors to a growth + margin profile that no longer exists. As consumer-facing metrics deteriorate visibly through FY26, consensus EPS revisions trail the print by ~2 quarters. Once consensus catches the actual run rate, the multiple compresses to peer median. Catalyst path is Q3 FY26 print (October) and Q4 FY26 holiday season (January 2027 print).

## What the market is pricing

A continuation of FY23–FY24 growth (~14% revenue, ~30% EPS) with margin expansion to ~22%. Implies same-store sales of +5–7%, inventory turns flat or improving, and customer-cohort stability.

## What we think is true

Same-store sales declining -3% (vs Street modeling +6%). Inventory days expanding 60% over six quarters indicating either demand shortfall or aggressive sell-in to channel. Customer demographic shift away from the core under-25 cohort. Reported revenue includes ~$110M of off-price channel placement recognized at full wholesale (~7% of FY25 revenue); on a true accrual basis, FY25 revenue is closer to $1.49B vs. reported $1.60B, and EPS is closer to $2.65 vs. reported $3.00.

## Catalyst path

Q3 FY26 print (3 Oct 2026): expected EPS revision -10% as inventory writedown begins. Holiday print (15 Jan 2027): cohort-driven demand miss compounds the inventory issue; multiple compression accelerates.

## Sizing and borrow

Position size 1.0% of model portfolio. ADV: $86M / day (`row_adv`). At 1.0% size, exit window 4 trading days at 25% participation. Borrow: 8.3M shares available (`row_borrow`), 12% utilization currently; position implies 4.1M shares short, 5.1% of available. Borrow rate: 3.2% annualized (`row_borrow_rate`). Net expected position return: ~24% over 18 months less ~4.8% borrow cost = ~19% net.

## Kill switch

See one-page summary. Four quantitative conditions, each on a load-bearing variable in the argument graph.

## Risks and counters

**R1.** Brand-driven re-acceleration (new product, viral marketing). *Counter:* the kill switch on same-store sales returning to ≥ +2% triggers exit. Recent peer reaccelerations from -3% to +2% have taken 4+ quarters; thesis horizon is 18 months.

**R2.** Activist or PE-led take-private bid. *Counter:* the position is sized 1.0% — half of typical short sizing — partly to absorb take-out risk. EV/EBITDA at base case is 10.5×; a take-private at 13× EBITDA would imply ~$78, modest mark-up from short entry.

**R3.** Short squeeze on cohort sentiment shift. *Counter:* short interest is currently 12% of float and rising; squeeze risk is real. Position size is constrained by borrow availability, not by conviction; the 5.1%-of-available position size leaves meaningful headroom.

## Reflexivity

If the short becomes consensus before Q3 FY26 print, the multiple-compression realizes faster and the IRR improves. Unlike long theses, contrarian consensus on the *same side* of a short trade accelerates the realization rather than compressing it. Concern is the opposite — the long thesis becoming over-consensus and triggering positioning unwinds; we monitor 13F filings for crowding.

## Appendix counter-construction disclosure

A counter-construction was attempted. The strongest counter (off-price disclosure interpretation) was addressed in the appendix: the paper's "$110M off-price at full wholesale" estimate is based on aggregating disclosed channel mix and average pricing; the company has not explicitly confirmed the figure. The paper's central thesis does not depend on this number being exactly $110M — it depends on the *direction* of off-price growth, which is clearly disclosed. See `counter_attempt.md`.

---

*See `appendix.md`, `argument_graph.json`, `counter_attempt.md`, `debate_transcript.md`, `disagreement_matrix.yaml`, `telemetry.yaml`.*
