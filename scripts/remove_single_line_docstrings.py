#!/usr/bin/env python3
"""
Pre-commit script to remove single-line docstrings and fail if any are found.

This script enforces the project rule that code should be self-documenting
and removes unnecessary single-line docstrings that just restate the function name.

Usage:
    python scripts/remove_single_line_docstrings.py [file1.py] [file2.py] ...

Exit codes:
    0: No single-line docstrings found
    1: Single-line docstrings found and removed (fails pre-commit)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple


def remove_single_line_docstrings(content: str) -> Tuple[str, int]:
    lines = content.split('\n')
    modified_lines = []
    removals_count = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this line contains a single-line docstring
        # Pattern: any indentation + """text""" (possibly with trailing whitespace)
        single_line_docstring_pattern = r'^(\s*)""".*?"""\s*$'

        if re.match(single_line_docstring_pattern, line):
            # Check if the previous line looks like a function/method/class definition
            if i > 0:
                prev_line = lines[i - 1].strip()
                if (
                    prev_line.startswith('def ')
                    or prev_line.startswith('async def ')
                    or (prev_line.endswith(':') and ('def ' in prev_line))
                    or prev_line.startswith('class ')
                    or (prev_line.endswith(':') and ('class ' in prev_line))
                ):
                    # This is a single-line docstring after a function/class definition
                    # Skip this line (remove it)
                    removals_count += 1
                    i += 1
                    continue

        modified_lines.append(line)
        i += 1

    return '\n'.join(modified_lines), removals_count


def process_file(file_path: Path) -> int:
    try:
        content = file_path.read_text(encoding='utf-8')
        modified_content, removals = remove_single_line_docstrings(content)

        if removals > 0:
            # Write the modified content back
            file_path.write_text(modified_content, encoding='utf-8')
            print(f'{file_path}: Removed {removals} single-line docstring(s)')
            return removals
        else:
            return 0

    except Exception as e:
        print(f'❌ Error processing {file_path}: {e}')
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='Remove single-line docstrings from Python files')
    parser.add_argument('files', nargs='*', help='Python files to process')
    args = parser.parse_args()

    if not args.files:
        print('No files specified')
        return 0

    total_removals = 0
    processed_files = 0

    for file_arg in args.files:
        file_path = Path(file_arg)

        if not file_path.exists():
            print(f'❌ File not found: {file_path}')
            continue

        if not file_path.suffix == '.py':
            continue

        removals = process_file(file_path)
        total_removals += removals
        processed_files += 1

    if total_removals > 0:
        print(f'❌ FAIL: {total_removals} single-line docstrings removed from {processed_files} files')
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
