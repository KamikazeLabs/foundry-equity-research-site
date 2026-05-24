# Gate 18 — Disclosure footprint

**Phase:** pre-publish
**Type:** deterministic
**Owner:** automation
**Required by shape:** all

## Purpose

Every material assumption made in the body of the paper must be enumerated in a single appendix section ("Assumptions"). The gate prevents *body-only* assumptions — assumptions that sit in body text and are easy to miss on a re-read.

## Pass condition

1. The paper has an `Assumptions` appendix section.
2. Every line in the body matching the assumption regex (`assume`, `we assume`, `assuming`, `if X holds`, `provided that`, etc., plus the LLM extractor's structured detection) has a corresponding entry in the appendix.
3. Conversely, every appendix `Assumptions` entry is referenced from the body (no inventing assumptions only in the appendix).

## Inputs

- `paper.md`
- `appendix.md`

## Outputs

```yaml
passed: bool
findings:
  - severity: error
    code: BODY_ONLY_ASSUMPTION | APPENDIX_ONLY_ASSUMPTION | DUPLICATE_ASSUMPTION
    message: "..."
    location: "..."
evidence:
  body_assumptions_count: int
  appendix_assumptions_count: int
  matched: int
```

## Failure modes the gate catches

- A claim in the body predicated on an assumption the paper never explicitly states.
- An assumption in the appendix that the body never relies on (dead disclosure).
- Duplicate assumptions (same content, two appendix rows).

## Failure modes the gate does NOT catch

- A *false* assumption. The gate checks structure, not truth. The debate and the reviewers handle truth.

## Cross-references

- Constitution §III.6 (argument graph) — every assumption is a leaf node.
- Gate 13 (argument-graph) — assumptions appear in the extracted graph.
