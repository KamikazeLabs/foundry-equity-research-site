"""Constitution conformance gate (gate 20).

Aggregates upstream gate results from telemetry.yaml and applies the
provision -> check mapping from helix/gates/20-constitution/spec.md.

Implemented checks (deterministic or heuristic):

  Sec II.5  kill switch quantitative language present
  Sec III.6 argument graph passed (delegated to gate 13's recorded result)
  Sec III.7 counter-construction passed (delegated to gate 14's recorded result)
  Sec III.8 disagreement matrix is published (telemetry assertion)
  Sec IV.9  disjoint priors satisfied (telemetry assertion)
  Sec V.11  every required gate passed (telemetry: gate_results.*.passed)
  Sec VI.15 constitution_sha recorded in telemetry

Not implemented (out of scope for runnable check; remain in the spec):
  Sec I.1 / I.2 / IV.10 / V.12 / VI.13 / VI.14

REQUIRED_GATES below names the gates that V.11 enforces. The legacy
12-ai-concurrence gate is treated as optional during transition; the
runtime can flip it back to required by editing the set.

Run:

    python check.py <telemetry.yaml> <paper.md>

Exits 0 on pass, 1 on fail, 2 on usage error.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


REQUIRED_GATES = {
    "01-number-tie",
    "02-citation-resolver",
    "03-date-consistency",
    "04-ticker-validity",
    "05-chart-render",
    "06-font-embedding",
    "07-brand-check",
    "08-toc-parity",
    "09-page-budget",
    "10-disclaimer",
    "11-spell-grammar",
    "13-argument-graph",
    "14-counter-thesis",
    "15-base-rate",
    "16-reflexivity",
    "18-disclosure-footprint",
    "19-audit-trail",
    # 12-ai-concurrence: legacy; not required during transition
    # 17-liquidity: shape-dependent
    # 20-constitution: not required-by-self
}

KILL_SWITCH_NUMERIC_PAT = re.compile(
    r"\d+(?:\.\d+)?\s*(?:%|bp|x|×|USD|days|months|quarters|MM|M|B)",
    re.IGNORECASE,
)
KILL_SWITCH_COMPARISON_PAT = re.compile(
    r"\b(?:above|below|less than|greater than|exceeds?|breaks?|falls?|"
    r"declines?|cuts?|drops?|grows?|expands?|invalidates?|<|>|<=|>=)\b",
    re.IGNORECASE,
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    provision: str | None = None

    def format(self) -> str:
        prov = f" [{self.provision}]" if self.provision else ""
        return f"{self.severity.upper():5s} {self.code}{prov}: {self.message}"


def _slice_section(text: str, header: str) -> str | None:
    pat = re.compile(rf"^##\s+{re.escape(header)}\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s+\S", text[start:], re.MULTILINE)
    return text[start:start + nxt.start()] if nxt else text[start:]


_SECTION_BODY_PAT = re.compile(r"^##\s+(.+?)$([\s\S]*?)(?=^##\s+|\Z)", re.MULTILINE)
_KILL_SWITCH_MENTION_PAT = re.compile(r"kill\s+switch", re.IGNORECASE)


def _check_kill_switch(paper_text: str, findings: list[Finding]) -> None:
    # Concatenate every H2 section that mentions "kill switch" anywhere
    # (title or body). This handles papers where the substance lives in the
    # one-page summary and a separate "## Kill switch" section just refers back.
    relevant_blobs = []
    for m in _SECTION_BODY_PAT.finditer(paper_text):
        title, body = m.group(1).strip(), m.group(2)
        combined = title + "\n" + body
        if _KILL_SWITCH_MENTION_PAT.search(combined):
            relevant_blobs.append(combined)

    if not relevant_blobs:
        findings.append(Finding(
            "error", "NO_KILL_SWITCH",
            "no section in the paper mentions a kill switch",
            provision="Sec II.5",
        ))
        return

    blob = "\n\n".join(relevant_blobs)

    if not KILL_SWITCH_NUMERIC_PAT.search(blob):
        findings.append(Finding(
            "error", "KILL_SWITCH_NOT_QUANTITATIVE",
            "kill-switch context contains no numeric thresholds "
            "(%, bp, x, USD, days, months, quarters)",
            provision="Sec II.5",
        ))
    if not KILL_SWITCH_COMPARISON_PAT.search(blob):
        findings.append(Finding(
            "error", "KILL_SWITCH_NO_COMPARISON",
            "kill-switch context contains no comparison language "
            "(above/below/exceeds/breaks/<,>)",
            provision="Sec II.5",
        ))


def _check_upstream_gates(telemetry: dict, findings: list[Finding]) -> None:
    gate_results = telemetry.get("gate_results", {})
    for gate in REQUIRED_GATES:
        result = gate_results.get(gate)
        if result is None:
            findings.append(Finding(
                "error", "GATE_MISSING",
                f"required gate '{gate}' has no telemetry record",
                provision="Sec V.11",
            ))
            continue
        if not result.get("passed", False):
            findings.append(Finding(
                "error", "GATE_FAILED",
                f"required gate '{gate}' did not pass",
                provision="Sec V.11",
            ))


def _check_disjoint_priors(telemetry: dict, findings: list[Finding]) -> None:
    panel = telemetry.get("reviewer_panel", {})
    if not panel.get("disjoint_priors_satisfied", False):
        findings.append(Finding(
            "error", "DISJOINT_PRIORS_VIOLATION",
            "reviewer panel does not satisfy disjoint-priors requirement",
            provision="Sec IV.9",
        ))
    distinct = panel.get("distinct_families_count")
    if distinct is not None and distinct < 2:
        findings.append(Finding(
            "error", "INSUFFICIENT_FAMILIES",
            f"reviewer panel has only {distinct} distinct model family/families "
            f"(>= 2 required)",
            provision="Sec IV.9",
        ))


def _check_disagreement_published(telemetry: dict, findings: list[Finding]) -> None:
    outputs = telemetry.get("publish_outputs", {}) or {}
    if not outputs.get("appendix_disagreement_matrix_present", False):
        findings.append(Finding(
            "error", "DISAGREEMENT_NOT_PUBLISHED",
            "appendix does not include the disagreement matrix",
            provision="Sec III.8",
        ))


def _check_constitution_sha(telemetry: dict, findings: list[Finding]) -> None:
    sha = telemetry.get("constitution_sha")
    if not sha:
        findings.append(Finding(
            "error", "NO_CONSTITUTION_SHA",
            "telemetry does not record constitution_sha",
            provision="Sec VI.15",
        ))


def check(telemetry: dict, paper_text: str) -> list[Finding]:
    findings: list[Finding] = []
    _check_kill_switch(paper_text, findings)
    _check_upstream_gates(telemetry, findings)
    _check_disjoint_priors(telemetry, findings)
    _check_disagreement_published(telemetry, findings)
    _check_constitution_sha(telemetry, findings)
    return findings


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} <telemetry.yaml> <paper.md>", file=sys.stderr)
        return 2
    tpath = Path(argv[1])
    ppath = Path(argv[2])
    if not tpath.exists() or not ppath.exists():
        print("file not found", file=sys.stderr)
        return 2

    telemetry = yaml.safe_load(tpath.read_text()) or {}
    paper_text = ppath.read_text()

    findings = check(telemetry, paper_text)
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
