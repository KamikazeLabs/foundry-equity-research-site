# Disagreement matrix — schema

Canonical schema for the disagreement-matrix artifact required by Constitution §III.8 and consumed by Gate 20.

## Files

- `appendix/disagreement_matrix.yaml` — machine-readable form. Required.
- `appendix/disagreement_matrix.md` — human-readable render of the YAML. Required for the published paper bundle; auto-generated from the YAML.

(Synthetic example bundles may include only the markdown for brevity; production bundles must include both.)

## YAML schema

```yaml
paper_id: "..."
generated_at: ISO-8601
reviewer_panel:
  - slug: "reviewer-forensics"
    verdict: "pass" | "concerns" | "block"
    confidence: 0.0 - 1.0
    model_family: "Claude 4.X" | "GPT-5.X" | "Gemini 3.X" | ...
    finding_count: int
    findings:
      - severity: "error" | "warn"
        code: "..."
        message: "..."
        paper_section: "..."
        evidence: ["..."]
  - slug: "reviewer-industry"
    # ... same shape
  - slug: "reviewer-macro"
    # ... same shape
pairwise:
  - {a: "reviewer-forensics", b: "reviewer-industry", agreement: "concur" | "disagree"}
  - {a: "reviewer-forensics", b: "reviewer-macro",    agreement: "concur" | "disagree"}
  - {a: "reviewer-industry",  b: "reviewer-macro",    agreement: "concur" | "disagree"}
disagreement_count: int
disjoint_priors_satisfied: bool
distinct_families_count: int        # must be >= 2 for satisfied=true
resolution:
  notes: "free text"
  additional_requirements_on_paper: ["..."]
```

## Definition: "agreement"

Two reviewers *concur* if their verdicts are within one level:

| | pass | concerns | block |
|-|-|-|-|
| **pass** | concur | concur | disagree |
| **concerns** | concur | concur | disagree |
| **block** | disagree | disagree | concur |

## Constraints (checked by gate 20)

- Exactly 3 reviewer entries: `reviewer-forensics`, `reviewer-industry`, `reviewer-macro`.
- Exactly 3 pairwise entries (covers all 3-choose-2 pairs).
- `disjoint_priors_satisfied` must be `true`. If `false`, the panel is misconfigured and gate 20 fails.
- `distinct_families_count` must be ≥ 2. (See `helix/agents/README.md` for the definition of "model family.")
- If any reviewer has verdict `block`, paper does not ship regardless of others.
- If any reviewer has verdict `concerns`, `resolution.notes` must be non-empty.

## Markdown render

The markdown form contains:

1. A "Reviewer outputs" section with one subsection per reviewer.
2. A "Pairwise disagreement" 3×3 table.
3. A "How disagreement is resolved" section.
4. A "Cross-check vs. debate" section noting which findings overlap with what the debate Bear surfaced or what the counter-construction flagged.

## Consumed by

- **Gate 20 (constitution):** §III.8 publication check, §IV.9 disjoint-priors check.
- **debate-judge:** the matrix is one input to the Judge's constitutional check.
- **Desk lead:** published with the paper as an appendix item, visible to institutional readers.
