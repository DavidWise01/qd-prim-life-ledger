from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from tools.toph_qk_handoff_v2 import handoff_twice_and_freeze

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "toph_merkle_backdraft_v3.json"

RESOLVED = {"Y", "N"}
OPS = {"HOLD", "FLIP", "SET_Y", "SET_N"}


class BackdraftError(ValueError):
    pass


class BackdraftConflict(BackdraftError):
    pass


def model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def make_node(address: str, state: str, kind: str, edges: list[dict], tick: int) -> dict:
    if state not in {"Y", "N", "?"}:
        raise ValueError("state must be Y, N, or ?")
    if tick < 0:
        raise ValueError("tick must be nonnegative")
    clean_edges = []
    for edge in edges:
        parent = edge["parent"]
        op = edge["op"]
        if op not in OPS:
            raise ValueError(f"unknown edge op: {op}")
        clean_edges.append({"parent": parent, "op": op})
    return {
        "address": address,
        "state": state,
        "kind": kind,
        "edges": clean_edges,
        "tick": tick,
    }


def node_hash(node: Mapping) -> str:
    return canonical_digest(dict(node))


def put_node(graph: dict[str, dict], node: dict) -> str:
    digest = node_hash(node)
    graph[digest] = node
    return digest


def apply_op(op: str, state: str) -> str:
    if state not in RESOLVED:
        raise BackdraftError("edge op requires a resolved parent state")
    if op == "HOLD":
        return state
    if op == "FLIP":
        return "N" if state == "Y" else "Y"
    if op == "SET_Y":
        return "Y"
    if op == "SET_N":
        return "N"
    raise BackdraftError(f"unknown edge op: {op}")


def validate_graph(graph: Mapping[str, dict]) -> bool:
    for digest, node in graph.items():
        if node_hash(node) != digest:
            raise BackdraftError(f"tamper/hash mismatch at {digest}")
        for edge in node["edges"]:
            if edge["parent"] not in graph:
                raise BackdraftError(f"missing parent {edge['parent']}")
    return True


def backdraft(target: str, graph: Mapping[str, dict]) -> dict:
    validate_graph(graph)
    memo: dict[str, str] = {}
    active: set[str] = set()
    trace: list[dict] = []

    def resolve(digest: str) -> str:
        if digest in memo:
            return memo[digest]
        if digest in active:
            raise BackdraftError("cycle detected")
        if digest not in graph:
            raise BackdraftError(f"unknown target {digest}")

        active.add(digest)
        node = graph[digest]
        edges = node["edges"]

        if not edges:
            if node["state"] not in RESOLVED:
                raise BackdraftError("MAYBE root has no provenance to follow")
            resolved = node["state"]
        else:
            projected = [
                apply_op(edge["op"], resolve(edge["parent"]))
                for edge in edges
            ]
            if len(set(projected)) != 1:
                raise BackdraftConflict(
                    f"parent projections disagree at {node['address']}: {projected}"
                )
            resolved = projected[0]
            if node["state"] in RESOLVED and node["state"] != resolved:
                raise BackdraftConflict(
                    f"stored state disagrees with provenance at {node['address']}"
                )

        active.remove(digest)
        memo[digest] = resolved
        trace.append(
            {
                "hash": digest,
                "address": node["address"],
                "stored_state": node["state"],
                "resolved_state": resolved,
                "kind": node["kind"],
                "parent_count": len(edges),
            }
        )
        return resolved

    state = resolve(target)
    return {
        "target": target,
        "state": state,
        "bit": model()["tri_state"]["bit_mapping"][state],
        "trace": trace,
        "visited": len(memo),
    }


def resolve_snow(pattern: str, proof_targets: list[str], graph: Mapping[str, dict]) -> dict:
    if any(c not in "01?" for c in pattern):
        raise ValueError("snow pattern may contain only 0, 1, ?")
    if pattern.count("?") != len(proof_targets):
        raise ValueError("one proof target is required for each MAYBE cell")

    proofs = iter(proof_targets)
    resolved_bits: list[str] = []
    proof_results: list[dict] = []

    for cell in pattern:
        if cell != "?":
            resolved_bits.append(cell)
            continue
        result = backdraft(next(proofs), graph)
        proof_results.append(result)
        resolved_bits.append(result["bit"])

    return {
        "input": pattern,
        "resolved": "".join(resolved_bits),
        "proofs": proof_results,
        "maybe_count": len(proof_targets),
    }


