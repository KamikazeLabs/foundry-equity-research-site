# Gate 16 — Reflexivity check

**Phase:** pre-publish
**Type:** classifier
**Owner:** automation
**Required by shape:** all except `special-situation`

## Purpose

If the thesis becomes consensus, does the trade still work? Many compelling theses are *priced in* the moment they become widely held. The gate forces the paper to address this explicitly. It is a single-paragraph requirement, not a deep analysis — but the paragraph must exist.

## Pass condition

The paper contains an explicit "reflexivity" or "consensus path" section / paragraph addressing:

1. What would the position look like if 70% of the institutional market shared this view?
2. What is the entry rule if the thesis is becoming consensus?
3. What is the exit / sizing adjustment if the position becomes overcrowded?

## Inputs

- `paper.md`

## Outputs

```yaml
passed: bool
findings:
  - severity: error
    code: MISSING | INADEQUATE
    message: "..."
```

## Failure modes the gate catches

- No reflexivity discussion at all.
- A reflexivity discussion that handwaves ("the market will eventually agree").
- A reflexivity discussion that does not specify an entry / exit / sizing implication.

## Failure modes the gate does NOT catch

- Bad reflexivity reasoning. The gate checks for presence and structure, not for quality. The debate handles quality.

## Example acceptable paragraph (~80 words)

> Reflexivity: if this view becomes consensus before the FY27 results print, the multiple expansion compresses our IRR by ~30%. Our entry rule incorporates this — we size down 20% for every 50bp of consensus EPS upgrade above the current $4.10 figure. We exit half the position if Street median reaches $5.10 (90% of our base-case FY27 EPS), regardless of price.

The gate's classifier accepts this. A paper without something like it does not pass.
