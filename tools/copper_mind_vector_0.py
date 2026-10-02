"""Copper Mind Vector 0 — frozen post-kernel symbolic overlay.

This is a model/analog layer, not a claim about measured Earth mechanics.
"""
from __future__ import annotations

from dataclasses import dataclass

EXP_MIN=-36
EXP_MAX=36
SHELL_WIDTH=10.0
PUSH=1.25
PUSHES_PER_SHELL=8
SHELLS=72
SUPERCYCLE_SHELLS=3
PUSHES_PER_SUPERCYCLE=24
SUPERCYCLES=24
CENTER=5.0
G=1.0
BREAKOUT_THRESHOLD=1.02
FORCE_CYCLE=("strong","middle","weak","weak","middle","strong")
SIGN_CYCLE="-++--+"
STATE_CENTER="000"
CONTRACT_SHA256="986a36616d7c1d49a89dc053ebb038d662b6757a87800da751b6fb95608efb1b"

@dataclass(frozen=True)
class RipplePoint:
    shell:int
    push_index:int
    forward:float
    reverse:float
    center:float
    ternary_phase:int

def ripple_point(shell:int,push_index:int)->RipplePoint:
    if not (0 <= shell < SHELLS):
        raise ValueError("shell out of range")
    if not (0 <= push_index <= PUSHES_PER_SHELL):
        raise ValueError("push_index out of range")
    f=push_index*PUSH
    r=SHELL_WIDTH-f
    phase=(-1,0,1)[(shell*PUSHES_PER_SHELL+push_index)%3]
    return RipplePoint(shell,push_index,f,r,(f+r)/2,phase)

def force_state(step:int)->tuple[str,str]:
    i=step%len(FORCE_CYCLE)
    return FORCE_CYCLE[i],SIGN_CYCLE[i]

def breakout(p:float)->bool:
    # Model-local rule: g remains pinned at 1; p must be negative,
    # and combined magnitude must meet the declared 1.02 threshold.
    return p < 0 and abs(G)+abs(p) >= BREAKOUT_THRESHOLD

def prove()->dict[str,bool]:
    centers=[ripple_point(s,j).center for s in range(SHELLS) for j in range(PUSHES_PER_SHELL+1)]
    boundary_phases=[ripple_point(s,0).ternary_phase for s in range(6)]
    return {
        "ten_equals_eight_pushes": PUSH*PUSHES_PER_SHELL == SHELL_WIDTH,
        "mirror_center_is_five": all(x==CENTER for x in centers),
        "three_shell_phase_reset": boundary_phases[:3] == boundary_phases[3:6],
        "seventy_two_shells": EXP_MAX-EXP_MIN == SHELLS,
        "twenty_four_supercycles": SHELLS//SUPERCYCLE_SHELLS == SUPERCYCLES,
        "force_cycle_is_symmetric": FORCE_CYCLE == tuple(reversed(FORCE_CYCLE)),
        "sign_cycle_locked": SIGN_CYCLE == "-++--+",
        "gravity_pinned": G == 1.0,
        "negative_p_can_breakout": breakout(-0.02),
        "positive_p_cannot_breakout": not breakout(+0.02),
        "center_frozen": STATE_CENTER == "000",
    }

def verify()->bool:
    return all(prove().values())

if __name__=="__main__":
    print(prove())
    print("0e / COPPER MIND VECTOR 0 FROZEN PASS" if verify() else "xe / FAIL")
