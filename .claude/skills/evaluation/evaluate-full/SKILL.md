---
name: evaluate-full
description: Holistic novel-level evaluation — arc completion, pacing curve, theme coherence, foreshadowing resolution, world/voice consistency, overall engagement. Returns the weakest chapter and the top single suggestion. Use after first draft and between revision cycles.
---

# Evaluate full novel

You are a literary critic. JSON only.

## Inputs (from `<novel-dir>/`)

- `voice.md`, `world.md` (truncate ~3000 words), `characters.md`, `outline.md` (full, including foreshadowing ledger)
- All `chapters/ch_*.md` files

## Build chapter summaries

For each chapter, compose:
```
Chapter N (W words):
  Opening: <first 500 chars>...
  Closing: ...<last 500 chars>
```

Concatenate into the prompt context. (For very long manuscripts, you may also include each chapter's most recent eval JSON if one exists in `eval_logs/`.)

## Score 0-10

- `arc_completion` — do character arcs resolve satisfyingly?
- `pacing_curve` — does tension build properly across the book? (This is usually the stubborn score; 7 is often a structural ceiling.)
- `theme_coherence` — themes explored consistently?
- `foreshadowing_resolution` — all planted threads harvested?
- `world_consistency` — any lore contradictions across chapters?
- `voice_consistency` — voice steady throughout? Use the `scripts/voice_fingerprint.py` outliers if available.
- `overall_engagement` — compelling read start to finish?

## Output JSON (to `<novel-dir>/eval_logs/<timestamp>_full.json`)

```json
{
  "arc_completion": {"score": N, "note": "..."},
  "pacing_curve": {"score": N, "note": "..."},
  "theme_coherence": {"score": N, "note": "..."},
  "foreshadowing_resolution": {"score": N, "note": "..."},
  "world_consistency": {"score": N, "note": "..."},
  "voice_consistency": {"score": N, "note": "..."},
  "overall_engagement": {"score": N, "note": "..."},
  "novel_score": N,
  "weakest_dimension": "...",
  "weakest_chapter": N,
  "top_suggestion": "..."
}
```

## After writing

Print the one-line summary. Note any chapter whose score has rotated as "weakest" — chasing a rotating weakest chapter is whack-a-mole; after 2 rotations, stop revising on that axis.
