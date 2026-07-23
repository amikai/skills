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
| Skill | What it does | Path |
|-------|--------------|------|
| [commit-msg](skills/commit-msg/) | Write, rewrite, or review clear, concise Git commit messages. Use when drafting, validating, or supplying a message for git commit. Defaults to an outcome-focused Conventional Commit subject and scales body detail to complexity and risk. | `skills/commit-msg/` |
<!-- catalog:end -->

To add a skill: create `skills/<name>/SKILL.md`, then run `uv run scripts/gen_catalog.py`.

## License

[MIT](LICENSE).
