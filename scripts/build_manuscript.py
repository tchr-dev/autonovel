#!/usr/bin/env python3
"""Concatenate all chapter files in a novel directory into a single manuscript.md.

Usage:
  python build_manuscript.py <novel-dir>           # writes <novel-dir>/manuscript.md
  python build_manuscript.py <novel-dir> -         # to stdout
"""
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    novel_dir = Path(sys.argv[1]).resolve()
    chapters = sorted((novel_dir / "chapters").glob("ch_*.md"))
    if not chapters:
        print(f"No chapters found in {novel_dir}/chapters", file=sys.stderr)
        sys.exit(1)
    parts = [c.read_text() for c in chapters]
    text = "\n\n---\n\n".join(parts)
    wc = len(text.split())
    if len(sys.argv) > 2 and sys.argv[2] == "-":
        sys.stdout.write(text)
    else:
        out = novel_dir / "manuscript.md"
        out.write_text(text)
        print(f"{out}: {len(chapters)} chapters, {wc:,} words", file=sys.stderr)


if __name__ == "__main__":
    main()
