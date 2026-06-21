"""Print UTF-8 text files with stable line numbers.

Use this instead of PowerShell Get-Content when a file may contain Chinese or
other non-ASCII text. Windows PowerShell 5.1 can decode UTF-8-without-BOM files
with the active ANSI code page, which produces mojibake and makes exact patch
contexts unreliable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="UTF-8 text file to print")
    parser.add_argument("--start", type=int, default=1, help="1-based first line")
    parser.add_argument("--count", type=int, default=120, help="number of lines")
    return parser.parse_args()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    path = Path(args.path)
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    start = max(args.start, 1)
    end = min(start + max(args.count, 0) - 1, len(lines))
    for line_no in range(start, end + 1):
        print(f"{line_no:5}: {lines[line_no - 1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
