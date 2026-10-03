from tools.toph_sapphon_direct_address_v3 import frame, verify

def test_direct_address_reflection_v3():
    assert verify(16)

def test_projection_does_not_change_transport():
    f = frame(1, 127, 7)
    assert f["TOPHProject"]["direct_address_v1"]["address"] == 1023
    assert f["TOPHProject"]["direct_address_v1"]["bits"] == "1111111111"
    assert f["TOPHTransport"]["state_out"] == "000"
    assert f["TOPHTransport"]["next_pin"] == "000"
    assert f["TOPHTransport"]["oe"] is True
