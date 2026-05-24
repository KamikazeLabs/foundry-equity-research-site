# `helix/telemetry/runs/`

One YAML file per published paper, named `<paper_id>.yaml`. Schema is documented in `../dashboard.md`.

This directory is intentionally empty in source control until the first paper ships under the new stack. Once papers start flowing, the per-paper telemetry artifacts live here and feed the cross-paper dashboard.

Production deployment will likely move this to private storage and only sync aggregated rollups back into the repo for the public site to render. For now: schema is the contract; the directory is the placeholder.
