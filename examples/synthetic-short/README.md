# Synthetic worked example — mean-reversion short

Third example. Exercises the **mean-reversion-short** shape: 8-turn debate, forensics-priority reviewer routing, mandatory liquidity gate, asymmetric risk profile.

**Subject:** GLITZ Apparel (fictional ticker `GLTZ`), a luxury / fast-fashion accessories business with deteriorating fundamentals and aggressive accounting.

**Outcome:** paper ships. Bull (defending the short thesis) wins the debate; counter-construction recommends ship_with_appendix; all 20 gates pass including liquidity.

## What this exercises beyond the prior examples

- **8-turn debate** instead of 6 (per mean-reversion-short shape config).
- **Forensics-first reviewer routing** — the forensics reviewer is the most-cited in the debate and contributes the strongest finding.
- **Liquidity gate (17) is mandatory**; borrow check passes at desk sizing.
- **Asymmetric risk treatment** — the kill switch is unusually detailed; the position size is constrained by both ADV and borrow.
- **A short thesis structure** — the "Bull" in the debate is the *defender of the short*; the "Bear" defends the long case for the stock.

## How to run

```bash
python3 helix/gates/13-argument-graph/check.py examples/synthetic-short/argument_graph.json
```

Expected: gate passes, 0 errors.

## Disclaimer

GLITZ is fictional. All numbers are illustrative. Nothing in this directory is investment research.
