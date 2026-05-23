# `helix/prm/` — Process Reward Model

**Direct inspiration:** "Let's Verify Step by Step" (Lightman et al., OpenAI 2023). Step-level supervision (PRM) outperforms outcome-level (ORM) for long reasoning chains; the gap widens with sample size.

**Premise:** Helix already has the ingredients to train a PRM specifically for equity-research argument steps:
- The historical ledger provides outcome labels (positions that worked, positions that didn't).
- The post-mortem on every closed position locates *which step* in the original paper was wrong.

A trained PRM scores not "is the conclusion right" but "is each step in the argument supported by the prior step + the cited evidence."

## Training data spec

One training example per *step* in a historical paper. Schema:

```yaml
example_id: "..."                    # unique
paper_id: "..."                      # the source paper
step_id: "..."                       # node id in the extracted argument graph
step_text: "..."                     # the claim or transition
inbound_evidence: [...]              # node ids of cited justifications
step_kind: "citation_to_claim" | "claim_to_claim" | "assumption_to_claim" | "claim_to_conclusion"
label: "correct" | "weak" | "incorrect" | "unknown"
label_source: "outcome" | "analyst_post_mortem" | "judge_finding"
ledger_outcome:
  position_id: "..."
  closed_at: "..."
  realized_return: float
  vs_thesis: "exceeded" | "matched" | "underperformed" | "inverted"
```

A "step" is an edge in the argument graph. Labels come from three sources:

1. **Outcome.** Position closed and realized return matched / missed the thesis. Weak signal — does not localize the wrong step.
2. **Post-mortem.** After a position closes, the analyst writes which step turned out to be wrong. Strong signal — direct step-level label.
3. **Judge finding.** During the pre-publish debate, if the Judge flagged a specific edge as weakly supported, that edge gets a `weak` label even if the position is still open.

Per the OpenAI PRM800K paper, ~100K step-level labels are sufficient for a useful PRM in a constrained domain. Helix's historical ledger is much smaller than that — likely a few thousand papers × few dozen steps each = order 10⁵ steps. Bootstrap with AI-generated weak labels (judge findings, see above) and high-quality labels from the analyst post-mortem corpus.

## Deployment

The PRM is **never** an autonomous reject. It is a flag.

- During pre-publish: the PRM scores every edge in the extracted argument graph. Edges below a configurable threshold appear as `warn`-severity findings on the gate-13 report.
- During FunSearch: PRM scores can feed into the fitness function as a side input.
- During post-mortem: PRM scores at publish time vs. realized outcome become the meta-learning signal.

## Training approach

- **Base model:** any reasoning-capable LM that supports per-token reward fine-tuning.
- **Loss:** standard PRM loss (BCE on per-step correct/incorrect; weak labels weighted 0.3).
- **Refresh cadence:** quarterly, once per published-papers batch.
- **Cross-validation:** hold out the most recent quarter's papers; PRM is evaluated on how well its publish-time step scores correlate with realized outcomes.

## Files (to be added in M3)

```
prm/
├── README.md                  (this file)
├── data_format.md             (the schema above, expanded)
├── train.py                   (training script)
├── eval.py                    (post-deployment evaluation against held-out outcomes)
├── data/                      (gitignored; lives in private storage)
│   ├── raw/                   (step-level labels from past papers)
│   └── prepared/              (training tensors)
└── checkpoints/               (gitignored)
```

## Risks (already noted in the transformation paper Part VII)

1. **Overfit to the labeler.** Mitigation: the PRM never auto-rejects; it flags. The Judge weighs PRM signals along with the debate.
2. **Outcome bias.** A correct step may sit inside a paper that lost money for reasons unrelated to that step. Mitigation: weight `post_mortem` labels much higher than `outcome` labels in training.
3. **Label sparsity.** Few historical post-mortems; need to bootstrap. Mitigation: start labeling now; the PRM gets better every quarter.
