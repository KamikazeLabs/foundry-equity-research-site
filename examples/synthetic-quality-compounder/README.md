# Synthetic worked example — quality-compounder

This directory is the **end-to-end validation artifact** for the Helix blueprint. It contains a synthetic paper bundle that exercises every schema and pipeline output the M0–M4 deliverables introduce.

**Subject:** ACME Industries (fictional ticker `ACME`), a precision industrial components manufacturer. Quality-compounder shape.

**Purpose:** validate the schemas concretely before the Forge runtime team builds against them. Surface spec ambiguities. Provide a reference example future synthetic and real papers can be tested against.

**Disclaimer:** ACME is fictional. All numbers are illustrative. Nothing in this directory is investment research.

## File map

| File | Validates |
|------|-----------|
| `paper.md` | overall structure (10 sections per quality-compounder shape) |
| `appendix.md` | source rows + assumptions (constitution §II.3, §III.6) |
| `argument_graph.json` | gate 13 (parsed end-to-end through the runnable checker) |
| `transformations.yaml` | gate 19 audit-trail DSL |
| `counter_attempt.md` | gate 14 + counter-construction agent spec |
| `debate_transcript.md` | bull/bear/judge spec |
| `judge_verdict.yaml` | judge spec output schema |
| `disagreement_matrix.md` | reviewer panel spec + constitution §III.8 |
| `telemetry.yaml` | telemetry per-paper schema |

## How to run

```bash
# from the repo root
python3 helix/gates/13-argument-graph/check.py examples/synthetic-quality-compounder/argument_graph.json
```

Expected: gate passes (0 errors).

## Findings

See `../VALIDATION_NOTES.md` for spec gaps surfaced while building this artifact.
