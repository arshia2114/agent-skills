#!/usr/bin/env python3
"""
Simple YAML frontmatter parser for Agent Skills.

No external dependencies - uses only Python standard library.
Handles the simple key: value format used in SKILL.md frontmatter.
"""

import re
from typing import Dict, Any, Optional


def parse_frontmatter(content: str) -> tuple:
    """
    Parse YAML frontmatter from SKILL.md content.

    Returns tuple of (frontmatter_dict, body_content).
    Works with simple key: value pairs and basic nested structures.

    No external dependencies required.
    """
    if not content.startswith('---'):
        return {}, content

    try:
        # Find closing ---
        end_idx = content.index('---', 3)
        yaml_section = content[3:end_idx].strip()
        body = content[end_idx + 3:].strip()
    except ValueError:
        return {}, content

    return parse_simple_yaml(yaml_section), body


def parse_simple_yaml(yaml_text: str) -> Dict[str, Any]:
    """
    Parse simple YAML format used in SKILL.md frontmatter.

    Handles:
    - key: value
    - key: "quoted value"
    - key: 'quoted value'
    - key: |
        multiline value
    - nested structures (limited)

    Does NOT handle:
    - Complex YAML features (anchors, references, etc.)
    - Lists with - syntax (limited support)
    """
    result = {}
    lines = yaml_text.split('\n')
    i = 0

    current_key = None
    multiline_value = []
    multiline_indent = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            if current_key and multiline_value:
                multiline_value.append('')
            i += 1
            continue

        # Check for multiline continuation
        if current_key and multiline_value:
            indent = len(line) - len(line.lstrip())
            if indent >= multiline_indent:
                multiline_value.append(line[multiline_indent:])
                i += 1
                continue
            else:
                # End of multiline
                result[current_key] = '\n'.join(multiline_value).strip()
                current_key = None
                multiline_value = []

        # Parse key: value
        match = re.match(r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:\s*(.*)$', stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            # Check for multiline indicator
            if value in ('|', '>'):
                current_key = key
                multiline_value = []
                multiline_indent = len(line) - len(line.lstrip()) + 2
                i += 1
                continue

            # Parse quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # Handle nested dict (simple case: key with no value followed by indented keys)
            if not value:
                nested = {}
                i += 1
                while i < len(lines):
                    nested_line = lines[i]
                    if not nested_line.strip():
                        i += 1
                        continue
                    # Check if still indented
                    if nested_line.startswith('  ') or nested_line.startswith('\t'):
                        nested_match = re.match(r'^\s+([a-zA-Z][a-zA-Z0-9_-]*)\s*:\s*(.*)$', nested_line)
                        if nested_match:
                            nested_key = nested_match.group(1)
                            nested_val = nested_match.group(2).strip()
                            # Handle list items
                            if nested_val.startswith('-'):
                                # Parse list
                                list_items = []
                                while i < len(lines) and lines[i].strip().startswith('-'):
                                    item_match = re.match(r'^\s*-\s*(.+)$', lines[i].strip())
                                    if item_match:
                                        list_items.append(parse_list_item(item_match.group(1)))
                                    i += 1
                                nested[nested_key] = list_items
                                continue
                            else:
                                if nested_val.startswith('"') and nested_val.endswith('"'):
                                    nested_val = nested_val[1:-1]
                                elif nested_val.startswith("'") and nested_val.endswith("'"):
                                    nested_val = nested_val[1:-1]
                                nested[nested_key] = nested_val
                        i += 1
                    else:
                        break
                result[key] = nested
                continue

            result[key] = value
        i += 1

    # Handle any remaining multiline content
    if current_key and multiline_value:
        result[current_key] = '\n'.join(multiline_value).strip()

    return result


def parse_list_item(item_text: str) -> Dict[str, Any]:
    """Parse a list item (simplified)."""
    item_text = item_text.strip()

    # Check for dict-like structure
    if ':' in item_text:
        result = {}
        parts = item_text.split()
        for part in parts:
            if ':' in part:
                key, _, val = part.partition(':')
                if val:
                    result[key.strip()] = val.strip()
        return result if result else item_text

    return item_text


def get_frontmatter_field(content: str, field: str) -> Optional[str]:
    """Get a specific field from frontmatter."""
    frontmatter, _ = parse_frontmatter(content)
    return frontmatter.get(field)


if __name__ == '__main__':
    # Test
    test_content = '''---
name: test-skill
description: "This is a test skill. Use when testing."
license: MIT
allowed-tools: Bash(gh:*) Read
hooks:
  UserPromptSubmit:
    - command: "python3 test.py"
      timeout: 500
---

# Test Skill

Body content here.
'''

    fm, body = parse_frontmatter(test_content)
    print("Frontmatter:")
    for k, v in fm.items():
        print(f"  {k}: {v}")
    print(f"\nBody preview: {body[:50]}...")
