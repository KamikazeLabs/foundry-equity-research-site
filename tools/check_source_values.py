"""Lint source_values.json against transformations.yaml.

Checks that every `row_*` identifier referenced from a transformations
file is present in the corresponding source_values file. Also reports
unused entries (in source_values but not referenced).

Useful as a quick check before running gate 19.

Run:
    python tools/check_source_values.py <transformations.yaml> <source_values.json>

Exits 0 if all referenced row_ids are present, 1 if any are missing,
2 on usage error.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROW_ID_PAT = re.compile(r"\brow_[a-z0-9_]+\b")


def referenced_row_ids(node) -> set[str]:
    """Walk a YAML/JSON-shaped data structure and collect every row_X reference."""
    ids: set[str] = set()

    def walk(n):
        if isinstance(n, dict):
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
        elif isinstance(n, str):
            ids.update(ROW_ID_PAT.findall(n))

    walk(node)
    return ids


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <transformations.yaml> <source_values.json>", file=sys.stderr)
        return 2
    tpath = Path(argv[1])
    spath = Path(argv[2])
    if not tpath.exists() or not spath.exists():
        print("file not found", file=sys.stderr)
        return 2

    t = yaml.safe_load(tpath.read_text()) or {}
    s = json.loads(spath.read_text())

    referenced = referenced_row_ids(t)
    available = set(s.keys())

    missing = sorted(referenced - available)
    unused = sorted(available - referenced)

    if missing:
        print(f"MISSING from source_values.json ({len(missing)}):")
        for r in missing:
            print(f"  - {r}")
    if unused:
        print(f"UNUSED in source_values.json ({len(unused)}):")
        for r in unused:
            print(f"  - {r}")

    if missing:
        return 1
    print(f"All {len(referenced)} referenced row_id(s) present; "
          f"{len(unused)} unused.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
