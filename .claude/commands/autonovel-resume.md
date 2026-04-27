---
description: Resume an interrupted autonovel run. Usage — /autonovel-resume <tag>. Reads novels/<tag>/state.json and picks up at the recorded phase / iteration / chapter.
---

Read `novels/$ARGUMENTS/state.json`. Print the current phase, iteration, and progress (chapters drafted / total, latest novel_score, latest weakest_dimension).

Confirm with the user that the resume point is correct, then invoke the `autonovel` skill with the same tag, instructing it to skip Phase 0 setup and continue from the recorded phase.

If `state.json` is absent: this is not a resumable run; suggest `/autonovel $ARGUMENTS` instead.
