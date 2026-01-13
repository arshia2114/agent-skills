#!/usr/bin/env python3
"""
Trigger Word Analyzer for Agent Skills.

Analyzes skill descriptions for trigger word coverage and suggests missing terms.
"""

import sys
import re
from pathlib import Path

from frontmatter import parse_frontmatter


# Common trigger word categories
TRIGGER_CATEGORIES = {
    'actions': [
        'show', 'list', 'get', 'fetch', 'create', 'make', 'build',
        'update', 'edit', 'delete', 'remove', 'add', 'check', 'view',
        'find', 'search', 'analyze', 'run', 'execute', 'start', 'stop',
    ],
    'questions': [
        'what is', 'how do', 'how to', 'where is', 'why', 'when',
        'can you', 'could you', 'please', 'help me', 'i need',
    ],
    'domains': {
        'github': ['github', 'repo', 'repository', 'issue', 'pr', 'pull request',
                   'commit', 'branch', 'fork', 'clone', 'star', 'release'],
        'documentation': ['docs', 'documentation', 'api', 'reference', 'guide',
                          'tutorial', 'how to use', 'example'],
        'testing': ['test', 'tests', 'testing', 'spec', 'coverage', 'tdd',
                    'unit test', 'integration'],
        'devops': ['deploy', 'deployment', 'ci', 'cd', 'pipeline', 'docker',
                   'kubernetes', 'k8s', 'terraform', 'aws', 'cloud'],
        'database': ['database', 'db', 'sql', 'query', 'schema', 'migration',
                     'table', 'index'],
        'ui': ['ui', 'ux', 'design', 'component', 'page', 'form', 'button',
               'layout', 'style', 'css'],
    },
}


def parse_description(skill_path: Path) -> dict:
    """Extract description from SKILL.md."""
    skill_file = skill_path / 'SKILL.md' if skill_path.is_dir() else skill_path

    if not skill_file.exists():
        return {'error': f"File not found: {skill_file}"}

    try:
        content = skill_file.read_text(encoding='utf-8')
        data, _ = parse_frontmatter(content)

        if not data:
            return {'error': "Missing or invalid frontmatter"}

        return {
            'name': data.get('name', ''),
            'description': data.get('description', ''),
        }
    except (ValueError, OSError) as e:
        return {'error': str(e)}


def find_triggers_in_text(text: str, triggers: list) -> list:
    """Find which triggers appear in text."""
    text_lower = text.lower()
    found = []
    for trigger in triggers:
        if trigger.lower() in text_lower:
            found.append(trigger)
    return found


def analyze_triggers(description: str) -> dict:
    """Analyze trigger word coverage in description."""
    result = {
        'found': {},
        'missing': {},
        'coverage': {},
        'suggestions': [],
    }

    desc_lower = description.lower()

    # Check action words
    found_actions = find_triggers_in_text(description, TRIGGER_CATEGORIES['actions'])
    missing_actions = [a for a in TRIGGER_CATEGORIES['actions'] if a not in desc_lower]
    result['found']['actions'] = found_actions
    result['missing']['actions'] = missing_actions[:5]  # Top 5 missing
    result['coverage']['actions'] = len(found_actions) / len(TRIGGER_CATEGORIES['actions'])

    # Check question patterns
    found_questions = find_triggers_in_text(description, TRIGGER_CATEGORIES['questions'])
    result['found']['questions'] = found_questions
    result['coverage']['questions'] = len(found_questions) / len(TRIGGER_CATEGORIES['questions'])

    # Detect domain and check domain-specific triggers
    for domain, triggers in TRIGGER_CATEGORIES['domains'].items():
        found = find_triggers_in_text(description, triggers)
        if found:
            result['found'][domain] = found
            missing = [t for t in triggers if t.lower() not in desc_lower]
            result['missing'][domain] = missing[:5]
            result['coverage'][domain] = len(found) / len(triggers)

    # Generate suggestions
    if result['coverage'].get('actions', 0) < 0.1:
        result['suggestions'].append("Add action verbs: 'show', 'list', 'create', 'analyze'")

    if not result['found'].get('questions'):
        result['suggestions'].append("Consider question phrases: 'how do I', 'what is'")

    # Check for quoted examples
    if not re.search(r"'[^']+'\s*,?\s*'[^']+'", description):
        result['suggestions'].append("Add quoted example phrases users might say")

    return result


def print_analysis(skill_name: str, result: dict):
    """Print trigger analysis."""
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return 1

    print(f"\n=== Trigger Analysis: {skill_name} ===\n")

    # Found triggers
    print("✅ Found Triggers:")
    for category, triggers in result['found'].items():
        if triggers:
            print(f"   {category}: {', '.join(triggers[:8])}")
            if len(triggers) > 8:
                print(f"            ...and {len(triggers) - 8} more")

    # Missing triggers
    print("\n⚠️  Consider Adding:")
    for category, triggers in result['missing'].items():
        if triggers:
            print(f"   {category}: {', '.join(triggers)}")

    # Coverage
    print("\n📊 Coverage:")
    for category, coverage in result['coverage'].items():
        bar_len = int(coverage * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"   {category:15} [{bar}] {coverage*100:.0f}%")

    # Suggestions
    if result['suggestions']:
        print("\n💡 Suggestions:")
        for suggestion in result['suggestions']:
            print(f"   - {suggestion}")

    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze-triggers.py <path/to/skill/>")
        print("\nAnalyzes trigger word coverage in skill descriptions.")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    data = parse_description(skill_path)

    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        sys.exit(1)

    result = analyze_triggers(data['description'])
    exit_code = print_analysis(data['name'], result)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
