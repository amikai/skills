---
name: commit-msg
description: Generate commit-msg. Use whenever writing, creating, or drafting a git commit.
---

# Git Commit Message Standard

Treat commit messages as durable engineering records appropriate to the scope and impact of the change.

## Pre-Writing Inspection

Before writing the message, inspect the complete staged diff (`git diff --staged`) and relevant verification results so the body accurately covers the whole commit.

## Tier Selection

Select the mode based on the scope, complexity, and impact of `git diff --staged`:

- **Fast Mode**: Trivial changes (typos, small doc updates, ignore-file tweaks).
- **Detail Mode**: Standard non-trivial changes (everyday features, refactors, bug fixes, component updates).
- **Verbose Mode**: Complex systems, architectural changes, breaking changes, critical performance optimizations, or subtle workarounds.

## 1. Fast Mode (Trivial Changes)

Acceptable only for genuinely trivial changes.

Format: `<type>(<scope>): <outcome>`
- **Subject line only** (max 72 chars, imperative mood, no trailing period).
- Focus on outcome/goal, not code edits (e.g., `docs: fix typo in installation guide`).

## 2. Detail Mode (Standard Non-Trivial Changes)

Required for everyday features, bug fixes, and refactors.

Format:
```text
<type>(<scope>): <outcome>

Why Needed:
<Problem, failure symptom, or requirement prompting the change>

Mechanism & Solution:
<Explanation of logic, affected modules/symbols, data flow, or workaround>

Rationale & Trade-offs (if applicable):
<Why this approach was chosen over simple alternatives>

Verification:
<Tests or checks executed>
```

## 3. Verbose Mode (Complex Systems & Architectural Changes)

Required for complex features, architectural overhauls, core data contract shifts, or breaking changes.

Format:
```text
<type>(<scope>): <outcome>

<Detailed body containing key engineering record elements>
```

### Body Content Requirements (Verbose Mode)
The body should **contain** the following key elements as relevant. These can be written as natural paragraphs (combining 1–2 elements per paragraph) or organized into logical sections as appropriate:

- **Concrete Behavior & Boundaries**: Behavior present in the codebase, entry points, data contracts, and ownership boundaries.
- **End-to-End Data & Control Flow**: Data or control flow when material to understanding the change.
- **Runtime & Concurrency Semantics**: Caching, persistence, atomic operations, polling intervals, concurrency, fallback behavior, and error handling.
- **Specific Identifiers**: Name specific symbols, commands, configuration keys, durations, versions, and error codes.
- **Implementation Decisions & Trade-offs**: Key choices and rationale, especially where diff alone doesn't explain why.
- **Verification Record**: Tests added, load testing, or manual verification exercised.

## Strict Rules & Constraints

- **No Premature Credit**: Describe only work actually included in the commit. Do not present planned follow-up work as completed.
- **No Superficial Summaries**: Do not merely restate the subject or list changed filenames.
- **No Collapsing**: Do not collapse substantial implementations into a one-line message.
- **Anti-Hallucination**: Stick strictly to facts verifiable from the diff and execution logs.

## Footers

When applicable, place footers at the very bottom of the commit message after a blank line:

- **Breaking Changes**: `BREAKING CHANGE: <details and migration instructions>`
- **Issue Tracking**: `Closes #<issue_number>`, `Fixes #<issue_number>`, or `Refs #<issue_number>`
- **Commit References**: `Fixes: <12-char-sha> ("<subject>")`
- **Co-authors**: `Co-authored-by: Name <email>`

## Reference Examples

### Fast Mode
```text
docs: fix typo in installation guide
```

### Detail Mode
```text
fix(auth): retry token exchange on transient clock skew

Why Needed:
Intermittent 401 errors occurred immediately after user login when the application server clock drifted >200ms behind the auth provider.

Mechanism & Solution:
Allow a 2-second grace period window in `VerifyToken()` during token verification instead of rejecting the request immediately. A strict expiration check is still enforced after the grace window.

Verification:
Ran unit tests in `auth_test.go` with simulated clock drift up to 500ms.
```

### Verbose Mode
```text
feat(rate-limit): add token bucket rate limiter to API gateway

Implement an in-memory token bucket algorithm for `GatewayRouter` to prevent downstream database connection pool exhaustion during traffic bursts.

Incoming HTTP requests to `GatewayRouter` pass through `TokenBucket.Consume()`. Requests exceeding capacity immediately return HTTP 429 (`ErrRateLimitExceeded`) without acquiring DB pool connections. State is maintained purely in-memory using atomic CAS operations for token deduction under high concurrency, with a background ticker (`100ms`) continuously replenishing tokens up to `bucket_capacity` (500). Pure in-memory state avoids Redis round-trip latency overhead for single-instance deployments.

Verification:
- Added unit tests in `token_bucket_test.go` verifying concurrent deduction across 100 goroutines.
- Ran load test with `vegeta` at 1000 QPS verifying zero 500 errors and immediate 429 response on capacity overflow.
```

