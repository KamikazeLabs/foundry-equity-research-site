"""Liquidity & capacity gate (gate 17).

Required for `mean-reversion-short` and `special-situation` shapes; optional
for others when implied size > capacity threshold.

Checks:
  1. position_size_usd / (adv_20d_usd * adv_fraction) <= 1.0
  2. For shorts: position_size_shares / shares_available_to_borrow <= 0.5

Configurable via module constants. Run:

    python check.py <inputs.yaml>

Where inputs.yaml has the shape (see helix/gates/17-liquidity/example_inputs.yaml):

    position_size_usd: ...
    adv_20d_usd: ...
    direction: long | short
    position_size_shares: ...        # required if direction == short
    shares_available_to_borrow: ...  # required if direction == short

Exits 0 on pass, 1 on fail, 2 on usage error.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path


ADV_FRACTION = 0.25                    # exit in ~4 trading days at 100% participation
BORROW_UTILIZATION_CEILING = 0.5       # max 50% of available borrow


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    metric: str | None = None
    value: float | None = None
    threshold: float | None = None

    def format(self) -> str:
        m = f" {self.metric}={self.value} threshold={self.threshold}" if self.metric else ""
        return f"{self.severity.upper():5s} {self.code}:{m} {self.message}"


def _load_inputs(path: Path) -> dict:
    text = path.read_text()
    # Accept either JSON or minimal YAML (key: value per line, no nesting).
    if text.lstrip().startswith("{"):
        return json.loads(text)
    out: dict = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.lower() in ("null", "none", ""):
            out[k.strip()] = None
            continue
        try:
            out[k.strip()] = float(v) if "." in v or "e" in v.lower() else int(v)
        except ValueError:
            out[k.strip()] = v.strip('"').strip("'")
    return out


def check(inputs: dict) -> list[Finding]:
    findings: list[Finding] = []

    pos_usd = inputs.get("position_size_usd")
    adv_usd = inputs.get("adv_20d_usd")
    direction = inputs.get("direction")

    if pos_usd is None or adv_usd is None:
        findings.append(Finding(
            "error", "DATA_MISSING",
            "position_size_usd and adv_20d_usd are required"
        ))
        return findings

    if not isinstance(pos_usd, (int, float)) or pos_usd <= 0:
        findings.append(Finding("error", "DATA_MISSING", f"invalid position_size_usd: {pos_usd}"))
        return findings
    if not isinstance(adv_usd, (int, float)) or adv_usd <= 0:
        findings.append(Finding("error", "DATA_MISSING", f"invalid adv_20d_usd: {adv_usd}"))
        return findings

    adv_ratio = pos_usd / (adv_usd * ADV_FRACTION)
    if adv_ratio > 1.0:
        findings.append(Finding(
            "error", "ADV_BREACH",
            f"position size cannot be exited inside the configured window "
            f"(implied exit-days fraction at {ADV_FRACTION*100:.0f}% participation: "
            f"{pos_usd / (adv_usd * ADV_FRACTION):.2f})",
            metric="adv_ratio", value=round(adv_ratio, 4), threshold=1.0,
        ))

    if direction == "short":
        shares = inputs.get("position_size_shares")
        borrow = inputs.get("shares_available_to_borrow")
        if shares is None or borrow is None:
            findings.append(Finding(
                "error", "DATA_MISSING",
                "shorts require position_size_shares and shares_available_to_borrow"
            ))
        else:
            if not isinstance(borrow, (int, float)) or borrow <= 0:
                findings.append(Finding(
                    "error", "DATA_MISSING",
                    f"invalid shares_available_to_borrow: {borrow}"
                ))
            else:
                borrow_util = shares / borrow
                if borrow_util > BORROW_UTILIZATION_CEILING:
                    findings.append(Finding(
                        "error", "BORROW_BREACH",
                        f"short position exceeds borrow utilization ceiling",
                        metric="borrow_utilization", value=round(borrow_util, 4),
                        threshold=BORROW_UTILIZATION_CEILING,
                    ))
    elif direction not in ("long", None):
        findings.append(Finding(
            "warn", "UNKNOWN_DIRECTION",
            f"direction '{direction}' not recognized; treating as long"
        ))

    return findings


def main(argv):
    if len(argv) != 2:
        print(f"usage: {argv[0]} <inputs.yaml|inputs.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    findings = check(_load_inputs(path))
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
