# Credits

Sources that shaped the rules in this skill.

## Chris Beams — "How to Write a Git Commit Message"

<https://cbea.ms/git-commit/>

- The 50-char subject / 72-char body-wrap limits and the blank line
  separating subject from body.
- No trailing period on the subject.
- Imperative mood, verified with his test sentence: "If applied, this
  commit will ___".
- The "what and why vs. how" body principle, which this skill sharpens
  into "write what the diff cannot show".

## Tim Pope — "A Note About Git Commit Messages"

<https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>

- The original statement of the 50/72 convention that Beams later
  popularized.

## Conventional Commits

<https://www.conventionalcommits.org/>

- The subject format `<type>(<scope>): <description>`, the type
  vocabulary, and the `BREAKING CHANGE:` footer.

## Linux kernel — "Submitting patches"

<https://www.kernel.org/doc/html/latest/process/submitting-patches.html>

- Problem-first bodies: establish the underlying problem before
  describing the solution.
- Describe the user-visible impact.
- Back performance/memory/size claims with numbers and acknowledge the
  trade-off paid.
- Include the distilled (greppable) error or backtrace excerpt for bug
  fixes, never the full dump.
- The `Fixes: <sha> ("subject")` tag format.

## Linus Torvalds — notes on commit messages

<https://yarchive.net/comp/linux/commit_messages.html>

- Write for an outsider with no context.
- Be honest about scope in the subject.
- Short paragraphs instead of one dense block.
- Never reference a commit by bare SHA without its human-readable
  subject.

## caveman-commit (Claude Code plugin marketplace, `caveman` plugin)

- The "what never goes in" list style (no "This commit does X", no
  first person, no emoji, no AI-attribution trailers).
- Expressing exceptions as observable conditions (mandatory body for
  breaking changes, security fixes, migrations, reverts) rather than
  vague "when needed".

## PaulRBerg/agent-skills — `commit` skill

<https://github.com/PaulRBerg/agent-skills>

- Workflow reference during design; reinforced deriving the message
  from the staged diff rather than the conversation.

## Example commit

The example in SKILL.md is Linux kernel commit
[`8173f7e2ce67`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8173f7e2ce67)
("rhashtable: clear stale iter->p on table restart") by Cen Zhang,
reproduced (crash stack condensed, review trailers omitted) under the
kernel's GPL-2.0 license terms.

## [@xavierforge](https://github.com/xavierforge) — "Commit discipline" guidance

Their guidance block shaped the deferred commit-workflow scope in the
design spec (docs/superpowers/specs/2026-07-23-commit-skill-design.md)
and should be re-credited when that skill ships:

- Framing commit discipline as applying while working, not only at
  ship time.
- The "and" test: if the subject line needs an "and", split the
  commit; one commit per coherent, reviewable decision.
- Push as the watershed for history hygiene: on an unpushed branch,
  fold fixes into the commit that introduced them (`--amend`, `fixup`
  + autosquash) instead of stacking "fix typo" commits — history is
  for reviewers, not a diary.
- Branch naming: `<type>/<kebab-case-description>`.
- Lowercase scope named after the subsystem in the subject.

## [@Nanako0129](https://github.com/Nanako0129) — "Commit message style" guidance

The single largest influence on this skill's body rules. Their
guidance block contributed:

- The "durable engineering records, not one-line summaries" framing.
- The `<type>(<scope>): <outcome>` subject phrasing.
- Most of the body checklist: concrete behavior now present (modules,
  components, entry points, data contracts, ownership boundaries),
  end-to-end data/control flow when material, runtime semantics
  (caching, persistence, polling intervals, concurrency, fallback,
  error handling, compatibility, migration), naming specific symbols/
  commands/configuration keys/durations/versions/upstream revisions,
  and mentioning verification.
- The honesty rules: describe only work actually included, never
  present planned follow-up as completed, don't restate the subject or
  list filenames, don't collapse a substantial implementation into one
  line.
- The trivial-change exception wording and the pre-write rule to
  inspect the complete staged diff so the body covers the whole
  commit.
