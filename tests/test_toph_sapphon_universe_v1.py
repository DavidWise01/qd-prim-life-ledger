import importlib.util
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "tools" / "toph_sapphon_universe_v1.py"
sp = importlib.util.spec_from_file_location("u", p)
u = importlib.util.module_from_spec(sp)
sp.loader.exec_module(u)

def test_all():
    assert all(u.invariants().values())
    assert u.gravity_metric(1000) == (1.0, 0.0)
    assert u.response_from_delta(u.gravity_metric(500)[1]) == "release/outward"
    assert u.response_from_delta(u.gravity_metric(1500)[1]) == "binding/inward"

    pressures = [900 + i for i in range(12)] + [1100 - i for i in range(12)]
    assert abs(u.weighted_homeostasis(u.sample_universe(pressures))) < 1e-12

    for a in range(1024):
        assert u.direct10_pack(*u.direct10_unpack(a)) == a
