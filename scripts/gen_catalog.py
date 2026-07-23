#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "python-frontmatter",
# ]
# ///
"""Synchronize README Catalog skills while preserving edited descriptions.

Usage:
  uv run scripts/gen_catalog.py          # rewrite README.md in place
  uv run scripts/gen_catalog.py --check  # exit 1 if README.md is stale
"""
import re
import sys
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SKILLS = ROOT / "skills"
START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"
CATALOG = re.compile(re.escape(START) + r"(.*?)" + re.escape(END), re.DOTALL)
ROW = re.compile(r"^\| \[([^\]]+)\]\([^)]+\) \| ([^|]+) \|$")


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def load_skills() -> list[tuple[str, str]]:
    skills = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            die(f"{skill_dir} has no SKILL.md")

        meta = frontmatter.load(skill_md).metadata
        name = str(meta.get("name") or "").strip()
        description = " ".join(str(meta.get("description") or "").split())

        if name != skill_dir.name:
            die(
                f"{skill_md}: frontmatter name {name!r} "
                f"!= directory name {skill_dir.name!r}"
            )
        if not description:
            die(f"{skill_md}: empty description")
        skills.append((name, description))
    return skills


def existing_descriptions(catalog: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in catalog.splitlines():
        match = ROW.match(line)
        if not match:
            continue
        name, description = match.groups()
        if name in rows:
            die(f"README.md Catalog has duplicate skill {name!r}")
        rows[name] = description.strip()
    return rows


def build_table(
    skills: list[tuple[str, str]], existing: dict[str, str]
) -> str:
    header = "| Skill | What it does |\n|-------|--------------|"
    rows = [
        f"| [{name}](skills/{name}/) | {existing.get(name, desc)} |"
        for name, desc in skills
    ]
    return header + ("\n" + "\n".join(rows) if rows else "")


def main() -> None:
    readme = README.read_text(encoding="utf-8")
    match = CATALOG.search(readme)
    if not match:
        die(f"README.md missing {START} / {END} markers")

    table = build_table(load_skills(), existing_descriptions(match.group(1)))
    updated = CATALOG.sub(f"{START}\n{table}\n{END}", readme)

    if "--check" in sys.argv:
        if updated != readme:
            die(
                "README.md catalog is stale; "
                "run: uv run scripts/gen_catalog.py"
            )
        print("catalog up to date")
        return

    README.write_text(updated, encoding="utf-8")
    print("catalog regenerated")


if __name__ == "__main__":
    main()
