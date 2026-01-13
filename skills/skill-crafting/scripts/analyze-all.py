#!/usr/bin/env python3
"""
Comprehensive Skill Analyzer - runs all checks on a skill.

The "ESLint for Agent Skills" - quality tooling that analyzes skills for
CSO compliance, structure, token efficiency, and cross-platform compatibility.
"""

import sys
import re
from pathlib import Path

# Import our simple frontmatter parser (no external dependencies)
try:
    from frontmatter import parse_frontmatter
except ImportError:
    # Inline simple parser if import fails
    def parse_frontmatter(content):
        if not content.startswith('---'):
            return {}, content
        try:
            end = content.index('---', 3)
            yaml_section = content[3:end].strip()
            body = content[end + 3:].strip()
        except ValueError:
            return {}, content

        result = {}
        for line in yaml_section.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip().strip('"\'')
                result[key] = value
        return result, body


# ============================================================================
# CONSTANTS
# ============================================================================

DEFAULT_CHAR_BUDGET = 15000

WORKFLOW_HINTS = [
    (r'\bruns?\b.*\bcommands?\b', 'Mentions running commands'),
    (r'\bexecutes?\b', 'Uses "execute"'),
    (r'\bdiscover\w*\s+\w*\s*dynamically', 'Mentions dynamic discovery'),
    (r'\bstep\s*\d', 'References steps'),
    (r'\bworkflow\b', 'Uses "workflow"'),
    (r'\bparses?\b', 'Uses "parse"'),
    (r'\bfirst\b.*\bthen\b', 'Sequential process description'),
]

STANDARD_FIELDS = {'name', 'description', 'license', 'compatibility', 'metadata'}
CLAUDE_CODE_FIELDS = {'allowed-tools', 'hooks', 'context'}


# ============================================================================
# PARSING
# ============================================================================

def _parse_fm(content: str) -> dict:
    """Extract frontmatter dict from content (wrapper for compatibility)."""
    fm, _ = parse_frontmatter(content)
    return fm


def load_skill(skill_path: Path) -> dict:
    """Load a skill from path."""
    if skill_path.is_file():
        skill_dir = skill_path.parent
        skill_file = skill_path
    else:
        skill_dir = skill_path
        skill_file = skill_path / 'SKILL.md'

    if not skill_file.exists():
        return {'error': f"SKILL.md not found in {skill_path}"}

    content = skill_file.read_text(encoding='utf-8')
    frontmatter = _parse_fm(content)

    if not frontmatter:
        return {'error': "Could not parse YAML frontmatter"}

    return {
        'path': str(skill_dir),
        'content': content,
        'frontmatter': frontmatter,
        'name': frontmatter.get('name', skill_dir.name),
        'description': frontmatter.get('description', ''),
        'lines': content.count('\n') + 1,
    }


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_structure(skill: dict) -> dict:
    """Analyze skill structure."""
    results = {'issues': [], 'warnings': [], 'good': []}
    fm = skill['frontmatter']

    # Required fields
    if 'name' in fm:
        name = fm['name']
        if name == name.lower() and re.match(r'^[a-z][a-z0-9\-]*$', name):
            results['good'].append("Name follows conventions")
        else:
            results['issues'].append("Name must be lowercase with hyphens only")
        if len(name) > 64:
            results['issues'].append(f"Name too long: {len(name)} chars (max 64)")
    else:
        results['issues'].append("Missing required field: name")

    if 'description' not in fm:
        results['issues'].append("Missing required field: description")

    # Line count
    if skill['lines'] > 500:
        results['warnings'].append(f"SKILL.md is {skill['lines']} lines (recommend <500)")
    else:
        results['good'].append(f"SKILL.md is {skill['lines']} lines")

    # Check for LICENSE
    skill_dir = Path(skill['path'])
    if not (skill_dir / 'LICENSE').exists():
        results['warnings'].append("No LICENSE file")

    return results


