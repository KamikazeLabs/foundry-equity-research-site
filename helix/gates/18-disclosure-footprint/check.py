"""Disclosure-footprint gate (gate 18).

Verifies that every assumption referenced from the body has an entry in the
appendix's Assumptions section, and every appendix assumption is referenced
from the body. Duplicate assumption entries (same `id`) also fail.

Run:

    python check.py <paper.md> <appendix.md>

Exits 0 on pass, 1 on fail, 2 on usage error.

This is a structural check; it does not evaluate the truth of any assumption.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    location: str | None = None

    def format(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"{self.severity.upper():5s} {self.code}{loc}: {self.message}"


# Inline references in the body look like `a_some_id` (backticked snake_case
# starting with `a_`). The convention is enforced by the appendix table format.
BODY_REF_RE = re.compile(r"`(a_[a-z0-9_]+)`")

# Appendix assumptions are table rows under the "## Assumptions" heading.
# Match the leading id cell of a markdown table row, ignoring header / divider rows.
APPENDIX_ROW_RE = re.compile(r"^\|\s*`(a_[a-z0-9_]+)`\s*\|", re.MULTILINE)


def _extract_body_refs(body_text: str) -> set[str]:
    return set(BODY_REF_RE.findall(body_text))


def _extract_appendix_assumption_ids(appendix_text: str) -> tuple[list[str], set[str]]:
    """Return (ordered list of ids found, set of duplicates)."""
    section = _slice_section(appendix_text, "Assumptions")
    if section is None:
        return [], set()
    ids = APPENDIX_ROW_RE.findall(section)
    seen, dups = set(), set()
    for i in ids:
        if i in seen:
            dups.add(i)
        seen.add(i)
    return ids, dups


def _slice_section(text: str, header: str) -> str | None:
    """Return the text starting from `## {header}` up to the next `## ` heading."""
    pat = re.compile(rf"^##\s+{re.escape(header)}\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s+\S", text[start:], re.MULTILINE)
    if nxt:
        return text[start:start + nxt.start()]
    return text[start:]


def check(paper_text: str, appendix_text: str) -> list[Finding]:
    findings: list[Finding] = []

    body_refs = _extract_body_refs(paper_text)
    appendix_ids_list, dups = _extract_appendix_assumption_ids(appendix_text)
    appendix_ids = set(appendix_ids_list)

    if not appendix_ids:
        findings.append(Finding(
            "error", "NO_ASSUMPTIONS_SECTION",
            "appendix has no '## Assumptions' section, or it contains no `a_*` rows"
        ))

    for d in sorted(dups):
        findings.append(Finding(
            "error", "DUPLICATE_ASSUMPTION",
            f"assumption id appears more than once in appendix", location=d,
        ))

    for ref in sorted(body_refs - appendix_ids):
        findings.append(Finding(
            "error", "BODY_ONLY_ASSUMPTION",
            "body references assumption id that does not appear in the appendix",
            location=ref,
        ))

    for ref in sorted(appendix_ids - body_refs):
        findings.append(Finding(
            "error", "APPENDIX_ONLY_ASSUMPTION",
            "appendix declares assumption id that is not referenced from the body",
            location=ref,
        ))

    return findings


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} <paper.md> <appendix.md>", file=sys.stderr)
        return 2
    paper = Path(argv[1])
    appendix = Path(argv[2])
    if not paper.exists() or not appendix.exists():
        print("file not found", file=sys.stderr)
        return 2

    findings = check(paper.read_text(), appendix.read_text())
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
