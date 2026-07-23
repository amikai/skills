# commit-msg Skill Design

Date: 2026-07-23
Status: awaiting user review

## Goal

A personal Agent Skill at `skills/commit-msg/SKILL.md` that governs how
commit messages are written: kernel-grade durable engineering records in
Conventional Commits form. It triggers automatically whenever a commit
message is about to be written — agents commit in the course of ordinary
work, so a message standard that waits for the user to invoke it would
miss most commits.

## Design decisions

| Decision | Choice |
|---|---|
| Scope | Commit message only (subject, body, footers). Staging, atomic splitting, and hook/safety handling are a future commit-workflow skill. |
| Knowledge source | Rules hardcoded in the skill (Conventional Commits). No style inference from `git log`. |
| Execution | Pure prose instructions. No helper scripts. |
| Timing | Automatic — applies whenever a commit message is being written, regardless of who initiated the commit. The skill still never defines *when* to commit. |

## Skill structure

### Frontmatter

- `name: commit-msg`
- `description`: triggering conditions only, kept minimal: "Use when
  writing a git commit message". Never summarize the rules in the
  description — agents follow the description instead of reading the
  body.

### Message rules (hardcoded)

Framing (opens the section verbatim): *Treat commit messages as durable
engineering records, not one-line summaries.*

Subject:

- Conventional Commits, always: `<type>(<scope>): <outcome>`, scope
  optional.
- Types: `feat` `fix` `refactor` `perf` `docs` `test` `chore` `build`
  `ci` `style` `revert`.
- Language: English.
- Imperative mood, ≤50 chars preferred (hard cap 72), no trailing
  period. States the *outcome* of the change, specific enough to
  understand without the diff; must fit "If applied, this commit will
  ___". Scope is a module/subsystem name, never a filename; omit when
  unclear or cross-cutting.

Body — for every non-trivial commit, add a blank line followed by a
body that opens with the problem, then describes the solution.

The list below is a checklist of dimensions, not a form to fill in
every time: the first two items (problem, what was implemented) appear
in every body; every other item is included only when the change
actually touches that dimension. Body depth scales with the blast
radius of the change — a small localized fix may need only a few
lines of problem and fix, while a cross-module feature warrants the
full record.

- States the problem first: the root cause, requirement, or motivation
  behind the change, and the user-visible impact (what breaks, what
  misbehaves, who is affected) — every change exists because of an
  underlying problem, so establish it before describing the fix.
- Describes what was actually implemented.
- Records the concrete behavior now present in the repository,
  including the relevant modules, components, entry points, data
  contracts, and ownership boundaries.
- Explains the end-to-end data or control flow when it is material to
  understanding the change.
- Documents important runtime semantics such as caching, persistence,
  polling intervals, concurrency, fallback behavior, error handling,
  compatibility, and migration behavior.
- Names specific symbols, commands, configuration keys, durations,
  versions, and upstream revisions when they are important.
- For bug fixes, includes the distilled error message, oops, or
  backtrace excerpt — the greppable lines, never the full dump — so
  future readers hitting the same error can find this commit.
- Mentions verification added or exercised when it helps explain the
  completed implementation.
- Captures important design decisions, design considerations, and
  trade-offs, especially where the diff alone would not explain why
  the code works that way: why this approach, alternatives rejected,
  constraints that shaped the design. Claims of improved performance,
  memory, or size must be backed by numbers and must acknowledge the
  trade-off paid.
- Written for an outsider: assume no context from the conversation or
  the subsystem; broken into short paragraphs, not one dense block.

Honesty and anti-patterns:

- Describe only work actually included in the commit. Do not present
  planned follow-up work as completed.
- Do not merely restate the subject, list changed filenames, or
  narrate line-level edits the diff already shows.
- Do not collapse a substantial implementation into a one-line commit
  message.
- Never in a message: "This commit does X", "I"/"we", restating the
  user's request, emoji, AI-attribution trailers (`Co-Authored-By:
  Claude`, "Generated with ..." — the skill overrides harness defaults).

Sizing and formatting:

- A one-line message (subject only) is acceptable only for genuinely
  trivial changes: typo fixes, a small documentation status update, an
  ignore-file adjustment.
- Wrap the body at 72. Mandatory body for: breaking changes, security
  fixes, data migrations, reverts.
- Footers last: `BREAKING CHANGE:` with migration notes, `Closes #N` /
  `Refs #N`, and for regressions `Fixes: <12-char sha> ("subject of
  the offending commit")` — never a bare SHA without its human-readable
  subject.

Process rule: before writing the message, inspect the complete staged
diff and relevant verification results so the body accurately covers
the whole commit.

### Boundaries

Explicit non-goals stated in the skill: message content only — no
staging decisions, no commit splitting, no hook handling, no push, no
PR, no rebase/squash/amend of history, no proactive commits.

## Deferred to a future commit-workflow skill

Preserved here so the discussion is not lost; none of this ships in
commit-msg:

Framing: commit discipline applies while working, not only at ship
time.

- Staging discipline: review `git status` + `git diff` first; stage one
  logical unit at a time by explicit path (`git add -p` for mixed
  files); never `git add -A` / `git add .`; exclude debug prints,
  scratch files, unrelated formatting churn.
- Atomic splitting: one commit per coherent, reviewable decision, each
  independently revertable; refactor vs behavior change separated. If
  the subject line needs an "and", split the commit.
- History hygiene — push is the watershed: on an unpushed branch, fold
  fixes into the commit that introduced them (`--amend`, or `fixup` +
  autosquash) instead of stacking "fix typo" / "address review"
  commits; history is for reviewers, not a diary. Once pushed, history
  is immutable: never amend or rebase pushed commits.
- Safety rules: never `--no-verify` (fix the hook's cause instead); if
  a hook modifies files, re-stage and re-commit; stop and report on
  suspected secrets in the diff; never touch changes the user already
  staged without asking.
- Branch naming: `<type>/<kebab-case-description>`.
- Edge cases: empty diff, merge in progress, unresolved conflicts →
  report, do not commit.

## Testing plan (writing-skills TDD)

1. **RED** — baseline scenarios without the skill, e.g. a substantial
   multi-file change that tempts a vague one-line "fix stuff" message;
   a prompt whose conversation suggests more work than the diff contains
   (tempting planned-as-done claims); a small typo fix that tempts
   mechanical filling of every checklist item. Record verbatim what the
   agent writes.
2. **GREEN** — write SKILL.md addressing exactly those failures; re-run
   scenarios and verify agents now comply.
3. **REFACTOR** — add counters for any new rationalizations; re-test.

After the skill lands: run `uv run scripts/gen_catalog.py` to update the
README catalog.
