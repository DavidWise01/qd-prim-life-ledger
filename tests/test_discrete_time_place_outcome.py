from tools.discrete_time_place_outcome import (
    MOVES,
    PIN_TARGETS,
    TIME_CYCLE,
    ZERO_LINE,
    bind_pipeline,
    outcome_label,
    resolve_no_choice,
    verify,
)

def test_signed_outcome_labels():
    assert outcome_label(-1) == "bad_outcome_timeline"
    assert outcome_label(0) == "implicit_natural_reference"
    assert outcome_label(1) == "good_outcome_timeline"

def test_zero_line_keeps_implicit_reference_and_one_explicit_marker():
    assert ZERO_LINE == (0, 0, 0, 0, 0, "{{1.00}}")

def test_time_closes_to_zero():
    assert TIME_CYCLE == (-1, 0, 1, 0)
    assert sum(TIME_CYCLE) == 0
    assert (1 / 10) * 10 * 0 == 0

def test_no_choice_resolves_packet_and_pins_direction():
    r = resolve_no_choice(3, "xr", -1)
    assert r["growth"] == 27
    assert r["notation"] == "{{n}}^3"
    assert r["packet"]["choice"] == "no"
    assert r["packet"]["consequence"] == "natural"
    assert r["packet"]["outcome"] == -1
    assert r["packet"]["direction"] == "xr"
    assert r["pin"] == "xr{}"
    assert r["pin"] in PIN_TARGETS

def test_movement_primitive():
    assert MOVES == (0, "xu", "yd", "xr", "yl")

def test_final_kernel_binding_is_append_only_and_frozen():
    b = bind_pipeline()
    assert list(b) == ["Event", "Commit", "Prove", "Project", "Transport"]
    assert b["Commit"]["append_only"] is True
    assert all(b["Prove"].values())
    assert b["Transport"]["closure"] == "oe"
    assert b["Transport"]["frozen"] is True
    assert verify() is True
