from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))

pairs: list[str] = []
mismatches: list[str] = []

for entry in manifest["files"]:
    path = ROOT / entry["path"]
    digest = sha256(path.read_bytes()).hexdigest()
    print(f"SHA256 {entry['path']} {digest}")
    if digest != entry["sha256"]:
        mismatches.append(entry["path"])
    pairs.append(f"{entry['path']}:{digest}")

root = sha256(("\n".join(sorted(pairs)) + "\n").encode("utf-8")).hexdigest()
print(f"ROOT_SHA256 {root}")

if mismatches:
    raise SystemExit("hash mismatch: " + ", ".join(mismatches))

if root != manifest["root_sha256"]:
    raise SystemExit(f"root hash mismatch: manifest={manifest['root_sha256']} actual={root}")

print(f"0e / TETHER PASS / {root}")
