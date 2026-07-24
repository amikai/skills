# Semantics-Preserving Skill Concision

## Goal

Shorten the three existing `SKILL.md` files without changing when they
trigger or how an agent should behave:

- `skills/commit-msg/SKILL.md`: target 15–20% fewer words
- `skills/pr-msg/SKILL.md`: target 25–35% fewer words
- `skills/modern-utility/SKILL.md`: target 10–15% fewer words

Targets are secondary to semantic preservation. Stop before the target if
further reduction would weaken, broaden, narrow, or obscure a rule.

## Semantic Invariants

Preserve every:

- trigger and scope boundary;
- requirement, prohibition, preference, and exception at the same strength;
- decision condition and step order;
- numeric limit, default, command, option, fallback, and output constraint;
- distinction between ordinary and exceptional cases;
- example behavior, contrast, and supported claim;
- repository- or user-instruction precedence rule.

Keep frontmatter names and triggering coverage unchanged. Do not add new
requirements, recommendations, tools, examples, or interpretations.

## Editing Method

Process and verify one skill at a time in this order:

1. `commit-msg`
2. `pr-msg`
3. `modern-utility`

For each skill:

1. Extract an atomic inventory of its normative rules and examples.
2. Establish baseline behavior on representative tasks.
3. Remove repetition, combine equivalent statements, and shorten syntax.
4. Compare every revised passage with its source inventory.
5. Validate structure and behavior before moving to the next skill.

Prefer deleting duplicated explanation over rewriting precise rules. Preserve
commands, code blocks, numeric values, and example outputs verbatim unless a
format-only change is demonstrably neutral.

## Validation

Each skill must pass:

1. **Structural validation**
   - valid YAML frontmatter and Markdown;
   - unchanged `name`;
   - description retains its original trigger coverage;
   - all referenced commands, tools, options, and examples remain valid.
2. **Static semantic comparison**
   - map every original atomic rule to revised text;
   - flag missing, added, weaker, stronger, broader, or narrower language;
   - compare all modal terms, conditions, exceptions, numbers, and precedence.
3. **Behavioral comparison**
   - run representative scenarios without the skill to expose the need for it;
   - run the same scenarios with the original and revised versions;
   - require materially equivalent decisions, output structure, constraints,
     and explanations from the original and revised versions.
4. **Size check**
   - report before/after line, word, and byte counts;
   - treat the target reduction as a goal, never as a pass condition.

Any semantic discrepancy blocks completion and must be corrected or restored
to the original wording.

## Scope

Change only the three `SKILL.md` files. Do not rename skills, add resources,
change repository configuration, or alter unrelated files.
