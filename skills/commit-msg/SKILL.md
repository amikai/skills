---
name: commit-msg
description: Generate commit-msg. Use whenever writing, creating, or drafting a git commit.
---

# Git Commit Message Standard

Follows Conventional Commits specification (`<type>(<scope>): <subject>`).

## Mode Selection

Select mode based on `git diff --staged`:
- **Fast Mode**: Routine changes, simple refactors, typo fixes, or self-evident diffs.
- **Detailed Mode**: Non-obvious bugs, complex logic/architectures, trade-offs, workarounds, or breaking changes.

---

## Fast Mode

Format: `<type>(<scope>): <outcome>`
- **Subject line only** (omit body unless a short bullet adds essential value).
- Imperative mood, max 72 chars (<= 50 preferred), no trailing period.
- Focus on outcome/goal, not code edits (e.g., `fix(auth): reject empty usernames`).

---

## Detailed Mode

- **Subject**: `<type>(<scope>): <intent>` (max 72 chars).
- **Body Structure**: Address the following 3 elements:
  1. **Why Needed**: Problem, failure symptom, or requirement prompting the change.
  2. **Mechanism / Intent**: High-level explanation of the logic or workaround.
  3. **Why This Approach**: Selection rationale, trade-offs, or discarded alternatives.
- **Context**: Include greppable error logs, exact symbols, configuration keys, or version numbers.
- **Anti-Hallucination**: Do not invent motivations or performance claims unsupported by diff/prompt; stick strictly to facts.
- **Footers**: `BREAKING CHANGE: <details>`, `Fixes: <12-char-sha> ("<subject>")`, or `Closes #<issue_number>`.

---

## Reference Examples

### Fast Mode
```text
docs: fix typo in installation guide
```

### Detailed Mode: Special Implementation
```text
fix(auth): retry token exchange on transient clock skew

Why Needed:
Intermittent 401 errors occurred immediately after user login when the application server clock drifted >200ms behind the auth provider.

Intent & Solution:
Allow a 2-second grace period window during token verification instead of rejecting the request. A strict expiration check is still enforced after the grace window to preserve security.
```

### Detailed Mode: Complex Implementation
```text
feat(rate-limit): add token bucket rate limiter to API gateway

Why Needed:
Traffic bursts during peak hours caused severe downstream database connection pool exhaustion. The previous fixed-window limiter allowed 100% of minute traffic to flood in during the first 100ms of every window.

High-Level Mechanism:
- Tokens are refilled asynchronously at a constant rate (`refill_rate`).
- Incoming requests consume tokens from the bucket; requests are rejected with 429 when empty.
- Burst capacity is capped by `bucket_capacity` to absorb short spikes smoothly.

Why Token Bucket over Leaky Bucket / Redis:
Token Bucket permits controlled traffic bursts while maintaining a steady average rate. Using an in-memory bucket avoids Redis roundtrip latency overhead for single-instance deployments.
```
