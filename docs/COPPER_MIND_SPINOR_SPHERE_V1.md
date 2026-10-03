# Copper Mind Spinor Sphere v1

**Status:** FROZEN / IMMUTABLE / APPEND-ONLY  
**Parent:** Copper Mind Vector 0  
**Center:** `000`  
**Scope:** somatic symbolic geometry / timing analog  
**Final q.d kernel modified:** no

## Base addressing

```text
15° × 24 sectors = 360°
360° × 4 passes  = 1440°
```

The equator is reserved as the safety band.

## Paired spinors

```text
spinor A = -+ = 720°
spinor B = +- = 720°

720° + 720° = 1440°
```

Each 720° spinor therefore occupies:

```text
720 / 15 = 48 sector steps
```

The pair occupies:

```text
1440 / 15 = 96 sector steps
```

which exactly matches:

```text
24 sectors × 4 passes = 96 visits
```

This is a derived closure invariant.

## Routing

Pass order is frozen as:

```text
1 -> 3 -> 4 -> 2 -> 1
```

It forms one exact four-state cycle. Its permutation has even parity.

## Inverse-bound layer rule

```text
+ <-> -
- <-> +
0 <-> 0
```

The two spinors cancel pointwise:

```text
-+ 
+-
--
00
```

so the center remains `000` while the shell still traverses the full 1440°
angular accounting.

## What falls out

```text
24 sectors / ring
4 passes
96 sector visits total

12 sectors / 180° half-turn
48 sectors / 720° spinor
96 sectors / paired 1440° spinors

sphere accounting = paired spinor accounting
route 1,3,4,2 closes after 4 passes
inverse spinor sum = 0
equator remains safety band
```

Thus the shell is balanced at the center without being static: the paired
spinors carry opposite orientation through the same closed addressing volume.

Contract SHA-256:

`76ea7a2df89058e8345874ec29e58eb8dad2496516300f360207727705b0c43c`
