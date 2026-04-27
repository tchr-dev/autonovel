# autonovel — Claude Code project notes

This file is auto-loaded by Claude Code when the repo is opened. It documents
the conventions a contributor (or Claude) needs to know before touching the
pipeline.

## What this repo is

An autonomous fantasy-novel pipeline implemented as Claude Code skills,
subagents, and slash commands. The user runs `/autonovel <tag>` and the
orchestrator drives foundation → drafting → revision → Opus review.

## Directory contract

| Path | Role | Edit policy |
|------|------|-------------|
| `.claude/skills/`   | LLM-driven pipeline steps          | Edit when changing pipeline behavior |
| `.claude/agents/`   | Persona subagents (panel, critics) | Edit when tuning persona voice |
| `.claude/commands/` | Slash commands (`/autonovel`)      | Edit when changing user-facing entry points |
| `framework/`        | Immutable craft references         | **Do not edit mid-run** — skills load these as ground truth |
| `templates/`        | Per-novel skeletons                | Edit to change what a fresh run starts with |
| `scripts/`          | Mechanical Python helpers (no LLM) | Pure functions; no API keys, no network |
| `novels/<tag>/`     | One per novel run                  | Gitignored; state lives here |
| `examples/`         | Worked examples (committed)        | Demo runs only — do not write new runs here |

## State

All run state lives in `novels/<tag>/state.json`. Resume via
`/autonovel-resume <tag>`. There is no global state outside a tag directory.

## Snapshots, not git

Phase transitions write snapshots to `novels/<tag>/.snapshots/`. "Discard"
means restore from snapshot — never `git reset --hard`. The repo's git
history tracks the *pipeline*, not any individual novel run.

## Models

Skills assume an Opus-class model is available for Phase 3b review and a
Sonnet-class model for drafting/evaluation. On a Haiku-only plan expect
degraded prose quality and weaker review signal. The harness (Claude Code)
chooses the model — there is no model-name branching in skills.

## API keys

Claude Code provides the LLM, so `ANTHROPIC_API_KEY` is **not needed** for
the pipeline itself. `.env.example` is preserved only for users who want to
run the standalone Python scripts in `scripts/` against the Anthropic API
directly (none currently require it; reserved for future helpers).

## Conventions when editing skills

- Skills must be idempotent on re-run — the orchestrator may invoke them
  twice on resume.
- Read state via `scripts/state.py`; never parse `state.json` ad-hoc.
- Use snapshots before any rewrite that touches more than one chapter.
- Keep `framework/*.md` immutable inside a single run; bump them between
  runs if craft references evolve.

## What's intentionally out of scope

Art generation, audiobook synthesis, ePub export, LaTeX typesetting,
landing-page generation. The legacy Python tooling for those lived in a
separate `inbox/autonovel/` directory in the original repo and is not
ported here.
