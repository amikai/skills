<div align="center">

# skills

**amikai's personal Agent Skills for coding agents.**

[![License](https://img.shields.io/github/license/amikai/skills?style=flat)](LICENSE)

</div>

[Agent Skills](https://agentskills.io) I use across coding agents. Each skill lives in `skills/<name>/SKILL.md`.

## Install

<details>
<summary><strong>Antigravity (agy)</strong></summary>

```bash
agy plugin install https://github.com/amikai/skills
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add amikai/skills
claude plugin install amikai-skills@amikai-skills
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add amikai/skills
codex plugin add amikai-skills@amikai-skills
```

</details>

<details>
<summary><strong>Grok</strong></summary>

```bash
grok plugin install amikai/skills
```

</details>

<details>
<summary><strong>Skills CLI</strong></summary>

```bash
npx skills add amikai/skills
```

</details>

## Catalog

<!-- catalog:start -->
| Skill | What it does |
|-------|--------------|
| [commit-msg](skills/commit-msg/) | Craft concise, outcome-focused commit messages with detail matched to complexity and risk. |
| [modern-utility](skills/modern-utility/) | Prefer fast, modern CLI tools (Rust/Go/C) and Bash pipelines over Python scripts for daily tasks and lightweight data analysis. |
| [pr-msg](skills/pr-msg/) | Craft reviewer-friendly PR/MR titles and descriptions focused on intent, architecture, and key changes, with diagrams when useful. |
<!-- catalog:end -->

To add a skill: create `skills/<name>/SKILL.md`, run
`uv run scripts/gen_catalog.py`, then simplify the generated Catalog
description if needed.

## License

[MIT](LICENSE).
