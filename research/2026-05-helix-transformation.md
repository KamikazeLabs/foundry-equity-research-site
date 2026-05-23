# From Unit Distances to Unit Theses

**A first-principles plan to transform Helix Site Forge using the OpenAI unit-distance disproof and adjacent AI/math research**

- Author: research draft prepared for KamikazeLabs / Helix
- Date: 2026-05-23
- Status: proposal, not editorial policy
- Scope: architecture, gates, agent topology, and an implementation plan

---

## Abstract

In May 2026, an internal OpenAI reasoning model disproved one of the longest-standing conjectures in discrete geometry — the Erdős unit-distance conjecture. The proof is striking not only as mathematics, but as evidence about how to organize an autonomous reasoning system that produces verifiable long-form output. A general-purpose model, given cheap downstream verification and permission to wander into an apparently unrelated subfield (class field towers in algebraic number theory), found a construction that disproved an 80-year conjecture by *varying a parameter everyone had silently held fixed*.

Helix Site Forge — the autonomous pipeline that produces Foundry Equity Research papers — has the same shape as a math-proof pipeline: long-form artifacts, end-to-end coherence requirements, gated verification, and a finite number of human reviewers as the last line of defense. The unit-distance disproof is therefore directly applicable to Helix, not as a metaphor but as a blueprint.

This paper does three things:

1. Reconstructs the OpenAI proof from first principles, in technical detail.
2. Surveys nine adjacent AI-and-math results — FunSearch, AlphaEvolve, AlphaProof, Process Reward Models, Self-Consistency, AI Safety via Debate, Mixture of Agents, Constitutional AI, and Deep Research Agents — and extracts the architectural invariants they share.
3. Translates those invariants into a concrete, implementable redesign of Helix: ten transformations, a 20-gate pipeline, a four-milestone delivery plan, and acceptance criteria for each component.

The thesis is simple: **Helix is structurally close to a discovery engine. The unit-distance proof and the surrounding literature describe exactly the structural moves that turn a verification pipeline into a discovery engine.** This document is the plan to make those moves.

---

# Part I — The Unit-Distance Disproof, in Detail

## 1.1 The 80-year problem

In 1946 Paul Erdős asked: among `n` points in the Euclidean plane, what is the maximum number of point-pairs at distance exactly 1? Call this number `u(n)`.

- **Lower bound (Erdős, 1946):** take a `√n × √n` sub-grid of the Gaussian integers `ℤ[i]`. Counting Gaussian integers of a given norm yields

  ```
  u(n) ≥ n^{1 + c / log log n}
  ```

  for some constant `c > 0`. The exponent slightly exceeds 1 but approaches 1 as `n → ∞`.

- **Upper bound (Erdős, conjecture):** `u(n) ≤ n^{1 + o(1)}` — the square grid is essentially optimal; no *fixed* improvement on the exponent exists.

- **What was open for 80 years:** whether some fixed `δ > 0` exists with `u(n) ≥ n^{1+δ}` infinitely often.

For context: the best known upper bound (Spencer–Szemerédi–Trotter, 1984) is `u(n) ≤ O(n^{4/3})`. Closing the gap between `n^{1 + o(1)}` (conjectured) and `n^{4/3}` (best known) is the unit-distance problem.

## 1.2 What the model proved

**Theorem (OpenAI, May 2026).** There exists a fixed `δ > 0` and an infinite sequence of finite point sets `P_i ⊂ ℝ²` with `|P_i| → ∞` such that the number of unit distances in `P_i` is at least `|P_i|^{1+δ}`.

Two corollaries:

- The Erdős conjecture (`u(n) ≤ n^{1+o(1)}`) is **false**.
- The square-grid family is **not** asymptotically optimal.

**Sawin's refinement (arXiv:2605.20695, May 20, 2026).** `δ ≥ 0.014`. The original OpenAI manuscript gave a constant on the order of `6.24 × 10⁻³⁸`; Sawin tightened the algebraic-number-theory accounting to push `δ` two orders of magnitude past Erdős's old bound's effective slope.

## 1.3 The construction — what the model actually built

The breakthrough is **generalizing Erdős's construction by treating the underlying number field as a free parameter**, not a fixed choice.

### 1.3.1 The classical case (Erdős, 1946)

- **Field:** `K = ℚ(i)`, degree `f = 2` over `ℚ`.
- **Ring of integers:** `𝒪_K = ℤ[i]` (Gaussian integers).
- **Embedding:** `𝒪_K ↪ ℂ` is just the identity; take a `√n × √n` sub-window.
- **Counting argument:** the number of Gaussian integers of norm `≤ N` with norm equal to a *specific* value `m` is roughly the number of ways `m = a² + b²`, which has `≈ 2^{ω(m)}` solutions when `m` has many prime factors `p ≡ 1 (mod 4)`. Summed over the window, you get `n^{1 + Ω(1/log log n)}` coincidences — the source of the slight `1/log log n` bump.

### 1.3.2 The new case (OpenAI, 2026)

The construction is a four-step program. Each step generalizes a fixed choice in Erdős's setup.

