---
name: autonovel
description: Top-level orchestrator for the autonomous novel pipeline. Drives Phase 1 (foundation), Phase 2 (drafting), Phase 3a (automated revision), and Phase 3b (Opus review loop) by delegating to the seed/gen-world/gen-characters/gen-outline/gen-canon/voice-discovery/draft-chapter/evaluate-*/adversarial-edit/apply-cuts/reader-panel/gen-brief/gen-revision/opus-review skills. State persists in <novel-dir>/state.json. Use when the user asks to run the full pipeline, resume an in-progress run, or run a specific phase end-to-end.
---

# Autonovel — pipeline orchestrator

This skill drives the full novel pipeline. It is a **state machine** over `<novel-dir>/state.json`. Each step delegates to a specialised skill (drafting, evaluation, revision) or a Python script (mechanical work).

## Inputs

The user invokes via `/autonovel <tag>` or `/autonovel-resume <tag>`. The `<tag>` resolves to `<novel-dir> = novels/<tag>/` relative to the autonovel project root.

If the directory does not exist:
1. Create `novels/<tag>/`
2. Initialise state: `python scripts/state.py novels/<tag>/ init`
3. Copy templates: `cp templates/{voice.md,world.md,characters.md,outline.md,canon.md,MYSTERY.md} novels/<tag>/`
4. Ask the user for `seed.txt` content (or run the `seed` skill if they want suggestions)

`AUTONOVEL_NOVEL_DIR=novels/<tag>` is exported for child Python scripts.

## Phase 0 — Setup

1. Verify `seed.txt` exists and is specific. A good seed has:
   - A world differentiator (one specific surreal/sensory thing)
   - A central tension (personal + cosmic, in conflict)
   - A cost/constraint on the magic
   - A sensory hook
   If it's vague, push back: "the seed reads like a back-cover blurb. What does breakfast smell like in this world?"
2. Verify `state.json` has `phase: foundation`.
3. Confirm with the user before starting. The pipeline is multi-hour.

## Phase 1 — Foundation

```
LOOP until foundation_score > 7.5 AND lore_score > 7.0:
  1. If iteration == 0:
       - Run `voice-discovery` (writes voice.md Part 2)
       - Run `gen-world`
       - Run `gen-characters`
       - Run `gen-outline`
       - Ask user to fill `MYSTERY.md` (or generate it from outline if user prefers)
       - Run `gen-canon`
     Else (iterations 2+):
       - Identify weakest layer/dimension from prior eval
       - Re-run only the relevant generator with a focus instruction (e.g. "expand magic_system: add 3 societal implications, focus on cost trade-offs")
       - Re-run `gen-canon` if any of world / characters changed
  2. Run `evaluate-foundation`
  3. If `overall_score` improved over `state.foundation_score`:
       - Snapshot novel dir to `novels/<tag>/.snapshots/foundation_iter_<N>/`
       - Update `state.foundation_score` and `state.lore_score`
       - Append to `results.tsv` (use `scripts/results_log.py`)
     Else:
       - Restore the previous snapshot
       - Try a different focus
  4. Note the weakest dimension for the next iteration.
  5. Halt the loop after 15 iterations regardless of score (operator escape).

Exit: state.phase = "drafting".
```

Cross-layer consistency checks every iteration:
- Outline references only lore that exists in `world.md`
- Character abilities match magic system rules
- Foreshadowing ledger balances (every plant has a payoff)
- Voice exemplars exist and aren't generic
- Canon contains all hard facts from world / characters

## Phase 2 — First draft

```
N = number of chapters in outline.md (parse the "### Ch N:" headers)
state.chapters_total = N

FOR ch in 1..N:
  FOR attempt in 1..5:
    1. Run `draft-chapter <ch>`
    2. Run `evaluate-chapter <ch>` (which itself runs slop_scan first)
    3. If overall_score > 6.0:
         - Snapshot the chapter file to chapters/.history/ch_NN_v<attempt>.md
         - Update state.chapters_drafted += 1
         - Append to results.tsv
         - Append new_canon_entries to canon.md
         - Break inner loop, move to next chapter
       Else:
         - If attempt < 5: continue (will redraft)
         - If attempt == 5: keep best-scoring version anyway, note the chapter as "weak" in state.debts

  After every 3 chapters drafted: pause and run a quick consistency sweep
    (evaluate the most recent chapter against canon.md, flag any new
    contradictions to address now rather than in revision).

After all chapters drafted:
  - Run mechanical slop_scan on each chapter; if any has slop_penalty > 4,
    flag for revision phase
  - state.phase = "revision"
```

