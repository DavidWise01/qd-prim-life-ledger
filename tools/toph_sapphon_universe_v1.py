from dataclasses import dataclass
from fractions import Fraction

HOMEOSTATIC_PRESSURE = 1000.0
DIRECTIONS = 24
SECTOR_DEGREES = 15.0
WEAK_BINS = 729
WEAK_INCREMENT = Fraction(1, 729)
WEAK_CENTER = 364
FIGHT_CLUB_STATES = 64
DIRECT10_ADDRESSES = 1024

@dataclass(frozen=True)
class MetricSample:
    direction: int
    angle_deg: float
    pressure_model: float
    g_model: float
    delta_g: float
    response: str

def gravity_metric(p):
    return p / HOMEOSTATIC_PRESSURE, (p - HOMEOSTATIC_PRESSURE) / HOMEOSTATIC_PRESSURE

def response_from_delta(d, eps=1e-12):
    return "binding/inward" if d > eps else ("release/outward" if d < -eps else "homeostatic")

def sample_direction(k, p):
    if not 0 <= k < 24:
        raise ValueError("direction must be in [0,23]")
    g, d = gravity_metric(p)
    return MetricSample(k, k * 15.0, p, g, d, response_from_delta(d))

def sample_universe(ps):
    ps = tuple(ps)
    if len(ps) != 24:
        raise ValueError("exactly 24 directional samples required")
    return tuple(sample_direction(i, p) for i, p in enumerate(ps))

def weighted_homeostasis(samples, weights=None):
    s = tuple(samples)
    w = (1.0,) * len(s) if weights is None else tuple(weights)
    if len(w) != len(s) or sum(w) == 0:
        raise ValueError("invalid weights")
    return sum(a * b.delta_g for a, b in zip(w, s)) / sum(w)

def opposite_direction(k):
    return (k + 12) % 24

def direct10_pack(lane, dot):
    if not 0 <= lane < 128 or not 0 <= dot < 8:
        raise ValueError("invalid Direct10 coordinate")
    return (lane << 3) | dot

def direct10_unpack(a):
    if not 0 <= a < 1024:
        raise ValueError("address must be in [0,1023]")
    return a >> 3, a & 7

def invariants():
    g, d = gravity_metric(1000)
    return {
        "home_G_is_1": g == 1,
        "home_delta_is_0": d == 0,
        "24x15_is_360": 24 * 15 == 360,
        "opposites_are_180": all(((opposite_direction(k) - k) % 24) * 15 == 180 for k in range(24)),
        "weak_exact_1deg": WEAK_BINS * WEAK_INCREMENT == 1,
        "weak_center": (WEAK_BINS - 1) - WEAK_CENTER == WEAK_CENTER,
        "fight_club_64": FIGHT_CLUB_STATES == 64,
        "direct10_1024": DIRECT10_ADDRESSES == 1024,
        "direct10_bijection": {direct10_pack(l, d) for l in range(128) for d in range(8)} == set(range(1024)),
    }

if __name__ == "__main__":
    inv = invariants()
    for k, v in inv.items():
        print(f"{k}: {v}")
    print("0e / TOPH SAPPHON UNIVERSE V1 PASS" if all(inv.values()) else "xe / TOPH SAPPHON UNIVERSE V1 FAIL")
