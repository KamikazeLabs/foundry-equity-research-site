"""Tests for the counter-thesis gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check  # noqa: E402


def _ok_counter() -> str:
    return """# Counter-construction

## thesis_being_attacked

Test thesis: Company X compounds at 15% for 5 years.

## outcome

partial — the strongest counter weakened the model by ~5%.

## strongest_counter

**Description:** Test description.

**Evidence:**
- Source A
- Source B

**Why it invalidates:** Some reasoning.

**Weakness:** A limitation of the counter.

## all_attempts

1. **Attempt one.** provenance: `fresh`. Result: strong. Used as strongest.

2. **Attempt two.** provenance: `fresh`. Result: weak.

3. **Attempt three.** provenance: `fresh`. Result: failed_to_produce.

4. **Attempt four.** provenance: `ledger`. Result: weak. Surfaced by ledger-query.

5. **Attempt five.** provenance: `fresh`. Result: weak.

6. **Attempt six.** provenance: `delegated`. Raised by macro reviewer; does not count toward the minimum.

## search_space_covered

Examined: filings, reports, ledger, industry data.

## recommendation

ship_with_appendix
"""


def _codes(findings):
    return {f.code for f in findings if f.severity == "error"}


def test_valid_counter_passes():
    assert _codes(check(_ok_counter())) == set()


def test_missing_section():
    text = _ok_counter().replace("## strongest_counter\n", "## strongest_counter_GONE\n")
    assert "MISSING_SECTION" in _codes(check(text))


def test_bad_outcome():
    text = _ok_counter().replace("partial —", "maybe —")
    assert "BAD_OUTCOME" in _codes(check(text))


def test_bad_recommendation():
    text = _ok_counter().replace("ship_with_appendix", "ship_it_now")
    assert "BAD_RECOMMENDATION" in _codes(check(text))


def test_too_few_candidates():
    # Drop attempts 4 and 5; only 3 fresh remain (delegated still doesn't count)
    text = _ok_counter().replace("4. **Attempt four.**", "X. ~~Removed.~~")
    text = text.replace("5. **Attempt five.**", "X. ~~Removed.~~")
    assert "TOO_FEW_CANDIDATES" in _codes(check(text))


def test_delegated_does_not_count_toward_minimum():
    # Replace attempt 5 (fresh) with another delegated; should now have only 4 countable
    text = _ok_counter().replace(
        "5. **Attempt five.** provenance: `fresh`. Result: weak.",
        "5. **Attempt five.** provenance: `delegated`. Result: weak.",
    )
    assert "TOO_FEW_CANDIDATES" in _codes(check(text))


def test_missing_provenance_annotation():
    text = _ok_counter().replace("provenance: `fresh`. Result: weak.", "Result: weak.", 1)
    assert "MISSING_PROVENANCE" in _codes(check(text))


def test_incomplete_strongest():
    text = _ok_counter().replace("**Weakness:** A limitation of the counter.\n", "")
    assert "INCOMPLETE_STRONGEST" in _codes(check(text))


def _check_example(bundle: str) -> list:
    root = Path(__file__).resolve().parents[3]
    return check((root / "examples" / bundle / "counter_attempt.md").read_text())


def test_synthetic_passing():
    findings = _check_example("synthetic-passing")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-passing should pass: " + "; ".join(f.format() for f in errors)


def test_synthetic_quality_compounder():
    findings = _check_example("synthetic-quality-compounder")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-quality-compounder should pass: " + "; ".join(f.format() for f in errors)


def test_synthetic_short():
    findings = _check_example("synthetic-short")
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "synthetic-short should pass: " + "; ".join(f.format() for f in errors)


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
