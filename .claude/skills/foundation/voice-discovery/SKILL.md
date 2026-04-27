---
name: voice-discovery
description: Discover the voice for a specific novel during the foundation phase. Writes 3-5 trial passages in different registers, evaluates which best serves the world and tone, then fills in voice.md Part 2 with the chosen register, exemplars, and anti-exemplars.
---

# Voice discovery

The voice should feel like it BELONGS in the world. Le Guin's insight: in fantasy, the language creates the world, not just describes it. A novel about salt-flat priests does not sound like a novel about a tide-bound port city.

## Inputs (from `<novel-dir>/`)

- `seed.txt`, `world.md`, `characters.md`
- `voice.md` (template — Part 1 guardrails are already filled; you fill Part 2)

Reference: `framework/voice-guardrails.md` (Tier 1/2/3 banned words and structural slop patterns — these apply to ALL voices, regardless of which register you choose).

## Procedure

### Step 1 — propose 3-5 candidate registers

Based on the world and characters, list candidate voices the novel could have. Examples (do not just pick from these — invent for the specific novel):

- **Mythic and weighty** — like stone tablets being read aloud. Long sentences. Latinate vocabulary. Clauses that echo psalms.
- **Spare and cold** — sentences like knife cuts. Anglo-Saxon vocabulary. Short paragraphs. Heavy white space.
- **Warm and breathless** — like a traveller telling stories by firelight. Run-on sentences. Colloquial register. Sensory rushes.
- **Dry and ironic** — flat affect. Dark humour. Subtext does the heavy lifting.
- **Childlike-strange** — present tense, unreliable register, fairy-tale syntax.
- **Reportorial / forensic** — emotionally restrained, observational, precise to the level of measurement.

Pick three to five candidates that fit THIS world.

### Step 2 — write a trial passage in each register

For each candidate, write a ~150-word scene from the novel. Same scene every time so registers are directly comparable. Pick a scene that touches the world's specifics — magic in use, a key location, a character speaking. Save the trial passages to `<novel-dir>/voice_trials.md`.

### Step 3 — evaluate

For each trial passage, list:
- What it achieves
- What it costs
- What kind of novel it implies
- Which audience it fits
- Whether it inherits any AI-tells from `framework/voice-guardrails.md`

Pick the register that best serves the story. Justify in 2-3 sentences.

### Step 4 — fill `voice.md` Part 2

Edit `<novel-dir>/voice.md`. Below the `## Part 2: Voice Identity` heading, fill in:

```
### Tone
<one sentence describing the chosen register and its emotional fingerprint>

### Sentence Rhythm
<tendencies, not rules — when sentences run long, when they fragment>

### Vocabulary Register
<the word-hoard for this world: Anglo-Saxon blunt? Latinate baroque? Mixed? Specific noun domains the prose draws from>

### POV and Tense
<third limited / first / present / past / shifts?>

### Dialogue Conventions
<tags? action beats? how do characters sound different from each other? subtext rules>

### Exemplar Passages
<3-5 paragraphs that ARE the voice. The chosen trial passage plus 2-3 more. These are the tuning fork — every chapter calibrates against them>

### Anti-Exemplars
<3-5 paragraphs showing what this voice is NOT. Specific to this novel — not just generic AI slop. "This is too flowery for our tone." "This is too modern.">
```

## Hard rules

- The exemplars must be SPECIFIC to the novel — they reference characters, locations, magic that exist in `world.md` / `characters.md`.
- The anti-exemplars must be SPECIFIC too. "Too flowery" alone is not enough — show a flowery passage that's wrong for THIS novel.
- The voice must avoid the universal Tier 1/2/3 slop in `framework/voice-guardrails.md`. Even the most baroque voice should not say "delve" or "tapestry."

## After writing

Tell the user which register won and why. Suggest running `evaluate-foundation` to score the planning docs as a whole.
