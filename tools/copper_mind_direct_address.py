"""10-bit direct-address projection for the frozen q.d kernel.

Post-kernel/read-only adapter:
  7-bit lane (0..127) + 3-bit local dot (0..7) = 10-bit address (0..1023).
"""
from __future__ import annotations

LANE_BITS = 7
DOT_BITS = 3
LANES = 1 << LANE_BITS
DOT_STATES = 1 << DOT_BITS
ADDRESS_BITS = LANE_BITS + DOT_BITS
ADDRESS_COUNT = 1 << ADDRESS_BITS
CONTRACT_SHA256 = "55116a0e12b3b8254b484a784a5f549455d0ccf0e60d96f049bf4fb7e66ce99a"

def pack(lane: int, dot: int) -> int:
    if not 0 <= lane < LANES:
        raise ValueError("lane must be in 0..127")
    if not 0 <= dot < DOT_STATES:
        raise ValueError("dot must be in 0..7")
    return (lane << DOT_BITS) | dot

def unpack(address: int) -> tuple[int, int]:
    if not 0 <= address < ADDRESS_COUNT:
        raise ValueError("address must be in 0..1023")
    return address >> DOT_BITS, address & (DOT_STATES - 1)

def lane_block(lane: int) -> tuple[int, ...]:
    return tuple(pack(lane, dot) for dot in range(DOT_STATES))

def project(lane: int, dot: int) -> dict:
    address = pack(lane, dot)
    return {
        "lane": lane,
        "dot": dot,
        "address": address,
        "bits": f"{address:010b}",
        "lane_bits": f"{lane:07b}",
        "dot_bits": f"{dot:03b}",
        "local_volume": DOT_STATES,
        "read_only": True,
    }

def verify() -> bool:
    seen = set()
    base = lane_block(0)
    for lane in range(LANES):
        block = lane_block(lane)
        assert tuple(x - lane * DOT_STATES for x in block) == base
        for dot in range(DOT_STATES):
            address = pack(lane, dot)
            assert unpack(address) == (lane, dot)
            seen.add(address)
    assert seen == set(range(ADDRESS_COUNT))
    assert ADDRESS_COUNT == 1024
    assert DOT_STATES == 2 ** 3
    return True

if __name__ == "__main__":
    print("0e / COPPER MIND DIRECT ADDRESS V1 PASS" if verify() else "xe")
