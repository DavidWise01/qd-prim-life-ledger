from tools.toph_sapphon_direct_address_v4 import frame, verify

def test_v4_weak_ganglia_reflection():
    assert verify(32)

def test_v4_preserves_direct_address_and_transport():
    f = frame(8, 127, 7)
    assert f["TOPHProject"]["direct_address_v1"]["address"] == 1023
    assert f["TOPHProject"]["weak_ganglia_v1"]["scale"] == 729
    assert f["TOPHProject"]["weak_ganglia_v1"]["nudge_degrees"] == 1.0
    assert f["TOPHTransport"]["state_out"] == "000"
    assert f["TOPHTransport"]["next_pin"] == "000"
