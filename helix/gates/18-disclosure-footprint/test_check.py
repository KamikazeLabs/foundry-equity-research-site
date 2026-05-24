"""Tests for the disclosure-footprint gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check  # noqa: E402


def _ok_pair():
    paper = """# Title

The thesis relies on `a_margin_persist` and `a_no_disruption`.
We also assume `a_growth_continues` continues through FY28.
"""
    appendix = """# Appendix

## Source rows
| id | value |
|----|-------|
| `row_revenue` | $1B |

## Assumptions
| id | text | body reference |
|----|------|----------------|
| `a_margin_persist` | Gross margin sustains within 100bp | financial-model |
| `a_no_disruption` | No tech disruption | durability |
| `a_growth_continues` | Growth continues at FY25 rate | financial-model |
"""
    return paper, appendix


def _codes(findings):
    return {f.code for f in findings if f.severity == "error"}


def test_valid_pair():
    paper, appendix = _ok_pair()
    findings = check(paper, appendix)
    assert _codes(findings) == set(), [x.format() for x in findings]


def test_body_only_assumption():
    paper, appendix = _ok_pair()
    paper += "\nAlso we assume `a_invented` which is not in the appendix.\n"
    assert "BODY_ONLY_ASSUMPTION" in _codes(check(paper, appendix))


def test_appendix_only_assumption():
    paper, appendix = _ok_pair()
    appendix = appendix.replace(
        "| `a_growth_continues` | Growth continues at FY25 rate | financial-model |",
        "| `a_growth_continues` | Growth continues at FY25 rate | financial-model |\n"
        "| `a_unused` | Floating dead assumption | nowhere |",
    )
    assert "APPENDIX_ONLY_ASSUMPTION" in _codes(check(paper, appendix))


def test_duplicate_assumption():
    paper, appendix = _ok_pair()
    appendix = appendix.replace(
        "| `a_no_disruption` | No tech disruption | durability |",
        "| `a_no_disruption` | No tech disruption | durability |\n"
        "| `a_no_disruption` | Duplicate row | nowhere |",
    )
    assert "DUPLICATE_ASSUMPTION" in _codes(check(paper, appendix))


def test_no_assumptions_section():
    paper, _ = _ok_pair()
    appendix = "# Appendix\n\n## Source rows\n| `row_x` | 1 |\n"
    assert "NO_ASSUMPTIONS_SECTION" in _codes(check(paper, appendix))


def _check_example(bundle: str) -> list:
    root = Path(__file__).resolve().parents[3]
    paper = (root / "examples" / bundle / "paper.md").read_text()
    appendix = (root / "examples" / bundle / "appendix.md").read_text()
    return check(paper, appendix)


def test_real_example_synthetic_passing():
    findings = _check_example("synthetic-passing")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-passing should pass gate 18: " + "; ".join(f.format() for f in errors)


def test_real_example_synthetic_quality_compounder():
    findings = _check_example("synthetic-quality-compounder")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-quality-compounder should pass gate 18: " + "; ".join(f.format() for f in errors)


def test_real_example_synthetic_short():
    findings = _check_example("synthetic-short")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-short should pass gate 18: " + "; ".join(f.format() for f in errors)


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
