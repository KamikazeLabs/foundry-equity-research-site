"""Argument-graph coherence checker.

A paper passes if its extracted argument graph satisfies:
  1. Every node has a unique id.
  2. Every node has a valid kind (citation, assumption, claim, conclusion).
  3. Every edge source and target exists.
  4. Exactly one conclusion node.
  5. No directed cycles.
  6. Every claim/conclusion node has at least one inbound edge.
  7. Every leaf (no inbound) is kind citation or assumption.
  8. Every node is reachable backwards from the conclusion (no orphans).
  9. Edge weights, where present, are numeric in [0.0, 1.0].
 10. Every edge to the conclusion node has an explicit `weight`.
 11. For every load-bearing edge (weight >= LOAD_BEARING_THRESHOLD) on the
     conclusion, the source node has >= 2 inbound edges (multi-sourced).

Run:
    python check.py <graph.json>

Exits 0 if the gate passes, 1 if it fails, 2 on usage error.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


VALID_LEAF_KINDS = {"citation", "assumption"}
VALID_INTERNAL_KINDS = {"claim", "conclusion"}
VALID_NODE_KINDS = VALID_LEAF_KINDS | VALID_INTERNAL_KINDS

LOAD_BEARING_THRESHOLD = 0.7


@dataclass
class Finding:
    severity: str   # "error" | "warn"
    code: str
    message: str
    node: str | None = None

    def format(self) -> str:
        loc = f" [{self.node}]" if self.node else ""
        return f"{self.severity.upper():5s} {self.code}{loc}: {self.message}"


def _validate_weight(w, edge_repr: str, findings: list[Finding]) -> bool:
    """Return True if the supplied weight is present and valid."""
    if w is None:
        return False
    if isinstance(w, bool) or not isinstance(w, (int, float)):
        findings.append(Finding(
            "error", "BAD_WEIGHT",
            f"edge {edge_repr}: weight must be a number, got {type(w).__name__} ({w!r})"
        ))
        return False
    if w < 0.0 or w > 1.0:
        findings.append(Finding(
            "error", "BAD_WEIGHT",
            f"edge {edge_repr}: weight must be in [0.0, 1.0], got {w}"
        ))
        return False
    return True


def _build_adjacency(edges, known_ids, conclusion_id, findings):
    incoming: dict[str, list[str]] = defaultdict(list)
    outgoing: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        s, t = e.get("from"), e.get("to")
        if s not in known_ids:
            findings.append(Finding("error", "BAD_EDGE", f"edge from missing node '{s}'"))
            continue
        if t not in known_ids:
            findings.append(Finding("error", "BAD_EDGE", f"edge to missing node '{t}'"))
            continue
        w = e.get("weight")
        edge_repr = f"{s} -> {t}"
        if w is not None:
            _validate_weight(w, edge_repr, findings)
        elif t == conclusion_id:
            findings.append(Finding(
                "error", "MISSING_CONCLUSION_WEIGHT",
                f"edge {edge_repr}: weight is required on edges to the conclusion node"
            ))
        incoming[t].append(s)
        outgoing[s].append(t)
    return incoming, outgoing


def _detect_cycles(node_ids, outgoing, findings):
    color = {nid: "white" for nid in node_ids}

    def dfs(u):
        color[u] = "gray"
        for v in outgoing.get(u, []):
            if color.get(v) == "gray":
                findings.append(Finding("error", "CYCLE", f"cycle through edge {u} -> {v}", u))
            elif color.get(v) == "white":
                dfs(v)
        color[u] = "black"

    for nid in node_ids:
        if color[nid] == "white":
            dfs(nid)


def _reverse_reachable(start, incoming):
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        for src in incoming.get(u, []):
            if src not in seen:
                seen.add(src)
                q.append(src)
    return seen


def _check_load_bearing_multi_sourcing(edges, conclusion_id, id_to_node, incoming, findings):
    """For every load-bearing edge to the conclusion, source must have >= 2 inbound edges."""
    for e in edges:
        if e.get("to") != conclusion_id:
            continue
        src = e.get("from")
        if src not in id_to_node:
            continue
        w = e.get("weight")
        if w is None or isinstance(w, bool) or not isinstance(w, (int, float)):
            continue
        if w < LOAD_BEARING_THRESHOLD:
            continue
        src_inbound_count = len(incoming.get(src, []))
        if src_inbound_count < 2:
            findings.append(Finding(
                "error", "SINGLE_SOURCED_LOAD_BEARING",
                f"load-bearing edge ({src} -> conclusion, weight {w}) but source has only "
                f"{src_inbound_count} inbound edge(s); load-bearing claims must be multi-sourced",
                src,
            ))


def check_graph(graph: dict) -> list[Finding]:
    findings: list[Finding] = []
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    seen_ids: set[str] = set()
    id_to_node: dict[str, dict] = {}
    for n in nodes:
        nid = n.get("id")
        if not nid:
            findings.append(Finding("error", "MISSING_ID", "node without id"))
            continue
        if nid in seen_ids:
            findings.append(Finding("error", "DUP_ID", f"duplicate id '{nid}'", nid))
            continue
        seen_ids.add(nid)
        id_to_node[nid] = n
        if n.get("kind") not in VALID_NODE_KINDS:
            findings.append(Finding(
                "error", "BAD_KIND",
                f"invalid kind '{n.get('kind')}' (allowed: {sorted(VALID_NODE_KINDS)})", nid,
            ))

    conclusions = [nid for nid, n in id_to_node.items() if n.get("kind") == "conclusion"]
    if not conclusions:
        findings.append(Finding("error", "NO_CONCLUSION", "graph has no conclusion node"))
    elif len(conclusions) > 1:
        findings.append(Finding(
            "error", "MULTI_CONCLUSION",
            f"graph has {len(conclusions)} conclusion nodes; expected exactly one"
        ))

    conclusion_id = conclusions[0] if len(conclusions) == 1 else None
    incoming, outgoing = _build_adjacency(edges, seen_ids, conclusion_id, findings)

    _detect_cycles(list(id_to_node.keys()), outgoing, findings)

    for nid, n in id_to_node.items():
        inbound = incoming.get(nid, [])
        outbound = outgoing.get(nid, [])
        kind = n.get("kind")
        if not inbound and not outbound:
            findings.append(Finding("error", "ORPHAN", "isolated node (no edges in or out)", nid))
            continue
        if not inbound:
            if kind not in VALID_LEAF_KINDS:
                findings.append(Finding(
                    "error", "UNJUSTIFIED",
                    f"node has no inbound justification but kind is '{kind}' (must be one of {sorted(VALID_LEAF_KINDS)})",
                    nid,
                ))

    if conclusion_id is not None:
        reachable = _reverse_reachable(conclusion_id, incoming)
        for nid in id_to_node:
            if nid not in reachable:
                findings.append(Finding(
                    "error", "UNREACHABLE",
                    "node does not support the conclusion (no directed path to conclusion)", nid,
                ))
        _check_load_bearing_multi_sourcing(edges, conclusion_id, id_to_node, incoming, findings)

    return findings


def main(argv):
    if len(argv) != 2:
        print(f"usage: {argv[0]} <graph.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    graph = json.loads(path.read_text())
    findings = check_graph(graph)
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
