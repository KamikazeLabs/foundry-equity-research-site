# Gate 20 — Constitution conformance

**Phase:** pre-publish (last gate)
**Type:** classifier
**Owner:** automation
**Required by shape:** all

## Purpose

The constitution (`/HELIX_CONSTITUTION.md`) is the highest-level rule set. This gate enforces conformance to each numbered provision mechanically — to the extent each provision can be mechanically checked. Provisions that cannot be checked deterministically defer to the Judge.

## Pass condition

For each provision in the constitution, one of:
- A deterministic check passes (e.g., §II.5 kill-switch is present in `kill-switch` section).
- The Judge has explicitly affirmed conformance in the debate output (e.g., §III.7 counter-construction was published).
- The provision is **classifier-judged** and the classifier returns `compliant` with confidence ≥ 0.85.

The gate fails on any provision marked `non-compliant`.

## Provision -> check mapping

| § | Provision summary | Check |
|---|------------------|-------|
| I.1 | Addressability | URL exists; no soft-404 |
| I.2 | Errata as new versions | If errata, original version still resolves |
| II.3 | Named source for every quantitative cell | Gate 1 + 2 must have passed |
| II.4 | Figure ties to (source, transformation, timestamp) | Gate 19 must have passed |
| II.5 | Forecast kill switch is quantitative | Classifier on `kill-switch` section: returns `quantitative_present` |
| III.6 | Paper is an argument graph; no orphans | Gate 13 must have passed |
| III.7 | Counter-construction attempted and published | Gate 14 must have passed; appendix contains transcript |
| III.8 | Reviewer disagreement is published | Appendix contains a disagreement matrix from the three reviewers |
| IV.9 | Reviewers hold disjoint priors | Reviewer panel composition logged; at least one model-family delta |
| IV.10 | Desk-lead override is documented | If gates pass and desk lead held, post-mortem entry exists |
| V.11 | 20 gates, no partial passes | All 20 gate records are `passed: true` |
| V.12 | Cadence | The publish date matches the quarter's first Wednesday OR an errata window |
| VI.13 | Full performance reporting in ledger | Ledger CSV is current; no curated omissions |
| VI.14 | Telemetry is auditable | Telemetry artifact for this paper exists in `helix/telemetry/runs/` |
| VI.15 | Constitution version dated | The paper bundle references the live constitution by SHA |

## Inputs

- All upstream gate outputs (1-19)
- Reviewer panel composition
- Debate transcript + Judge rationale
- Telemetry artifact for this paper
- `HELIX_CONSTITUTION.md` SHA at publish time

## Outputs

```yaml
passed: bool
findings:
  - severity: error
    code: NONCONFORMANT
    provision: "§II.5"
    message: "kill-switch section does not contain a quantitative invalidation condition"
constitution_version_sha: "..."
```

## Failure modes the gate catches

- A gate further upstream passed by accident (e.g., a malformed kill switch slipped through gate 16).
- A reviewer composition that doesn't satisfy disjoint priors.
- A paper that ships with a stale constitution SHA.

## Implementation note

The classifier sub-checks (§II.5, the qualitative ones) are LLM-based with structured output. They run after all the deterministic checks, so a paper that fails on §II.3 doesn't burn cycles on the qualitative checks.
