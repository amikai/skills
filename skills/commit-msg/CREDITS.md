# Credits

Sources that shaped the rules in this skill.

- [Chris Beams — "How to Write a Git Commit Message"](https://cbea.ms/git-commit/):
  the 50/72 limits, the blank line after the subject, no trailing
  period, the imperative-mood test sentence, and the "what and why vs.
  how" body principle.
- [Tim Pope — "A Note About Git Commit Messages"](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html):
  the original statement of the 50/72 convention.
- [Conventional Commits](https://www.conventionalcommits.org/): the
  `<type>(<scope>): <description>` subject format, the type
  vocabulary, and the `BREAKING CHANGE:` footer.
- [Linux kernel — "Submitting patches"](https://www.kernel.org/doc/html/latest/process/submitting-patches.html):
  problem-first bodies, user-visible impact, numbers behind
  performance claims, distilled error excerpts for bug fixes, and the
  `Fixes:` tag format.
- [Linus Torvalds — notes on commit messages](https://yarchive.net/comp/linux/commit_messages.html):
  write for an outsider, keep the subject honest about scope, use
  short paragraphs, and never cite a bare SHA without its subject.
- caveman-commit (Claude Code plugin marketplace, `caveman` plugin):
  the "what never goes in" list style and phrasing exceptions as
  observable conditions instead of "when needed".
- [PaulRBerg/agent-skills — `commit` skill](https://github.com/PaulRBerg/agent-skills):
  workflow reference; reinforced deriving the message from the staged
  diff rather than the conversation.
- [@xavierforge](https://github.com/xavierforge) — "Commit discipline"
  guidance: the "and" test for splitting commits, push as the
  watershed for history hygiene, and branch/scope naming; shaped the
  deferred commit-workflow scope in the design spec
  (docs/superpowers/specs/2026-07-23-commit-skill-design.md) and
  should be re-credited when that skill ships.
- [@Nanako0129](https://github.com/Nanako0129) — "Commit message
  style" guidance: the largest influence on the body rules: the
  durable-record framing, most of the body checklist, and the honesty
  rules.
