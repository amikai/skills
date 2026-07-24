---
name: commit-msg
description: Write clear Git commit messages using Fast Mode for routine changes or Detailed Mode for motivation (Why), implementation mechanisms, and non-obvious choices. Use when creating or reviewing git commits.
---

# Git Commit Message Standard

This skill enforces deterministic commit message generation with two operational modes: **Fast Mode** for routine changes and **Detailed Mode** for complex or special implementations.

## Phase 1: Legwork & Mode Selection

Before drafting the message, inspect the staged diff or changes (`git diff --staged`) and select the appropriate mode:

### Fast Mode (Select if ALL apply):
- Routine feature additions, simple refactors, typo fixes, or test additions.
- The change logic is self-evident directly from reading the diff.
- No breaking changes, race conditions, workarounds, or hidden trade-offs involved.

### Detailed Mode (Select if ANY apply):
- Fixes a non-obvious bug, race condition, or edge case (Special Implementation).
- Introduces a new algorithm, subsystem, architectural pattern, or state machine (Complex Implementation).
- Involves architectural trade-offs, performance workarounds, or third-party bug mitigations.
- Introduces a breaking change or alters existing API contracts.

---

## Fast Mode Workflow

Use Fast Mode for quick, self-evident commits.

### Rules
1. **Format**: `<type>(<scope>): <outcome>`
2. **Subject Only**: Body is omitted unless a short 1-bullet summary adds clear value.
3. **Imperative Mood**: State what the commit achieves (e.g., `add`, `fix`, `update`).
4. **Length**: <= 50 chars preferred, max 72 chars. No trailing period.

### Fast Mode Completion Criteria
- [ ] Imperative mood in English (completes "If applied, this commit will _____").
- [ ] Focuses on the outcome/goal, not code edits (e.g., `fix(auth): reject empty usernames`).
- [ ] Contains no emojis, no AI attribution tags, and no pronouns.

---

## Detailed Mode Workflow

Use Detailed Mode to document **Why** the change was needed, **What** the high-level mechanism is, and **Why this specific approach** was chosen.

### Step 1: Formulate Subject
Format: `<type>(<scope>): <high-level-intent>`
Focus on the primary system outcome or problem prevented.

### Step 2: Formulate Body Structure (Must Answer "Why")

A Detailed Mode body must address the following 3 elements:

1. **Why Needed (Motivation & Problem)**
   - What root problem, failure symptom, performance bottleneck, or business requirement forced this change?

2. **Mechanism / Intent (High-Level Overview)**
   - **For Special Implementations**: State the specific intent behind the workaround, retry logic, or edge case handling.
   - **For Complex Implementations**: Provide a high-level description of what the mechanism is doing conceptually (e.g., how data flows through the Rate Limiter, State Machine, or Queue).

3. **Why This Approach & Trade-offs (Selection Rationale)**
   - Why was this specific mechanism or pattern chosen over simpler alternatives?
   - What trade-offs were made (e.g., higher memory usage traded for lower CPU latency)?
   - (Optional) Document any discarded alternatives that failed during testing.

### Step 3: Precise Context & Traceability
Include exact details that make the commit searchable:
- **Error logs**: Distilled, greppable error line (for future `git log --grep` searches).
- **Exact symbols**: Relevant configuration keys, duration limits, or version numbers.

### Step 4: Anti-Hallucination Guardrail
If the underlying motivation (Why) or mechanism logic is NOT present in the diff, code comments, or prompt:
- DO NOT invent reasons (e.g., do not claim "improves performance" without benchmarks).
- State factual behavior changes only, or prompt the user for missing rationale.

### Step 5: Footers
- `BREAKING CHANGE: <migration details>`
- `Fixes: <12-char-sha> ("<original commit subject>")` for regressions.
- `Closes #<issue_number>` for issue links.

---

## Phase 5: Verification Checklist & Fluff Detection (Both Modes)

Verify the generated message against these strict criteria before completion:

### Fluff & Buzzword Blacklist
Must NOT contain vague phrases unless backed by concrete metrics or specific technical details:
- "Cleaned up code" / "Refactored for readability"
- "Improved performance" (without metrics or exact bottleneck)
- "Enhanced security / robustness"
- "Various fixes and improvements"

### Structural Constraints
- [ ] **Answers Why**: Does the message explicitly state *why* the change was needed and *why* this approach was chosen?
- [ ] **No Pronouns**: Contains no "I", "we", "my".
- [ ] **No AI Attribution**: Contains no `Co-Authored-By: AI...` or `Generated with...` tags.
- [ ] **No Emoji**: No emoji characters in subject or body.
- [ ] **Context Over Diff**: Can a developer reading this 2 years later understand the problem, mechanism, and trade-offs without reading line-by-line diffs?

> **Completion Criterion**: All checklist items pass, and zero blacklisted phrases exist in the message.

---

## Reference Examples

### Fast Mode Example
```text
docs: fix typo in installation guide
```

### Detailed Mode Example 1: Special Implementation (Why & Workaround Intent)
```text
fix(auth): retry token exchange on transient clock skew

Why Needed:
Intermittent 401 errors occurred immediately after user login when the application server clock drifted >200ms behind the auth provider.

Intent & Solution:
Allow a 2-second grace period window during token verification instead of rejecting the request. A strict expiration check is still enforced after the grace window to preserve security.
```

### Detailed Mode Example 2: Complex Implementation (Why Needed + High-Level Mechanism + Why This Approach)
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
