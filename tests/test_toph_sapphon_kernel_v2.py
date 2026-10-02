from tools.toph_sapphon_kernel_v2 import ADDRESS, life_frame, verify_cycles

def test_address_and_carrier_are_frozen():
    assert ADDRESS == "{{Gg.Aa.Ii.Aa}}"
    f=life_frame(1)
    assert f["SapphonSnapshot"]["state_space"] == "000"
    assert f["TOPHTransport"]["state_out"] == "000"

def test_finite_life_packet_closes_exactly():
    f=life_frame(1)
    assert f["TOPHProject"]["local_packet"] == [-1,0,1]
    assert f["TOPHProject"]["closure"] == "-1 + 0 + 1 = 0"
    assert f["TOPHProve"]["terminal_zero_has_no_residual"] is True

def test_terminal_zero_selects_new_pin_not_dead_dot():
    f=life_frame(1)
    assert f["TOPHTransport"]["next_pin"] == "000"
    assert f["TOPHTransport"]["reuse_dead_dot"] is False

def test_two_cycles_close_cleanly():
    r=verify_cycles(2)
    assert r["status"] == "0e"
    assert all(r["checks"].values())
    assert len(r["frames"]) == 2
