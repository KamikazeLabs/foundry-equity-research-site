"""Counter-thesis survival gate (gate 14).

Verifies that a counter_attempt.md exists for the paper and follows the
schema in `helix/agents/counter-construction/spec.md`:

  - Required sections present (thesis_being_attacked, outcome,
    strongest_counter, all_attempts, search_space_covered, recommendation)
  - outcome is one of {succeeded, failed, partial}
  - all_attempts contains >= 5 entries with provenance `fresh` or `ledger`
    (delegated items do not count toward the minimum, per spec A.5)
  - strongest_counter section has the 4 required labeled subsections
    (Description, Evidence, Why it invalidates, Weakness)
  - search_space_covered is non-empty
  - recommendation is one of {kill, ship_with_appendix, ship_as_is}

This is a structural check; it does NOT evaluate the *quality* of the
counter-construction (the Judge does that).

Run:

    python check.py <counter_attempt.md>

Exits 0 on pass, 1 on fail, 2 on usage error.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


VALID_OUTCOMES = {"succeeded", "failed", "partial"}
VALID_RECOMMENDATIONS = {"kill", "ship_with_appendix", "ship_as_is"}
MIN_FRESH_LEDGER_CANDIDATES = 5
COUNTABLE_PROVENANCES = {"fresh", "ledger"}
ALL_PROVENANCES = {"fresh", "ledger", "delegated"}

REQUIRED_SECTIONS = [
    "thesis_being_attacked",
    "outcome",
    "strongest_counter",
    "all_attempts",
    "search_space_covered",
    "recommendation",
]

STRONGEST_SUBSECTIONS = ["Description", "Evidence", "Why it invalidates", "Weakness"]


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    location: str | None = None

    def format(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"{self.severity.upper():5s} {self.code}{loc}: {self.message}"


def _slice_section(text: str, header: str) -> str | None:
    pat = re.compile(rf"^##\s+{re.escape(header)}\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s+\S", text[start:], re.MULTILINE)
    return text[start:start + nxt.start()] if nxt else text[start:]


def _extract_outcome(section: str) -> str | None:
    line = section.strip().split("\n", 1)[0].strip().lower()
    for o in VALID_OUTCOMES:
        if line.startswith(o):
            return o
    return None


def _extract_recommendation(section: str) -> str | None:
    line = section.strip().split("\n", 1)[0].strip().lower()
    for r in VALID_RECOMMENDATIONS:
        if line.startswith(r):
            return r
    return None


ATTEMPT_RE = re.compile(r"^\d+\.\s+(.+?)(?=^\d+\.|\Z)", re.MULTILINE | re.DOTALL)
PROVENANCE_RE = re.compile(r"provenance:\s*`?(\w+)`?", re.IGNORECASE)


def _count_attempts_by_provenance(section: str) -> dict[str, int]:
    counts = {p: 0 for p in ALL_PROVENANCES}
    counts["missing"] = 0
    for m in ATTEMPT_RE.finditer(section):
        body = m.group(1)
        prov_m = PROVENANCE_RE.search(body)
        if prov_m:
            prov = prov_m.group(1).lower()
            if prov in counts:
                counts[prov] += 1
            else:
                counts["missing"] += 1
        else:
            counts["missing"] += 1
    return counts


def _strongest_has_subsections(section: str) -> tuple[bool, list[str]]:
    missing = []
    for label in STRONGEST_SUBSECTIONS:
        pat = re.compile(rf"\*\*{re.escape(label)}\b", re.IGNORECASE)
        if not pat.search(section):
            missing.append(label)
    return (not missing, missing)


def check(counter_text: str) -> list[Finding]:
    findings: list[Finding] = []

    # required sections
    sections: dict[str, str | None] = {}
    for h in REQUIRED_SECTIONS:
        sections[h] = _slice_section(counter_text, h)
        if sections[h] is None:
            findings.append(Finding(
                "error", "MISSING_SECTION",
                f"required section '## {h}' is absent",
                location=h,
            ))

    # outcome value
    outcome_section = sections.get("outcome")
    if outcome_section is not None:
        outcome = _extract_outcome(outcome_section)
        if outcome is None:
            findings.append(Finding(
                "error", "BAD_OUTCOME",
                f"outcome must begin with one of {sorted(VALID_OUTCOMES)}",
                location="outcome",
            ))

    # recommendation value
    rec_section = sections.get("recommendation")
    if rec_section is not None:
        rec = _extract_recommendation(rec_section)
        if rec is None:
            findings.append(Finding(
                "error", "BAD_RECOMMENDATION",
                f"recommendation must begin with one of {sorted(VALID_RECOMMENDATIONS)}",
                location="recommendation",
            ))

    # all_attempts counts
    attempts_section = sections.get("all_attempts")
    if attempts_section is not None:
        counts = _count_attempts_by_provenance(attempts_section)
        if counts["missing"] > 0:
            findings.append(Finding(
                "error", "MISSING_PROVENANCE",
                f"{counts['missing']} attempt(s) have no provenance annotation; "
                f"every attempt must declare provenance as fresh|ledger|delegated",
                location="all_attempts",
            ))
        countable = counts["fresh"] + counts["ledger"]
        if countable < MIN_FRESH_LEDGER_CANDIDATES:
            findings.append(Finding(
                "error", "TOO_FEW_CANDIDATES",
                f"all_attempts contains only {countable} candidate(s) of provenance "
                f"fresh+ledger (delegated does not count); minimum is "
                f"{MIN_FRESH_LEDGER_CANDIDATES}",
                location="all_attempts",
            ))

    # strongest_counter subsections
    strongest = sections.get("strongest_counter")
    if strongest is not None:
        ok, missing = _strongest_has_subsections(strongest)
        if not ok:
            findings.append(Finding(
                "error", "INCOMPLETE_STRONGEST",
                f"strongest_counter is missing required subsection(s): "
                f"{', '.join(missing)}",
                location="strongest_counter",
            ))

    # search_space_covered non-empty
    space = sections.get("search_space_covered")
    if space is not None and not space.strip():
        findings.append(Finding(
            "error", "EMPTY_SEARCH_SPACE",
            "search_space_covered section is empty",
            location="search_space_covered",
        ))

    return findings


def main(argv):
    if len(argv) != 2:
        print(f"usage: {argv[0]} <counter_attempt.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    findings = check(path.read_text())
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]

    for f in findings:
        print(f.format())

    if errors:
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s) -- gate FAILS", file=sys.stderr)
        return 1
    print(f"\n{len(warns)} warning(s) -- gate PASSES")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
