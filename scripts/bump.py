#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Bump the plugin version across every manifest that carries one.

Usage:
  uv run scripts/bump.py patch|minor|major|<x.y.z>  # rewrite manifests
  uv run scripts/bump.py --check                    # exit 1 on version drift
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / ".claude-plugin" / "plugin.json"
MANIFESTS = [
    CANONICAL,
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".grok-plugin" / "plugin.json",
]


def read_version(path: Path) -> str:
    return json.loads(path.read_text(encoding="utf-8"))["version"]


def check() -> None:
    versions = {p.relative_to(ROOT).as_posix(): read_version(p) for p in MANIFESTS}
    if len(set(versions.values())) != 1:
        sys.exit(f"error: version drift: {versions}")
    print(f"versions consistent: {next(iter(versions.values()))}")


def next_version(current: str, arg: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", arg):
        return arg
    major, minor, patch = map(int, current.split("."))
    if arg == "major":
        return f"{major + 1}.0.0"
    if arg == "minor":
        return f"{major}.{minor + 1}.0"
    if arg == "patch":
        return f"{major}.{minor}.{patch + 1}"
    sys.exit(f"error: expected patch|minor|major|x.y.z, got {arg!r}")


def write_version(path: Path, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, n = re.subn(
        r'("version":\s*)"[^"]+"', rf'\g<1>"{new}"', text, count=1
    )
    if n != 1:
        sys.exit(f"error: {path}: no version field found")
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip())
    if sys.argv[1] == "--check":
        check()
        return
    new = next_version(read_version(CANONICAL), sys.argv[1])
    for path in MANIFESTS:
        write_version(path, new)
    print(f"bumped to {new}")
    print(
        f"next: git commit -am 'release: v{new}' && git tag v{new} "
        "&& git push --follow-tags"
    )


if __name__ == "__main__":
    main()
