from tools.toph_sapphon_soft_transmon_infra import frame, verify_cycle

def test_infrastructure_phase_cycle_closes_at_oe():
    r = verify_cycle()
    assert r["status"] == "0e"
    assert all(r["checks"].values())

def test_tick_is_bound_to_sapphon_globe_and_toph_commit():
    f = frame(1)
    assert f["SoftTransmonClock"]["phase"] == 0.25
    assert f["SoftTransmonClock"]["local_states"] == 8
    assert f["SapphonSnapshot"]["globe"] == "GLOBE[1]"
    assert f["TOPHCommit"]["append_only"] is True
    assert len(f["TOPHCommit"]["sha256"]) == 64
    assert all(f["TOPHProve"].values())

def test_fourth_tick_is_oe_transport_checkpoint():
    f = frame(4)
    assert f["SoftTransmonClock"]["phase"] == 0.0
    assert f["TOPHTransport"]["oe"] is True
    assert f["TOPHProject"]["seed_resolved"] == "0.0.0"
