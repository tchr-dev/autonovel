# Examples

Worked runs of the autonovel pipeline, committed to the repo so you can
inspect what each phase produces without burning tokens to find out.

## `ashen-crown/`

A classic sword-and-dragons novella, paused mid-pipeline. Useful for seeing:

- **Foundation artifacts**: `world.md`, `characters.md`, `outline.md`,
  `canon.md`, `MYSTERY.md`, `voice.md`, `voice_trials.md` — what Phase 1
  produces before drafting begins.
- **First chapter draft**: `chapters/ch_01.md` — what `draft-chapter`
  outputs given the foundation above.
- **Evaluation logs**: `eval_logs/` — judge-model scoring of foundation
  and chapter quality.
- **State at pause**: `state.json` — `phase: drafting`, foundation
  scores ~7.8, 1 of 12 chapters drafted. This is exactly what
  `/autonovel-resume ashen-crown` would pick up from.
- **Results trail**: `results.tsv` — per-iteration score history.

The seed that produced this run is `seed.txt`, identical to the one at
the repo root.

### Re-running this example

```bash
cp -r examples/ashen-crown novels/ashen-crown
# In Claude Code:
/autonovel-resume ashen-crown
```

The pipeline will continue drafting chapters 2–12, then enter Phase 3a
(automated revision) and 3b (Opus review).

> **Cost note.** Resuming this example to completion takes several hours
> and burns substantial tokens (Opus review in Phase 3b is the heaviest
> step). Inspect the artifacts first; only resume if you want a finished
> novella.
