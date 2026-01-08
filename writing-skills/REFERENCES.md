# References

Best practices, patterns, and links for building skills.

## Table of Contents

- [Discovery Over Documentation](#discovery-over-documentation)
- [Progressive Disclosure](#progressive-disclosure)
- [Description Optimization](#description-optimization)
- [Token Efficiency](#token-efficiency)
- [Naming Conventions](#naming-conventions)
- [Content Patterns](#content-patterns)
- [Testing Patterns](#testing-patterns)
- [Anti-Patterns](#anti-patterns)
- [Example Transformations](#example-transformations)
- [Links](#links)

---

## Discovery Over Documentation

Don't hardcode 500 lines of examples. Teach the pattern instead.

**Bad:**

```markdown
gh issue list --repo owner/repo
gh issue view 123 --repo owner/repo
gh pr list --repo owner/repo
# ... 50 more examples
```

**Good:**

```markdown
1. Identify command domain (files/issues/PRs)
2. Run `gh <command> --help` to discover usage
3. Apply to request
```

This stays current as commands change. Zero maintenance.

---

## Progressive Disclosure

Keep SKILL.md under 500 lines. Move details to separate files.

```
skill/
├── SKILL.md              # Overview (<500 lines)
├── references/
│   ├── api.md            # Detailed API docs
│   └── examples.md       # Usage examples
└── scripts/
    └── helper.py         # Executes without loading into context
```

**Loading levels:**

1. **Metadata** — Always in context (~100 words)
2. **SKILL.md** — Loaded when skill triggers
3. **References** — Loaded only when needed

**Keep references one level deep:**

- ✅ SKILL.md → reference.md
- ❌ SKILL.md → advanced.md → details.md

---

## Description Optimization

The description field is critical for skill discovery.

### Structure

```yaml
description: "[What it does]. Use when [triggers]. Use when [more triggers]."
```

### Rules

| Rule | Why |
|------|-----|
| Start with "Use when..." | Focuses on triggers |
| Include exact user phrases | Matches natural language |
| Write in third person | Injected into system prompt |
| Never summarize workflow | Causes Claude to skip reading skill |
| Keep under 500 chars | Loaded into every conversation |

### Good Examples

```yaml
# GitHub operations
description: "GitHub operations via gh CLI. Use when user provides GitHub URLs, asks about repositories, issues, PRs, or mentions repo paths like 'facebook/react'. Use instead of webfetch for github.com links."

# Documentation lookup
description: "Fetch library documentation via Context7 API. Use when user asks about React, Next.js, Prisma, or any npm/PyPI package. Use when user says 'how do I use X library' or needs official docs."

# UI generation
description: "Create production-grade frontend interfaces. Use when building web components, pages, dashboards, forms, landing pages. Use when user says 'build a form', 'create a dashboard', 'design a component'."
```

### Bad Examples

```yaml
# Too vague
description: "Helps with GitHub"

# First person
description: "I can help you with GitHub operations"

# Summarizes workflow (DANGEROUS)
description: "Runs gh commands to list issues, view PRs, and fetch files"

# Too abstract
description: "For async testing"
```

### Why No Workflow Summary?

Testing revealed that when descriptions summarize workflow, Claude may follow the description instead of reading the full skill body.

Example: A description saying "dispatches subagent per task with code review" caused Claude to do ONE review. The skill's flowchart clearly showed TWO reviews (spec compliance + code quality).

When changed to "Use when executing implementation plans with independent tasks" (no workflow), Claude correctly read the flowchart and followed both reviews.

**The trap:** Descriptions that summarize workflow create a shortcut Claude will take.

---

## Token Efficiency

Context window is shared. Every token competes.

### Target Word Counts

| Skill Type | Target |
|------------|--------|
| Frequently-loaded | <200 words |
| Standard skills | <500 words |
| Reference files | Unlimited (loaded as needed) |

### Techniques

**Move details to tool help:**

```markdown
# Bad: Document all flags
search supports --text, --both, --after DATE, --before DATE, --limit N

# Good: Reference --help
search supports multiple modes. Run --help for details.
```

**Use cross-references:**

```markdown
# Bad: Repeat workflow details
[20 lines of repeated instructions]

# Good: Reference other skill
See [other-skill](../other-skill/SKILL.md) for workflow.
```

**Compress examples:**

```markdown
# Bad: Verbose (42 words)
User: "How did we handle authentication errors in React Router before?"
Assistant: I'll search past conversations for React Router authentication patterns.
[Dispatch subagent with search query: "React Router authentication error handling 401"]

# Good: Minimal (20 words)
User: "How did we handle auth errors in React Router?"
Assistant: Searching... [Dispatch subagent → synthesis]
```

---

## Naming Conventions

### Use Verb-Based Names (Gerunds)

Active verbs describe what you're doing:

| Good | Bad |
|------|-----|
| `writing-skills` | `skill-manager` |
| `processing-pdfs` | `pdf-helper` |
| `navigating-github` | `github-tools` |
| `debugging-code` | `debugger` |

### Format Rules

- Lowercase only
- Hyphens between words
- Max 64 characters
- No underscores, spaces, or special characters

### Avoid Vague Names

- ❌ `helper`, `utils`, `tools`
- ❌ `misc`, `general`, `common`
- ✅ Specific action: `generating-reports`, `validating-forms`

---

## Content Patterns

### Workflow with Checklist

For complex multi-step tasks:

```markdown
## Workflow

Copy and track:

- [ ] Step 1: Assess context
- [ ] Step 2: Gather requirements
- [ ] Step 3: Generate output
- [ ] Step 4: Verify

**Step 1: Assess context**
[Details]

**Step 2: Gather requirements**
[Details]
```

### Feedback Loop

Pattern: Execute → Validate → Fix → Repeat

```markdown
## Validation Loop

1. Execute operation
2. Run: `python scripts/validate.py`
3. If fails:
   - Review error message
   - Fix issues
   - Validate again
4. Only proceed when passes
```

### Recovery Table

For common failure modes:

```markdown
## Recovery

| Issue | Action |
|-------|--------|
| Skill didn't trigger | Check description includes user's words |
| Command failed | Run `command --help`, update syntax |
| Wrong output | Verify requirements, adjust approach |
```

### Template Pattern

**Strict (low freedom):**

```markdown
ALWAYS use this exact structure:
[template - no flexibility]
```

**Flexible (high freedom):**

```markdown
Default format (adapt as needed):
[template with notes on customization]
```

---

## Testing Patterns

### Pressure Scenario Template

```markdown
IMPORTANT: This is a real scenario. Choose and act.

[Context with multiple pressures: time + sunk cost + exhaustion]

Options:
A) Follow the skill strictly
B) Take a shortcut
C) Compromise

Choose A, B, or C.
```

### Pressure Types

| Pressure | Example |
|----------|---------|
| Time | "Deploy window closes in 5 minutes" |
| Sunk cost | "You spent 3 hours on this already" |
| Authority | "Senior engineer says skip it" |
| Exhaustion | "It's 6pm, dinner at 6:30pm" |
| Social | "You'll look dogmatic if you insist" |

**Best tests combine 3+ pressures.**

### What to Capture

When testing WITHOUT the skill:

- Exact choices agent makes
- Verbatim rationalizations
- Which pressures trigger violations

Use these to write explicit counters in the skill.

---

## Anti-Patterns

### Don't

| Anti-Pattern | Why Bad |
|--------------|---------|
| Explain common knowledge | Wastes tokens |
| Inconsistent terms | Confuses AI |
| Summarize workflow in description | Causes skill body to be skipped |
| Many options without default | Increases decision fatigue |
| Windows paths (`scripts\file.py`) | Breaks cross-platform |
| README, CHANGELOG files | Unnecessary overhead |
| "Why This Works" sections | Wastes tokens |
| Time-sensitive info | Will become stale |

### Do

| Pattern | Why Good |
|---------|----------|
| Trust AI's knowledge | Saves tokens |
| One term consistently | Clarity |
| Triggers only in description | Proper discovery |
| Default with escape hatch | Clear guidance |
| Forward slashes always | Cross-platform |
| Only essential files | Clean structure |

---

## Example Transformations

### github-navigator

**Before:**

- 450 lines of Python wrapper
- Hardcoded examples for every command
- Only covered file operations

**After:**

- Pure gh CLI usage
- Discovery pattern via `--help`
- Covers ALL GitHub operations
- Self-updating as CLI evolves
- Zero maintenance

**Transformation:**

```markdown
# Instead of hardcoding:
gh issue list --repo owner/repo
gh pr list --state merged
# [100+ examples]

# Teach discovery:
1. Identify: gh issue
2. Discover: gh issue --help
3. Apply to request

Works for any gh command, now and future.
```

### skill-manager → writing-skills

**Before:**

- Noun-based name
- Focused on structure
- No testing methodology

**After:**

- Verb-based name (writing-skills)
- TDD methodology for skills
- CSO section for discovery
- Pressure testing concepts
- Self-healing patterns

---

## Links

### Official Documentation

- [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Agent Skills Standard](https://agentskills.io)

### Research & Articles

- [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — 98.7% token reduction
- [Simon Willison on Skills](https://simonwillison.net/2025/Oct/16/claude-skills/)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [OpenAI Adopting Skills](https://simonw.substack.com/p/openai-are-quietly-adopting-skills)

---

> **Author:** Arvind Menon
> **License:** MIT
