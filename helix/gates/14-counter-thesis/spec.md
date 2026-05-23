# Gate 14 — Counter-thesis survival

**Phase:** pre-publish
**Type:** classifier (over the counter-construction agent's output)
**Owner:** automation; desk lead approves any override
**Required by shape:** all

## Purpose

A paper does not ship without a documented counter-construction attempt. This gate enforces that *the attempt was made and the artifact exists* (not whether it succeeded). Quality of the attempt is a separate evaluation by the Judge.

## Pass condition

1. A `counter_attempt.md` exists for the paper.
2. The document follows the schema in `helix/agents/counter-construction/spec.md`.
3. `outcome` is one of `succeeded | failed | partial`.
4. `all_attempts` contains at least five distinct candidate counter-constructions.
5. `strongest_counter` is fully populated.
6. `search_space_covered` is non-empty and specific.
7. If `recommendation == kill`, either:
   - the paper has been withdrawn (gate passes; paper does not ship), or
   - the desk lead has signed off on a documented rebuttal (gate passes; paper ships with appendix entry).
8. If `recommendation == ship_with_appendix`, the published paper's appendix contains an entry that addresses the counter.

## Inputs

- `counter_attempt.md`
- `paper.md` (to verify appendix entry exists if required)

## Outputs

```yaml
passed: bool
findings:
  - severity: error | warn
    code: MISSING | SCHEMA | TOO_FEW_CANDIDATES | UNADDRESSED | OTHER
    message: "..."
```

## Failure modes the gate catches

- No counter-construction attempt at all.
- Document exists but is incomplete (missing `strongest_counter`, missing `all_attempts`).
- Counter-construction recommended `ship_with_appendix` but the paper does not address the counter in its appendix.
- Counter-construction recommended `kill` but the paper is queued for publish without a documented override.

## Failure modes the gate does NOT catch

- Quality of the counter-construction attempt. (The Judge evaluates that.)
- Whether the counter is correct. (That's an editorial judgment.)
