# Disagreement matrix — ACME Industries

**Paper:** FER-SYN-2026-Q2-ACME
**Pre-publish reviewer panel (M1 disjoint-priors)**

Constitution §III.8 requires this artifact to be published with the paper.

## Reviewer outputs

### `reviewer-forensics`

- **Verdict:** pass
- **Confidence:** 0.86
- **Model family:** A
- **Findings:**
  - severity: warn, code: `WC_GAMING`
    - Working capital noise FY25: DSO declined 4 days FY24→FY25 contributing ~$22M to FCF. Not material at ACME's $1.34B revenue, but flagged for awareness. Paper does not depend on FCF conversion for the thesis, so this does not block.

### `reviewer-industry`

- **Verdict:** pass
- **Confidence:** 0.78
- **Model family:** B
- **Findings:**
  - severity: warn, code: `CUSTOMER_CONCENTRATION`
    - MajorOEM Inc 10-K FY25 Item 7 discloses $58M spend with ACME (4.3% of revenue), marginally above the paper's "no customer over 4%" framing. Paper should clarify whether MajorOEM's spend includes affiliates.

### `reviewer-macro`

- **Verdict:** concerns
- **Confidence:** 0.71
- **Model family:** A
- **Findings:**
  - severity: warn, code: `REFI_RISK`
    - $180M of 3.25% coupon debt matures FY27. Paper assumes refi at +75bp; equivalent-rated 5yr issuance today prices at +130bp. Refi at market adds ~$1.4M annual interest expense, reducing FY28 EPS by ~$0.15. Paper does not disclose this sensitivity.

## Pairwise disagreement

| | forensics | industry | macro |
|--|--|--|--|
| **forensics** | — | concur | disagree (verdict gap) |
| **industry** | concur | — | disagree (verdict gap) |
| **macro** | disagree | disagree | — |

**Disagreement count:** 1 (forensics + industry vs. macro)
**Disjoint-priors satisfied:** yes (model family A used by forensics + macro; B by industry; ≥1 family delta present)

## How disagreement is resolved

Per constitution §III.8: disagreement is published, not hidden. The macro reviewer's `REFI_RISK` finding is incorporated into the appendix as a sensitivity row. Paper proceeds *if* the body or appendix discloses the refi sensitivity. The current draft does not — this is an additional pre-publish requirement on top of the debate outcome.

## Cross-check vs. debate

The reviewer panel surfaced refi risk; the Bear in the debate did not raise refi (focused on conversion and multiple). The counter-construction agent surfaced conversion risk; the debate Bear corroborated. None of the three independent processes surfaced multiple compression as a primary risk, but the debate did expose it under Bear's escalation. The three processes are partially complementary, partially overlapping — exactly what disjoint-priors is designed to produce.
