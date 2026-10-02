import copy

import pytest

from tools.toph_merkle_backdraft_v3 import (
    BackdraftConflict,
    BackdraftError,
    backdraft,
    bolt_to_qk,
    demo_graph,
    make_node,
    model,
    put_node,
    resolve_snow,
    validate_graph,
    verify,
)


def test_yes_no_maybe_is_not_probability():
    m = model()
    assert m["tri_state"]["resolved"] == ["Y", "N"]
    assert m["tri_state"]["maybe"] == "?"
    assert m["tri_state"]["probability_layer"] is False
    assert "unresolved provenance" in m["tri_state"]["maybe_meaning"]


def test_backdraft_follows_hashes_and_replays_forward():
    graph, h = demo_graph()
    y = backdraft(h["maybe_y"], graph)
    n = backdraft(h["maybe_n"], graph)
    coop = backdraft(h["coop_y"], graph)
    assert y["state"] == "Y" and y["bit"] == "1"
    assert n["state"] == "N" and n["bit"] == "0"
    assert coop["state"] == "Y"
    assert y["visited"] >= 3


def test_branch_fork_merge_coop_keep_parent_provenance():
    graph, h = demo_graph()
    assert len(graph[h["fork_n"]]["edges"]) == 1
    assert len(graph[h["maybe_y"]]["edges"]) == 2
    assert len(graph[h["maybe_n"]]["edges"]) == 1
    assert len(graph[h["coop_y"]]["edges"]) == 3
    assert graph[h["maybe_y"]]["edges"][0]["parent"] != graph[h["maybe_y"]]["edges"][1]["parent"]


def test_conflicting_merge_fails_closed():
    graph = {}
    y = put_node(graph, make_node("000.y", "Y", "seed", [], 0))
    n = put_node(graph, make_node("000.n", "N", "seed", [], 0))
    conflict = put_node(
        graph,
        make_node(
            "000.merge",
            "?",
            "merge",
            [
                {"parent": y, "op": "HOLD"},
                {"parent": n, "op": "HOLD"},
            ],
            1,
        ),
    )
    with pytest.raises(BackdraftConflict):
        backdraft(conflict, graph)


def test_tamper_detection_fails_closed():
    graph, h = demo_graph()
    bad = copy.deepcopy(graph)
    bad[h["maybe_y"]]["address"] = "tampered"
    with pytest.raises(BackdraftError):
        validate_graph(bad)


def test_maybe_root_without_provenance_fails_closed():
    graph = {}
    maybe = put_node(graph, make_node("000.maybe", "?", "seed", [], 0))
    with pytest.raises(BackdraftError):
        backdraft(maybe, graph)


def test_proof_count_must_equal_snow_count():
    graph, h = demo_graph()
    with pytest.raises(ValueError):
        resolve_snow("00??", [h["maybe_y"]], graph)


def test_backdraft_bolts_into_qk_and_freezes_on_eo():
    m = model()
    graph, h = demo_graph()
    proofs = [h["maybe_n"], h["maybe_n"], h["maybe_n"], h["coop_y"]]
    out = bolt_to_qk(m["demo"]["snow"], proofs, graph, 60)
    assert out["backdraft"]["resolved"] == "000110110001"
    assert out["freeze"] is True
    assert out["status"] == "eo"
    assert len(out["qk"]["handoffs"]) == 2
    assert out["qk"]["handoffs"][0]["digest"] == out["qk"]["handoffs"][1]["digest"]


def test_full_verifier():
    assert verify() is True
