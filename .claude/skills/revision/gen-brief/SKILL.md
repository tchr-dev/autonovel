---
name: gen-brief
description: Auto-generate a chapter revision brief from structured feedback (eval JSON + reader panel JSON + adversarial cuts JSON + Opus review items). Output is a markdown brief suitable as input to gen-revision. Picks the right brief shape (compression / expansion / dramatisation / character-deepening / consistency).
---

# Generate revision brief

A revision brief is a focused instruction to the writer, NOT a full re-spec of the chapter. It says: keep what works, change THIS specifically, here's what to add or cut, here are the constraints.

The brief replaces hand-written editorial notes. Quality of the brief drives quality of the revision.

## Inputs

Caller passes either:
- `--auto` — pick the chapter automatically based on lowest score / strongest consensus signal
- `--chapter N` — a specific chapter

For each chapter under consideration, gather (where present):
- `<novel-dir>/chapters/ch_<N:02d>.md`
- Latest `<novel-dir>/eval_logs/*_chNN.json` for that chapter
- Latest `<novel-dir>/eval_logs/*_full.json` and any `top_suggestion`/`weakest_chapter` references
- `<novel-dir>/edit_logs/reader_panel.json` — extract any consensus items mentioning this chapter
- `<novel-dir>/edit_logs/chNN_cuts.json` — adversarial cut data
- Latest `<novel-dir>/reviews/*_parsed.json` — Opus items mentioning this chapter

## Auto-pick logic

If `--auto`:
1. From `reader_panel.json` consensus items: any `cut_candidate`, `missing_scene`, or `worst_scene` with 3-of-4 or 4-of-4 agreement → pick that chapter, brief shape inferred from the question.
2. If no consensus, pick the chapter with lowest `overall_score` in latest eval logs.
3. If scores are tied within 0.5 across the bottom three, pick the one with most adversarial cuts ≥17% fat.

## Brief shapes

Pick the shape that fits the dominant signal:

### A. COMPRESSION (cut_candidate consensus, or chapter > target word count by >20%)
Target: 40-60% word reduction. Identify the 2-3 essential beats (what the reader panel said worked or what the outline marks as load-bearing). Cut everything else, but DO NOT compress below 1800 words — sweet spot is 2200-3000 for a compressed chapter.

### B. EXPANSION (missing_scene consensus, or chapter is too short for its structural importance)
Target: +800-1500 words. Specify WHAT BEATS to expand (the missing scene from panel feedback, or the under-developed beat from eval). Specify WHAT TO KEEP unchanged. Don't write "make it longer" — write "add a private moment between X and Y after the existing scene at the bell tower."

### C. DRAMATISATION (weak scene, low engagement, summary-heavy)
Change HOW information arrives, not WHAT information. "Reading a document" → investigation/confrontation. "Briefing" → confrontation with resistance. The plot beats stay; the medium changes.

### D. CHARACTER DEEPENING (thin_character consensus)
Identify 1-2 existing scenes where the character appears. Add a private/unguarded moment the POV catches. Connect to backstory in `characters.md`. **Do NOT add a new scene** — deepen an existing one.

### E. CONSISTENCY / TIMELINE FIX (canon_compliance violations, contradictions_found)
Specify the contradiction. Specify which value is canonical. Specify all places that need to update (canon.md + outline.md + the affected chapters).

### F. VOICE / SLOP CLEANUP (high `slop_penalty`, voice fingerprint outlier)
Bullet-list specific patterns to fix: "remove all 7 instances of 'a sense of'", "reduce em-dash density from 23/1k to ≤15/1k", "vary sentence-start: only 18 of 47 sentences should start with 'He' — currently 31."

## Brief format (write to `<novel-dir>/briefs/ch<NN>_<shape>.md`)

```markdown
# Revision brief — Ch <NN> (<TITLE>) — shape: <SHAPE>

## Why this revision

<2-3 sentences. Cite the specific evidence: panel consensus item / eval weakest_dimension / Opus review item / adversarial cuts %. Quote the source brief.>

## What to keep

<3-5 specific elements that work. Quote 1-2 sentences that the editor or panel praised, if available. The writer needs these as anchors.>

## What to change

<The specific change, broken into 3-6 numbered items. Each item is a concrete instruction, not a wish.>

## Constraints

- Word count target: <NNNN> (range, with reason)
- Voice: stay within voice.md Part 2; in particular, watch for <pattern>
- Continuity: ending must flow into Ch <N+1>'s opening (currently: "<paste 1-2 sentences>")
- Canon: do not contradict <list of relevant canon entries>

## Anti-patterns to avoid (from prior versions)

<2-4 specific tics flagged by adversarial-edit or evaluate-chapter on the previous draft. Quote them.>
```

## Output

Write the brief, then print:
- The chosen chapter and brief shape
- A one-line summary of the change
- The expected word count delta

Suggest: `gen-revision <NN> briefs/ch<NN>_<shape>.md`.
