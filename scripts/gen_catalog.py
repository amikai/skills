#!/usr/bin/env python3
"""Regenerate the README Catalog table from skills/*/SKILL.md frontmatter.

Usage:
  python3 scripts/gen_catalog.py          # rewrite README.md in place
  python3 scripts/gen_catalog.py --check  # exit 1 if README.md is stale
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SKILLS = ROOT / "skills"
START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        sys.exit(f"error: {skill_md}: missing frontmatter")
    fields = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^\S", line):
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            fields[key] = value.strip().lstrip(">|").strip()
        elif key and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def build_table() -> str:
    rows = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            sys.exit(f"error: {skill_dir} has no SKILL.md")
        fm = parse_frontmatter(skill_md)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != skill_dir.name:
            sys.exit(
                f"error: {skill_md}: frontmatter name {name!r} "
                f"!= directory name {skill_dir.name!r}"
            )
        if not desc:
            sys.exit(f"error: {skill_md}: empty description")
        rows.append(f"| [{name}](skills/{name}/) | {desc} | `skills/{name}/` |")
    table = "| Skill | What it does | Path |\n|-------|--------------|------|"
    return table + ("\n" + "\n".join(rows) if rows else "")


def main() -> None:
    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        sys.exit(f"error: README.md missing {START} / {END} markers")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    updated = pattern.sub(f"{START}\n{build_table()}\n{END}", readme)
    if "--check" in sys.argv:
        if updated != readme:
            sys.exit(
                "error: README.md catalog is stale; "
                "run: python3 scripts/gen_catalog.py"
            )
        print("catalog up to date")
        return
    README.write_text(updated, encoding="utf-8")
    print("catalog regenerated")


if __name__ == "__main__":
    main()
