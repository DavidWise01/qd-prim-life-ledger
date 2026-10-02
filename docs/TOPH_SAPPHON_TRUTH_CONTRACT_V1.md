# TOPH + Sapphon Historical Truth Contract v1

**Status:** FROZEN / APPEND-ONLY / MEDIA-ONLY SIMULATION  
**Closure:** `oe`  
**Final q.d kernel modified:** no

This adapter treats "truth" as a dated evidence contract rather than an eternal overwrite.

```text
claim @ frame n
      ↓
media-only evidence available at frame n
      ↓
+1 supported
 0 unresolved / archived alternate
-1 contradicted
      ↓
append next frame
      ↓
re-test
```

Prior frames remain intact. A contradicted branch is not deleted; it is demoted from the active line to the `0` provenance archive.

## Frame size

```text
176 country lanes × 10 generations = 1760 cells
```

Generation cadence:

```text
grand → parent → child
grand → parent → child
grand → parent → child
grand
```

So `10 = 3 + 3 + 3 + 1`.

## Truth contract

```text
T_frame(x) = best-supported classification available in that frame
```

It is explicitly **not** a claim of metaphysical certainty.

Example:

```text
1832:
  country exists → +1

2026 alternate media claim:
  "country was wiped out" → contradicted → -1

archive:
  -1 → 0_archive
```

The contradicted alternate remains provenance but cannot remain on the active historical line unless later evidence reopens it.

## TOPH/Sapphon binding

```text
SapphonSnapshot
      ↓
TOPHCommit
      ↓
TOPHProve
      ↓
TOPHProject
      ↓
TOPHTransport
      ↓
oe
```

Contract SHA-256:

```text
52fb62216eeee276f26c67576cb2d0b03034699108fac074f2c9b20303f40ff9
```
