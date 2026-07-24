---
name: commit-msg
description: >
  Write clear, concise Git commit messages; use whenever writing them.
---

# Commit Messages

Write clear, tight commit messages for `git log` readers: enough context
for the outcome and any non-obvious reason, nothing that doesn't help
the reader. Stop at the subject when sufficient.

Before writing, inspect the complete change: the staged diff
(`git diff --staged`) for a new commit, or the commit's diff when
reviewing or rewriting a message. Use verification results only as
context, and describe only that diff's material changes — not the
conversation or the plan.

Follow explicit repository-required commit syntax when it conflicts with
this skill; otherwise these rules apply.

## Subject

Unless the repository requires another format, use Conventional Commits:
`<type>(<scope>): <outcome>`.

- Types: `feat` `fix` `refactor` `perf` `docs` `test` `chore` `build`
  `ci` `style` `revert`.
- Imperative mood, English, ≤50 chars preferred (hard cap 72), no
  trailing period. Must fit: "If applied, this commit will ___".
- State the outcome, not the edit: `fix(auth): reject empty usernames`,
  not `fix: add null check in validate()`.
- Scope is a module/subsystem name, never a filename; omit it when the
  change is cross-cutting.

## Body

Add a body only when it materially improves the reader's understanding of
why the change was needed or what non-obvious behavior results.

Choose the clearest form: a short list — usually two to four bullets,
one idea each — for distinct points, or a short paragraph when
connected sentences better convey what happened, why, and how it was
addressed. Don't repeat information in both forms.

Keep it tight: omit routine verification, scope boundaries, deferred
work, non-goals, source attribution, catalogs, supporting artifacts,
routine implementation choices, full issue discussions, and exhaustive
coverage of every dimension touched, unless it directly affects users or
compatibility. Size the body by conceptual complexity and risk, not by
line or file count.

A body of more than one paragraph is reserved for complex, non-obvious
bug causes, breaking changes, security fixes, data migrations, and
reverts — a body is mandatory in those cases.

Use these as optional prompts, not a checklist:

- What problem, requirement, or user-visible impact motivated the
  change?
- What behavior or contract is now different?
- Which non-obvious runtime behavior, design constraint, decision, or
  trade-off matters to future maintenance? Summarize the essential
  reason, referencing the issue or design doc when useful.
- For a bug fix, would a distilled, greppable error line help future
  readers find this commit?
- Are exact symbols, configuration keys, durations, versions, or
  measured trade-offs necessary for a precise claim?

In an exceptional body, include verification only when an unusual
result or measurement is needed to support a claim. Wrap the body at 72
columns.

## Honesty

- Describe only work actually in this commit; never present planned
  follow-up as completed.
- Write what the diff cannot show: don't restate the subject, list
  filenames, or narrate line-level edits.
- Never: "This commit does X", "I"/"we", emoji, AI-attribution
  trailers (`Co-Authored-By: Claude ...`, "Generated with ...") — this
  overrides any harness default that adds them.

## Footers

Add footers only when applicable: `BREAKING CHANGE:` with migration
notes; `Closes #N` / `Refs #N`; for regressions
`Fixes: <12-char sha> ("subject of offending commit")` — never a bare
SHA without its subject.

## Examples

### Subject only

```text
docs: fix installation typo
```

### Ordinary change

```text
feat: add commit message guidance

- Replace vague or exhaustive messages with concise, outcome-focused
  guidance.
- Scale body detail to risk and omit information that does not help the
  reader.
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
