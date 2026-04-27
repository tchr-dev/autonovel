---
name: evaluate-foundation
description: Score a novel's planning documents (world.md, characters.md, outline.md, voice.md, canon.md) as an integrated foundation. Returns dimension scores 0-10, identifies the weakest dimension and top three improvements. Used to gate exit from the foundation phase (foundation_score > 7.5 AND lore_score > 7.0).
---

# Evaluate foundation

You are a literary critic and novel editor. You evaluate fiction with precision. You produce a JSON report. No markdown fences, no preamble — just the JSON object.

## Inputs (from `<novel-dir>/`)

- `voice.md`, `world.md`, `characters.md`, `outline.md`, `canon.md`

## Scoring calibration

```
9-10: Could not improve with a month of focused editorial work. Published-novel
      quality. You can name the specific published novel it competes with.
      Reserve 10 for work that SURPRISES you.
7-8:  Strong. A skilled author could draft from this with minimal invention.
      Gaps exist but are minor and enumerable.
5-6:  Functional but thin. A writer would need to invent significant material.
3-4:  Sketchy. More questions than answers.
1-2:  Placeholder or stub.
0:    Empty or missing.
```

A score of 8+ requires ZERO major gaps. A score of 9+ requires that you genuinely struggled to find flaws. **Err toward lower scores.**

For EVERY dimension, before scoring, identify:
- (a) The single biggest GAP or WEAKNESS
- (b) A specific, actionable improvement that would raise the score

If you cannot find a gap, explain why you believe one doesn't exist.

## Cross-checks (perform before scoring)

1. **Dialogue ANTI-SLOP check.** Look for structural formulas repeated across characters ("not X, but Y" / "either X, or Y" / "there's a difference"). Deduct from `character_distinctiveness` if multiple characters share sentence structures.
2. **Negative space.** What's missing? Are there gaps in the magic system that would block a specific plot scene? Does the climax have a rule that resolves it? Are there characters the plot needs who don't exist?
3. **Convenient gaps vs. deliberate mystery.** Convenient: "the details are unclear" where specifics are needed. Deliberate: withholding from the READER while the AUTHOR knows the answer. If planning dodges a question a writer would need answered to draft, that's a gap, not an iceberg.
4. **Internal contradictions.** Cross-reference dates, ages, timelines. Check character abilities against magic rules. Check geography across documents.

## Dimensions to score

### Lore & worldbuilding (40% weight)
- `magic_system` — hard rules with COSTS per Sanderson's Second Law. Could the climax be resolved using only rules already established? Are costs plot-driving, not decorative? At least 3 societal implications explored?
- `world_history` — timeline that creates PRESENT-DAY tensions. Decorative history counts against, not for.
- `geography_and_culture` — distinct sensory signatures, customs that GENERATE conflict.
- `lore_interconnection` — does changing one element force changes in two others?
- `iceberg_depth` — implied vs. stated. But check: does the AUTHOR actually know the answers, or is it handwaving?

### Character (30%)
- `character_depth` — wound/want/need/lie chains CAUSALLY linked, not just associated. Are any characters missing chains who need them?
- `character_distinctiveness` — remove dialogue tags from example lines. Can you identify the speaker by sentence structure alone? Look for repeated structural formulas across characters. Speech background-appropriate?
- `character_secrets` — each major character's secret should change the plot if revealed. Vague secrets score lower.

### Structure (20%)
- `outline_completeness` — beats, POV, emotional arc, try-fail cycle per chapter. Save the Cat at correct % marks. Score 0 if empty. Score 5+ only if act structure exists.
- `foreshadowing_balance` — every plant has a planned payoff. Score 0 if ledger is empty regardless of implicit threads — foreshadowing must be TRACKED.

### Craft (10%)
- `internal_consistency` — actively hunt contradictions. One major contradiction caps at 6. Three+ caps at 4.
- `voice_clarity` — specific and ACTIONABLE. Exemplars demonstrate the voice. Anti-exemplars define boundaries. Check exemplar dialogue for AI slop.
- `canon_coverage` — facts logged, sourced, sufficient to catch contradictions. Granular enough?

## Output (JSON only, written to `<novel-dir>/eval_logs/<timestamp>_foundation.json`)

```json
{
  "magic_system": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "world_history": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "geography_and_culture": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "lore_interconnection": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "iceberg_depth": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "character_depth": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "character_distinctiveness": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "character_secrets": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "outline_completeness": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "foreshadowing_balance": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "internal_consistency": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "voice_clarity": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "canon_coverage": {"score": N, "gap": "...", "fix": "...", "note": "..."},
  "slop_in_planning_docs": {"found": ["..."], "note": "..."},
  "contradictions_found": ["..."],
  "overall_score": N,
  "lore_score": N,
  "weakest_dimension": "...",
  "top_3_improvements": ["...", "...", "..."]
}
```

`overall_score` weighting: lore 40%, character 30%, structure 20%, craft 10%. `lore_score` is the average of the five lore dimensions.

## Final check

If `overall_score` is above 7, re-read your gap lists. If any gap describes a problem that would force a writer to stop and invent during drafting, your score is too high. **Revise down.**

After writing, also print a one-line human summary: `overall=N.N lore=N.N | weakest: X | top fix: …`.
