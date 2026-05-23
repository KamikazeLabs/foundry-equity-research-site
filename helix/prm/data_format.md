# PRM training data format

One JSON line per step-level training example. Files live in `prm/data/raw/`.

## Schema

```json
{
  "example_id": "FER-2025-Q3-XYZ-step-007",
  "paper_id": "FER-2025-Q3-XYZ",
  "paper_published_at": "2025-09-15T14:00:00Z",
  "step_id": "claim_organic_growth_to_value_creation",
  "step_text": "Core segment grew 18% organic in FY25 -> Equity value compounds at ~15% per annum",
  "step_kind": "claim_to_claim",
  "inbound_evidence": [
    {"node_id": "cite_10k_seg", "kind": "citation", "label": "10-K FY25 p.45"},
    {"node_id": "claim_organic_growth", "kind": "claim"}
  ],
  "label": "incorrect",
  "label_source": "analyst_post_mortem",
  "label_rationale": "Organic growth slowed to 6% in FY26 driven by the channel attrition the paper did not anticipate; the step from segment growth to value creation was the load-bearing inference that broke.",
  "ledger_outcome": {
    "position_id": "POS-2025-XYZ-001",
    "opened_at": "2025-09-22T14:30:00Z",
    "closed_at": "2026-04-18T15:00:00Z",
    "realized_return": -0.18,
    "vs_thesis": "underperformed"
  }
}
```

## Field definitions

- `example_id`: unique across all training examples. Convention: `<paper_id>-step-<sequence>`.
- `paper_id`: links back to the source paper.
- `paper_published_at`: ISO-8601. Used for temporal validation splits.
- `step_id`: matches the edge id in the paper's extracted argument graph.
- `step_text`: human-readable description of the step.
- `step_kind`: one of `citation_to_claim`, `claim_to_claim`, `assumption_to_claim`, `claim_to_conclusion`.
- `inbound_evidence`: array of `{node_id, kind, label}` for every node that feeds this step.
- `label`: one of `correct`, `weak`, `incorrect`, `unknown`.
- `label_source`: one of `outcome` (weakest), `analyst_post_mortem` (strongest), `judge_finding` (medium).
- `label_rationale`: required for any non-`unknown` label.
- `ledger_outcome`: nullable. Present for steps in papers whose positions have closed.

## Label semantics

- `correct`: the step's inference held in retrospect, OR the step was supported by evidence that turned out to be predictive.
- `weak`: the step's inference held but the supporting evidence was sparse / borderline.
- `incorrect`: the step's inference was the load-bearing one that broke; the post-mortem cites this step.
- `unknown`: position is still open and no Judge finding was attached to this step.

## Class weighting (during training)

Per the PRM800K methodology, with adjustments for label-source quality:

- `analyst_post_mortem` labels: weight 1.0
- `judge_finding` labels: weight 0.5
- `outcome` labels: weight 0.2 (weak signal — does not localize)

## Temporal validation

Always hold out the most recent rolling 90 days of papers. The PRM is evaluated on whether its publish-time step scores correlate with outcomes on the held-out set.

## Storage

`prm/data/raw/` is gitignored. Data lives in a private bucket. The schema is the contract.
