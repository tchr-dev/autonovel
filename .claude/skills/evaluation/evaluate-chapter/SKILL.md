---
name: evaluate-chapter
description: Score a single drafted chapter against the planning docs and the universal slop guardrails. Returns voice/beat/character/prose/canon dimension scores 0-10 and a top-3 revision list. Used during drafting (keep if score > 6.0, retry otherwise) and to find weakest chapters during revision.
---

# Evaluate chapter

You are a literary critic and novel editor. JSON output only. No markdown fences.

## Inputs

Caller passes the chapter number N. From `<novel-dir>/`:
- `voice.md`, `world.md` (truncate to ~4000 words for context budget), `characters.md`, `canon.md`
- `outline.md` — extract Ch N's entry
- `chapters/ch_<N-1:02d>.md` — last ~3000 chars
- `chapters/ch_<N:02d>.md` — the chapter being evaluated

Also run the mechanical scanner first:
```
python scripts/slop_scan.py <novel-dir>/chapters/ch_<N:02d>.md --json
```
Capture its `slop_penalty` (0-10). This is subtracted from your raw judge score after you score.

## Scoring calibration

```
9-10: Among the best chapters in published fantasy. Name a specific
      published chapter it competes with, or don't give 9+.
7-8:  Strong, publishable with editorial polish. Specific flaws but
      don't break the read.
5-6:  Functional but flat. Generic where it should be specific.
3-4:  Significant problems. Voice breaks, beats missed, prose generic.
1-2:  Not usable. Rewrite from scratch.
```

The MEDIAN score for a competent AI-generated chapter is **6**. A 7 means it does something a generic AI draft wouldn't. An 8 means a human editor would keep it with minor notes. **Reserve 8+ for genuine excellence.**

For each dimension you must identify:
- (a) The single WEAKEST MOMENT — quote the specific sentence or passage
- (b) What would make it better — concrete revision, not vague

If every sentence is perfect, you're not reading carefully enough.

## Cross-checks (before scoring)

1. **QUOTE TEST:** Find 3 best and 3 weakest sentences. If you can't find 3 weak ones, lower your standards — every chapter has weak moments.
2. **DIALOGUE REALISM:** Read all dialogue mentally. Speech or written prose? Background-appropriate?
3. **SCENE VS SUMMARY:** How much in-scene vs summary? Heavy on summary lowers engagement regardless of prose.
4. **AI PATTERN CHECK:** Same-length paragraphs. Triadic observations. Emotions on schedule. Characters who never say the wrong thing. Description that catalogs instead of selecting. Internal monologue restating what the scene showed.
5. **EARNED VS GIVEN:** Tension earned through scene work or asserted by narrator? Mystery from genuine withholding or from the character conveniently not thinking about things?

## Dimensions

- `voice_adherence` — match `voice.md` Part 2: rhythm variation, vocabulary domains, body-before-emotion, the tone described. Quote strongest AND weakest voice moment. Generic-fantasy passages that could appear in any novel cap at 7.
- `beat_coverage` — every beat from the outline hit? Dramatised vs merely mentioned (half-credit for summarised beats).
- `character_voice` — remove dialogue tags mentally. Identifiable? Speech as speech? Anyone say something REAL (not just the right thing)?
- `plants_seeded` — placed naturally? Obvious plant scores lower than invisible.
- `prose_quality` — sentence variety (3+ consecutive same-start = penalty), specificity, metaphors from POV's experience, show-don't-tell at peaks. Quote weakest sentence + the rewrite.
- `continuity` — logical/emotional flow from previous chapter.
- `canon_compliance` — check ALL facts against `canon.md`. List violations. One major violation caps at 6.
- `lore_integration` — does the world DO work, or is it set dressing? Find-and-replaceable scene caps at 5.
- `engagement` — would the reader turn the page? Surprise present? Predictable excellence still predictable — 8+ requires something unexpected.

## Output

Write JSON to `<novel-dir>/eval_logs/<timestamp>_ch<NN>.json`:

```json
{
  "voice_adherence": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "beat_coverage": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "character_voice": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "plants_seeded": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "prose_quality": {"score": N, "weakest_sentence": "...", "fix": "...", "strongest_sentence": "...", "note": "..."},
  "continuity": {"score": N, "note": "..."},
  "canon_compliance": {"score": N, "violations": [], "note": "..."},
  "lore_integration": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "engagement": {"score": N, "weakest_moment": "...", "fix": "...", "note": "..."},
  "three_weakest_sentences": ["...", "...", "..."],
  "three_strongest_sentences": ["...", "...", "..."],
  "ai_patterns_detected": ["..."],
  "raw_judge_score": N,
  "slop": { /* paste the slop_scan JSON */ },
  "overall_score": N,
  "weakest_dimension": "...",
  "top_3_revisions": ["...", "...", "..."],
  "new_canon_entries": ["..."]
}
```

`overall_score` = `raw_judge_score - slop.slop_penalty`, clamped to [0, 10].

## Final check

If `raw_judge_score` is above 7, re-read your weakest_moment quotes. If any of them describe a problem an editor would flag, your score is too high. The median AI chapter is 6. An 8 is exceptional. A 9 is rare. A 10 does not exist for a first draft.

After writing JSON, print: `ch NN: overall=N.N (raw=N.N - slop=N.N) | weakest: X | top fix: …`.

Append the new canon entries to `<novel-dir>/canon.md` (under appropriate section headers).
