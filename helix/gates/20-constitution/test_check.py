"""Tests for the constitution conformance gate."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check, REQUIRED_GATES  # noqa: E402


def _ok_telemetry() -> dict:
    gate_results = {g: {"passed": True} for g in REQUIRED_GATES}
    gate_results["12-ai-concurrence"] = {"passed": True}
    gate_results["17-liquidity"] = {"passed": True}
    gate_results["20-constitution"] = {"passed": True}
    return {
        "constitution_sha": "deadbeef",
        "gate_results": gate_results,
        "reviewer_panel": {
            "disjoint_priors_satisfied": True,
            "distinct_families_count": 2,
        },
        "publish_outputs": {
            "appendix_disagreement_matrix_present": True,
            "appendix_debate_transcript_present": True,
        },
    }


def _ok_paper() -> str:
    return """# Test paper

## One-page summary

Position. **Kill switch (quantitative):** thesis invalidates if:
- inventory days fall below 100 for two consecutive quarters
- same-store sales return to >= +2% YoY
- gross margin contracts more than 250bp from FY25

**Horizon:** 18 months.
"""


def _codes(findings):
    return {f.code for f in findings if f.severity == "error"}


def test_valid_passes():
    assert _codes(check(_ok_telemetry(), _ok_paper())) == set()


def test_missing_gate_fails():
    t = _ok_telemetry()
    del t["gate_results"]["13-argument-graph"]
    assert "GATE_MISSING" in _codes(check(t, _ok_paper()))


def test_failed_gate_caught():
    t = _ok_telemetry()
    t["gate_results"]["13-argument-graph"] = {"passed": False}
    assert "GATE_FAILED" in _codes(check(t, _ok_paper()))


def test_disjoint_priors_violation():
    t = _ok_telemetry()
    t["reviewer_panel"]["disjoint_priors_satisfied"] = False
    assert "DISJOINT_PRIORS_VIOLATION" in _codes(check(t, _ok_paper()))


def test_one_family_caught():
    t = _ok_telemetry()
    t["reviewer_panel"]["distinct_families_count"] = 1
    assert "INSUFFICIENT_FAMILIES" in _codes(check(t, _ok_paper()))


def test_disagreement_not_published():
    t = _ok_telemetry()
    t["publish_outputs"]["appendix_disagreement_matrix_present"] = False
    assert "DISAGREEMENT_NOT_PUBLISHED" in _codes(check(t, _ok_paper()))


def test_no_constitution_sha():
    t = _ok_telemetry()
    del t["constitution_sha"]
    assert "NO_CONSTITUTION_SHA" in _codes(check(t, _ok_paper()))


def test_kill_switch_not_quantitative():
    paper = """# Test paper

## One-page summary

**Kill switch:** invalidates if anything goes wrong; we get out.
"""
    assert "KILL_SWITCH_NOT_QUANTITATIVE" in _codes(check(_ok_telemetry(), paper))


def test_kill_switch_no_comparison():
    paper = """# Test paper

## One-page summary

**Kill switch:** 100% inventory thresholds 250bp.
"""
    # has numbers + units but no comparison verb / operator
    assert "KILL_SWITCH_NO_COMPARISON" in _codes(check(_ok_telemetry(), paper))


def test_no_kill_switch_section():
    paper = "# Test paper\n\nNo summary, no kill switch."
    assert "NO_KILL_SWITCH" in _codes(check(_ok_telemetry(), paper))


def _load_bundle(bundle: str) -> tuple[dict, str]:
    import yaml as _yaml
    root = Path(__file__).resolve().parents[3]
    t = _yaml.safe_load((root / "examples" / bundle / "telemetry.yaml").read_text())
    p = (root / "examples" / bundle / "paper.md").read_text()
    return t, p


def test_synthetic_passing_passes():
    t, p = _load_bundle("synthetic-passing")
    findings = check(t, p)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-passing should pass gate 20: " + "; ".join(f.format() for f in errors)


def test_synthetic_short_passes():
    t, p = _load_bundle("synthetic-short")
    findings = check(t, p)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-short should pass gate 20: " + "; ".join(f.format() for f in errors)


def test_synthetic_quality_compounder_is_held():
    """The held bundle has telemetry showing gate 12 + 20 failed; gate 20
    runnable should also detect this as non-conforming."""
    t, p = _load_bundle("synthetic-quality-compounder")
    findings = check(t, p)
    errors = [f for f in findings if f.severity == "error"]
    assert errors, "synthetic-quality-compounder (held) should fail gate 20"


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and callable(v)]
    failed = []
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed.append(t.__name__)
    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    print(f"\nAll {len(tests)} tests passed")
