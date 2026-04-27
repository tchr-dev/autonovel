# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- **Subagent model selection is now pinned in agent frontmatter** rather than
  inherited from the orchestrator session. Each persona now runs on the model
  appropriate to its workload regardless of which model `/autonovel` is
  launched from.
  - `literary-critic` → `model: opus` (full-manuscript long-form criticism)
  - `professor-of-fiction` → `model: opus` (full-manuscript severity-tagged
    punch list — feeds the Phase 3b stopping condition)
  - `panel-editor` → `model: sonnet` (arc summary in, structured JSON out)
  - `panel-writer` → `model: sonnet`
  - `panel-genre-reader` → `model: sonnet`
  - `panel-first-reader` → `model: sonnet`
- README "Models" section expanded with the per-agent table and a note on
  switching the two Opus agents to `claude-opus-4-7[1m]` for manuscripts
  that crowd the standard 200k Opus context window (≳120k words).