**Step 1. Use a CM number field, not just `ℚ(i)`.**

Take `K = L(i)` where `L` is a totally real number field of degree `f` over `ℚ`. Then `K` is a "CM field" of degree `2f`. Its ring of integers `𝒪_K` embeds via the Minkowski map into `ℂ^f` as a rank-`2f` lattice `Λ`.

**Step 2. Project to `ℂ = ℝ²`.**

Pick one of the `f` complex embeddings `σ: K → ℂ` and project `Λ → ℂ`. The image is a dense set of points in a bounded window.

**Step 3. Manufacture unit-norm algebraic integers, lots of them.**

The key combinatorial ingredient: an element `ξ ∈ 𝒪_K` with `|σ(ξ)| = 1` *in every embedding* `σ` induces a rotation that maps lattice points to lattice points and preserves distances. The number of such `ξ` (up to roots of unity) is bounded below by

```
≥ ∏_j (k_j + 1) / h(K)
```

where the product is over a chosen set of conjugate split prime ideal pairs `(𝔭_j, 𝔭̄_j)` in `𝒪_K`, each with multiplicity bound `k_j`, and `h(K)` is the class number of `K`. This is a pigeonhole argument **on the ideal class group**: enough split primes force collisions, and each collision produces a unit-norm element.

**Step 4. Make the degree `f` blow up while keeping the discriminant tame.**

This is the deep input. The proof uses **Golod–Shafarevich infinite class field towers**: infinite sequences `K_1 ⊂ K_2 ⊂ K_3 ⊂ ...` of unramified extensions with `[K_j : ℚ] → ∞` but root discriminant `(disc K_j)^{1/[K_j:ℚ]}` bounded by `∏_{p ∈ T} p` for a fixed finite set `T` of primes.

The Golod–Shafarevich theorem (1964): if a number field `K` has class group of rank `r` and `r² > 4(d + 2)` where `d` is the number of "generators" of the maximal `p`-class field tower, then the tower is infinite — degree can grow without bound while the root discriminant stays put.

### 1.3.3 Why this beats the grid

The geometric lemma in the OpenAI proof says: a lattice `Λ ⊂ ℂ^f` with `u^f` unit-norm elements yields at least `(u π R² / 4 v δ²)^f` unit distances among at most `(9 R² / δ²)^f` projected points.

Set `N = (9 R² / δ²)^f` (point count) and `U = (u π R² / 4 v δ²)^f` (unit-distance count). Then

```
U / N^{1+ε} = (u π / 4v · (9)^{-ε})^f · (R² / δ²)^{-εf}
```

If you can pick `u` large enough relative to `v` and `δ` — which the class-field-tower construction guarantees — then `U ≥ N^{1+ε}` for some fixed `ε > 0` independent of `f`. The degree `f → ∞` is what amplifies a tiny per-field improvement into a fixed-exponent gain.

**Erdős kept `f = 2` fixed.** The model treated `f` as a free dimension to push to infinity.

## 1.4 What is structurally novel for AI

Four observations from the OpenAI release and the verifying mathematicians (Alon, Wood, Bloom, Sawin, Tsimerman):

1. **General-purpose model.** The proof came from a reasoning model not trained, scaffolded, or targeted for math problems specifically.
2. **Cross-domain bridge.** Class field towers — a deep tool in algebraic number theory — were imported into discrete geometry. Humans had not made this connection in 80 years.
3. **Long-argument coherence.** The proof is multi-page, multi-lemma, with a structure that fails if any link breaks. Tsimerman: "the problems are precise, potential proofs can be checked, and a long argument only works if the reasoning holds together from beginning to end."
4. **"Treacherous waters" tolerance.** Tsimerman again: AI can "play for longer and in more treacherous waters than mathematicians without getting overwhelmed."

These four observations are the seed material for the Helix redesign.

---

# Part II — Adjacent AI/Math Research That Sharpens the Lesson

This section surveys nine results from 2018–2026 that, taken together, describe the design space of reasoning systems with verifiable long-form output. Each ends with a one-line transferable principle.

## 2.1 FunSearch (DeepMind, *Nature*, 2023)

LLM + automated evaluator in an evolutionary loop. The LLM generates code (not free text); the evaluator scores it; high-scoring programs are sampled back into the prompt. FunSearch found new lower bounds for the cap-set problem (an open question in combinatorics) and improved heuristics for online bin packing.

> **Principle:** an LLM trapped behind an evaluator can search a space too large for direct enumeration; the output is *programs that explain how the solution is constructed*, not just answers.

## 2.2 AlphaEvolve (DeepMind, 2025)

