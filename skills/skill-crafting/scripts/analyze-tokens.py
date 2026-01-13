#!/usr/bin/env python3
"""
Token Analyzer for Agent Skills.

Estimates token usage and context cost of loading a skill.
"""

import sys
from pathlib import Path

from frontmatter import parse_simple_yaml


def estimate_tokens(text: str) -> int:
    """
    Rough token estimate.
    Average: ~1.3 tokens per word for English text.
    Code tends to be higher (~1.5-2 tokens per word).
    """
    words = len(text.split())
    return int(words * 1.3)


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def parse_frontmatter(content: str) -> tuple:
    """Parse frontmatter and return (frontmatter_dict, body)."""
    if not content.startswith('---'):
        return {}, content

    try:
        end = content.index('---', 3)
        yaml_content = content[3:end].strip()
        body = content[end + 3:].strip()
        return parse_simple_yaml(yaml_content), body
    except ValueError:
        return {}, content


def analyze_skill_tokens(skill_path: Path) -> dict:
    """Analyze token usage of a skill."""
    if skill_path.is_file():
        skill_dir = skill_path.parent
        skill_file = skill_path
    else:
        skill_dir = skill_path
        skill_file = skill_path / 'SKILL.md'

    if not skill_file.exists():
        return {'error': f"SKILL.md not found"}

    content = skill_file.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(content)

    result = {
        'name': frontmatter.get('name', skill_dir.name),
        'description': {
            'chars': len(frontmatter.get('description', '')),
            'words': count_words(frontmatter.get('description', '')),
            'tokens': estimate_tokens(frontmatter.get('description', '')),
        },
        'body': {
            'chars': len(body),
            'words': count_words(body),
            'tokens': estimate_tokens(body),
            'lines': body.count('\n') + 1,
        },
        'total': {
            'chars': len(content),
            'words': count_words(content),
            'tokens': estimate_tokens(content),
        },
        'references': [],
    }

    # Check for reference files
    refs_dir = skill_dir / 'references'
    if refs_dir.exists():
        for ref_file in refs_dir.glob('*.md'):
            ref_content = ref_file.read_text(encoding='utf-8')
            result['references'].append({
                'name': ref_file.name,
                'words': count_words(ref_content),
                'tokens': estimate_tokens(ref_content),
            })

    # Also check REFERENCES.md in root
    refs_file = skill_dir / 'REFERENCES.md'
    if refs_file.exists():
        ref_content = refs_file.read_text()
        result['references'].append({
            'name': 'REFERENCES.md',
            'words': count_words(ref_content),
            'tokens': estimate_tokens(ref_content),
        })

    return result


def print_analysis(result: dict):
    """Print token analysis."""
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return 1

    print(f"\n=== Token Analysis: {result['name']} ===\n")

    # Description (always loaded)
    desc = result['description']
    print("📝 Description (always in context):")
    print(f"   {desc['chars']:,} chars | {desc['words']} words | ~{desc['tokens']} tokens")

    # Body (loaded when skill triggers)
    body = result['body']
    print(f"\n📄 SKILL.md body (loaded when triggered):")
    print(f"   {body['lines']} lines | {body['words']:,} words | ~{body['tokens']:,} tokens")

    # References (loaded on demand)
    if result['references']:
        print(f"\n📚 Reference files (loaded on demand):")
        for ref in result['references']:
            print(f"   {ref['name']}: {ref['words']:,} words | ~{ref['tokens']:,} tokens")

    # Total
    total = result['total']
    print(f"\n📊 Total SKILL.md:")
    print(f"   {total['chars']:,} chars | {total['words']:,} words | ~{total['tokens']:,} tokens")

    # Recommendations
    print("\n💡 Context Window Impact:")

    if desc['tokens'] > 100:
        print(f"   ⚠️  Description is ~{desc['tokens']} tokens (recommend <100)")
    else:
        print(f"   ✅ Description is efficient (~{desc['tokens']} tokens)")

    if body['tokens'] > 2000:
        print(f"   ⚠️  Body is ~{body['tokens']} tokens (consider splitting to references)")
    elif body['tokens'] > 4000:
        print(f"   ❌ Body is ~{body['tokens']} tokens (too large, will impact context)")
    else:
        print(f"   ✅ Body size is reasonable (~{body['tokens']} tokens)")

    # Target guidance
    print("\n📏 Target Guidelines:")
    print("   Frequently-loaded skills: <200 words body")
    print("   Standard skills: <500 words body")
    print("   Reference files: Unlimited (loaded on demand)")

    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze-tokens.py <path/to/skill/>")
        print("\nEstimates token usage and context window impact.")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    result = analyze_skill_tokens(skill_path)
    exit_code = print_analysis(result)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
