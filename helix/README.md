# `helix/` — Forge blueprint package

This directory is the **blueprint** for the next generation of Helix Site Forge — the autonomous pipeline that produces Foundry Equity Research papers.

**Where the actual runtime lives.** The Helix Site Forge runtime is a separate repository inside KamikazeLabs. This directory does not run the pipeline. It specifies what the pipeline must do.

**What is in here.**

- `shapes/` — per-paper-type structural templates. Picked by the shape-selector agent per brief.
- `gates/` — one directory per gate (20 total). Each contains `spec.md` and, where appropriate, a reference implementation.
- `agents/` — one directory per agent (reviewers, debate roles, counter-construction, thesis generator, ledger query). Each contains a `spec.md` with the system prompt, rubric, and independence requirements.
- `pipelines/` — YAML pipeline definitions (`pre-paper`, `pre-publish`, `post-mortem`).
- `prm/` — process reward model: training-data format, approach, and roll-out plan.
- `funsearch/` — evolutionary thesis search.
- `telemetry/` — dashboard specifications.

**Working code.** One gate ships with a runnable reference: `gates/13-argument-graph/`. It is the canonical example of the gate contract — input format, deterministic check, exit codes. Other gates that are deterministic (e.g., `19-audit-trail`) will follow the same pattern when implemented.

**Source of truth.** The full design rationale lives in `../research/2026-05-helix-transformation.md`. Read that first. This directory is what to build from it.

**Acceptance.** A milestone is "done" when:
1. Every file under the milestone's scope exists and is committed.
2. Any reference code passes its tests.
3. The Forge runtime team has an open ticket to implement against the spec.

**Order of build.** M0 (foundation) → M1 (graph + panel) → M2 (debate + counter) → M3 (search + PRM) → M4 (constitution gate + ledger). See `../research/2026-05-helix-transformation.md` Part VI for the time estimate and exit criterion for each.
