"""Tests for the liquidity & capacity gate."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check  # noqa: E402


def _codes(findings):
    return {f.code for f in findings if f.severity == "error"}


def test_long_passes():
    f = check({
        "position_size_usd": 5_000_000,
        "adv_20d_usd": 86_000_000,
        "direction": "long",
    })
    assert _codes(f) == set(), [x.format() for x in f]


def test_long_adv_breach():
    f = check({
        "position_size_usd": 30_000_000,    # too large vs 86M ADV * 0.25 = 21.5M cap
        "adv_20d_usd": 86_000_000,
        "direction": "long",
    })
    assert "ADV_BREACH" in _codes(f)


def test_short_passes():
    f = check({
        "position_size_usd": 800_000,
        "adv_20d_usd": 86_000_000,
        "direction": "short",
        "position_size_shares": 4_100_000,
        "shares_available_to_borrow": 8_300_000,
    })
    assert _codes(f) == set(), [x.format() for x in f]


def test_short_borrow_breach():
    f = check({
        "position_size_usd": 800_000,
        "adv_20d_usd": 86_000_000,
        "direction": "short",
        "position_size_shares": 5_000_000,           # 60% of 8.3M
        "shares_available_to_borrow": 8_300_000,
    })
    assert "BORROW_BREACH" in _codes(f)


def test_short_missing_borrow_data():
    f = check({
        "position_size_usd": 800_000,
        "adv_20d_usd": 86_000_000,
        "direction": "short",
    })
    assert "DATA_MISSING" in _codes(f)


def test_missing_required_fields():
    f = check({"direction": "long"})
    assert "DATA_MISSING" in _codes(f)


def test_invalid_position_size():
    f = check({
        "position_size_usd": -100,
        "adv_20d_usd": 86_000_000,
        "direction": "long",
    })
    assert "DATA_MISSING" in _codes(f)


def test_unknown_direction_warns():
    f = check({
        "position_size_usd": 1_000_000,
        "adv_20d_usd": 86_000_000,
        "direction": "neutral",
    })
    warns = {x.code for x in f if x.severity == "warn"}
    assert "UNKNOWN_DIRECTION" in warns


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
