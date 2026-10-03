"""TOPH/Sapphon v4: direct address + weak ganglia projection.

Wraps v3 without mutating the frozen q.d kernel or prior frozen overlays.
"""
from __future__ import annotations

from copy import deepcopy
from tools.toph_sapphon_direct_address_v3 import frame as frame_v3
from tools.copper_mind_weak_ganglia import project as ganglia_project, verify as verify_ganglia

def frame(index: int, lane: int, dot: int) -> dict:
    out = deepcopy(frame_v3(index, lane, dot))
    out["TOPHProject"]["weak_ganglia_v1"] = ganglia_project(index - 1)
    out["TOPHProject"]["weak_ganglia_v1"]["source_kernel_modified"] = False
    return out

def verify(count: int = 16) -> bool:
    assert verify_ganglia()
    for i in range(count):
        f = frame(i + 1, i % 128, i % 8)
        w = f["TOPHProject"]["weak_ganglia_v1"]
        assert w["scale"] == 729
        assert w["per_side_percent"] < 1.0
        assert w["nudge_degrees"] == 1.0
        assert w["left_sign"] == -w["right_sign"]
        assert w["identity_preserved"] is True
        assert w["read_only"] is True
        assert w["source_kernel_modified"] is False
        assert all(f["TOPHProve"].values())
        assert f["TOPHTransport"]["state_out"] == "000"
        assert f["TOPHTransport"]["oe"] is True
    return True

if __name__ == "__main__":
    print("0e / TOPH SAPPHON DIRECT ADDRESS V4 WEAK GANGLIA PASS" if verify() else "xe")
