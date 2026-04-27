---
name: apply-cuts
description: Apply adversarial-edit cuts to chapter files (mechanical quote-matching removal). Wraps scripts/apply_cuts.py. Filters by cut type (OVER-EXPLAIN, REDUNDANT typically yield ~55-60% of cuts). Use after adversarial-edit during revision cycles.
---

# Apply cuts

Mechanical pass — no LLM call. Reads `<novel-dir>/edit_logs/chNN_cuts.json` produced by `adversarial-edit` and removes matching quotes from chapters.

## Common invocations

```bash
# Dry run on all chapters with cuts files
AUTONOVEL_NOVEL_DIR=<novel-dir> python scripts/apply_cuts.py all --dry-run

# Apply only OVER-EXPLAIN and REDUNDANT cuts (the safest/most common types)
AUTONOVEL_NOVEL_DIR=<novel-dir> python scripts/apply_cuts.py all --types OVER-EXPLAIN REDUNDANT

# Apply all cuts to chapters where adversarial-edit found ≥17% fat
AUTONOVEL_NOVEL_DIR=<novel-dir> python scripts/apply_cuts.py all --min-fat 17

# Single chapter
AUTONOVEL_NOVEL_DIR=<novel-dir> python scripts/apply_cuts.py 12
```

## Failure modes

- `not found` — the quote doesn't appear in the chapter (often because a previous cut already shifted whitespace; the script tries whitespace-normalised match before giving up)
- `ambiguous (N matches)` — the quote appears more than once; the script refuses to guess which instance was meant
- Skipped if quote < 25 chars

The script collapses runs of 3+ newlines down to 2 after applying cuts.

## After running

Report:
- Total words removed across chapters
- Per-chapter applied / failed / skipped breakdown
- Which chapters had the highest cut counts (revision priorities)

Suggest:
- Re-evaluate any heavily-cut chapter with `evaluate-chapter` to confirm the score moved in the right direction
- If `failed` count is high, manually inspect the cuts file — some quotes may need rephrasing in the cuts JSON before retrying
