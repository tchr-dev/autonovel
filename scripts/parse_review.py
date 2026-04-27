#!/usr/bin/env python3
"""Parse an Opus dual-persona review (literary critic + professor of fiction)
into a structured JSON of actionable items, plus a stop-or-continue verdict.

Usage:
  python parse_review.py path/to/review.md > parsed.json
"""
import json
import re
import sys
from pathlib import Path


def parse(text: str) -> dict:
    sections = re.split(r'(?:Professor|PROFESSOR|professor).*?(?:Review|Assessment|Analysis|Craft)',
                        text, maxsplit=1)
    critic_text = sections[0] if sections else text
    professor_text = sections[1] if len(sections) > 1 else ""

    star_match = re.search(r'★+½?|(\d+\.?\d*)\s*/?\s*(?:out of\s*)?(?:five|5)', critic_text)
    stars = None
    if star_match:
        s = star_match.group(0)
        stars = s.count('★') + (0.5 if '½' in s else 0)

    items = []
    for section in re.split(r'\n(?=\d+\.\s+[A-Z])', professor_text):
        if not section.strip():
            continue
        title_match = re.match(r'(\d+)\.\s+(.+?)(?:\n|$)', section)
        if not title_match:
            continue
        num = int(title_match.group(1))
        title = title_match.group(2).strip()
        low = section.lower()

        if any(w in low for w in ['major', 'significant', 'primary', 'most important']):
            severity = "major"
        elif any(w in low for w in ['minor', 'small', 'slight', 'cosmetic']):
            severity = "minor"
        else:
            severity = "moderate"

        if any(w in low for w in ['cut', 'compress', 'trim', 'reduce', 'consolidate']):
            fix_type = "compression"
        elif any(w in low for w in ['add', 'expand', 'introduce', 'give', 'more']):
            fix_type = "addition"
        elif any(w in low for w in ['repetit', 'recurring', 'frequency', 'tic', 'gesture']):
            fix_type = "mechanical"
        elif any(w in low for w in ['restructur', 'rearrang', 'move', 'reorganiz']):
            fix_type = "structural"
        else:
            fix_type = "revision"

        qualified = any(p in low for p in [
            'individually fine', 'largely successful', 'each instance works',
            'minor relative to', 'small complaint', 'costs of ambition',
            'not a flaw', 'deliberate choice', 'thematically coherent'
        ])

        suggestion = ""
        sugg_match = re.search(r'(?:Specific\s+)?[Ss]uggestion[s]?:?\s*\n?(.*?)(?=\n\d+\.|\n\n[A-Z]|\Z)',
                               section, re.DOTALL)
        if sugg_match:
            suggestion = sugg_match.group(1).strip()[:500]

        items.append({
            "number": num, "title": title, "severity": severity, "type": fix_type,
            "qualified": qualified, "suggestion": suggestion,
            "full_text": section.strip()[:1000],
        })

    total = len(items)
    major = sum(1 for i in items if i["severity"] == "major")
    qualified_count = sum(1 for i in items if i["qualified"])
    unqualified = total - qualified_count

    s = stars or 0
    if s >= 4.5 and major == 0:
        stop, reason = True, "★★★★½ with no major items"
    elif s >= 4 and total > 0 and qualified_count / total > 0.5:
        stop, reason = True, f"{qualified_count}/{total} items qualified"
    elif total <= 2:
        stop, reason = True, f"only {total} items found"
    else:
        stop, reason = False, f"{major} major, {unqualified} unqualified"

    return {
        "stars": stars,
        "critic_summary": critic_text.strip()[:500],
        "professor_items": items,
        "total_items": total,
        "major_items": major,
        "qualified_items": qualified_count,
        "stop": stop,
        "stop_reason": reason,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    text = Path(sys.argv[1]).read_text()
    print(json.dumps(parse(text), indent=2))


if __name__ == "__main__":
    main()