A Gemini-driven coding agent that runs evolutionary search over algorithms. Uses Gemini Flash for breadth and Gemini Pro for depth, plus automated scoring. Notable results: a 48-step `4×4` complex matrix multiplication (beating Strassen's 56), new lower bounds for the Traveling Salesman Problem and Ramsey numbers, and a 23% speedup on a production matrix-multiplication kernel inside Gemini's own training.

> **Principle:** mixed-model ensembles (cheap-and-broad + expensive-and-deep) outperform single models when the cost of evaluation is amortized across many candidates.

## 2.3 AlphaProof + AlphaGeometry 2 (DeepMind, *Nature*, 2024–2025)

AlphaProof translates IMO problems into Lean's formal language, then uses AlphaZero-style reinforcement learning to search for a proof. At IMO 2024 it solved 4/6 problems for a silver-medal score. The key architectural feature: **the verifier (Lean) is not a model — it is a deterministic proof checker.** The model proposes; Lean disposes.

> **Principle:** the cheaper and more deterministic the verifier, the more aggressively the proposer can be allowed to wander.

## 2.4 Process Reward Models — "Let's Verify Step by Step" (OpenAI, 2023)

Instead of scoring only the *final answer* of a chain of reasoning (Outcome Reward Model, ORM), score *each step* (Process Reward Model, PRM). OpenAI's PRM, trained on 800K step-level human labels (PRM800K), beat ORM-supervised models on the MATH benchmark — and crucially, the gap widened as the number of sampled candidate solutions grew.

> **Principle:** for long arguments, step-level supervision dominates outcome-level supervision because it localizes the failure and the gain compounds with sample size.

## 2.5 Self-Consistency (Wang et al., 2022)

Sample many chain-of-thought reasoning paths, take the most common final answer. +17.9% on GSM8K, +12.2% on AQuA. The intuition: a complex problem admits many reasoning paths to the same correct answer; convergence across paths is evidence of correctness.

> **Principle:** agreement across *independent* reasoning paths is a stronger signal than confidence within one.

## 2.6 AI Safety via Debate (Irving, Christiano, Amodei, OpenAI, 2018)

Two adversarial agents argue; a (limited) judge decides. Theoretically, debate with optimal play raises a polynomial-time judge's effective capability from NP to PSPACE: the adversarial structure makes lying harder than refuting a lie. The hard-to-verify problem becomes tractable through adversarial decomposition.

> **Principle:** adversarial structure converts a verifier's reach from "what I can check" to "what someone could not successfully refute."

## 2.7 Mixture of Agents (Wang et al., 2024)

Multiple LLMs arranged in sequential layers; each layer reads the previous layer's outputs as context and produces refined output. With three layers and six models per layer, MoA using only open-source models beat GPT-4 Omni on AlpacaEval 2.0 (65.1% vs 57.5%).

> **Principle:** layered refinement of natural-language outputs by heterogeneous specialists outperforms any single model, even a frontier one.

## 2.8 Constitutional AI (Anthropic, 2022)

A written set of principles ("constitution") plus a critique-and-revise loop. The model generates, critiques itself against the constitution, revises. Phase 2 uses RL with AI-generated preference labels grounded in the constitution.

> **Principle:** explicit, written principles plus a self-critique loop yield more stable behavior than implicit fine-tuning.

## 2.9 Deep Research Agents (OpenAI / Google / xAI, 2024–2026)

Long-horizon retrieval agents that decompose a research question, retrieve multi-hop, cite sources, and synthesize a long-form report. Open questions remain around multi-document grounding and consistency across conflicting sources.

> **Principle:** retrieval, decomposition, and citation grounding belong in a *separate* agent layer from synthesis — keep the wandering and the grounding apart so each can be checked.

## Summary table

| Result | Year | Single-line lesson |
| --- | --- | --- |
| OpenAI unit-distance | 2026 | Vary the parameter you held fixed; cross domains for the tool. |
| FunSearch | 2023 | LLM + automated evaluator + evolution finds new objects. |
| AlphaEvolve | 2025 | Mix breadth-cheap and depth-expensive models around an evaluator. |
| AlphaProof | 2024 | Deterministic verifiers let proposers wander. |
| PRM (Verify Step by Step) | 2023 | Step-level supervision beats outcome-level for long reasoning. |
| Self-Consistency | 2022 | Convergence across independent paths beats single-path confidence. |
| Debate | 2018 | Adversarial structure amplifies a weaker verifier. |
| Mixture of Agents | 2024 | Layered heterogeneous specialists beat a single frontier model. |
| Constitutional AI | 2022 | Written principles + self-critique stabilize behavior. |
| Deep Research | 2024–2026 | Separate retrieval/citation from synthesis. |

---

# Part III — First-Principles Distillation: Ten Invariants

Across the ten results above (the unit-distance proof plus the nine survey items), the same architectural invariants recur. These are the constraints that any next-generation Helix should satisfy.

1. **Vary what you held fixed.** Identify the structural choices in the pipeline that are constants by habit, not by necessity. (Unit-distance: field choice. Helix: paper template, number of gates, number of agents, section ordering.)

2. **General reasoner + cheap verifier > specialized reasoner.** Build verifiers that are cheap, deterministic, and many; let the proposing models be broad and unspecialized. (AlphaProof, FunSearch, unit-distance.)

3. **Step-level supervision dominates outcome-level.** For any artifact built by a long chain of reasoning, score steps, not just outputs. (PRM, unit-distance.)

4. **Convergence across independent paths is the signal.** Independence is the source of strength; correlation is the source of weakness. (Self-Consistency, MoA.)

5. **Adversarial structure expands a verifier's reach.** Sycophantic agreement is cheap; surviving an honest attempt to refute is expensive. (Debate, unit-distance counter-construction.)

6. **Layered heterogeneous specialists beat monoliths.** Different priors, different training, different roles. (MoA, AlphaEvolve.)

7. **Cross-domain transfer is a moat, not a bug.** The best non-obvious tool comes from the field you wouldn't look in. (Unit-distance: class field towers in geometry.)

8. **Separate the wandering from the grounding.** Retrieval and citation belong in a distinct layer from synthesis. (Deep Research, Helix's number-tie gate.)

9. **Written principles plus self-critique stabilize behavior.** A constitution is verifiable; a vibe is not. (Constitutional AI.)

10. **Long arguments are graphs, not lists.** End-to-end coherence is a graph-traversal property; check every edge. (Unit-distance, PRM.)

These ten invariants are the design contract for the new Helix.

---

# Part IV — Helix Today: An Audit

The current Helix Site Forge pipeline (per `method/index.html` of this repo) has the following structure:

**Pre-publish review:**

- One human fundamental analyst (thesis + sourcing).
- One human quantitative reviewer (model + numbers + data ties).
- Three independent AI reviewers; *all three must concur*; dissent holds the paper.

**12 mechanical gates:**

1. Number-tie
2. Citation resolver
3. Date consistency
4. Ticker validity
5. Chart render
6. Font embedding
7. Brand check
8. TOC parity
9. Page budget
10. Disclaimer
11. Spell and grammar
12. AI triple-review concurrence

**Editorial rule:** any gate failure blocks shipping. No partial passes.

### Audit against the ten invariants

| Invariant | Helix today | Status |
| --- | --- | --- |
| 1. Vary what you held fixed | Section template, number of gates, number of AI reviewers, paper length are constants. | **Gap.** |
| 2. General reasoner + cheap verifier | Verifiers exist (12 gates). Reasoners likely a single class of model. | **Partial.** |
| 3. Step-level supervision | Gates are mostly artifact-level (cell, citation, page). | **Partial.** |
| 4. Convergence across independent paths | Three AI reviewers — but no guarantee of independent priors. | **Weak.** |
| 5. Adversarial structure | None; concurrence is consensus, not survival of refutation. | **Missing.** |
| 6. Layered specialists | Two human roles (fundamental, quant). AI reviewers undifferentiated. | **Partial.** |
| 7. Cross-domain transfer | Not architected. | **Missing.** |
| 8. Wandering vs. grounding | Number-tie and citation resolver separate grounding well. | **Strong.** |
| 9. Written principles + self-critique | Implicit editorial policy; no formal "constitution" or self-critique loop. | **Missing.** |
| 10. Long arguments as graphs | Number-tie checks cells; no argument-graph check. | **Missing.** |

**Net assessment:** Helix is structurally sound on **grounding** (invariants 2, 8) but has gaps or weaknesses on **diversity of reasoning** (4, 6), **adversariality** (5), **cross-domain reach** (7), **self-critique discipline** (9), and **argument-as-graph verification** (3, 10). Invariant 1 (vary what was fixed) is the meta-gap that explains all the others.

This audit is the basis for the redesign in Part V.

---

# Part V — The Helix Transformation

Ten transformations, mapped to the ten invariants. Each is described as: *current state → target state → mechanism → success criterion*. These are not all of equal cost; Part VI sequences them.

## 5.1 Parameterize the pipeline shape per paper (Invariant 1)

- **Current:** every paper uses the same template, the same gate set, the same number of reviewers.
- **Target:** the forge selects a paper *shape* (sections, evidence depth, chart budget, gate sub-set, reviewer panel composition) as a function of the thesis type.
- **Mechanism:** a `paper_shape.yaml` schema describes 6–10 prototypical shapes (e.g., *Quality compounder*, *Mean-reversion short*, *Special situation*, *Macro-driven*); a *shape selector* agent reads the brief and picks one.
- **Criterion:** at least three distinct shapes used across a quarter's four papers, with shape choice reviewed in the post-mortem.

## 5.2 Twelve gates → twenty gates: add eight (Invariants 3, 9, 10)

Add the following gates, each implemented as a deterministic check or a narrowly-scoped LLM classifier:

13. **Argument-graph coherence.** Parse the paper into a DAG `(premises → sub-claims → conclusion)`. Verify every edge resolves to either a cited datum, a previously-established node, or a stated assumption. Reject orphan claims.
14. **Counter-thesis survival.** A red-team agent attempts the strongest publicly-supported case *against* the thesis. The paper must explicitly address the surviving counter-points or shape its position accordingly.
15. **Base-rate sanity.** For every quantitative forward claim (growth rate, margin expansion, multiple re-rating), check against base rates from a structured ledger of historical equivalents.
16. **Reflexivity check.** If the thesis becomes consensus, does the trade still work? A separate gate guarded by a single short paragraph.
17. **Liquidity & capacity check.** Position size implied by the ledger framework vs. ADV.
18. **Disclosure footprint.** Cross-reference all material assumptions to a single appendix; reject assumptions made in body without appendix entry.
19. **Audit trail completeness.** Every figure must trace back to a source row, a transformation, and a timestamp.
20. **Constitution conformance.** The paper passes a final pass against the written Helix constitution (see 5.9).

## 5.3 Three-AI concurrence → adversarial debate (Invariants 4, 5)

- **Current:** three AI reviewers must agree; dissent holds the paper.
- **Target:** an adversarial structure modeled on Irving–Christiano–Amodei (2018). Two AI agents — *Bull* and *Bear* — argue the thesis for a bounded number of turns. A third AI agent — *Judge* — decides. The desk lead reviews the judge's reasoning before sign-off.
- **Mechanism:** Bull and Bear are given asymmetric briefings: Bull sees the draft; Bear sees the draft plus an instruction to find the weakest claim and attack it with publicly available data. Each turn is capped at 400 words. Judge applies the Helix constitution to decide.
- **Criterion:** publish the debate transcript with the paper as an appendix item. (Auditability of reasoning, not just numbers.)

## 5.4 Counter-construction adversary (Invariants 5, 7)

A standing agent whose only job is to attempt to construct a publicly-verifiable counterexample to the paper's central claim. This is the direct analog of "build the construction, don't refine the upper bound" from the unit-distance proof.

- **Output:** a documented counter-construction attempt — a specific dataset, comparable, or precedent that would, if true, invalidate the thesis. Either it succeeds (kill the paper) or it survives serious effort (publish, with the failed counter included as an appendix).
- **Why this matters:** publishing the *attempt* and its failure is a far stronger signal to institutional readers than triple-AI agreement.

## 5.5 Argument-graph coherence verifier (Invariants 3, 10)

Parse the paper into a directed graph. Each node is a *claim* (atomic, declarative, falsifiable). Each edge is a *justification* (citation, derivation, prior node).

- **Implementation:** an extractor LLM converts paper text → graph; a deterministic checker verifies (a) acyclicity, (b) every leaf is either an external citation or a stated assumption, (c) the conclusion node is reachable from the entry point, (d) no node has more in-degree than declared.
- **Rejection condition:** any orphan, any cycle, any unreachable conclusion.
- **Step-level supervision:** each edge is scored individually. The paper's overall coherence score is the *minimum* over edges, not the average — one bad link breaks the chain (per invariant 10, per the unit-distance proof's coherence requirement).

## 5.6 Evolutionary thesis search — "FunSearch for theses" (Invariants 1, 6, 7)

Inspired by FunSearch and AlphaEvolve: treat the *thesis itself* as the object under search, with the gate stack as the evaluator.

- **Mechanism:**
  - Start from a brief (sector, theme, time horizon).
  - A *generator* agent emits 10–50 candidate thesis statements, each in a structured form (`subject`, `claim`, `mechanism`, `time horizon`, `magnitude`, `kill switch`).
  - Each candidate runs through a *cheap-gate subset* (number-tie, base-rate sanity, liquidity, counter-construction).
  - Top survivors are mutated and recombined by a stronger model.
  - Iterate until convergence or a fixed budget.
- **Why this works:** the gate stack is already the evaluator. We are not adding subjective scoring; we are searching over the space of theses *the existing gates would already pass*.
- **What's new:** the thesis is no longer the analyst's first instinct. It is the survivor of a tournament.

## 5.7 Process Reward Model for thesis scoring (Invariant 3)

Train a PRM (in the OpenAI sense) on the historical Helix ledger plus internal step-level annotations from past papers. The PRM scores not "is the conclusion right" but "is each step in the argument supported by the prior step plus the cited evidence."

- **Training data:** the ledger itself provides outcome labels (positions that worked, positions that didn't). Step-level labels come from the post-mortem on each closed position — *which step in the original paper was wrong*.
- **Deployment:** the PRM is one input to the Judge in 5.3.
- **Risk:** PRMs can overfit to the labeler's style. Mitigation: use the PRM only to *flag* steps below a threshold; never to autoreject.

## 5.8 Disjoint-priors agent panel (Invariants 4, 6)

The three AI reviewers should not share priors. Concretely:

- **Reviewer A — Accounting forensics prior.** Trained / prompted to look for non-GAAP discrepancies, working-capital games, recognition policies. (Howard Schilit / Financial Shenanigans style.)
- **Reviewer B — Industry primary-source prior.** Optimized for channel checks, customer concentration, supply chain.
- **Reviewer C — Macro / credit prior.** Optimized for refinancing risk, cycle position, rate sensitivity, demand elasticity.

If all three approve a thesis *via disjoint reasoning paths*, that is the unit-distance proof's "convergence across independent paths" — much stronger than three similar models agreeing.

## 5.9 Constitutional Helix (Invariant 9)

Write a one-page Helix constitution. Examples of provisions:

- "No quantitative cell ships without a named source row."
- "A counter-construction must be attempted and the attempt must be published."
- "Errata ship as new versions; originals remain addressable."
- "If a paper relies on a forecast, the kill switch must be quantitative."
- "Disagreement between reviewers is published, not hidden."

The constitution becomes Gate 20. Every paper passes a final classifier that checks conformance.

## 5.10 The ledger as algebraic structure (Invariants 1, 7)

The ledger is currently a *log*. It is also a *structure* — every position has an entry date, entry price, sector, exit rule, kill switch, current state. That structure admits combinatorial queries.

- **Pigeonhole over the ledger:** instead of screening the universe of tickers for candidates, look for *coincidences* in the ledger — positions where a small set of structured invariants (sector + opposite direction + same kill switch type + overlapping named sources) cluster. That is a counting argument, analogous to the class-group pigeonhole in the unit-distance proof.
- **Concretely:** add a *ledger-query* agent that, before any new paper begins, surfaces past positions whose structure rhymes with the proposed thesis. The new paper must address each surfaced precedent — *this is what we said before; here is what happened; here is why this time is different (or the same).*

This single move converts the ledger from a *track record artifact* into an *idea-generation engine*.

---

# Part VI — Implementation Plan

A four-milestone rollout. Each milestone is shippable on its own and provides measurable value before the next.

## M0 — Constitution and audit (1 week)

**Deliverables:**

- `HELIX_CONSTITUTION.md` at the repo root: ~one page, 10–15 provisions, signed off by the desk lead.
- This research paper merged.
- A short audit document: which gates are currently deterministic vs. LLM-classifier; which are passing/failing on the last 4 papers.

**Exit criterion:** constitution approved; audit reviewed.

## M1 — Argument-graph coherence + disjoint-priors panel (4–6 weeks)

**Deliverables:**

- Argument-graph extractor (LLM) and checker (deterministic). Library: `helix-coherence`.
- Three reviewer specs (A: forensics, B: industry, C: macro/credit). Each is a prompt + an evaluation rubric + a model choice.
- Gate 13 (argument-graph) integrated into pre-publish.
- Reviewer panel composition logged per paper.

**Telemetry:**

- Mean coherence score, distribution of failures by edge type.
- Disagreement matrix across the three reviewers.

**Exit criterion:** one paper passes through the new gate + panel end-to-end. Disagreement matrix recorded.

## M2 — Adversarial debate + counter-construction (6–8 weeks)

**Deliverables:**

- Bull/Bear/Judge debate harness (`helix-debate`). Transcript published as appendix item.
- Counter-construction adversary agent. Spec: given a thesis, find the strongest public dataset / comparable / precedent that would invalidate it. Output: a one-page attempt document.
- Gate 14 (counter-thesis survival) integrated.

**Telemetry:**

- Debate length (turns), Judge confidence.
- Counter-construction outcomes: succeeded (paper killed), survived (paper proceeds), inconclusive (paper proceeds with appendix caveat).

**Exit criterion:** counter-construction has killed at least one candidate paper. (A pipeline that never kills its own papers is not adversarial enough.)

## M3 — Evolutionary thesis search + PRM scoring (8–12 weeks)

**Deliverables:**

- `helix-funsearch`: a thesis-generation and selection harness. Brief in, ranked theses out.
- Process Reward Model: trained on historical ledger + step-level labels.
- Integration of both into the pre-paper phase.

**Telemetry:**

- How many of the final 4 published theses came from the evolutionary search (vs. analyst's initial pick).
- Correlation between PRM step-score variance and final ledger outcome.

**Exit criterion:** at least 1 of the next quarter's 4 papers originates from an evolutionary-search candidate that was not the analyst's first instinct.

## M4 — Constitutional gate + ledger-as-structure (4–6 weeks)

**Deliverables:**

- Gate 20 (constitutional conformance), automated classifier.
- Ledger-query agent: pre-paper precedent surfacing.
- Public-facing appendix template: debate transcript, counter-construction, disagreement matrix, precedent set — all shipped *with the paper*.

**Exit criterion:** the appendix becomes a visible artifact, not an internal one. Institutional readers can audit the *reasoning*, not just the *numbers*.

## Repository layout (target)

```
foundry-equity-research-site/
├── HELIX_CONSTITUTION.md         (new, M0)
├── research/
│   ├── 2026-05-helix-transformation.md  (this document)
│   ├── audits/
│   │   └── 2026-Q2-pre-redesign-audit.md  (M0)
│   └── post-mortems/
│       └── <ticker>-<date>.md     (one per closed position)
├── helix/                          (logical name for the forge — actual repo elsewhere)
│   ├── shapes/                    (M0)
│   │   ├── quality-compounder.yaml
│   │   ├── mean-reversion-short.yaml
│   │   ├── special-situation.yaml
│   │   └── macro-driven.yaml
│   ├── gates/                     (M1–M4)
│   │   ├── 01-number-tie/
│   │   ├── 02-citation-resolver/
│   │   ├── ...
│   │   ├── 13-argument-graph/     (M1)
│   │   ├── 14-counter-thesis/     (M2)
│   │   ├── 15-base-rate/          (M2)
│   │   └── 20-constitution/       (M4)
│   ├── agents/
│   │   ├── reviewer-forensics/    (M1)
│   │   ├── reviewer-industry/     (M1)
│   │   ├── reviewer-macro/        (M1)
│   │   ├── debate-bull/           (M2)
│   │   ├── debate-bear/           (M2)
│   │   ├── debate-judge/          (M2)
│   │   ├── counter-construction/  (M2)
│   │   ├── thesis-generator/      (M3)
│   │   └── ledger-query/          (M4)
│   ├── prm/                       (M3)
│   │   ├── train.py
│   │   ├── data/
│   │   └── checkpoints/
│   └── pipelines/
│       ├── pre-paper.yaml
│       ├── pre-publish.yaml
│       └── post-mortem.yaml
└── ledger/                        (existing — extend with structured fields, M4)
```

## Acceptance criteria, gate-by-gate

For each new gate, what does "passes" mean concretely?

| # | Gate | Pass condition |
|---|------|---------------|
| 13 | Argument-graph | Every edge in the extracted DAG resolves to a cited datum, a previously-established node, or a stated assumption; no orphans, no cycles. |
| 14 | Counter-thesis survival | A serious counter-construction has been attempted, documented, and either addressed in the paper or found to fail. |
| 15 | Base-rate sanity | Every forward-looking quantitative claim is annotated with the historical base rate for similar claims (from the ledger or a base-rate library), and the claim is within 2σ of the base rate *or* the paper explicitly justifies the outlier. |
| 16 | Reflexivity | The paper contains a paragraph addressing "what changes if this becomes consensus." |
| 17 | Liquidity & capacity | Implied position size at desk capacity < a configured fraction of 20-day ADV. |
| 18 | Disclosure footprint | Every material assumption appears in the appendix index; no body-only assumptions. |
| 19 | Audit trail | Every figure ties to `(source, transformation, timestamp)`. |
| 20 | Constitution | Constitutional-classifier returns "compliant" with confidence ≥ threshold. |

## Telemetry & meta-evaluation

The pipeline should measure itself. Minimum dashboard:

- **Paper-level:** gate pass/fail breakdown; mean argument-graph score; counter-construction outcome; debate length and Judge confidence; PRM minimum-step score.
- **Reviewer-panel-level:** pairwise disagreement matrix across A/B/C; how often disagreement holds a paper that would otherwise pass.
- **Ledger-level:** at 12 and 24 months, what gate score correlates with realized outcome? This is the meta-learning signal for the PRM and for future gate weights.
- **Pipeline-level:** % of published papers that originated from evolutionary search; % of candidate papers killed by counter-construction; mean time from brief to publish.

These metrics close the loop: the gates are no longer black boxes, they are instruments with measurable correlation to outcomes.

---

# Part VII — Risks, Failure Modes, Open Questions

## Risks

1. **Gate proliferation reduces throughput.** 20 gates is more than 12. Mitigation: gates 13–20 are *parallel*, not serial, where possible. The argument-graph check, counter-construction, and debate can run concurrently with mechanical gates.

2. **Adversarial debate becomes theater.** If Bull and Bear are the same model with different prompts, the debate is a stylistic exercise, not an epistemic one. Mitigation: enforce model-class diversity (a different model family for at least one of the three roles) and asymmetric information.

3. **PRM overfits to the labeler.** Step-level labels are subjective. Mitigation: PRM never autorejects; it flags. The PRM is one input to the Judge, not a gate on its own.

4. **Evolutionary search produces contrarianism for its own sake.** Mitigation: the gate stack is the evaluator. A thesis that survives the gates is, by construction, well-grounded — contrarian *and* defensible, not contrarian alone.

5. **Constitutional conformance becomes circular.** The constitution must be human-written and human-revisable. If it becomes a moving target adjusted to whatever the model wants to publish, it stops being a constraint.

6. **Counter-construction agent becomes a saboteur.** A counter-construction that succeeds via a marginal datum can kill a strong thesis. Mitigation: the Judge weighs the *strength* of the counter, not its mere existence.

## Open questions

- **How many gates is too many?** This proposal goes from 12 to 20. The right number is probably between 15 and 25; the only way to find out is to instrument and measure.
- **Is the debate transcript a feature or a liability?** Publishing it is unusual. Some readers may find it confidence-inspiring (transparent reasoning); some may find it confidence-eroding (the desk argued with itself before publishing). The market for the artifact will tell us.
- **Should the constitution be public?** Probably yes. The trust differentiator for an institutional research desk is auditability of process, not the secrecy of the prompt stack.
- **Can the PRM be open-sourced?** The PRM trained on the Helix ledger encodes Helix's history. Open-sourcing it is both a flex (here is our process) and a leak (here is what we got wrong). Decide later.

## Things not in this plan that probably should be next

- **A formal-verification layer (Lean-style) for the *quantitative* parts of papers.** AlphaProof shows formal verification is now within reach for non-experts. A long-form research paper isn't a Lean proof, but the *quantitative spine* — the model, the numbers, the comparables — could be expressed in a constrained DSL that admits formal checks.
- **Citation provenance via cryptographic commitment.** Every named source row could be hashed and committed at draft time; later edits to the source flag the paper. This is overkill until it isn't.
- **A multi-modal critique layer.** Charts are part of the argument. A vision model that checks chart-to-text consistency is a natural extension of the existing chart-render gate.

---

# Part VIII — Appendix

## A. Technical notes on the unit-distance proof

Letting `K/ℚ` be a CM field of degree `2f` with totally real subfield `L`, the proof's central inequality is roughly:

```
#{unit distances in P} ≥ |U_K|² · |Λ ∩ B_R| / |W|
```

where `U_K` is the group of unit-norm elements of `𝒪_K`, `Λ ⊂ ℂ^f` is the Minkowski-embedded lattice, `B_R` is a ball of radius `R`, and `W` is a window in one complex coordinate. Choose `R` and the window so that `|Λ ∩ B_R|` and `|W|` are both `≈ N^{1/f}`. Then

```
#{unit distances} / N^{1+δ}
```

is controlled by `|U_K|^{2/f}` divided by a polynomial in `N`. Class field towers give `|U_K| ≥ exp(α f)` for a fixed `α > 0`, which provides the `δ > 0` we need.

The key technical inputs:
- **Golod–Shafarevich (1964):** existence of infinite unramified `p`-class-field towers with bounded root discriminant.
- **Schur–Siegel–Smyth type bounds:** lower bounds on the Mahler measure of algebraic integers (used to ensure that "small" elements in `𝒪_K` are actually rare).
- **Pigeonhole on `Cl(K)`:** enough split primes force collisions in the class group, each collision yields a principal ideal generator with controlled norm.

The original OpenAI manuscript yielded an explicit `δ ≈ 6.24 × 10⁻³⁸`. Sawin's refinement to `δ ≥ 0.014` came from tightening (a) the discriminant control in the class field tower, (b) the constants in the geometric lemma, and (c) the bound on `|U_K|` via better unit-rank arguments.

## B. Glossary

- **CM field:** a number field `K` that is a totally imaginary quadratic extension of a totally real field. Example: `ℚ(i)`, `ℚ(ζ_12)`.
- **Class number `h(K)`:** the order of the ideal class group of `K`; measures the failure of unique factorization in `𝒪_K`.
- **Class field tower:** an infinite sequence of unramified abelian extensions. Golod–Shafarevich gives a criterion for infiniteness.
- **Root discriminant:** `|disc(K)|^{1/[K:ℚ]}`. Bounded root discriminant is the technical condition that makes the tower useful here.
- **Minkowski embedding:** the standard embedding `𝒪_K ↪ ℝ^{r_1} × ℂ^{r_2}` realizing `𝒪_K` as a lattice.
- **Unit-norm element:** an `ξ ∈ 𝒪_K` with `|σ(ξ)| = 1` in every embedding `σ`. Generates a rotation that maps lattice points to lattice points.
- **Process Reward Model (PRM):** a model that assigns a reward to each step in a chain of reasoning, not just to the final answer.
- **Outcome Reward Model (ORM):** the contrasting model that scores only the final answer.

## C. References

### The OpenAI result
- OpenAI. *An OpenAI model has disproved a central conjecture in discrete geometry* (May 2026). https://openai.com/index/model-disproves-discrete-geometry-conjecture/
- OpenAI. *Remarks on the disproof of the unit distance conjecture* (PDF, May 2026). https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf
- W. Sawin. *An explicit lower bound for the unit distance problem*. arXiv:2605.20695 (May 2026). https://arxiv.org/html/2605.20695v1
- G. Kalai. *Amazing: Erdős' Unit Distance Problem was Disproved! It was achieved by AI!* Combinatorics and More (May 2026). https://gilkalai.wordpress.com/2026/05/21/amazing-erdos-unit-distance-problem-was-disproved-it-was-achieved-by-ai/

### Adjacent AI/math results
- B. Romera-Paredes et al. *Mathematical discoveries from program search with large language models* (FunSearch). *Nature*, 2023. https://www.nature.com/articles/s41586-023-06924-6
- DeepMind. *AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms*. 2025. https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- DeepMind. *AI achieves silver-medal standard solving International Mathematical Olympiad problems* (AlphaProof, AlphaGeometry 2). 2024. https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
- H. Lightman et al. *Let's Verify Step by Step*. OpenAI, 2023. arXiv:2305.20050. https://arxiv.org/abs/2305.20050
- X. Wang et al. *Self-Consistency Improves Chain of Thought Reasoning in Language Models*. 2022. arXiv:2203.11171. https://arxiv.org/abs/2203.11171
- G. Irving, P. Christiano, D. Amodei. *AI Safety via Debate*. OpenAI, 2018. arXiv:1805.00899. https://arxiv.org/abs/1805.00899
- J. Wang et al. *Mixture-of-Agents Enhances Large Language Model Capabilities*. 2024. arXiv:2406.04692. https://arxiv.org/abs/2406.04692
- Y. Bai et al. *Constitutional AI: Harmlessness from AI Feedback*. Anthropic, 2022. arXiv:2212.08073. https://arxiv.org/pdf/2212.08073
- *Deep Research: A Survey of Autonomous Research Agents*. 2025. arXiv:2508.12752. https://arxiv.org/html/2508.12752v1

---

*End of paper.*
