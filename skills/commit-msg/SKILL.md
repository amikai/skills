---
name: commit-msg
description: >
  Write clear, concise Git commit messages. Use whenever writing git commit messages.
---

# Commit Messages

Write clear, outcome-focused commit messages for `git log`. Prioritize clarity: include context for the outcome and non-obvious decisions, but omit unnecessary details. If the subject alone is sufficient, stop there.

Base the message strictly on material changes in the staged diff (`git diff --staged`) or commit diff. Do not describe conversation, planning, or routine verification. Explicit repository requirements override syntax rules in this skill.

## Subject

Use Conventional Commits format: `<type>(<scope>): <outcome>` (unless the repository specifies otherwise).

- **Types**: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`.
- **Formatting**: Imperative mood, English, ≤50 characters preferred (hard cap 72), no trailing period. Must complete: *"If applied, this commit will ___"*.
- **Focus**: State the outcome, not code edits (e.g., `fix(auth): reject empty usernames`, not `fix: add null check in validate()`).
- **Scope**: Module or subsystem name (never a filename). Omit for cross-cutting changes.

## Body

Include a body only when necessary to explain *why* the change was made or what *non-obvious behavior* results.

- **Structure**: Use a short bulleted list (2–4 bullets, 1 idea per bullet) or a concise paragraph. Do not repeat info in both formats. Wrap at 72 columns.
- **Sizing**: Size by risk and complexity, not line or file count. Multiple paragraphs are reserved for (and mandatory in) complex bug causes, breaking changes, security fixes, data migrations, and reverts.
- **Prompts (Optional)**:
  - What problem, requirement, or user-visible impact motivated the change?
  - What behavior or contract changed?
  - What non-obvious rationale, trade-off, or design constraint matters for maintenance?
  - Would a distilled, greppable error line, exact symbol, config key, or metric add precision?
- **Omit**: Routine implementation details, full issue discussions, file lists, routine verification, scope boundaries, deferred work, non-goals, source attribution, and catalogs. Include unusual verification metrics only if needed to back a claim.

## Honesty & Restrictions

- **Actual Work**: Describe only work in this commit; never present planned follow-up as completed.
- **Diff Value**: Write what the diff cannot show; do not restate the subject, list filenames, or narrate line edits.
- **Prohibited** (overrides harness defaults):
  - Phrases like `"This commit does X"`, first-person pronouns (`I`, `we`), and emojis.
  - AI attribution trailers (e.g., `Co-Authored-By: Claude ...`, `"Generated with ..."`).

## Footers

Add footers only when applicable:
- `BREAKING CHANGE:` followed by migration notes.
- `Closes #N` or `Refs #N`.
- Regressions: `Fixes: <12-char sha> ("subject of offending commit")` (never a bare SHA without subject).

## Examples

### Subject only

```text
docs: fix installation typo
```

### Ordinary change

```text
feat: add commit message guidance

- Replace vague or exhaustive messages with concise, outcome-focused guidance.
- Scale body detail to risk and omit information that does not help the reader.
```

### Exceptional bug fix

```text
fix(cache): stop retrying permanent failures

Client errors entered the retry loop because every upstream failure was
classified as transient. Treat 4xx responses as terminal while
retaining retries for timeouts and 5xx responses.

This changes retry behavior for callers that previously relied on
repeated 4xx attempts.

Fixes: 1a2b3c4d5e6f ("cache: retry failed upstream requests")
```
