"""Tests for the argument-graph checker."""

from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import check_graph  # noqa: E402


def _ok_graph() -> dict:
    """A passing graph: two well-sourced claims, both load-bearing."""
    return {
        "paper_id": "test",
        "nodes": [
            {"id": "c1", "kind": "citation", "label": "10-K p.45 segment revenue table"},
            {"id": "c2", "kind": "citation", "label": "Channel check Apr 2026"},
            {"id": "c3", "kind": "citation", "label": "Peer ROIC data"},
            {"id": "a1", "kind": "assumption", "label": "Margin expansion sustains 24 months"},
            {"id": "claim1", "kind": "claim", "label": "Segment X grew 18% organic"},
            {"id": "claim2", "kind": "claim", "label": "Market share gains are durable"},
            {"id": "conc", "kind": "conclusion", "label": "Multiple should re-rate to 22x by FY28"},
        ],
        "edges": [
            {"from": "c1", "to": "claim1"},
            {"from": "a1", "to": "claim1"},
            {"from": "c2", "to": "claim2"},
            {"from": "c3", "to": "claim2"},
            {"from": "claim1", "to": "conc", "weight": 0.8},
            {"from": "claim2", "to": "conc", "weight": 0.8},
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
    g["edges"].append({"from": "claim3", "to": "conc", "weight": 0.3})  # non-load-bearing
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
    g["edges"].append({"from": "claim1", "to": "conc2", "weight": 0.8})
    assert "MULTI_CONCLUSION" in _codes(check_graph(g))


def test_dangling_edge():
    g = _ok_graph()
    g["edges"].append({"from": "ghost", "to": "conc", "weight": 0.5})
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


# --- Weight + load-bearing tests (A.6) ---


def test_missing_conclusion_weight():
    """Edges to conclusion must carry a weight."""
    g = _ok_graph()
    for e in g["edges"]:
        if e["to"] == "conc":
            e.pop("weight", None)
    assert "MISSING_CONCLUSION_WEIGHT" in _codes(check_graph(g))


def test_invalid_weight_type():
    g = _ok_graph()
    for e in g["edges"]:
        if e["to"] == "conc":
            e["weight"] = "high"
            break
    assert "BAD_WEIGHT" in _codes(check_graph(g))


def test_invalid_weight_range():
    g = _ok_graph()
    for e in g["edges"]:
        if e["to"] == "conc":
            e["weight"] = 1.5
            break
    assert "BAD_WEIGHT" in _codes(check_graph(g))


def test_load_bearing_single_sourced():
    """A load-bearing edge whose source has only 1 inbound fails."""
    g = _ok_graph()
    # claim2 currently has 2 inbounds (c2, c3); drop one to make it single-sourced
    g["edges"] = [e for e in g["edges"] if not (e["from"] == "c3" and e["to"] == "claim2")]
    g["nodes"] = [n for n in g["nodes"] if n["id"] != "c3"]
    assert "SINGLE_SOURCED_LOAD_BEARING" in _codes(check_graph(g))


def test_low_weight_no_load_bearing_check():
    """An edge below the threshold does not trigger SINGLE_SOURCED_LOAD_BEARING."""
    g = _ok_graph()
    # Make claim2's edge to conclusion non-load-bearing and remove c3 so claim2 is single-sourced
    for e in g["edges"]:
        if e["from"] == "claim2" and e["to"] == "conc":
            e["weight"] = 0.4
    g["edges"] = [e for e in g["edges"] if not (e["from"] == "c3" and e["to"] == "claim2")]
    g["nodes"] = [n for n in g["nodes"] if n["id"] != "c3"]
    findings = check_graph(g)
    assert "SINGLE_SOURCED_LOAD_BEARING" not in _codes(findings)


def test_no_weight_on_non_conclusion_edge_ok():
    """Edges not pointing at the conclusion need no weight."""
    g = _ok_graph()
    # _ok_graph already has unweighted non-conclusion edges; just verify no findings about them
    findings = check_graph(g)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == []


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