Watch for:
- **Freshness decay** after Ch 6. If chapters 7+ score consistently lower, push the writer to vary chapter openings and endings explicitly via the brief.
- **Compounding tics.** If the same AI tell appears in 3+ early chapters, hand-fix in `voice.md` Part 2 by adding it as an anti-exemplar BEFORE drafting more chapters.

## Phase 3a — Automated revision

Cycle structure (3-6 cycles, plateau-detect to stop):

```
CYCLE C:
  Diagnosis:
    1. `adversarial-edit all` (writes edit_logs/chNN_cuts.json for each)
    2. `apply-cuts all --types OVER-EXPLAIN REDUNDANT` (or --min-fat 17 first cycle)
    3. `compare-chapters` (Swiss tournament, writes tournament_results.json)
    4. `voice-fingerprint` (writes voice_fingerprint.json) — flag outliers
    5. `reader-panel` (parallel 4 personas, writes reader_panel.json)

  Structural fixes (act on consensus):
    For each consensus item from reader_panel.json (3-of-4 or 4-of-4):
      a. `gen-brief --chapter <X>` with shape inferred from question type
         - cut_candidate → COMPRESSION
         - missing_scene → EXPANSION
         - thinnest_character → DEEPENING
         - worst_scene / momentum_loss → DRAMATISATION
      b. Snapshot chapter to chapters/.history/ before rewrite
      c. `gen-revision <X> briefs/chXX_<shape>.md`
      d. `evaluate-chapter <X>`
      e. If score improved → keep. Else → restore snapshot.

  Targeted fixes (act on eval callouts):
    1. `evaluate-full` → top_suggestion + weakest_chapter
    2. `gen-brief --chapter <weakest_chapter>` (shape inferred from weakest_dimension)
    3. `gen-revision`, evaluate, keep/discard same as above

  Plateau detection:
    novel_score = result of evaluate-full
    If |novel_score - state.novel_score| < 0.5 AND cycle ≥ 3:
      Break — diminishing returns
    Else:
      state.novel_score = novel_score
      Append to results.tsv

After cycles:
  state.phase = "opus_review"
```

Whack-a-mole protection: if `weakest_chapter` rotates twice across cycles, stop chasing it — that score is structural to the novel.

## Phase 3b — Opus review loop

```
LOOP (max 4 rounds):
  1. `opus-review`
     - Spawns literary-critic + professor-of-fiction in parallel
     - Writes reviews/<ts>_review.md and reviews/<ts>_parsed.json
  2. Read parsed.json. If parsed.stop == true: break and report.
  3. For each top unqualified item (priority: major > moderate > minor):
       a. `gen-brief --chapter <ch>` (chapter inferred from item title/text)
       b. snapshot, `gen-revision`, evaluate, keep/discard
       c. If pattern-level (e.g. "X recurs across 4 chapters"), do a
          mechanical apply-cuts pass with a custom filter
  4. Re-run opus-review.

Items that persist across 3+ rounds → accept. They're structural to the
novel's voice/approach, not bugs.
```

Stopping conditions are computed by `scripts/parse_review.py`:
- ★★★★½ with 0 major items
- ≥4 stars and >50% of items qualified
- ≤2 items found

## Phase 4 — Export (out of scope for the core build)

Out of scope per the user's instruction. If reached, just note it and stop.

## Output to user during run

Print one block per phase transition. Inside a phase, print short progress lines per iteration / chapter:

```
[Phase 1, iter 4] focused: lore_interconnection
  evaluate-foundation: overall=7.6 lore=7.1 ← exit threshold met
  Phase 1 complete in 4 iterations. Snapshot saved to .snapshots/foundation_final.

[Phase 2] drafting 23 chapters
  ch 01: drafted 3147w → eval 7.2 ✓ keep
  ch 02: drafted 2980w → eval 5.4 ✗ retry
  ch 02: drafted 3204w → eval 6.4 ✓ keep
  ...
```

Don't quote-dump the full eval JSON in the conversation — write it to disk and print the one-line summary.

## Recovery / resume

If interrupted:
- `state.json` records `phase`, `current_focus`, `iteration`, `chapters_drafted`, `novel_score`
- `/autonovel-resume <tag>` reads state and continues from the appropriate point
- All snapshots are in `<novel-dir>/.snapshots/` and per-chapter history in `chapters/.history/`
