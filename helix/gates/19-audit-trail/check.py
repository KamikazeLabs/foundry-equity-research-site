"""Audit-trail gate (gate 19): DSL executor.

Re-executes each figure definition in `transformations.yaml` deterministically
and compares the recomputed value to the published `expected_value` within
the figure's `tolerance_pct`.

Supported ops (see ../19-audit-trail/spec.md):
  identity, sum, subtract, multiply, divide, growth_rate, cagr,
  weighted_avg, irr_simple, multiple_apply

Not yet implemented (in this reference): irr (with cash flow schedule), npv.

Run:

    python check.py <transformations.yaml> <source_values.json>

Where source_values.json is `{ "row_id": numeric_value, ... }` for every
source row referenced by transformations.yaml. Exits 0 on pass, 1 on fail,
2 on usage error.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


SUPPORTED_OPS = {
    "identity", "sum", "subtract", "multiply", "divide",
    "growth_rate", "cagr", "weighted_avg", "irr_simple", "multiple_apply",
}

DEFAULT_TOLERANCE_PCT = 1.0
ABS_TOLERANCE_FLOOR = 1e-9


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    figure_id: str | None = None
    expected: float | None = None
    actual: float | None = None

    def format(self) -> str:
        loc = f" [{self.figure_id}]" if self.figure_id else ""
        return f"{self.severity.upper():5s} {self.code}{loc}: {self.message}"


def _resolve_scalar(value, source_values: dict, prev):
    """Resolve a single scalar arg (row_id, __prev, or literal)."""
    if isinstance(value, str):
        if value == "__prev":
            return prev
        if value in source_values:
            return source_values[value]
        return None
    if isinstance(value, (int, float)):
        return value
    return None


def _apply_op(op: str, args: dict, figure_source, source_values: dict, prev):
    """Apply one DSL op. Returns the result, or None on evaluation failure."""
    if op == "identity":
        if isinstance(figure_source, str):
            return source_values.get(figure_source)
        return None
    if op == "sum":
        inputs = args.get("inputs", [])
        vals = [_resolve_scalar(v, source_values, prev) for v in inputs]
        if any(v is None for v in vals):
            return None
        return sum(vals)
    if op == "subtract":
        a = _resolve_scalar(args.get("from"), source_values, prev)
        b = _resolve_scalar(args.get("value"), source_values, prev)
        if a is None or b is None:
            return None
        return a - b
    if op == "multiply":
        a = _resolve_scalar(args.get("value"), source_values, prev)
        b = _resolve_scalar(args.get("factor"), source_values, prev)
        if a is None or b is None:
            return None
        return a * b
    if op == "divide":
        n = _resolve_scalar(args.get("numerator"), source_values, prev)
        d = _resolve_scalar(args.get("denominator"), source_values, prev)
        if n is None or d is None or d == 0:
            return None
        return n / d
    if op == "growth_rate":
        cur = _resolve_scalar(args.get("current"), source_values, prev)
        pri = _resolve_scalar(args.get("prior"), source_values, prev)
        if cur is None or pri is None or pri == 0:
            return None
        return (cur - pri) / pri
    if op == "cagr":
        start = _resolve_scalar(args.get("start"), source_values, prev)
        end = _resolve_scalar(args.get("end"), source_values, prev)
        years = _resolve_scalar(args.get("years"), source_values, prev)
        if start is None or end is None or years is None or start <= 0 or years <= 0:
            return None
        return (end / start) ** (1.0 / years) - 1
    if op == "weighted_avg":
        vals = [_resolve_scalar(v, source_values, prev) for v in args.get("values", [])]
        wts = [_resolve_scalar(w, source_values, prev) for w in args.get("weights", [])]
        if not vals or len(vals) != len(wts) or any(v is None for v in vals + wts):
            return None
        wsum = sum(wts)
        if wsum == 0:
            return None
        return sum(v * w for v, w in zip(vals, wts)) / wsum
    if op == "irr_simple":
        sp = _resolve_scalar(args.get("start_price"), source_values, prev)
        ep = _resolve_scalar(args.get("end_price"), source_values, prev)
        years = _resolve_scalar(args.get("years"), source_values, prev)
        if sp is None or ep is None or years is None or sp <= 0 or years <= 0:
            return None
        return (ep / sp) ** (1.0 / years) - 1
    if op == "multiple_apply":
        v = _resolve_scalar(args.get("value"), source_values, prev)
        m = _resolve_scalar(args.get("multiple"), source_values, prev)
        if v is None or m is None:
            return None
        return v * m
    return None


def _evaluate_figure(fig_id: str, figure: dict, source_values: dict, findings: list[Finding]) -> None:
    expected = figure.get("expected_value")
    tolerance_pct = figure.get("tolerance_pct", DEFAULT_TOLERANCE_PCT)

    if expected is None:
        findings.append(Finding(
            "error", "MISSING_EXPECTED",
            "figure has no expected_value", figure_id=fig_id,
        ))
        return

    steps = figure.get("steps", [])
    if not steps:
        findings.append(Finding(
            "error", "NO_STEPS", "figure has no steps", figure_id=fig_id,
        ))
        return

    prev = None
    for i, step in enumerate(steps):
        op = step.get("op")
        if op not in SUPPORTED_OPS:
            findings.append(Finding(
                "error", "UNKNOWN_OP",
                f"step {i}: op '{op}' not supported (allowed: {sorted(SUPPORTED_OPS)})",
                figure_id=fig_id,
            ))
            return
        args = step.get("args", {}) or {}
        try:
            result = _apply_op(op, args, figure.get("source"), source_values, prev)
        except (TypeError, ZeroDivisionError, ValueError) as e:
            findings.append(Finding(
                "error", "EVAL_FAILED",
                f"step {i} (op '{op}') raised {type(e).__name__}: {e}",
                figure_id=fig_id,
            ))
            return
        if result is None:
            findings.append(Finding(
                "error", "EVAL_FAILED",
                f"step {i} (op '{op}') could not be evaluated; check args and source values",
                figure_id=fig_id,
            ))
            return
        prev = result

    actual = prev
    abs_tolerance = max(abs(expected) * tolerance_pct / 100.0, ABS_TOLERANCE_FLOOR)
    if abs(actual - expected) > abs_tolerance:
        findings.append(Finding(
            "error", "RECOMPUTE_MISMATCH",
            f"expected {expected}, recomputed {actual:.6g} "
            f"(delta {abs(actual - expected):.6g}; tolerance {abs_tolerance:.6g})",
            figure_id=fig_id, expected=expected, actual=actual,
        ))


def check(transformations: dict, source_values: dict) -> list[Finding]:
    findings: list[Finding] = []
    for fig_id, figure in transformations.items():
        if not isinstance(figure, dict):
            continue
        if "steps" not in figure:
            continue
        _evaluate_figure(fig_id, figure, source_values, findings)
    return findings


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} <transformations.yaml> <source_values.json>", file=sys.stderr)
        return 2
    tpath = Path(argv[1])
    spath = Path(argv[2])
    if not tpath.exists() or not spath.exists():
        print("file not found", file=sys.stderr)
        return 2

    transformations = yaml.safe_load(tpath.read_text()) or {}
    source_values = json.loads(spath.read_text())

    findings = check(transformations, source_values)
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
