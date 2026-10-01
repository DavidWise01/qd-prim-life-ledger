from tools.frame_clock import (
    BUBBLES_PER_SECOND,
    CUBIC_CELLS,
    FPS_LEFT,
    FPS_RIGHT,
    FPS_TOTAL,
    FRAMES_PER_BUBBLE,
    INVARIANT,
    NORMALIZED_CELLS_PER_DOT,
    PLANK_TICKS_PER_SECOND,
    RETAINED_DOTS,
    TICKS_PER_TWO_SECONDS,
    frame_distance,
)

def test_frame_split_and_bubble_clock():
    assert FPS_TOTAL == 60
    assert FPS_LEFT == FPS_RIGHT == 30
    assert FRAMES_PER_BUBBLE == 2
    assert BUBBLES_PER_SECOND == PLANK_TICKS_PER_SECOND == 30
    assert TICKS_PER_TWO_SECONDS == 60

def test_root0_distance_tick():
    s = frame_distance(60)
    assert s["frames"] == 120
    assert s["bubbles"] == 60
    assert s["i_distance"] == 60
    assert s["seconds"] == 2

def test_foam_reduction_and_7200_invariant():
    assert RETAINED_DOTS == 20
    assert CUBIC_CELLS == 8000
    assert NORMALIZED_CELLS_PER_DOT == 400
    assert INVARIANT == 7200
