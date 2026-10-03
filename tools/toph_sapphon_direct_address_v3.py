"""TOPH/Sapphon direct-address reflection v3.

Read-only post-kernel adapter. Wraps v2 and adds the 10-bit
7-bit-lane + 3-bit-dot projection only at TOPHProject.
"""
from __future__ import annotations

from copy import deepcopy
from tools.toph_sapphon_kernel_v2 import life_frame
from tools.copper_mind_direct_address import project, verify as verify_direct

def frame(index: int, lane: int, dot: int) -> dict:
    base = deepcopy(life_frame(index))
    base["TOPHProject"]["direct_address_v1"] = project(lane, dot)
    base["TOPHProject"]["direct_address_v1"]["source_kernel_modified"] = False
    return base

def verify(count: int = 8) -> bool:
    assert verify_direct()
    for i in range(count):
        lane = i % 128
        dot = i % 8
        f = frame(i + 1, lane, dot)
        p = f["TOPHProject"]["direct_address_v1"]
        assert p["address"] == (lane << 3) | dot
        assert p["read_only"] is True
        assert p["source_kernel_modified"] is False
        assert f["TOPHTransport"]["state_out"] == "000"
        assert f["TOPHTransport"]["oe"] is True
        assert all(f["TOPHProve"].values())
    return True

if __name__ == "__main__":
    print("0e / TOPH SAPPHON DIRECT ADDRESS V3 PASS" if verify() else "xe")
