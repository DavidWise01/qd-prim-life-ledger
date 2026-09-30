# Tether Map

This repository is intentionally tethered: every executable, test, notation file, and specification points back to one canonical PRIM root.

```text
                         CANONICAL ROOT
                         PRIM = 1 1 2 8
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

1. `README.md` is the human entry point.
2. `SPEC.md` defines normative model behavior.
3. `docs/NOTATION.md` preserves literal symbolic notation and semantic glosses.
4. `src/qd_prim.py` is the executable reference implementation.
5. `tests/test_qd_prim.py` checks the executable invariants.
6. `.github/workflows/test.yml` re-runs the invariants on every push and pull request.
7. `MANIFEST.json` hashes the tethered files and supplies one deterministic root hash.

## Append-only tether

At repository level, Git history supplies the outer provenance chain. At q.d level, `parent_hash` supplies the inner trajectory chain.

```text
Git commit n ---> Git commit n+1
      |                |
      v                v
q.d event n ----> q.d event n+1
        parent_hash = SHA256(event n)
```

## Manifest rule

`MANIFEST.json` hashes all canonical tether files except itself. Its `root_sha256` is computed from sorted lines of:

```text
path:sha256
```

This avoids self-hash recursion while giving the repository a single auditable tether root.
