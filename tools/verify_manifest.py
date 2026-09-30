from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))

pairs: list[str] = []
for entry in manifest["files"]:
    path = ROOT / entry["path"]
    digest = sha256(path.read_bytes()).hexdigest()
    if digest != entry["sha256"]:
        raise SystemExit(f"hash mismatch: {entry['path']}")
    pairs.append(f"{entry['path']}:{digest}")

root = sha256(("\n".join(sorted(pairs)) + "\n").encode("utf-8")).hexdigest()
if root != manifest["root_sha256"]:
    raise SystemExit("root hash mismatch")

print(f"0e / TETHER PASS / {root}")
