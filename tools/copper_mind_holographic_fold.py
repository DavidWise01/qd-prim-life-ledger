"""Copper Mind Holographic Fold v1 — frozen post-kernel overlay."""

WORD = "00 11 00"
RELATIONS = ("EO", "EI", "IE", "II")
RUNGS = (1, 2, 3)

MIRROR = {"EO":"EI", "EI":"EO", "IE":"II", "II":"IE"}
INVERSE = {"EO":"IE", "IE":"EO", "EI":"II", "II":"EI"}
REVERSE_RUNG = {1:3, 2:2, 3:1}

def transform(state, mirror=False, inverse=False, reverse=False):
    rung, boundary = state
    if mirror:
        boundary = MIRROR[boundary]
    if inverse:
        boundary = INVERSE[boundary]
    if reverse:
        rung = REVERSE_RUNG[rung]
    return rung, boundary

def orbit(state):
    return {
        transform(state, m, i, r)
        for m in (False, True)
        for i in (False, True)
        for r in (False, True)
    }

def canonical(state):
    return min(orbit(state))

def classes():
    out = {}
    for state in ((r,b) for r in RUNGS for b in RELATIONS):
        out.setdefault(canonical(state), []).append(state)
    return out

def fold(payload):
    return f"00[{payload}]00"

def verify():
    c = classes()
    assert len(c) == 2
    assert len(orbit((1, "EO"))) == 8
    assert len(orbit((2, "EO"))) == 4
    assert WORD.replace(" ", "") == "001100"
    assert REVERSE_RUNG[2] == 2
    assert REVERSE_RUNG[REVERSE_RUNG[1]] == 1
    return True

if __name__ == "__main__":
    verify()
    print("0e / HOLOGRAPHIC FOLD PASS")
    print("word:", WORD)
    print("classes:", classes())
