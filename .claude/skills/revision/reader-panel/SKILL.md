---
name: reader-panel
description: Run a 4-persona reader panel (editor, genre reader, writer, first reader) on the full novel. Spawns four subagents in parallel, each evaluating independently, then merges results into consensus + disagreement findings. Use during revision cycles to surface novel-level issues that per-chapter eval misses.
---

# Reader panel

A reader panel evaluates the novel AS A WHOLE, not chapter by chapter. The disagreements between readers are where editorial decisions live.

## Procedure

### Step 1 — build the arc summary

If `<novel-dir>/arc_summary.md` does not already exist (or is stale), generate it. The arc summary is what you hand to each persona — they don't read 80k words.

For each chapter, write:
```
## Ch N — [title]

OPENING (~150 words, lightly trimmed from the actual chapter open)
...

KEY BEATS:
- beat 1
- beat 2
- beat 3

KEY DIALOGUE (1-2 lines that capture the chapter's tone)

CLOSING (~100 words from the chapter's actual ending)
```

Concatenate all chapters into `<novel-dir>/arc_summary.md`. Total target ~12,000-18,000 words for a 75k-word novel.

### Step 2 — spawn four subagents in parallel

Use the Agent tool with one tool-use block containing four parallel calls:

| subagent_type | Persona |
|---|---|
| `panel-editor` | Senior fiction editor |
| `panel-genre-reader` | Avid fantasy reader |
| `panel-writer` | Published novelist |
| `panel-first-reader` | Thoughtful general reader |

To each, pass:
- The full content of `<novel-dir>/arc_summary.md` inline in the prompt
- A note that the novel is N chapters / W words
- The JSON schema (in each agent's instructions, but reiterate it: the 10 questions)

Each agent returns JSON with the 10 questions answered.

### Step 3 — merge

Save each persona's JSON to `<novel-dir>/edit_logs/reader_panel.json` under `readers.<persona_key>`.

For consensus detection across these questions: `momentum_loss`, `cut_candidate`, `thinnest_character`, `worst_scene`:

1. Extract chapter numbers each persona mentions (`re.findall(r'Ch(?:apter)?\s*(\d+)', answer, re.IGNORECASE)`).
2. For each chapter mentioned by any persona, list which personas flagged it and which didn't.
3. **Consensus item** = 3-of-4 or 4-of-4 agreement. These are revision priorities.
4. **Disagreement item** = 1-of-4 or 2-of-4. These are editorial calls — flag them but don't auto-act.

Write `<novel-dir>/edit_logs/reader_panel.json`:

```json
{
  "readers": {
    "editor": { /* the editor's JSON */ },
    "genre_reader": { /* ... */ },
    "writer": { /* ... */ },
    "first_reader": { /* ... */ }
  },
  "consensus_items": [
    {"question": "cut_candidate", "chapter": 14, "agreement": "4/4", "details": {...}}
  ],
  "disagreements": [
    {"question": "thinnest_character", "chapter": 8, "flagged_by": ["editor"], "not_flagged": ["genre_reader", "writer", "first_reader"]}
  ],
  "timestamp": "..."
}
```

## Output to user

Print:
- Each persona's `would_recommend` and `best_scene` answer (one line each)
- All consensus items with the question and chapter
- All disagreements with the split

Suggest: pass each consensus item to `gen-brief` to generate a revision brief, then `gen-revision`.
