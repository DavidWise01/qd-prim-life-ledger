"""TOPH root0 metronome / frame-distance clock."""
from __future__ import annotations

FPS_TOTAL = 60
FPS_LEFT = 30
FPS_RIGHT = 30
FRAMES_PER_BUBBLE = 2
BUBBLES_PER_SECOND = FPS_TOTAL // FRAMES_PER_BUBBLE
PLANK_TICKS_PER_SECOND = BUBBLES_PER_SECOND
SECONDS_PER_PLANK_TICK = 1 / PLANK_TICKS_PER_SECOND

TICKS_PER_TWO_SECONDS = 60
GENERATIONS = 40
BUBBLES_PER_GENERATION_SCALE = 3
INVARIANT = TICKS_PER_TWO_SECONDS * GENERATIONS * BUBBLES_PER_GENERATION_SCALE

TRAPPED_BUBBLES = 30
RETAINED_DOTS = 20
CUBIC_CELLS = RETAINED_DOTS ** 3
NORMALIZED_CELLS_PER_DOT = CUBIC_CELLS // RETAINED_DOTS


def frame_distance(ticks: int) -> dict:
    if ticks < 0:
        raise ValueError("ticks must be >= 0")
    return {
        "ticks": ticks,
        "frames": ticks * FRAMES_PER_BUBBLE,
        "bubbles": ticks,
        "i_distance": ticks,
        "seconds": ticks * SECONDS_PER_PLANK_TICK,
    }
