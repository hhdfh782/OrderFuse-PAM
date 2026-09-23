"""Audit the preview tree and write a checksum manifest."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release_manifest.json"
FORBIDDEN_SUFFIXES = {
    ".mat", ".h5", ".hdf5", ".npy", ".npz", ".pth", ".pt", ".ckpt",
    ".onnx", ".pkl", ".pickle",
}
TEXT_SUFFIXES = {".py", ".md", ".toml", ".cff", ".txt", ".gitignore", ""}
PRIVATE_PATTERNS = {
    "windows_absolute_path": re.compile(r"[A-Za-z]:[\\/]"),
    "ssh_destination": re.compile(r"\b(?:root|admin|ubuntu)@[-A-Za-z0-9.]+"),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]+"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


files = [p for p in ROOT.rglob("*") if p.is_file() and p != MANIFEST]
forbidden = [p for p in files if p.suffix.lower() in FORBIDDEN_SUFFIXES]
if forbidden:
    raise SystemExit(f"forbidden artifact types: {[str(p.relative_to(ROOT)) for p in forbidden]}")

findings = []
for path in files:
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name != ".gitignore":
        continue
    text = path.read_text(encoding="utf-8")
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            findings.append({"file": path.relative_to(ROOT).as_posix(), "pattern": label})
if findings:
    raise SystemExit(f"private strings found: {findings}")

records = [
    {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    for path in sorted(files)
]
report = {
    "release": "0.1.0-preview",
    "status": "passed",
    "reproducibility_scope": "metrics-only; manuscript results are not reproducible from this preview",
    "forbidden_artifact_count": 0,
    "private_string_findings": [],
    "files": records,
}
MANIFEST.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k != "files"}, indent=2))

