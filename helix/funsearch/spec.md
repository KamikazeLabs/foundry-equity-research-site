# `helix/funsearch/` — evolutionary thesis search

**Direct inspiration:** FunSearch (DeepMind, *Nature* 2023), AlphaEvolve (DeepMind, 2025).

**Premise:** the gate stack is already an evaluator. We can treat thesis generation as a search problem over structured candidates, with the gate subset as the fitness function. The published paper is not the analyst's first instinct; it is the survivor of a tournament.

## Loop

```
brief
  |
  v
[thesis-generator]  -- emits N candidates (mix fresh + mutated + recombined)
  |
  v
[cheap-gate-subset]  -- runs number-tie, citation-resolver, base-rate,
  |                     liquidity, counter-thesis (light pass) on each
  v
[fitness scoring]  -- rolls per-gate results into a fitness score
  |
  v
[selection]  -- keep top K, plus a diversity sample from the rest
  |
  v
[stop?]  -- yes: emit top T to the desk; no: feed survivors back to the
  |         generator as seed_theses
  v
[done]
```

Cycles per brief: configurable, typical 3–5. Total candidate budget per brief: ~100–500 (depends on cost ceiling per quarter).

## Fitness function

```
fitness = (
  0.30 * pass_rate(cheap_gates) +
  0.25 * base_rate_z_inverse +              # closer to median is better, unless paper explains
  0.20 * liquidity_headroom +
  0.15 * counter_thesis_strength_inverse +  # weaker public counter = stronger thesis
  0.10 * structural_diversity_bonus         # penalize duplicates of past candidates
)
```

Weights are configurable per brief. The configuration is checked into the brief artifact so the post-mortem can replay it.

## Mode-collapse guard

Track structural similarity across all candidates per brief. If the top 5 candidates cluster on `subject` or `mechanism`, force the generator to produce a diversity-only batch for the next cycle.

## Output

After the final cycle, emit:

- Top T candidates (default T = 3) with full structured records.
- All evaluated candidates, with their fitness and which gates they failed.
- A `funsearch_report.md` for the desk lead summarizing what was explored, what survived, what was dropped, and why.

The desk lead picks one of the top T to draft into a paper, OR documents why none of the top T were selected (in which case the human-originated thesis enters the standard pipeline).

## Telemetry to capture

- Number of cycles per brief.
- Number of candidates evaluated.
- Distribution of fitness scores.
- % of published papers that originated from a FunSearch top-T candidate vs. analyst's initial pick.
- 12-month and 24-month outcome of FunSearch-originated vs. analyst-originated theses.

The acceptance criterion for M3 (per the transformation paper): at least 1 of the next quarter's 4 papers originates from a FunSearch candidate that was not the analyst's first instinct.

## What this is NOT

- A replacement for the analyst. FunSearch generates; the analyst writes; the gates evaluate.
- A contrarianism engine. The gate stack filters for grounded, defensible theses. Surviving the gates *and* being non-obvious is the bar.
- A magic ROI generator. FunSearch optimizes for *survivability through the pipeline*, which is a proxy for thesis quality — not a direct return forecast.
