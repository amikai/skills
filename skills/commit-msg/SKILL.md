---
name: commit-msg
description: >
  Write clear, concise Git commit messages. Use whenever writing git commit messages.
---

# Commit Messages

Write clear, concise commit messages for people reading `git log`.
Clarity comes first: choose the form and length that communicates the
meaning most directly. Include enough context to understand the outcome
and any non-obvious reason, but no detail that does not help the reader.
Avoid long explanations unless the change's complexity requires them.
If the subject is sufficient, stop there.

Before writing, inspect the complete change being described: use the
staged diff (`git diff --staged`) for a new commit and the corresponding
commit diff when reviewing or rewriting an existing message. Use
relevant verification results only as context. Describe the material
changes in that diff and nothing outside it: not the conversation or
the plan.

Follow explicit repository-required commit syntax when it conflicts
with this skill. Preserve the remaining rules wherever they still
apply.

## Subject

Unless the repository requires another format, use Conventional
Commits: `<type>(<scope>): <outcome>`.

- Types: `feat` `fix` `refactor` `perf` `docs` `test` `chore` `build`
  `ci` `style` `revert`.
- Imperative mood, English, ≤50 chars preferred (hard cap 72), no
  trailing period. Must fit: "If applied, this commit will ___".
- State the outcome, not the edit: `fix(auth): reject empty usernames`,
  not `fix: add null check in validate()`.
- Scope is a module/subsystem name, never a filename; omit it when the
  change is cross-cutting.

## Body

Use a body only when it materially improves the reader's understanding
of why the change was needed or what non-obvious behavior results from
it.

When a body is needed, choose the form that makes its meaning clearest.
Prefer a short list—usually two to four bullets—for distinct points,
with one idea per bullet. Use a short paragraph when connected
sentences make it easier to understand what happened, why it happened,
and how the change addresses it. Do not repeat information in both
forms.

Omit routine verification, scope boundaries, deferred work, non-goals,
source attribution, catalogs, supporting artifacts, and exhaustive
coverage of every dimension touched by the diff unless they directly
affect users or compatibility.

Size the body by conceptual complexity and risk, not by line count or
number of files. More than one paragraph is reserved for complex,
non-obvious bug causes, breaking changes, security fixes, data
migrations, and reverts. A body is mandatory for those cases.

Use these as optional prompts, not a checklist:

- What problem, requirement, or user-visible impact motivated the
  change?
- What behavior or contract is now different?
- Which non-obvious runtime behavior, design constraint, decision, or
  trade-off matters to future maintenance? Summarize the essential
  reason and reference the relevant issue or design document for details
  when useful.
- For a bug fix, would a distilled, greppable error line help future
  readers find this commit?
- Are exact symbols, configuration keys, durations, versions, or
  measured trade-offs necessary to make a claim precise?

Omit routine implementation choices and do not reproduce the full issue
discussion.

In an exceptional body, include verification only when an unusual
result or measurement is needed to support a claim. Keep paragraphs
short, bullets concise, and wrap the body at 72 columns.

## Honesty

- Describe only work actually in this commit; never present planned
  follow-up as completed.
- Do not restate the subject, list filenames, or narrate line-level
  edits the diff already shows. Write what the diff cannot show.
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
