---
description: Start the full autonovel pipeline for a tagged novel run. Usage — /autonovel <tag>. Creates novels/<tag>/ if absent, drives foundation → drafting → automated revision → Opus review. Multi-hour run; state persists in novels/<tag>/state.json.
---

Invoke the `autonovel` skill with argument `$ARGUMENTS` (the user's tag).

If `$ARGUMENTS` is empty, ask the user for a tag (short, slug-style — `bell-tuner`, `salt-priest`, etc.) before proceeding.

If `novels/$ARGUMENTS/` exists with `state.json` showing a non-zero phase, ask the user whether to resume or start over before overwriting.

Otherwise: create the novel directory, initialise state, copy templates from `templates/`, and walk Phase 0 → 4 of the `autonovel` skill.
