# `helix/agents/` — agent specifications

Each agent in the Helix pipeline has a spec file: role, phase, model class, system prompt, evaluation rubric, independence requirements, and failure modes.

## Agent inventory

| Slug | Role | Phase | Milestone |
|------|------|-------|-----------|
| `shape-selector` | Picks the paper shape from the brief | pre-paper | M0 (existing in pipeline; spec only) |
| `reviewer-forensics` | Accounting-forensics-prior AI reviewer | pre-publish | M1 |
| `reviewer-industry` | Industry-primary-sources-prior AI reviewer | pre-publish | M1 |
| `reviewer-macro` | Macro/credit-prior AI reviewer | pre-publish | M1 |
| `debate-bull` | Argues the long case in adversarial debate | pre-publish | M2 |
| `debate-bear` | Argues the short / counter case in debate | pre-publish | M2 |
| `debate-judge` | Decides the debate against the constitution | pre-publish | M2 |
| `counter-construction` | Builds the public-data counterexample to the thesis | pre-publish | M2 |
| `thesis-generator` | Generates candidate theses for evolutionary search | pre-paper | M3 |
| `ledger-query` | Surfaces precedent positions from the ledger | pre-paper | M4 |

## Independence requirements

The three reviewers (`forensics`, `industry`, `macro`) must:

1. Run with **different system prompts** (the rubric files in each agent dir).
2. Have **no shared context** during their pass — each receives the paper and metadata independently, no awareness of the other reviewers' outputs.
3. **Model-class diversity** where feasible: at least one of the three runs on a different model family than the other two.

The same independence rules apply to debate roles: `debate-bull` and `debate-bear` do not see each other's planning notes, only their statements during the debate.

## Spec template

Every agent spec contains:

- **Role** — one sentence
- **Phase** — when the agent runs
- **Model class** — broad LM | specialist | classifier
- **Inputs**
- **Outputs** (structured)
- **System prompt** (full)
- **Evaluation rubric** (how downstream agents score this output)
- **Independence requirements**
- **Failure modes**
- **Example** (compact I/O)