def analyze_cso(skill: dict) -> dict:
    """Analyze CSO compliance."""
    results = {'issues': [], 'warnings': [], 'good': []}
    desc = skill['description']

    if not desc:
        results['issues'].append("No description")
        return results

    desc_lower = desc.lower()

    # Check for workflow hints
    for pattern, msg in WORKFLOW_HINTS:
        if re.search(pattern, desc_lower):
            results['issues'].append(f"CSO: {msg} (workflow hint)")

    # Check for first person
    if re.search(r'\bI\s+(can|will|am)\b', desc, re.IGNORECASE):
        results['issues'].append("CSO: Uses first person")

    # Check for good patterns
    if re.search(r'\buse\s+when\b', desc_lower):
        results['good'].append("Includes 'Use when' triggers")
    else:
        results['warnings'].append("Consider adding 'Use when...' triggers")

    if re.search(r"'[^']+'\s*,?\s*'[^']+'", desc):
        results['good'].append("Includes example trigger phrases")
    else:
        results['warnings'].append("Consider adding example phrases in quotes")

    # Length
    if len(desc) > 500:
        results['warnings'].append(f"Description is {len(desc)} chars (recommend <500)")
    if len(desc) > 1024:
        results['issues'].append(f"Description exceeds 1024 char limit")

    return results


def analyze_compatibility(skill: dict) -> dict:
    """Analyze cross-platform compatibility."""
    results = {
        'is_cross_platform': True,
        'standard': [],
        'claude_code': [],
        'unknown': [],
    }

    for field in skill['frontmatter']:
        if field in STANDARD_FIELDS:
            results['standard'].append(field)
        elif field in CLAUDE_CODE_FIELDS:
            results['claude_code'].append(field)
            results['is_cross_platform'] = False
        else:
            results['unknown'].append(field)

    return results


def estimate_tokens(content: str) -> int:
    """Rough token estimate (words * 1.3)."""
    words = len(content.split())
    return int(words * 1.3)


# ============================================================================
# OUTPUT
# ============================================================================

def print_analysis(skill: dict, structure: dict, cso: dict, compat: dict):
    """Print full analysis results."""
    print(f"\n{'='*60}")
    print(f"  Skill Analysis: {skill['name']}")
    print(f"{'='*60}")
    print(f"  Path: {skill['path']}")
    print(f"{'='*60}\n")

    # Structure
    print("📁 STRUCTURE")
    for item in structure['good']:
        print(f"   ✅ {item}")
    for item in structure['warnings']:
        print(f"   ⚠️  {item}")
    for item in structure['issues']:
        print(f"   ❌ {item}")

    # CSO
    print("\n🔍 CSO (Claude Search Optimization)")
    for item in cso['good']:
        print(f"   ✅ {item}")
    for item in cso['warnings']:
        print(f"   ⚠️  {item}")
    for item in cso['issues']:
        print(f"   ❌ {item}")

    # Compatibility
    print("\n🌐 PLATFORM COMPATIBILITY")
    if compat['is_cross_platform']:
        print("   ✅ Fully cross-platform")
    else:
        print("   ⚠️  Uses Claude Code extensions")
        print(f"   🔵 Extensions: {', '.join(compat['claude_code'])}")

    # Metrics
    print("\n📊 METRICS")
    print(f"   Description: {len(skill['description'])} chars")
    print(f"   SKILL.md: {skill['lines']} lines")
    print(f"   Est. tokens: ~{estimate_tokens(skill['content'])}")

    # Summary
    total_issues = len(structure['issues']) + len(cso['issues'])
    total_warnings = len(structure['warnings']) + len(cso['warnings'])

    print(f"\n{'─'*60}")
    if total_issues == 0 and total_warnings == 0:
        print("✅ No issues found!")
    elif total_issues == 0:
        print(f"⚠️  {total_warnings} warning(s)")
    else:
        print(f"❌ {total_issues} issue(s), {total_warnings} warning(s)")

    return total_issues


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze-all.py <path/to/skill/>")
        print("\nRuns all quality checks on a skill:")
        print("  - Structure validation")
        print("  - CSO compliance")
        print("  - Platform compatibility")
        print("  - Token estimation")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    skill = load_skill(skill_path)

    if 'error' in skill:
        print(f"❌ Error: {skill['error']}")
        sys.exit(1)

    structure = analyze_structure(skill)
    cso = analyze_cso(skill)
    compat = analyze_compatibility(skill)

    issues = print_analysis(skill, structure, cso, compat)
    sys.exit(1 if issues > 0 else 0)


if __name__ == '__main__':
    main()
