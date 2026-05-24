# `research/base-rates/`

Gate 15 (base-rate sanity) compares every forward quantitative claim in a paper against the historical distribution for `(metric, sector_anchor, horizon)`. The distributions live here, one YAML file per tuple.

## File naming

```
<sector_anchor>_<metric>.yaml
```

Examples:
- `software_application_revenue_cagr_3y.yaml`
- `industrial_components_operating_margin_expansion_3y.yaml`
- `diagnostic_platforms_revenue_cagr_5y.yaml`

## Refresh cadence

Annually, at the end of each calendar Q1. Source data should be reproducible from a named provider (Compustat, Capital IQ, FactSet) with a documented screening filter.

## Schema

See `software_application_revenue_cagr_3y.yaml` for the canonical schema. Required fields:

- `metric` (string)
- `sector_anchor` (string)
- `sample_size` (int)
- `period` (YYYY-YYYY)
- `last_refreshed` (quarter)
- `source.provider` (string)
- `source.filter` (string description)
- `distribution.median` + `.p25/.p75/.p90/.p95/.p99`
- `notes` (string)

## Status

This directory ships with one worked example to validate the schema. The full library is a quarterly data project per `HANDOFF.md` (open decision points). When the library reaches ~20 entries covering the desk's primary coverage universe, gate 15 can flip from spec-only to runnable.
