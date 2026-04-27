---
name: opus-review
description: Send the full manuscript to two parallel personas — literary critic + professor of fiction — for deep prose-level review. Parses the result with scripts/parse_review.py to extract numbered actionable items with severity and qualification status. Decides whether to keep revising or stop based on stopping conditions. Use after automated revision cycles plateau.
---

# Opus review loop

This is the deepest evaluation. It catches what automated tools miss: prose-level repetition, character thinness, ethical gaps, structural monotony.

## Procedure

### Step 1 — build the manuscript

```bash
python scripts/build_manuscript.py <novel-dir>
```

Writes `<novel-dir>/manuscript.md` (concatenated chapters separated by `---`).

### Step 2 — spawn two subagents in parallel

In a single Agent tool call (parallel):

- `subagent_type: literary-critic` — full manuscript inline. Returns plain-prose newspaper-style review.
- `subagent_type: professor-of-fiction` — full manuscript inline. Returns numbered actionable items.

For very long manuscripts (>200k chars), pass `manuscript.md` to each agent and let it Read the file from its own context.

### Step 3 — assemble the review document

Write to `<novel-dir>/reviews/<timestamp>_review.md`:

```
# Review — <novel title> — <timestamp>

## Literary critic

<critic agent output>

## Professor of fiction

<professor agent output>
```

### Step 4 — parse

```bash
python scripts/parse_review.py <novel-dir>/reviews/<timestamp>_review.md > <novel-dir>/reviews/<timestamp>_parsed.json
```

This extracts:
- star rating (if present)
- numbered professor items, each with `severity` (major/moderate/minor), `type` (compression/addition/structural/mechanical/revision), `qualified` (boolean), `suggestion`
- aggregate counts
- `stop` (boolean) and `stop_reason`

### Step 5 — stopping conditions

Stop revising if any of:

1. ★★★★½ rating with **0 major items**
2. ≥4 stars with **>50% of items qualified/hedged**
3. **≤2 items found total**

The parser sets `stop: true` automatically when these fire.

### Step 6 — if not stopping

Print the top 3 unqualified major/moderate items. For each one the user / orchestrator wants to address:

1. `gen-brief --auto` (or with the specific item) → produces a revision brief
2. `gen-revision <ch>` with the brief → rewrites the chapter
3. Mechanical fixes via `apply-cuts` for pattern-level issues
4. `evaluate-chapter <ch>` to confirm improvement
5. Commit-style snapshot of the novel directory

Then re-run `opus-review` for the next round.

## Severity heuristics from the Bells production

- Multiple major items → structural work needed
- Few major, some moderate → targeted revisions, 2-3 more rounds
- All moderate/minor → polish only, 1-2 more rounds
- Mostly qualified hedges → done; ship it

Items that persist across 3+ rounds may be structural to the novel's voice/approach, not bugs. Learn to accept them. The reviewer will ALWAYS find something.

## Output to user

Print: stars (if any), total / major / qualified counts, stop verdict and reason. If continuing, list the top 3 actionable items with chapter references.
