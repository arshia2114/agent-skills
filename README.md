# Skills

Portable skills for AI coding assistants. Works with Claude Code, GitHub Copilot, OpenCode, Cursor, and any [Agent Skills](https://agentskills.io)-compatible tool.

## Installation

### Option 1: Clone to Claude Skills Directory

```bash
git clone https://github.com/arvindand/agent-skills.git ~/.claude/skills
```

This makes skills available to:

- Claude Code (native support)
- GitHub Copilot (auto-loads `.claude/skills`)
- OpenCode (Agent Skills standard)
- VS Code with Copilot

### Option 2: Clone Anywhere and Symlink

```bash
# Clone to your preferred location
git clone https://github.com/arvindand/agent-skills.git ~/projects/skills

# Symlink individual skills (Unix/macOS)
ln -s ~/projects/skills/context7 ~/.claude/skills/context7
ln -s ~/projects/skills/github-navigator ~/.claude/skills/github-navigator

# Windows (run as Administrator)
mklink /D %USERPROFILE%\.claude\skills\context7 %USERPROFILE%\projects\skills\context7
```

## Available Skills

| Skill | Description | Use For |
|-------|-------------|---------|
| [context7](context7/) | Library documentation lookup via Context7 REST API | Getting up-to-date docs for React, Next.js, Prisma, etc. |
| [github-navigator](github-navigator/) | GitHub operations via gh CLI with dynamic command discovery | All GitHub operations: files, issues, PRs, releases, actions |
| [maven-tools](maven-tools/) | JVM dependency intelligence via [Maven Tools MCP server](https://github.com/arvindand/maven-tools-mcp) | Version checks, upgrade planning, CVE scanning, license compliance |
| [ui-ux-design](ui-ux-design/) | Create production-grade interfaces with strong UX foundations | Building functional, accessible, visually distinctive UI/UX |
| [writing-skills](writing-skills/) | Create effective, discoverable skills for AI agents | Creating new skills, improving discovery, testing under pressure |

## Usage

Once installed, skills activate automatically when relevant to your prompt:

```txt
You: "How do I use React hooks?"
→ context7 skill loads and fetches React hooks documentation

You: "Show me open issues in facebook/react"
→ github-navigator skill loads and uses gh CLI to list issues

You: "Should I upgrade Spring Boot from 2.7 to 3.2?"
→ maven-tools skill loads and analyzes versions, CVEs, breaking changes

You: "Create a skill for processing PDFs"
→ writing-skills skill loads and guides you through skill creation
```

No manual invocation needed — the AI determines when each skill is relevant.

## Documentation

See [writing-skills/REFERENCES.md](writing-skills/REFERENCES.md) for best practices and patterns.

## Compatibility

Works with [Agent Skills](https://agentskills.io)-compatible tools: Claude Code, GitHub Copilot, OpenCode, Cursor, and others.

## Contributing

**Skills I'm looking to collect:**

- Frequent operations with zero context overhead
- CLI tools that can be discovered via `--help`
- Discovery patterns that teach AI dynamically
- Cross-platform workflows

> Note: Would appreciate contributions or references to implementations for other useful skills, especially geared toward helping senior devs focused on backend, architecture, and DevOps.

## Why Skills over MCP?

I'm biased towards skills over MCP. Here's why.

### Skills are cheaper and at least as effective as MCP tools when done well

MCP loads all tool schemas into every conversation whether you use them or not. Ten tools? That's roughly 1,000 tokens added to every single request.

Skills are free until you need them. When a skill triggers, you pay for ~100 words of metadata. That's it.

> Anthropic found that using code execution to call tools (what skills enable) cut token usage from >150,000 to 2,000. That's a 98.7% reduction. <https://www.anthropic.com/engineering/code-execution-with-mcp>

### If there's a CLI, use a skill

AI models already know how to read `--help` output. You don't need to write MCP schemas for things like `gh`, `npm`, or `curl`.

Instead, teach the pattern:

- "Run `gh issue --help` to see what's available"
- "Check `npm --help` for commands"

The skill stays current as the CLI evolves. No maintenance needed.

> See <https://simonw.substack.com/p/openai-are-quietly-adopting-skills>

### When the line is blurry, optimize for cost

Sometimes both approaches work. When in doubt, ask: will I use this frequently? If yes, a skill costs you nothing when idle. An MCP costs you tokens on every request.

### When MCP makes sense

Use MCP when:

- Works and well maintained and doesn't contain a gazillion tools
- You need bidirectional communication (push updates, subscriptions)
- Carries complex state and sophisticated caching
- No CLI exists and you can't easily wrap the API

Skills and MCP can work together. You can write a skill that teaches the AI how to use your MCP servers effectively.

### Summary

**Default to skills.** They're free when idle, stay current with CLI changes, and work everywhere. Use MCP when you need its specific capabilities or when there's an official integration worth using.

## License

MIT License — See individual skill LICENSE files for details.

**Author:** Arvind Menon

---
