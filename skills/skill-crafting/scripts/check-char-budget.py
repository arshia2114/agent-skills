#!/usr/bin/env python3
"""
Character Budget Checker for Agent Skills.

Claude Code has a 15,000 character limit for all skill descriptions combined.
This script checks if you're approaching or exceeding that limit.
"""

import sys
from pathlib import Path

from frontmatter import parse_frontmatter

# Claude Code's default character budget for skill descriptions
DEFAULT_CHAR_BUDGET = 15000


def parse_skill_description(skill_path: Path) -> dict:
    """Extract name and description from a SKILL.md file."""
    skill_md = skill_path / 'SKILL.md' if skill_path.is_dir() else skill_path

    if not skill_md.exists():
        return None

    try:
        content = skill_md.read_text(encoding='utf-8')
        data, _ = parse_frontmatter(content)

        if not data:
            return None

        return {
            'name': data.get('name', skill_path.name),
            'description': data.get('description', ''),
            'path': str(skill_path),
        }
    except (ValueError, OSError):
        return None


def scan_skills_directory(skills_dir: str) -> list:
    """Scan a directory for skills and extract descriptions."""
    path = Path(skills_dir)
    skills = []

    if not path.exists():
        return skills

    # Check if it's a single skill
    if (path / 'SKILL.md').exists():
        skill = parse_skill_description(path)
        if skill:
            skills.append(skill)
        return skills

    # Scan for skills in subdirectories
    for item in path.iterdir():
        if item.is_dir():
            skill = parse_skill_description(item)
            if skill:
                skills.append(skill)

    return skills


def analyze_budget(skills: list, budget: int = DEFAULT_CHAR_BUDGET) -> dict:
    """Analyze character budget usage."""
    total_chars = 0
    breakdown = []

    for skill in sorted(skills, key=lambda x: len(x['description']), reverse=True):
        desc_len = len(skill['description'])
        total_chars += desc_len
        breakdown.append({
            'name': skill['name'],
            'chars': desc_len,
            'path': skill['path'],
        })

    return {
        'total': total_chars,
        'budget': budget,
        'remaining': budget - total_chars,
        'percent_used': (total_chars / budget) * 100 if budget > 0 else 0,
        'over_budget': total_chars > budget,
        'breakdown': breakdown,
        'skill_count': len(skills),
    }


def print_analysis(analysis: dict):
    """Print budget analysis results."""
    print("\n=== Character Budget Analysis ===\n")

    # Summary
    status = "❌ OVER BUDGET" if analysis['over_budget'] else "✅ Within budget"
    print(f"Status: {status}")
    print(f"Skills found: {analysis['skill_count']}")
    print(f"Total characters: {analysis['total']:,} / {analysis['budget']:,}")
    print(f"Remaining: {analysis['remaining']:,} characters")
    print(f"Usage: {analysis['percent_used']:.1f}%")

    # Warning thresholds
    if analysis['percent_used'] > 80:
        print("\n⚠️  Warning: Above 80% usage - consider shortening descriptions")

    # Breakdown by skill
    print("\n--- Breakdown by Skill ---\n")
    for item in analysis['breakdown']:
        bar_len = min(50, int(item['chars'] / 20))
        bar = '█' * bar_len
        print(f"{item['name']:30} {item['chars']:5} chars  {bar}")

    # Recommendations
    if analysis['over_budget']:
        print("\n🔧 Recommendations:")
        print("   1. Shorten descriptions - focus on triggers, not workflow")
        print("   2. Remove less-used skills")
        print("   3. Set SLASH_COMMAND_TOOL_CHAR_BUDGET=30000 for more headroom")
        top_skill = analysis['breakdown'][0]
        print(f"   4. Biggest skill: {top_skill['name']} ({top_skill['chars']} chars)")

    return 0 if not analysis['over_budget'] else 1


def main():
    if len(sys.argv) < 2:
        print("Usage: check-char-budget.py <path/to/skills/>")
        print("\nChecks if skill descriptions exceed Claude Code's 15K character limit.")
        print("\nExamples:")
        print("  check-char-budget.py ~/.claude/skills/")
        print("  check-char-budget.py ./")
        sys.exit(1)

    skills_dir = sys.argv[1]
    budget = DEFAULT_CHAR_BUDGET

    # Optional: custom budget from env or arg
    if len(sys.argv) > 2:
        try:
            budget = int(sys.argv[2])
        except ValueError:
            pass

    skills = scan_skills_directory(skills_dir)

    if not skills:
        print(f"No skills found in: {skills_dir}")
        sys.exit(1)

    analysis = analyze_budget(skills, budget)
    exit_code = print_analysis(analysis)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
