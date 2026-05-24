# Gate 13 — Argument-graph coherence

**Phase:** pre-publish
**Type:** hybrid (LLM extractor + deterministic checker)
**Owner:** automation; quant reviewer approves the extracted graph
**Required by shape:** all

## Purpose

Treat the paper as a directed acyclic graph of claims. Every claim must be justified by either a cited datum, a stated assumption, or a previously-established claim. The conclusion must be reachable. Nothing dangles. This is the step-level supervision invariant (PRM, "Let's Verify Step by Step") translated to long-form equity research, and the long-argument-coherence invariant (the unit-distance proof) made mechanical.

## Pass condition

The extracted argument graph satisfies all of:

1. **Unique IDs.** No duplicate node identifiers.
2. **Valid kinds.** Every node is one of `{citation, assumption, claim, conclusion}`.
3. **No dangling edges.** Every edge source and target exists.
4. **Single conclusion.** Exactly one node has `kind: conclusion`.
5. **Acyclic.** No directed cycles.
6. **Justified claims.** Every node with `kind in {claim, conclusion}` has at least one inbound edge.
7. **Valid leaves.** Every node with zero inbound edges has `kind in {citation, assumption}`.
8. **All nodes support the conclusion.** Every node is reachable backwards from the conclusion (no orphans, no parallel arguments that go nowhere).
9. **Weight validity.** Where `weight` is present on an edge, it is a number in `[0.0, 1.0]`. Weight is **required** on edges to the conclusion; optional elsewhere.
10. **Load-bearing multi-sourcing.** For every edge to the conclusion with weight ≥ 0.7 ("load-bearing"), the source node must have ≥ 2 inbound edges (i.e., the load-bearing claim is not single-sourced). The threshold is configurable via the module constant `LOAD_BEARING_THRESHOLD` in `check.py`.

## Inputs

- `paper.md` — the draft paper
- `appendix.md` — citations and assumptions
- `debate_transcript.md` — every Bull/Bear turn (extractor must cover claims made here, not just the body)
- `counter_attempt.md` — the counter-construction artifact (claims the paper addresses become nodes)
- `graph.json` — produced by the extractor (see `extractor_prompt.md`); subject to quant-reviewer approval

The extractor runs **after** the debate and counter-construction so all four documents are available. Gate 13 therefore runs after the adversarial block in the pre-publish pipeline.

## Outputs

```yaml
passed: true | false
findings:
  - severity: error | warn
    code: ORPHAN | CYCLE | UNJUSTIFIED | NO_CONCLUSION | MULTI_CONCLUSION | BAD_KIND | BAD_EDGE | DUP_ID | UNREACHABLE | BAD_WEIGHT | MISSING_CONCLUSION_WEIGHT | SINGLE_SOURCED_LOAD_BEARING
    message: "..."
    node: "claim2"
evidence:
  node_count: int
  edge_count: int
  citation_count: int
  assumption_count: int
  min_path_length_to_conclusion: int
  max_path_length_to_conclusion: int
```

## Failure modes the gate catches

- A claim made in the body that has no supporting evidence.
- A circular argument (A justifies B, B justifies A).
- A side argument that does not actually support the conclusion (filler).
- An assumption that masquerades as a claim (no explicit `kind: assumption`, so the gate forces it to be backed).
- A conclusion that cannot be derived from the rest of the graph (missing edges).

## Failure modes the gate does NOT catch

- A factually wrong citation (gate 2 does that).
- A weak argument that is *technically valid* but should not convince (the debate gate, M2, does that).
- A bad base rate (gate 15 does that).

## Implementation notes

- The extractor is a single-shot LLM call with strict JSON schema output. Prompt in `extractor_prompt.md`.
- The checker is pure Python, deterministic, in `check.py`. No external dependencies.
- The quant reviewer signs off on the extracted graph before the deterministic check runs. (Catches extractor errors before they cause false rejects.)

## Acceptance tests

Run `python test_check.py` from this directory. All six tests must pass:

- `test_valid_graph` — a well-formed graph passes.
- `test_orphan_node` — an isolated node is caught.
- `test_cycle` — a directed cycle is caught.
- `test_unjustified_claim` — a `claim` with no inbound edges is caught.
- `test_no_conclusion` — a graph missing a conclusion node is caught.
- `test_dangling_edge` — an edge to a non-existent node is caught.

## Example

See `example_graph.json` for a passing graph that mirrors a six-page quality-compounder thesis.
