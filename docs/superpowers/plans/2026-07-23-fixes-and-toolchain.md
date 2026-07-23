# Fixes + Catalog/Version Toolchain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the two validated bugs in the scaffold (marketplace `owner` schema, Grok install docs) and add the catalog-generation + version-bump toolchain with CI enforcement.

**Architecture:** Two stacked deliverables. Task 1 fixes bugs on the existing `scaffold-plugin-manifests` branch (updates PR #1). Tasks 2–5 build the toolchain on a new `toolchain` branch: two zero-dependency Python scripts (`scripts/gen_catalog.py` regenerates the README catalog from SKILL.md frontmatter and validates it; `scripts/bump.py` syncs versions across the three plugin manifests) plus a GitHub Actions workflow that runs both in `--check` mode and lints all JSON.

**Tech Stack:** Python 3 stdlib only (no pip deps), GitHub Actions, `gh` CLI.

## Global Constraints

- Python scripts use **stdlib only** — no PyYAML, no third-party imports.
- JSON files keep **2-space indent** and a trailing newline (matches existing manifests).
- Plugin name is `amikai-skills` everywhere; canonical version source is `.claude-plugin/plugin.json`.
- Do not add any real skills, templates/, CONTRIBUTING.md, or CATALOG.md.
- Repo root: `/Users/amikai/Workspace/skills`. Base branch for Task 1: `scaffold-plugin-manifests`.

---

### Task 1: Fix marketplace `owner` schema + Grok install docs (updates PR #1)

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.codex-plugin/marketplace.json`
- Delete: `.grok-plugin/marketplace.json` (dead weight — Grok installs straight from a git URL; its marketplace format is xai's SHA-pinned catalog, not this self-referencing form)
- Modify: `README.md` (Grok section)

**Interfaces:**
- Produces: repo passes `claude plugin validate` and `grok plugin validate`; later tasks assume `.grok-plugin/` contains only `plugin.json`.

- [x] **Step 1: Confirm current failure**

Run: `claude plugin validate /Users/amikai/Workspace/skills`
Expected: FAIL with `owner: Invalid input: expected object, received string`

- [x] **Step 2: Fix `owner` in both remaining marketplace files**

In `.claude-plugin/marketplace.json` and `.codex-plugin/marketplace.json`, replace:

```json
  "owner": "amikai",
```

with:

```json
  "owner": { "name": "amikai" },
```

- [x] **Step 3: Delete the Grok marketplace file**

```bash
git rm .grok-plugin/marketplace.json
```

- [x] **Step 4: Fix the Grok install section in README.md**

Replace the body of the `<details>` Grok block:

```bash
grok plugin marketplace add amikai/skills
grok plugin install amikai-skills@amikai-skills
```

with:

```bash
grok plugin install amikai/skills
```

- [x] **Step 5: Verify with real validators**

Run: `claude plugin validate /Users/amikai/Workspace/skills`
Expected: PASS (no errors)

Run: `grok plugin validate /Users/amikai/Workspace/skills`
Expected: `Plugin manifest is valid.` with `1 skill dir(s)`

Run: `agy plugin validate /Users/amikai/Workspace/skills`
Expected: `[ok]`

- [x] **Step 6: Commit and push (updates PR #1)**

```bash
git add -A
git commit -m "fix: marketplace owner must be an object; correct Grok install docs"
git push
```

---

### Task 2: Catalog markers + `scripts/gen_catalog.py`

**Files:**
- Create: `scripts/gen_catalog.py`
- Modify: `README.md` (wrap Catalog table in markers, add a one-line dev note)

**Interfaces:**
- Produces: `python3 scripts/gen_catalog.py` (rewrite mode) and `python3 scripts/gen_catalog.py --check` (exit 1 when stale, used by Task 4 CI). Also validates every `skills/*/SKILL.md`: frontmatter exists, `name` matches directory name, `description` non-empty.

- [x] **Step 1: Create the `toolchain` branch off the fixed scaffold branch**

```bash
git checkout -b toolchain scaffold-plugin-manifests
```

- [x] **Step 2: Add markers around the Catalog table in README.md**

Replace:

```markdown
## Catalog

| Skill | What it does | Path |
|-------|--------------|------|
```

with:

```markdown
## Catalog

<!-- catalog:start -->
| Skill | What it does | Path |
|-------|--------------|------|
<!-- catalog:end -->

To add a skill: create `skills/<name>/SKILL.md`, then run `python3 scripts/gen_catalog.py`.
```

- [x] **Step 3: Write `scripts/gen_catalog.py`**

```python
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
```

- [x] **Step 4: Verify against the empty catalog**

Run: `python3 scripts/gen_catalog.py --check`
Expected: `catalog up to date` (empty table regenerates to itself, exit 0)

- [x] **Step 5: Verify with a throwaway fixture skill**

```bash
mkdir -p skills/tmp-demo
cat > skills/tmp-demo/SKILL.md <<'EOF'
---
name: tmp-demo
description: >
  Throwaway fixture used only to test catalog generation.
---
# tmp-demo
EOF
python3 scripts/gen_catalog.py
grep 'tmp-demo' README.md
python3 scripts/gen_catalog.py --check
```

Expected: `catalog regenerated`; grep prints the row `| [tmp-demo](skills/tmp-demo/) | Throwaway fixture used only to test catalog generation. | `skills/tmp-demo/` |`; check prints `catalog up to date`.

Also verify the failure paths:

```bash
sed -i '' 's/^name: tmp-demo/name: wrong-name/' skills/tmp-demo/SKILL.md
python3 scripts/gen_catalog.py
```

Expected: exits non-zero with `frontmatter name 'wrong-name' != directory name 'tmp-demo'`.

- [x] **Step 6: Remove the fixture and restore the empty table**

```bash
rm -rf skills/tmp-demo
python3 scripts/gen_catalog.py
git diff --stat
```

Expected: only README.md (markers + dev note) and `scripts/gen_catalog.py` changed vs. branch point; catalog table back to header-only.

- [x] **Step 7: Commit**

```bash
git add scripts/gen_catalog.py README.md
git commit -m "feat: generate README catalog from SKILL.md frontmatter"
```

---

### Task 3: `scripts/bump.py` — version bump + drift check

**Files:**
- Create: `scripts/bump.py`

**Interfaces:**
- Consumes: the three manifests carrying `version`: `.claude-plugin/plugin.json` (canonical), `.codex-plugin/plugin.json`, `.grok-plugin/plugin.json`.
- Produces: `python3 scripts/bump.py patch|minor|major|<x.y.z>` (rewrites all three) and `python3 scripts/bump.py --check` (exit 1 on drift, used by Task 4 CI).

- [x] **Step 1: Write `scripts/bump.py`**

```python
#!/usr/bin/env python3
"""Bump the plugin version across every manifest that carries one.

Usage:
  python3 scripts/bump.py patch|minor|major|<x.y.z>  # rewrite manifests
  python3 scripts/bump.py --check                    # exit 1 on version drift
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
```

Notes: the script prints the tag command instead of tagging — tagging before the commit exists would pin the wrong tree. Version is replaced with a targeted `re.subn` on the `"version"` field instead of a `json.dumps` round-trip, so the manifests' existing formatting (inline `author`/`keywords` objects) is preserved byte-for-byte; `json` is still imported for `read_version`/`check`, which only parse.

- [x] **Step 2: Verify check mode passes on the clean tree**

Run: `python3 scripts/bump.py --check`
Expected: `versions consistent: 0.1.0`

- [x] **Step 3: Verify bump + drift detection round-trip**

```bash
python3 scripts/bump.py patch
grep -h '"version"' .claude-plugin/plugin.json .codex-plugin/plugin.json .grok-plugin/plugin.json
python3 scripts/bump.py --check
git checkout -- .claude-plugin .codex-plugin .grok-plugin
```

Expected: `bumped to 0.1.1`; three identical `"version": "0.1.1",` lines; `versions consistent: 0.1.1`; then working tree restored to 0.1.0.

Drift detection:

```bash
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path(".codex-plugin/plugin.json")
d = json.loads(p.read_text()); d["version"] = "9.9.9"
p.write_text(json.dumps(d, indent=2) + "\n")
EOF
python3 scripts/bump.py --check; echo "exit=$?"
git checkout -- .codex-plugin
```

Expected: `error: version drift: {...}` and `exit=1`.

- [x] **Step 4: Verify JSON formatting is preserved**

```bash
python3 scripts/bump.py 0.1.0
git diff --exit-code
```

Expected: no diff — the targeted regex rewrites only the `"version"` value, so rewriting the same version is a byte-for-byte no-op and the manifests' inline `author`/`keywords` style survives untouched.

- [x] **Step 5: Commit**

```bash
git add scripts/bump.py
git commit -m "feat: version bump script with drift check"
```

---

### Task 4: CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `scripts/gen_catalog.py --check` (Task 2), `scripts/bump.py --check` (Task 3).

- [x] **Step 1: Write `.github/workflows/ci.yml`**

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate JSON manifests
        run: |
          for f in plugin.json .claude-plugin/*.json .codex-plugin/*.json .grok-plugin/*.json; do
            python3 -m json.tool "$f" > /dev/null || exit 1
            echo "OK $f"
          done
      - name: Catalog up to date
        run: python3 scripts/gen_catalog.py --check
      - name: Versions consistent
        run: python3 scripts/bump.py --check
```

- [x] **Step 2: Run every CI step locally**

```bash
for f in plugin.json .claude-plugin/*.json .codex-plugin/*.json .grok-plugin/*.json; do
  python3 -m json.tool "$f" > /dev/null || exit 1; echo "OK $f"
done
python3 scripts/gen_catalog.py --check
python3 scripts/bump.py --check
```

Expected: `OK` for 6 files (root `plugin.json`; claude plugin + marketplace; codex plugin + marketplace; grok plugin — its marketplace.json was deleted in Task 1), then `catalog up to date`, then `versions consistent: 0.1.0`.

- [x] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: validate manifests, catalog freshness, version consistency"
```

---

### Task 5: Push and open PR #2

**Files:** none (git/gh only)

- [x] **Step 1: Push the branch**

```bash
git push -u origin toolchain
```

- [x] **Step 2: Open PR #2 stacked on PR #1's branch**

```bash
gh pr create --base scaffold-plugin-manifests --title "Catalog generation, version bump tooling, and CI" --body "$(cat <<'EOF'
## What changed

- `scripts/gen_catalog.py` — regenerates the README Catalog table from `skills/*/SKILL.md` frontmatter (markers in README); `--check` mode for CI. Also validates frontmatter: name matches dir, description non-empty.
- `scripts/bump.py` — bumps `version` across all three plugin manifests from one command; `--check` fails CI on drift. Prints the tag command instead of tagging.
- `.github/workflows/ci.yml` — JSON lint + catalog freshness + version consistency on every PR.

## Why

Catalog and version fields are duplicated by design (per-tool manifests); generation + CI checks make drift impossible instead of relying on discipline.

Stacked on #1; GitHub will retarget to `main` automatically when #1 merges.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [x] **Step 3: Verify CI runs green on the PR**

Run: `gh pr checks --watch`
Expected: `ci / validate` passes.

---

## Out of scope (noted, not planned)

- README pin-by-tag instructions (`@v0.1.0`) — add at first real release.
- Running `claude`/`grok`/`agy` validators in CI — needs CLI installs in the runner; revisit if manifest schemas bite again.
- Same `owner` bug in amikai/anti-skills — separate repo, separate fix.
