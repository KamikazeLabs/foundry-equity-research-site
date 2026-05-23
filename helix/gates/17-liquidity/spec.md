# Gate 17 — Liquidity & capacity

**Phase:** pre-publish
**Type:** deterministic
**Owner:** automation
**Required by shape:** `mean-reversion-short`, `special-situation`; optional on others

## Purpose

A thesis that requires position sizing beyond achievable liquidity is not investable for an institutional reader at desk scale. The gate enforces a hard ratio of implied position size to average daily volume.

## Pass condition

For the published target position sizing (or the desk's typical institutional sizing, configurable):

```
position_size_usd / (ADV_20d_usd * configurable_fraction) <= 1.0
```

Default `configurable_fraction = 0.25` (i.e., the position should be exitable in roughly 4 trading days at 100% of typical participation, or 20 trading days at 20%). The fraction is overridable per shape.

For shorts, an additional borrow check:

```
position_size_shares / shares_available_to_borrow <= 0.5
```

## Inputs

- Target position size (from the paper or desk default)
- Trailing 20-day ADV (in dollars)
- Shares available to borrow (for shorts; from prime broker or public short-interest data)

## Outputs

```yaml
passed: bool
findings:
  - severity: error | warn
    code: ADV_BREACH | BORROW_BREACH | DATA_MISSING
    metric: "..."
    value: float
    threshold: float
    message: "..."
```

## Failure modes the gate catches

- Sizing that cannot be exited inside a reasonable window.
- Shorts that cannot be borrowed at scale.

## Failure modes the gate does NOT catch

- Liquidity drying up during the position's holding period. (No gate can.)
- Borrow rates becoming uneconomic. The gate checks availability, not cost.

## Implementation notes

ADV pulled from a daily-refreshed data source. Borrow availability pulled from prime broker file or public short-interest. Both refresh weekly with the ledger.
