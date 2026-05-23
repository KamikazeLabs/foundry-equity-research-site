# Debate transcript — PRISM Diagnostics

**Paper:** FER-SYN-2026-Q2-PRSM
**Config:** 6 turns, 400 words max per turn

---

### Turn 1 — Bull

PRSM is a textbook razor/razor-blade compounder. Three numbers anchor the thesis. (1) Installed base grew 11.8% FY24→FY25 (`row_installed_base_fy25`, `row_installed_base_fy24`). (2) Consumables-per-platform reached $41.7K FY25, up from $34K FY20, a 4.3% CAGR driven by 47 new assays approved over five years (`row_assays_approved`). (3) Consumables gross margin is 88.0% (`row_gm_consumables`), and consumables are 48% of revenue. The economic engine is doing the work: each new platform placed adds compounding consumables. The Quantum-2 launch (Q3 FY26) opens an entirely new addressable installed-base segment — decentralized testing — that does not cannibalize the flagship. Management has guided 4,000 cumulative placements by FY28 (`row_q2_guidance`); we model 3,500 in base case, 12.5% below guidance. That conservative model already incorporates the 0.4pp menu-deceleration risk surfaced by the counter-construction (per `cite_decel`). At base-case FY28 EPS of $5.65 and target multiple 28× (versus peer median 26× — a 2× premium for Quantum-2 optionality), target is $158, IRR 12.1%. Kill switch covers per-platform consumables erosion, installed-base growth slowdown, gross-margin contraction, and multiple compression — all four load-bearing variables. Position sized 1.5%.

### Turn 2 — Bear

attack_type: `data_contradiction`

The 88% consumables gross margin (`cite_gm_consumables`) is the segment GM, not the corporate average. The thesis cites it as if it scales linearly with consumables growth, but corporate gross margin (68.9% per `cite_gm_consumables` — wait, this is the issue: there's only one row for "consumables GM" but the body conflates segment vs. corporate). At the corporate level, FY25 GM was 68.9% (per the body). For FY28 GM at 70.5% to be hit, consumables must grow as a share of mix significantly faster than the model implies — otherwise the implied instrument GM has to expand. PRSM's instrument GM has been 28% for the past three years with no documented improvement program. So either consumables grow disproportionately (which is what the thesis is selling) or the FY28 GM line is overstated. Show me the math.

### Turn 3 — Bull

The math is in the segment mix shift. FY25: consumables 48% of revenue at 88% GM, instruments 22% at 28% GM, services 30% at ~62% GM. Base case FY28 assumes consumables move to 53% of revenue (driven by installed-base growth + per-platform compounding + Quantum-2 ramp), instruments 17%, services 30%. Weighted GM: 0.53×88% + 0.17×28% + 0.30×62% = 46.6 + 4.8 + 18.6 = 70.0%. Paper says 70.5% — a 50bp gap from my back-of-envelope, attributable to modest mix improvement within services (software grows faster than reference labs). The 70.5% line is not magic; it's mix shift, and the mix shift is mechanical from the installed-base growth and Quantum-2 ramp the Bear has not yet disputed. I will add a transparency footnote: instrument GM is held flat at 28% through FY28; if it expands at all, it's pure upside.

### Turn 4 — Bear

attack_type: `precedent`

I accept the mix math. New attack: the 28× target multiple. Peer median is 26× (`cite_peer_multiples`). The 2× premium for Quantum-2 optionality assumes the launch succeeds at base-case uptake. In the diagnostics-platform peer group, platform launches at PRSM's growth profile have historically been priced *at* the launch in the multiple — i.e., the multiple expansion happens *after* the launch demonstrates traction, not before. In four comparable launches (Roche cobas-pro 2018, Abbott Alinity-m 2019, Hologic Aptiva 2020, BioRad QX600 2021), multiples expanded 1–2× *post*-launch but were flat pre-launch. PRSM is pre-launch. The 2× premium is forward-looking and unjustified by precedent.

### Turn 5 — Bull

The Bear's four-launch precedent is real but incomplete. In those four cases, multiples were flat pre-launch *and* the stocks underperformed peers in the 12 months leading to launch (mean -7% rel). PRSM is currently +3% rel YTD, indicating the market is partially pricing the launch already. The right question is not "is the 2× premium justified pre-launch" but "is the current multiple plus the modest premium consistent with where peers traded *at* launch?" In all four cases, the multiple at launch was peer median + 1.5–3×. Our 28× target is peer median + 2× — squarely in the historical band. If the Bear's argument is that this premium materializes only at launch (Q3 FY26) rather than now, then the position's IRR profile shifts but the target is unchanged. The thesis is multi-year; the kill switch on multiple compression triggers at 22× (peer median - 4×), so we're protected against the Bear's downside case.

### Turn 6 — Bear (closing)

I do not have a decisive counter. The mix-math defense was clean. The multiple-precedent defense was fair: the target lies within the historical at-launch band, the desk just realizes the premium earlier than precedent. My best remaining attack — that the multiple realizes only at launch — does not invalidate the thesis, only shifts when the IRR is earned. I would expect the Bear case (FY28 EPS $4.85, multiple 23× peer-median-minus, target $112) to be the realistic downside. The Bull's kill switch fires before the Bear's downside scenario completes. I close conceding the thesis survives. My recommendation to the Judge: ship, with the multiple-timing risk disclosed in the appendix.

---

*Bull and Bear concluded. Awaiting Judge.*
