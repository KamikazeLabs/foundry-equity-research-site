# `helix/gates/` — the 20-gate pre-publish stack

Every paper passes 20 gates before publication. Any failure blocks. There are no partial passes (Constitution §V.11).

## Gate inventory

| # | Slug | Type | Phase | Status |
|---|------|------|-------|--------|
| 01 | number-tie | deterministic | pre-publish | existing |
| 02 | citation-resolver | deterministic | pre-publish | existing |
| 03 | date-consistency | deterministic | pre-publish | existing |
| 04 | ticker-validity | deterministic | pre-publish | existing |
| 05 | chart-render | deterministic | pre-publish | existing |
| 06 | font-embedding | deterministic | pre-publish | existing |
| 07 | brand-check | deterministic | pre-publish | existing |
| 08 | toc-parity | deterministic | pre-publish | existing |
| 09 | page-budget | deterministic | pre-publish | existing |
| 10 | disclaimer | deterministic | pre-publish | existing |
| 11 | spell-grammar | classifier | pre-publish | existing |
| 12 | ai-concurrence | classifier | pre-publish | existing — being replaced by debate (M2) |
| 13 | **argument-graph** | hybrid | pre-publish | **M1, runnable reference here** |
| 14 | **counter-thesis** | classifier | pre-publish | M2 |
| 15 | **base-rate** | hybrid | pre-publish | M2 |
| 16 | **reflexivity** | classifier | pre-publish | M2 |
| 17 | **liquidity** | deterministic | pre-publish | M2 |
| 18 | **disclosure-footprint** | deterministic | pre-publish | M2 |
| 19 | **audit-trail** | deterministic | pre-publish | M2 |
| 20 | **constitution** | classifier | pre-publish | M4 |

## Gate contract

Every gate exposes the same interface:

```
input:  a paper bundle (markdown + appendix + metadata)
output: { passed: bool, findings: [Finding], evidence: { ... } }
```

A `Finding` has `severity` ("error" | "warn"), `code`, `message`, optional `location`.

The pipeline fails the gate if any finding has `severity == "error"`. Warnings do not fail the gate but are reported.

## Reference implementation

`13-argument-graph/` is the canonical example of the gate contract. Read it first when implementing a new gate.

## Phase mapping

- **pre-paper:** runs during the drafting phase (gates that constrain shape; the shape-selector gate; thesis-generator gates if FunSearch is on).
- **pre-publish:** runs once the draft is complete (the 20 above).
- **post-mortem:** runs after a position closes, to feed the PRM and the ledger.
