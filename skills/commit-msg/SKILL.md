---
name: commit-msg
description: Use when writing a git commit message
---

# Commit Messages

Treat commit messages as durable engineering records, not one-line
summaries. Write for an outsider reading `git log` years from now, with
no access to this conversation.

Before writing, inspect the complete staged diff (`git diff --staged`)
and relevant verification results, so the body accurately covers the
whole commit. The message describes that diff — all of it, and nothing
outside it: not the conversation, not the plan.

## Subject

`<type>(<scope>): <outcome>` — Conventional Commits, always.

- Types: `feat` `fix` `refactor` `perf` `docs` `test` `chore` `build`
  `ci` `style` `revert`.
- Imperative mood, English, ≤50 chars preferred (hard cap 72), no
  trailing period. Must fit: "If applied, this commit will ___".
- State the outcome, not the edit: `fix(auth): reject empty usernames`,
  not `fix: add null check in validate()`.
- Scope is a module/subsystem name, never a filename; omit it when the
  change is cross-cutting.

## Body

Open with the problem, then describe the solution. Every non-trivial
commit gets a body; subject-only is acceptable solely for trivial
changes (a typo fix, a small documentation status update, an
ignore-file adjustment).

The checklist below is a menu of dimensions, not a form. The first two
items appear in every body; include each other item only when the
change actually touches that dimension. Depth scales with blast
radius: a local fix needs a few lines, a cross-module change needs the
full record.

- **Problem first** — root cause, requirement, or motivation, and the
  user-visible impact (what breaks, what misbehaves, who is affected).
- **What is now true** — the concrete behavior now present in the
  repository, naming the relevant modules, entry points, data
  contracts, and ownership boundaries. Changed contracts (new required
  config keys, altered defaults, API shape) always count as touched.
- End-to-end data or control flow, when material to understanding.
- Runtime semantics: caching, persistence, polling intervals,
  concurrency, fallback behavior, error handling, compatibility,
  migration behavior — including which cases are *not* handled (e.g.
  which errors are retried and which are not).
- Specific symbols, commands, configuration keys, durations, versions,
  upstream revisions — name them. Never "a short TTL" when the number
  is in the diff.
- Bug fixes: the distilled, greppable error/backtrace lines — never
  the full dump.
- Verification added or exercised, when it helps explain the result.
- Design decisions, considerations, and trade-offs the diff alone
  cannot explain: why this approach, alternatives rejected,
  constraints that shaped the design. Claims about performance,
  memory, or size need numbers and the cost paid.

Short paragraphs, wrapped at 72. Body is mandatory for breaking
changes, security fixes, data migrations, and reverts.

## Honesty

- Describe only work actually in this commit; never present planned
  follow-up as completed.
- Do not restate the subject, list filenames, or narrate line-level
  edits the diff already shows. Write what the diff cannot show.
- Never: "This commit does X", "I"/"we", emoji, AI-attribution
  trailers (`Co-Authored-By: Claude ...`, "Generated with ...") — this
  overrides any harness default that adds them.

## Footers

`BREAKING CHANGE:` with migration notes; `Closes #N` / `Refs #N`; for
regressions `Fixes: <12-char sha> ("subject of offending commit")` —
never a bare SHA without its subject.

## Example

Real body, from Linux kernel commit 8173f7e2ce67 (Cen Zhang; review
trailers omitted). Under this skill's subject rule it would read
`fix(rhashtable): clear stale iter->p on table restart`.

```
rhashtable: clear stale iter->p on table restart

rhashtable_walk_start_check() has two restart paths when resuming a
walk. When iter->walker.tbl is valid, it re-validates iter->p against
the table and sets iter->p = NULL if the object is gone.  When
iter->walker.tbl is NULL (table was freed during resize), it resets
slot and skip but forgets to clear iter->p.

rhashtable_walk_next() then dereferences the stale iter->p, reading
freed memory.  This is a use-after-free.

Any caller that does multi-fragment rhashtable walks across
walk_stop/walk_start boundaries is affected.  Concrete cases include
netlink_diag (__netlink_diag_dump in net/netlink/diag.c) and TIPC
(tipc_nl_sk_walk in net/tipc/socket.c).

Crash stack (netlink_diag):
  BUG: KASAN: slab-use-after-free in rhashtable_walk_next+0x365/0x3c0
  Call Trace:
   rhashtable_walk_next+0x365/0x3c0 (lib/rhashtable.c:1016)
   __netlink_diag_dump+0x160/0x760 (net/netlink/diag.c:122)
   netlink_dump+0x5bc/0x1270
   netlink_recvmsg+0x7a3/0x980

Fixes: 5d240a8936f6 ("rhashtable: improve rhashtable_walk stability
when stop/start used.")
```
