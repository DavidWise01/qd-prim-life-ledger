from tools.copper_mind_direct_address import (
    LANES, DOT_STATES, ADDRESS_COUNT, pack, unpack, lane_block, project, verify
)

def test_direct_address_contract():
    assert verify()
    assert LANES == 128
    assert DOT_STATES == 8
    assert ADDRESS_COUNT == 1024

def test_bijection():
    addresses = [pack(lane, dot) for lane in range(128) for dot in range(8)]
    assert addresses == list(range(1024))
    assert all(unpack(a) == divmod(a, 8) for a in addresses)

def test_lane_isomorphism():
    base = lane_block(0)
    for lane in range(128):
        assert tuple(a - lane * 8 for a in lane_block(lane)) == base

def test_projection_bits():
    p = project(127, 7)
    assert p["address"] == 1023
    assert p["bits"] == "1111111111"
    assert p["lane_bits"] == "1111111"
    assert p["dot_bits"] == "111"
    assert p["read_only"] is True
