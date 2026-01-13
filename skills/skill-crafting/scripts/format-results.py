#!/usr/bin/env python3
"""
PostToolUse hook: Add summary recommendations after skill analysis.
"""

import sys
import os


def format_results():
    """Add helpful summary after analysis commands."""
    output = os.environ.get('TOOL_OUTPUT', '')

    # Check if this was an analysis command
    if 'Skill Analysis' in output or 'CSO Analysis' in output:
        # Check for issues
        issue_count = output.count('❌')
        warning_count = output.count('⚠️')

        if issue_count > 0:
            print(f"\n[skill-crafting] Found {issue_count} issue(s) to fix.")
            print("[skill-crafting] See REFERENCES.md for best practices.")
        elif warning_count > 0:
            print(f"\n[skill-crafting] {warning_count} warning(s) - consider addressing.")

    sys.exit(0)


if __name__ == '__main__':
    format_results()
