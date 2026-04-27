#!/usr/bin/env python3
"""Append an entry to a novel's results.tsv.

Usage:
  python results_log.py <novel-dir> <phase> <action> <score> <word_count> <note>
"""
import sys
from datetime import datetime
from pathlib import Path


def main():
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)
    novel_dir = Path(sys.argv[1])
    phase, action, score, words, note = sys.argv[2:7]
    p = novel_dir / "results.tsv"
    new_file = not p.exists()
    with p.open("a") as f:
        if new_file:
            f.write("timestamp\tphase\taction\tscore\tword_count\tnote\n")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts}\t{phase}\t{action}\t{score}\t{words}\t{note}\n")


if __name__ == "__main__":
    main()
