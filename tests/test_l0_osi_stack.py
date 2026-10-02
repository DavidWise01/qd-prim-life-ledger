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
