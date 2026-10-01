# Tether Map

This repository is intentionally tethered: every executable, test, notation file, and specification points back to one canonical PRIM root.

```text
                         CANONICAL ROOT
                         {{5/3/2/1/1}} FROZEN
                         PRIM = 1 1 2 8
                         dot = sapphon
                    append only -> add next
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
          SPEC.md         docs/NOTATION.md     src/qd_prim.py
              |                 |                 |
              +-----------------+-----------------+
                                |
                                v
                         tests/test_qd_prim.py
                                |
                                v
                      .github/workflows/test.yml
                                |
                                v
                           MANIFEST.json
```

## Canonical relationships

1. `FREEZE.md` pins the completed Gen-1 mother/daughter kernel state.
2. `README.md` is the human entry point.
3. `SPEC.md` defines normative model behavior.
4. `docs/NOTATION.md` preserves literal symbolic notation and semantic glosses.
5. `src/qd_prim.py` is the executable reference implementation.
6. `tests/test_qd_prim.py` checks the executable invariants, including Paralax daughter inference.
7. `.github/workflows/test.yml` re-runs the invariants on every push and pull request.
8. `MANIFEST.json` hashes the tethered files and supplies one deterministic root hash.

## Append-only tether

At repository level, Git history supplies the outer provenance chain. At q.d level, `parent_hash` supplies the inner trajectory chain. Each append also tethers `dot[n] = sapphon[n] = Plank[n]`.

```text
Git commit n ---> Git commit n+1
      |                |
      v                v
q.d event n ----> q.d event n+1
 sapphon[n]       sapphon[n+1]
        parent_hash = SHA256(event n)
```

## Manifest rule

`MANIFEST.json` hashes all canonical tether files except itself. Its `root_sha256` is computed from sorted lines of:

```text
path:sha256
```

This avoids self-hash recursion while giving the repository a single auditable tether root.


## Append-only skill adapter

The frozen mother kernel is unchanged. Skill assessment is appended outside the freeze:

```text
frozen q.d ledger
      |
      v
tools/skill_probe.py
      |
      v
tests/test_skill_probe.py
```

The probe reports demonstrated structural complexity from 0..5:
`1=unary`, `2=binary`, `3=ternary`, `4=ternary+4 payloads`, `5=ternary+5 payloads`.
It reads committed q.d evidence only and never grants generation authority.
