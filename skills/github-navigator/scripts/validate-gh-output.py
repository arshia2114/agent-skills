#!/usr/bin/env python3
"""
PostToolUse hook: Validate gh CLI output and suggest fixes for common errors.
"""

import sys
import os
import re


# Common error patterns and suggestions
ERROR_PATTERNS = [
    (r'HTTP 401', 'Authentication required. Run: gh auth login'),
    (r'HTTP 404', 'Resource not found. Check the repo/path exists and you have access.'),
    (r'HTTP 403', 'Permission denied. You may need additional scopes: gh auth refresh -s repo'),
    (r'rate limit', 'Rate limited. Authenticate for higher limits: gh auth login'),
    (r'Could not resolve', 'Repository not found. Verify owner/repo format.'),
    (r'unknown flag', 'Invalid flag. Run: gh <command> --help'),
    (r'command not found: gh', 'gh CLI not installed. Install: brew install gh'),
]


def check_output():
    """Check tool output for errors and provide suggestions."""
    # Get output from environment (PostToolUse provides this)
    output = os.environ.get('TOOL_OUTPUT', '')
    exit_code = os.environ.get('TOOL_EXIT_CODE', '0')

    if exit_code == '0' and not any(err in output.lower() for err, _ in ERROR_PATTERNS):
        # Success - no action needed
        sys.exit(0)

    # Check for known error patterns
    output_lower = output.lower()
    for pattern, suggestion in ERROR_PATTERNS:
        if re.search(pattern, output_lower, re.IGNORECASE):
            print(f"[github-navigator] Error detected: {suggestion}")
            break

    # Always exit 0 to not block (we're just providing suggestions)
    sys.exit(0)


if __name__ == '__main__':
    check_output()
