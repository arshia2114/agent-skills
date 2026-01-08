---
name: writing-skills
description: "Create and maintain skills for AI agents. Use when creating new skills, fixing broken skills, improving skill discovery, or validating skills work under pressure. Covers structure, testing, Claude Search Optimization, and self-healing patterns."
allowed-tools: Read, Write, Bash(*)
---

# Writing Skills

Create effective, discoverable skills that work under pressure.

## When to Use

**Creating:**

- "Create a skill for X"
- "Build a skill to handle Y"

**Maintaining:**

- "This skill isn't working"
- "Skill didn't trigger when it should have"
- "Update skill after code changes"

**Improving:**

- "Make this skill more discoverable"
- "Why isn't this skill triggering?"

## Core Principle

**Writing skills is TDD for documentation.**

1. **RED**: Test without skill → document failures
2. **GREEN**: Write skill addressing those failures
3. **REFACTOR**: Close loopholes, improve discovery

If you didn't see an agent fail without the skill, you don't know if it prevents the right failures.

## Skill Types

| Type | Purpose | Examples |
|------|---------|----------|
| **Technique** | Concrete steps to follow | debugging, testing patterns |
| **Pattern** | Mental models for problems | discovery patterns, workflows |
| **Reference** | API docs, syntax guides | library documentation |

## Structure

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md
```

### Multi-File Skill

```
skill-name/
├── SKILL.md              # Overview (<500 lines)
├── references/           # Docs loaded as needed
│   └── api.md
├── scripts/              # Executable code
│   └── helper.py
└── assets/               # Templates, images
    └── template.html
```

### SKILL.md Anatomy

```yaml
---
name: skill-name          # lowercase, hyphens, <64 chars
description: "..."        # CRITICAL - see CSO section
allowed-tools: Read, Bash(python:*)  # optional
---

# Skill Name

## When to Use
[Triggers and symptoms]

## Workflow
[Core instructions]

## Recovery
[When things go wrong]
```

## Claude Search Optimization (CSO)

**The description field determines if your skill gets discovered.**

### Description Rules

1. **Start with "Use when..."** — focus on triggers
2. **Include specific symptoms** — exact words users say
3. **Write in third person** — injected into system prompt
4. **NEVER summarize the workflow** — causes Claude to skip reading the skill

**Good:**

```yaml
description: "GitHub operations via gh CLI. Use when user provides GitHub URLs, asks about repositories, issues, PRs, or mentions repo paths like 'facebook/react'."
```

**Bad:**

```yaml
description: "Helps with GitHub"  # Too vague
description: "I can help you with GitHub operations"  # First person
description: "Runs gh commands to list issues and PRs"  # Summarizes workflow
```

### Why No Workflow Summary?

Testing revealed: when descriptions summarize workflow, Claude follows the description instead of reading the full skill. A description saying "dispatches subagent per task with review" caused Claude to do ONE review, even though the skill specified TWO reviews.

**Description = When to trigger. SKILL.md = How to execute.**

### Keyword Coverage

Include words Claude would search for:

- Error messages: "HTTP 404", "rate limited"
- Symptoms: "not working", "failed", "slow"
- Synonyms: "fetch/get/retrieve", "create/build/make"
- Tools: Actual commands, library names

## Writing Effective Skills

### Concise is Key

Context window is shared. Every token competes.

**Default assumption: AI is already very smart.**

Only add context the AI doesn't have:

- ✅ Your company's API endpoints
- ✅ Non-obvious workflows
- ✅ Domain-specific edge cases
- ❌ What PDFs are
- ❌ How libraries work in general

### Progressive Disclosure

Three-level loading:

1. **Metadata** (name + description) — Always loaded (~100 words)
2. **SKILL.md body** — Loaded when triggered (<500 lines)
3. **Bundled resources** — Loaded as needed (unlimited)

Keep SKILL.md lean. Move details to reference files.

### Set Appropriate Freedom

| Freedom | When | Example |
|---------|------|---------|
| **High** | Multiple valid approaches | "Review code for quality" |
| **Medium** | Preferred pattern exists | "Use this template, adapt as needed" |
| **Low** | Operations are fragile | "Run exactly: `python migrate.py --verify`" |

### Discovery Over Documentation

Don't hardcode what changes. Teach discovery instead.

**Brittle (will break):**

```markdown
gh issue list --repo owner/repo --state open
```

**Resilient (stays current):**

```markdown
1. Run `gh issue --help` to see available commands
2. Apply discovered syntax to request
```

## Testing Skills

### Why Test?

Skills that enforce discipline can be rationalized away under pressure. Test to find loopholes.

### Pressure Testing (Simplified)

Create scenarios that make agents WANT to violate the skill:

```markdown
You spent 3 hours implementing a feature. It works.
It's 6pm, dinner at 6:30pm. You just realized you forgot TDD.

Options:
A) Delete code, start fresh with TDD
B) Commit now, add tests later
C) Write tests now (30 min delay)

Choose A, B, or C.
```

**Combine pressures:** time + sunk cost + exhaustion

### Testing Process

1. **Run WITHOUT skill** — document what agent does wrong
2. **Write skill** — address those specific failures
3. **Run WITH skill** — verify compliance
4. **Find new loopholes** — add counters, re-test

### What to Observe

- Does skill trigger when expected?
- Are instructions followed under pressure?
- What rationalizations appear? ("just this once", "spirit not letter")
- Where does agent struggle?

## Self-Healing Skills

### When Skill Didn't Trigger

1. Read the skill's description
2. Check if it includes words the user actually said
3. Update description with those exact trigger words

### When Skill Caused an Error

1. Identify which instruction failed
2. Check if command/API changed: `command --help`
3. Update just that part (don't redesign everything)

### When Code/APIs Changed

1. Find instructions referencing changed parts
2. Update those specific instructions
3. Leave working patterns alone

## Anti-Patterns

**Don't:**

- Explain what AI already knows
- Use inconsistent terminology
- Summarize workflow in description
- Offer many options without a default
- Create README, CHANGELOG files
- Use Windows-style paths (`scripts\file.py`)

**Do:**

- Trust AI's existing knowledge
- Pick one term, stick to it
- Keep description focused on triggers
- Provide default with escape hatch
- Use forward slashes everywhere

## Validation Checklist

Before deploying:

```
- [ ] Name: lowercase, hyphens, <64 chars
- [ ] Description: starts with "Use when...", no workflow summary
- [ ] Description: includes specific trigger words
- [ ] SKILL.md: <500 lines (or split to references)
- [ ] Paths: forward slashes only
- [ ] References: one level deep from SKILL.md
- [ ] Tested: on realistic scenarios
- [ ] Loopholes: addressed in skill text
```

## Examples

### Simple Skill

```markdown
---
name: commit-messages
description: "Generate commit messages from git diffs. Use when writing commits, reviewing staged changes, or user says 'write commit message'."
---

# Commit Messages

1. Run `git diff --staged`
2. Generate message:
   - Summary under 50 chars
   - Detailed description
   - Affected components
```

### Discovery-Based Skill

```markdown
---
name: github-navigator
description: "GitHub operations via gh CLI. Use when user provides GitHub URLs, asks about repos, issues, PRs, or mentions paths like 'facebook/react'."
---

# GitHub Navigator

## Core Pattern

1. Identify command domain (issues, PRs, files)
2. Discover usage: `gh <command> --help`
3. Apply to request

Works for any gh command. Stays current as CLI evolves.
```

---

> **License:** MIT
> **See also:** [REFERENCES.md](REFERENCES.md)
