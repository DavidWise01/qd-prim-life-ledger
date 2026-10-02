from tools.l0_osi_stack import (
    BASE_EXPONENT,
    ExactScale,
    L0Ledger,
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


def test_one_tick_is_minus_one():
    ledger = L0Ledger()
    for n in range(1, 101):
        rec = ledger.append()
        assert rec.tick == n
        assert rec.state == -n
    assert ledger.verify()


def test_overlays_share_clock_without_forced_update():
    ledger = L0Ledger()
    rec = ledger.append(
        physics={"event": "p"},
        chemistry={},
        cellular={},
    )
    assert rec.physics == {"event": "p"}
    assert rec.chemistry == {}
    assert rec.cellular == {}


def test_osi_l2_frame_round_trip():
    ledger = L0Ledger()
    for _ in range(10):
        rec = ledger.append()
    frame = encode_l2_frame(rec)
    decoded = decode_l2_header(frame)
    assert decoded["tick"] == 10
    assert decoded["elapsed"] == ExactScale(1, -34)
    assert decoded["state"] == -10
    assert decoded["digest"] == rec.digest()


def test_overlay_stride():
    assert overlay_due(10, 10)
    assert overlay_due(100, 10)
    assert not overlay_due(99, 10)


def test_full_verifier():
    assert verify()
