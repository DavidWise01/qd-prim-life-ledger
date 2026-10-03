from fractions import Fraction
import random

SEED = 20261003

def mirror(left):
    return [(-sigma, -delta_g) for sigma, delta_g in reversed(left)]

def valid(left, right):
    if len(left) != len(right):
        return False

    for (ls, lg), (rs, rg) in zip(left, reversed(right)):
        if rs != -ls:
            return False
        if rg != -lg:
            return False

    total_sign = sum(sigma for sigma, _ in left + right)
    total_g = sum((delta_g for _, delta_g in left + right), Fraction(0))
    return total_sign == 0 and total_g == 0

def run():
    rng = random.Random(SEED)

    lawful = 100_000
    for _ in range(lawful):
        left = []
        for _ in range(3):
            sigma = rng.choice((-1, 1))
            delta_g = Fraction(rng.randint(-10_000, 10_000),
                               rng.randint(1, 10_000))
            left.append((sigma, delta_g))

        right = mirror(left)
        assert valid(left, right)

    attacks = 10_000
    detected = 0

    for _ in range(attacks):
        left = []
        for _ in range(3):
            sigma = rng.choice((-1, 1))
            delta_g = Fraction(rng.randint(-1_000, 1_000),
                               rng.randint(1, 1_000))
            left.append((sigma, delta_g))

        right = mirror(left)
        j = rng.randrange(3)

        if rng.random() < 0.5:
            sigma, delta_g = right[j]
            right[j] = (-sigma, delta_g)
        else:
            sigma, delta_g = right[j]
            right[j] = (sigma, delta_g + Fraction(1, 10**9))

        if not valid(left, right):
            detected += 1

    assert detected == attacks

    print(f"{lawful}/{lawful} lawful cases PASS")
    print(f"{detected}/{attacks} mutations detected")
    print("0e / SOMATIC SHREDDER++ GRAVITY-TETHER v00 PASS")

if __name__ == "__main__":
    run()
