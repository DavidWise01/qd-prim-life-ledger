from tools.l0_osi_stack import (
    BASE_EXPONENT,
    ExactScale,
    FastL0Ledger,
    L0Ledger,
    canonical_overlay_digest,
    carry,
    decode_l2_header,
    encode_l2_frame,
    overlay_due,
    verify,
)


def test_decimal_carry_is_exact():
    assert BASE_EXPONENT == -35
    assert carry(9) == ExactScale(9, -35)
    assert carry(10) == ExactScale(1, -34)
    assert carry(90) == ExactScale(9, -34)
    assert carry(100) == ExactScale(1, -33)
    assert carry(1000) == ExactScale(1, -32)


def test_fast_and_legacy_semantics_match():
    legacy = L0Ledger()
    fast = FastL0Ledger()
    for n in range(1, 1001):
        a = legacy.append()
        b = fast.append()
        assert a.tick == b.tick == n
        assert a.elapsed == b.elapsed
        assert a.state == b.state == -n
    assert legacy.verify()
    assert fast.verify()


def test_overlay_digests_are_canonical():
    a = {"event": "p", "value": 1}
    b = {"value": 1, "event": "p"}
    assert canonical_overlay_digest(a) == canonical_overlay_digest(b)


def test_fast_parent_chain_is_append_only():
    fast = FastL0Ledger()
    a = fast.append()
    b = fast.append()
    c = fast.append()
    assert a.parent_digest == bytes(32)
    assert b.parent_digest == a.digest_bytes
    assert c.parent_digest == b.digest_bytes
    assert fast.verify()


def test_osi_l2_frame_round_trip_fast():
    fast = FastL0Ledger()
    for _ in range(10):
        rec = fast.append()
    frame = encode_l2_frame(rec)
    decoded = decode_l2_header(frame)
    assert decoded["tick"] == 10
    assert decoded["elapsed"] == ExactScale(1, -34)
    assert decoded["state"] == -10
    assert decoded["digest"] == rec.digest


def test_overlay_stride():
    assert overlay_due(10, 10)
    assert overlay_due(100, 10)
    assert not overlay_due(99, 10)


def test_full_verifier():
    assert verify()


from tools.l0_osi_stack import (
    MerkleL0Ledger,
    benchmark_merkle_block_sizes,
    verify_merkle_v3,
)


def test_merkle_blocks_preserve_all_ticks_and_chain_commits():
    ledger = MerkleL0Ledger(block_size=8, retain_leaves=True)
    for _ in range(25):
        ledger.append()
    ledger.finalize()
    assert ledger.tick == 25
    assert len(ledger.leaves) == 25
    assert [c.first_tick for c in ledger.commits] == [1, 9, 17, 25]
    assert [c.last_tick for c in ledger.commits] == [8, 16, 24, 25]
    assert ledger.commits[0].parent_commit == bytes(32)
    assert ledger.commits[1].parent_commit == ledger.commits[0].digest_bytes
    assert ledger.verify()


def test_merkle_tamper_fails_closed():
    ledger = MerkleL0Ledger(block_size=4, retain_leaves=True)
    for _ in range(8):
        ledger.append()
    ledger.finalize()
    assert ledger.verify()
    ledger._leaves[0] = bytes(32)
    assert not ledger.verify()


def test_merkle_v3_verifier():
    assert verify_merkle_v3()


def test_merkle_benchmark_small():
    out = benchmark_merkle_block_sizes(iterations=1000, block_sizes=(4, 8, 16))
    assert out["best_block_size"] in (4, 8, 16)
    assert all(v["verified"] for v in out["results"].values())


from tools.l0_osi_stack import (
    merkle_proof,
    verify_merkle_proof,
    benchmark_merkle_proofs,
)


def test_merkle_inclusion_proofs_all_leaves():
    ledger = MerkleL0Ledger(block_size=8, retain_leaves=True)
    for _ in range(8):
        ledger.append()
    ledger.finalize()
    leaves = list(ledger.leaves)
    root = ledger.commits[0].root
    for i, leaf in enumerate(leaves):
        proof = merkle_proof(leaves, i)
        assert verify_merkle_proof(leaf, proof, root)


def test_merkle_inclusion_proof_rejects_wrong_leaf():
    ledger = MerkleL0Ledger(block_size=8, retain_leaves=True)
    for _ in range(8):
        ledger.append()
    ledger.finalize()
    leaves = list(ledger.leaves)
    root = ledger.commits[0].root
    proof = merkle_proof(leaves, 3)
    assert not verify_merkle_proof(bytes(32), proof, root)


def test_merkle_proof_benchmark_small():
    out = benchmark_merkle_proofs(block_size=8, rounds=100)
    assert out["proof_depth"] == 3
    assert out["all_verified"]