def bolt_to_qk(
    pattern: str,
    proof_targets: list[str],
    graph: Mapping[str, dict],
    hz: float,
) -> dict:
    recovered = resolve_snow(pattern, proof_targets, graph)
    handoff = handoff_twice_and_freeze(recovered["resolved"], hz)
    if not handoff["freeze"] or handoff["status"] != model()["qk_bolt"]["freeze_sentinel"]:
        raise BackdraftError("resolved Merkle state did not freeze through QK handoff")
    return {
        "backdraft": recovered,
        "qk": handoff,
        "status": handoff["status"],
        "freeze": handoff["freeze"],
    }


def demo_graph() -> tuple[dict[str, dict], dict[str, str]]:
    graph: dict[str, dict] = {}

    root_y = put_node(
        graph,
        make_node("000.vector0.voxel0.vogel0", "Y", "seed", [], 0),
    )
    fork_n = put_node(
        graph,
        make_node(
            "000.vector0.voxel0.vogel1",
            "N",
            "fork",
            [{"parent": root_y, "op": "FLIP"}],
            1,
        ),
    )
    maybe_y = put_node(
        graph,
        make_node(
            "000.vector0.voxel1.vogel0",
            "?",
            "merge",
            [
                {"parent": root_y, "op": "HOLD"},
                {"parent": fork_n, "op": "FLIP"},
            ],
            2,
        ),
    )
    maybe_n = put_node(
        graph,
        make_node(
            "000.vector0.voxel1.vogel1",
            "?",
            "branch",
            [{"parent": maybe_y, "op": "FLIP"}],
            3,
        ),
    )
    coop_y = put_node(
        graph,
        make_node(
            "000.vector1.voxel0.vogel0",
            "?",
            "coop",
            [
                {"parent": root_y, "op": "HOLD"},
                {"parent": fork_n, "op": "FLIP"},
                {"parent": maybe_y, "op": "HOLD"},
            ],
            4,
        ),
    )
    return graph, {
        "root_y": root_y,
        "fork_n": fork_n,
        "maybe_y": maybe_y,
        "maybe_n": maybe_n,
        "coop_y": coop_y,
    }


def verify() -> bool:
    m = model()
    assert m["authority"]["frozen_mother_kernel_modified"] is False
    assert m["authority"]["qk_v2_modified"] is False
    assert m["tri_state"]["literal"] == "yes/no/maybe"
    assert m["tri_state"]["probability_layer"] is False
    assert m["tri_state"]["bit_mapping"] == {"Y": "1", "N": "0"}
    assert m["qk_bolt"]["retest_count"] == 2
    assert m["qk_bolt"]["freeze_sentinel"] == "eo"

    graph, h = demo_graph()
    assert validate_graph(graph) is True
    assert backdraft(h["root_y"], graph)["state"] == "Y"
    assert backdraft(h["fork_n"], graph)["state"] == "N"
    assert backdraft(h["maybe_y"], graph)["state"] == "Y"
    assert backdraft(h["maybe_n"], graph)["state"] == "N"
    assert backdraft(h["coop_y"], graph)["state"] == "Y"

    proofs = [h["maybe_n"], h["maybe_n"], h["maybe_n"], h["coop_y"]]
    out = bolt_to_qk(m["demo"]["snow"], proofs, graph, 60)
    assert out["backdraft"]["resolved"] == m["demo"]["resolved_qk_window"]
    assert out["status"] == "eo"
    assert out["freeze"] is True
    assert len(out["qk"]["handoffs"]) == 2
    assert out["qk"]["handoffs"][0]["digest"] == out["qk"]["handoffs"][1]["digest"]
    return True


if __name__ == "__main__":
    graph, hashes = demo_graph()
    proofs = [
        hashes["maybe_n"],
        hashes["maybe_n"],
        hashes["maybe_n"],
        hashes["coop_y"],
    ]
    print(json.dumps(backdraft(hashes["maybe_y"], graph), indent=2, sort_keys=True))
    print(json.dumps(bolt_to_qk(model()["demo"]["snow"], proofs, graph, 60), indent=2, sort_keys=True))
    print("eo / TOPH MERKLE BACKDRAFT V3 PASS" if verify() else "xe")
