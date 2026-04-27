---
name: voice-fingerprint
description: Run the mechanical voice-fingerprint scanner across all chapters to identify outliers in sentence rhythm, vocabulary domain balance, dialogue ratio, abstract noun density, and similar metrics. No LLM call — just runs the Python script. Use during revision to find chapters that drift from the novel's voice.
---

# Voice fingerprint

This skill runs `scripts/voice_fingerprint.py` and presents the result.

## Procedure

1. Set the env var so the script targets the right novel:
   ```bash
   AUTONOVEL_NOVEL_DIR=<novel-dir> python scripts/voice_fingerprint.py
   ```
2. Output is written to `<novel-dir>/edit_logs/voice_fingerprint.json` and a summary table is printed.

## Important caveat

The vocabulary wells in `scripts/voice_fingerprint.py` (`WELL_MUSICAL`, `WELL_TRADE`, `WELL_BODY`) are defaults from "The Second Son of the House of Bells." For a different novel, these need to be replaced with vocabulary domains relevant to the new world.

If the vocab wells haven't been customised for this novel, edit the script first. Otherwise the well percentages are noise. The other metrics (sentence length CV, paragraph length, dialogue ratio, em-dash density, "the way" count, simile density, "He"-start %) are universal and worth running unchanged.

## Reading the output

- `sentence_length_cv` ≥ 0.4 is healthy. Below 0.3 is uniform-prose territory.
- `he_start_pct` > 25% suggests sentence-start monotony.
- `the_way_count` > 5 in a single chapter is leaning on a simile crutch.
- Outliers (>1.5σ from mean) are the chapters where voice has drifted. Investigate them first.

After running, summarise outliers and recommend chapters to inspect with `evaluate-chapter` or hand to `gen-brief` for a voice-deviation revision.
