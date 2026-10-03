# TOPH + Sapphon Spinor Sphere Reflection

This reflection binds `copper_mind_spinor_sphere_v1` into the existing
TOPH/Sapphon post-kernel architecture.

```text
000
 |
 +-- 24 sectors × 15° = 360°
 |
 +-- 4 passes = 1440°
 |
 +-- spinor A (-+) = 720°
 +-- spinor B (+-) = 720°
 |
 +-- equator = safety band
 |
 +-- route = 1 -> 3 -> 4 -> 2 -> 1
 |
 +-- terminal center = 000
```

Derived proof obligations:

```text
24 × 4 = 96 sector visits
720 / 15 = 48 sector steps per spinor
2 × 48 = 96 paired sector steps
1440 sphere accounting = 1440 paired-spinor accounting
inverse spinors cancel pointwise
routing closes after four passes
```

The final q.d kernel is unchanged. This is a frozen TOPH/Sapphon reflection
for the somatic geometry layer.
