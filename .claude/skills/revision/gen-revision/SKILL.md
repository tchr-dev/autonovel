---
name: gen-revision
description: Rewrite a single chapter from a revision brief. Preserves voice, world, and characters from the existing draft while making the structural changes the brief specifies. Used after gen-brief and during revision cycles.
---

# Generate revision

You are rewriting a fantasy novel chapter from a specific revision brief. You follow the brief exactly. You preserve the voice, world, and characters from the existing draft while making the structural changes specified.

You write the FULL chapter. Do not truncate or summarise.

## Inputs

Caller passes chapter number N and brief path. From `<novel-dir>/`:
- `voice.md`, `characters.md`, `world.md`, `canon.md`
- `chapters/ch_<N-1:02d>.md` — last 2000 chars (skip if N=1)
- `chapters/ch_<N+1:02d>.md` — first 1500 chars (skip if last chapter)
- `chapters/ch_<N:02d>.md` — the existing draft (raw material; keep what works, change per brief)
- The brief markdown file

## Procedure

1. Read the brief carefully. Identify the brief shape (compression / expansion / dramatisation / etc.) and the word-count target range.
2. Read the existing chapter. Note the "what to keep" anchors from the brief — locate them in the existing draft.
3. Plan the changes in your head before writing:
   - Where do the changes go (paragraph-level)?
   - Which existing passages survive verbatim or near-verbatim?
   - Which beats are added / cut / restructured?
4. Write the FULL revised chapter to `<novel-dir>/chapters/ch_<N:02d>.md` (overwrite).
5. Hit the word-count target ±10%.

## Anti-patterns (apply, even on revision)

Same as `draft-chapter`:

1. No banned words from `voice.md` Part 1
2. No AI fiction tells (`framework/ANTI-SLOP.md`)
3. No triadic sensory lists
4. No "He did not [verb]" more than once per chapter
5. No "He thought about [X]" constructions — convert to fragment, action, or dialogue
6. No "the way [X] did [Y]" more than twice per chapter
7. No "not X, but Y" formula in narration
8. No over-explaining after showing
9. Max 2 section breaks (---)
10. At least one moment that genuinely surprises
11. 70%+ in-scene
12. Dialogue sounds like speech, not prose

## Important: gen-revision tends to overshoot word count

In production, expansion briefs targeting 3200w produced 3800-4200w. **Aim low.** If the brief says 3200, write 3000. The model adds ~30% by default; counter-bias.

## After writing

Print:
- New word count vs. target
- The 3 most significant changes from the previous draft (paragraph-level)
- One sentence on what felt riskiest

Suggest: `evaluate-chapter <N>` to confirm score improved. If it didn't, revert from `chapters/ch_<N:02d>.md.bak` (you can save a `.bak` copy before overwriting).
