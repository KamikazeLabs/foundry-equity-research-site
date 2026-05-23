# Synthetic worked example — passing

Companion to `synthetic-quality-compounder/`. This bundle exercises the **happy path**: all 20 gates pass, the Judge rules bull, the paper ships.

**Subject:** PRISM Diagnostics (fictional ticker `PRSM`), a molecular-diagnostics platform + consumables business. Quality-compounder shape.

**Why two examples?** The first example demonstrates how the pipeline holds a weak paper (Judge ruled bear). This one demonstrates how a sound paper survives the same machinery. Together they bracket the design space.

## What this example validates

- The full pipeline produces a `SHIPPED` paper when all gates pass.
- Counter-construction recommends `ship_with_appendix`; the paper addresses the counter in its appendix and proceeds.
- The reviewer panel produces material disagreement (industry vs. macro) but no `block` verdicts; the paper acknowledges the disagreement.
- The argument graph uses weights on conclusion edges (per spec A.6).
- The disagreement matrix uses the YAML schema (per spec A.7).
- The counter-construction `all_attempts` uses provenance (per spec A.5).

## How to run

```bash
python3 helix/gates/13-argument-graph/check.py examples/synthetic-passing/argument_graph.json
```

Expected: gate passes, 0 errors.

## Disclaimer

PRISM is fictional. All numbers are illustrative. Nothing in this directory is investment research.
