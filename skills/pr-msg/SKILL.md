---
name: pr-msg
description: >
  Write clear, structured Pull Request titles and descriptions. Use whenever creating or updating a pull request.
---

# Pull Requests

Write PR and MR titles and descriptions at the level of intent and architecture — not a line-by-line narration of the diff, which is already visible in the code view.

- **5-minute rule**: a reviewer must grasp the purpose, context, and approach within 5 minutes; simplify until that's true.
- **Small and focused**: build each PR around one cohesive goal. Don't mix unrelated changes (e.g., a refactor with a new feature); use Draft PRs for work-in-progress.

## Gathering Context

Before drafting or rewriting, run `git log <base>..HEAD` and `git diff <base>...HEAD` to inspect the actual changes. Check for repository PR templates in `.github/` or `.gitlab/`, plus linked issues, specs, and design docs. Ground the description only in work actually present in the diff — never uncommitted local changes or planned follow-ups.

### Reviewing an existing PR

1. Read the current title and body (e.g. `gh pr view --json title,body`).
2. Compare them against the diff, the repository template, and linked requirements; identify missing, inaccurate, or unsupported claims.
3. Report findings first, grouped by severity, then give suggested wording or a revised description.

### Large or complex PRs

- Suggest a reading order for the files (e.g., "schema change, then core handler, then tests").
- Specify the feedback type needed: high-level design review, performance verification, security check, or simple sanity check.

## Title

Unless the repository specifies another format, use Conventional Commits: `<type>(<scope>): <outcome>`.
- Types: `feat` `fix` `refactor` `perf` `docs` `test` `chore` `build` `ci` `style` `revert`.
- Imperative mood, English, ≤72 characters, no trailing period.
- Name the outcome, not the edit: `feat(auth): add multi-factor authentication`, not `fix: update logic in user_service.go`.

## Description

Use these sections in the PR body, omitting any that are empty or irrelevant. For a small, low-risk PR, a single concise paragraph covering the change, its motivation or user impact, and verification replaces the full template and diagram.

```markdown
## Summary
A 1–3 sentence high-level overview of what this PR accomplishes.

## Motivation & Context
Why is this change necessary? Link relevant issues (`Closes #123`, `Refs #456`) and explain the business impact or constraints.

## Architecture & Diagrams
For structural changes, include a Mermaid diagram (sequence, flowchart, state, ER) to visualize flows, transitions, or component interactions.

## Key Changes
Logical high-level changes (e.g., subsystem updates, API contract updates). Avoid line-by-line file details.

## Reviewer Guidance
(Optional) Suggested file review sequence or specific areas requiring closer inspection.

## Verification & Testing
Explain how the changes were verified (e.g., unit test commands run, manual verification steps executed).

## Risks & Rollout
Known risks, monitoring signals, rollback steps, or security impact. Omit when irrelevant.

## Breaking Changes & Migration
Required configuration updates, database migrations, or breaking API changes.
```

## Mermaid Diagrams

Use a diagram for complex refactors, multi-service integrations, or state-machine changes, to cut reviewer cognitive load:
- **Sequence (`sequenceDiagram`)**: multi-service request/response flows or async messaging.
- **Flowchart (`flowchart TD`)**: logical routing, decision branching, or data pipelines.
- **State (`stateDiagram-v2`)**: lifecycle states or finite state machines.
- **Class/Entity (`classDiagram` / `erDiagram`)**: database schema or data model shifts.

Keep the diagram scoped strictly to the changed path, and confirm the syntax renders in markdown preview.

## Evidence and Hygiene

- Never invent test results, impact, component ownership, or implementation details — state uncertainty or omit the unsupported claim.
- Skip filler text and AI-attribution footers.
- Include before/after screenshots or recordings for UI changes when available.

## Examples

`references/examples.md` has three worked examples — a small bug-fix PR, a feature PR, and a complex architectural refactor with a Mermaid diagram — load it when drafting one of these shapes from scratch.
