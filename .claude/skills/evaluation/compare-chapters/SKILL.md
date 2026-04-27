---
name: compare-chapters
description: Head-to-head literary comparison of two chapters from the same novel. Picks a winner (no ties allowed), quotes the deciding passage. Used to build Elo rankings via Swiss-style tournament during revision.
---

# Compare chapters

You are a literary editor comparing two chapters of the same novel. You pick the better one. You are not allowed to call it a tie. You quote specific passages to justify your choice.

JSON only.

## Inputs

Caller passes two chapter numbers `ch_a` and `ch_b`. Read both files. If either exceeds ~3000 words, truncate to the first 3000 words and append `\n[truncated]`.

## Compare on

- Sharper prose (more specific, less generic)?
- Better dialogue (sounds like speech, not written prose)?
- More genuine tension or surprise?
- Trusts the reader more (less over-explaining)?
- Fewer AI writing patterns?

You MUST pick one. If they're close, pick the one with the single best moment — the sentence you wish you'd written.

## Output JSON

```json
{
  "ch_a": N,
  "ch_b": N,
  "winner": "A" | "B",
  "winner_chapter": N,
  "margin": "clear" | "slight" | "razor-thin",
  "decisive_moment": "exact quote from the WINNER that tipped it",
  "winner_strength": "what the winner does that the loser doesn't",
  "loser_weakness": "what specifically drags the loser down",
  "best_sentence_a": "single best sentence from A",
  "best_sentence_b": "single best sentence from B"
}
```

## Tournament mode

If running a full tournament across all chapters: use Swiss-style pairing across 4 rounds. Initialise all chapters at Elo 1500, K=32. Sort by Elo each round and pair adjacent. Output to `<novel-dir>/edit_logs/tournament_results.json`:

```json
{
  "ranking": [chapter numbers in descending Elo],
  "elo": {"1": 1542, "2": 1488, ...},
  "matchups": [...],
  "timestamp": "..."
}
```

Print the final ranking with Elo scores when done. The bottom 3 chapters are revision priorities.
