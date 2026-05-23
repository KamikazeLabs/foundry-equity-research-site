"""Tests for the argument-graph checker."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check_graph  # noqa: E402


def _ok_graph() -> dict:
    return {
        "paper_id": "test",
        "nodes": [
            {"id": "c1", "kind": "citation", "label": "10-K p.45 segment revenue table"},
            {"id": "c2", "kind": "citation", "label": "Channel check Apr 2026"},
            {"id": "a1", "kind": "assumption", "label": "Margin expansion sustains 24 months"},
            {"id": "claim1", "kind": "claim", "label": "Segment X grew 18% organic"},
            {"id": "claim2", "kind": "claim", "label": "Market share gains are durable"},
            {"id": "conc", "kind": "conclusion", "label": "Multiple should re-rate to 22x by FY28"},
        ],
        "edges": [
            {"from": "c1", "to": "claim1"},
            {"from": "c2", "to": "claim2"},
            {"from": "claim1", "to": "conc"},
            {"from": "claim2", "to": "conc"},
            {"from": "a1", "to": "conc"},
        ],
    }


def _codes(findings):
    return {f.code for f in findings if f.severity == "error"}


def test_valid_graph():
    g = _ok_graph()
    findings = check_graph(g)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], f"expected no errors, got {[f.format() for f in errors]}"


def test_orphan_node():
    g = _ok_graph()
    g["nodes"].append({"id": "orphan", "kind": "claim", "label": "Floating claim"})
    assert "ORPHAN" in _codes(check_graph(g))


def test_cycle():
    g = _ok_graph()
    g["edges"].append({"from": "conc", "to": "claim1"})
    assert "CYCLE" in _codes(check_graph(g))


def test_unjustified_claim():
    g = _ok_graph()
    g["nodes"].append({"id": "claim3", "kind": "claim", "label": "Bare claim"})
    g["edges"].append({"from": "claim3", "to": "conc"})
    assert "UNJUSTIFIED" in _codes(check_graph(g))


def test_no_conclusion():
    g = _ok_graph()
    for n in g["nodes"]:
        if n["kind"] == "conclusion":
            n["kind"] = "claim"
    assert "NO_CONCLUSION" in _codes(check_graph(g))


def test_multi_conclusion():
    g = _ok_graph()
    g["nodes"].append({"id": "conc2", "kind": "conclusion", "label": "Second conclusion"})
    g["edges"].append({"from": "claim1", "to": "conc2"})
    assert "MULTI_CONCLUSION" in _codes(check_graph(g))


def test_dangling_edge():
    g = _ok_graph()
    g["edges"].append({"from": "ghost", "to": "conc"})
    assert "BAD_EDGE" in _codes(check_graph(g))


def test_duplicate_id():
    g = _ok_graph()
    g["nodes"].append(deepcopy(g["nodes"][0]))
    assert "DUP_ID" in _codes(check_graph(g))


def test_unreachable_subgraph():
    g = _ok_graph()
    g["nodes"].append({"id": "side_cite", "kind": "citation", "label": "Unused source"})
    g["nodes"].append({"id": "side_claim", "kind": "claim", "label": "Unused claim"})
    g["edges"].append({"from": "side_cite", "to": "side_claim"})
    assert "UNREACHABLE" in _codes(check_graph(g))


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and callable(v)]
    failed: list[str] = []
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
