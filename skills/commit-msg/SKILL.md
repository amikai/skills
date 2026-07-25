---
name: commit-msg
description: Generate commit-msg, conventional commit. Use whenever writing, creating, or drafting a git commit. Trigger for git commit -F.
---

# Git Commit Message Standard

Treat commit messages as durable engineering records appropriate to the scope and impact of the change.

## 0. Pre-requisite & Agent Operation Boundary

- **Empty Staging Area**: Before generating the message, inspect `git diff --staged`. If the diff is empty, STOP and ask the user if they want you to stage files (`git add`). **DO NOT run `git add` autonomously** without explicit permission.
- **Commit Execution**: When executing the commit on behalf of the user, **DO NOT** use `git commit -m "..."` for multi-line messages, as shell escaping often corrupts the formatting. Write the generated commit message to a temporary file (e.g., `/tmp/commit-msg.txt`), then execute `git commit -F /tmp/commit-msg.txt`.
- **Language**: Default to English unless the user explicitly requests another language or the repository convention dictates otherwise.
- **Formatting Rule (50/72 Rule)**: The subject line MUST be max 72 chars (target around 50 chars). The body MUST be manually word-wrapped at 72 characters per line.

## 1. Type & Scope Definitions

Format: `<type>(<scope>): <outcome>`

### Allowed `<type>` List:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Defining `<scope>`:
- Represents the module, package, directory, or architectural layer affected (e.g., `api`, `auth`, `db`, `ui`).
- Omit the scope if the change is global or affects multiple unrelated areas.

## 2. Tier Selection Heuristics

Select the mode based on objective indicators in `git diff --staged`:

- **Fast Mode**: Trivial changes (e.g., single-file typos, minor doc tweaks, `.gitignore` updates).
- **Detail Mode**: Standard non-trivial changes (e.g., typical bug fixes, standard features, refactors affecting a few files or a single module).
- **Verbose Mode**: Complex or critical changes (e.g., modifying public API contracts or data schemas, database migrations, concurrency/persistence logic, sweeping refactors across multiple modules, breaking changes).

## 3. Mode Templates

### Fast Mode
- **Subject line only**. Imperative mood. No trailing period.
- *Check*: "If applied, this commit will [your subject]".

### Detail / Verbose Mode
Use the following unified structure for all non-trivial commits. For Verbose Mode, provide deeper architectural, concurrency, and system-level details under these same headers:

```text
<type>(<scope>): <outcome>

Why Needed:
<Problem, failure symptom, or requirement prompting the change. Explain the 'Why'>

Mechanism & Solution:
<Explanation of logic, affected modules, data flow, or workaround. For Verbose mode: include runtime semantics, concurrency, and trade-offs>

Verification (if applicable):
<ONLY record tests or checks actually executed in the current session>
```

**⚠️ STRICT ANTI-HALLUCINATION WARNING for Verification**:
Do NOT guess test filenames or CI pipelines. If you have not executed any tests or verification commands in the current session, **delete/omit the `Verification` section entirely**.

## 4. Footers

When applicable, place footers at the very bottom of the commit message after a blank line:

- **Breaking Changes**: `BREAKING CHANGE: <details and migration instructions>`
- **Issue Tracking**: `Closes #<issue_number>`, `Fixes #<issue_number>`, or `Refs #<issue_number>`
- **Commit References**: `Fixes: <12-char-sha> ("<subject>")`

## 5. Reference Examples

### Fast Mode
```text
docs: fix typo in installation guide
```

### Detail Mode
```text
fix(auth): retry token exchange on transient clock skew

Why Needed:
Intermittent 401 errors occurred immediately after user login when the
application server clock drifted >200ms behind the auth provider.

Mechanism & Solution:
Allow a 2-second grace period window in `VerifyToken()` during token
verification instead of rejecting the request immediately. A strict
expiration check is still enforced after the grace window.

Verification (if applicable):
Ran `go test ./pkg/auth/...` with simulated clock drift up to 500ms.
```

### Verbose Mode
```text
feat(rate-limit): add token bucket rate limiter to API gateway

Why Needed:
Downstream database connection pools were exhausted during traffic spikes,
causing cascading HTTP 500 outages across dependent gateway services.

Mechanism & Solution:
Implement an in-memory token bucket algorithm for `GatewayRouter`. Requests
exceeding capacity immediately return HTTP 429 (`ErrRateLimitExceeded`)
without acquiring DB connections.

State is maintained purely in-memory using atomic CAS operations for token
deduction under high concurrency. A background ticker (100ms) replenishes
tokens up to `bucket_capacity` (500). Pure in-memory state avoids Redis
round-trip latency overhead for single-instance deployments.

Verification (if applicable):
Ran `go test -v ./pkg/ratelimit/...` and load test with `vegeta` at 1000 QPS.
```
