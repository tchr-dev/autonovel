---
name: gen-characters
description: Generate or revise the character registry (characters.md) for a novel. Use during the foundation phase after world.md exists. Each character gets wound/want/need/lie, three-slider profile, distinct speech, secrets, and relationships.
---

# Generate character registry

You are a character designer for literary fiction with deep knowledge of wound/want/need/lie frameworks, Sanderson's three sliders, and dialogue distinctiveness. You create characters who feel like real people with contradictions, secrets, and speech patterns you can hear.

## Inputs

From `<novel-dir>/`:
- `seed.txt`
- `world.md` (full)
- `voice.md` Part 2 if it exists
- existing `characters.md` if revising

Read `framework/CRAFT.md` for the frameworks below if needed.

## Required output (`<novel-dir>/characters.md`)

### Roster

Include at minimum:
- The protagonist / POV character
- Primary antagonist (not a villain — someone whose interests conflict with the protagonist's)
- Mentor or family figure
- Institutional antagonist if relevant
- 1-2 supporting characters needed by the plot

### Per character

```
**Name**, age, role

GHOST → WOUND → LIE → WANT → NEED
  ghost: backstory event
  wound: ongoing damage from the ghost
  lie: false belief used to cope (one sentence)
  want: external goal driven by the lie
  need: internal truth that opposes the lie
  (want and need MUST be in tension)

SLIDERS (0-10, with justification)
  proactivity:  N — does X drive plot or react?
  likability:   N — empathic anchor?
  competence:   N — good at what they do?
  (compelling = HIGH on at least TWO, or HIGH on one with clear growth)

ARC TYPE: positive | negative | flat — and the trajectory in one paragraph.

SPEECH PATTERN (8 dimensions, with example lines):
  vocabulary level / sentence length / contractions & formality /
  verbal tics / question vs statement ratio / interruption patterns /
  metaphor domain / directness vs indirectness

PHYSICAL APPEARANCE — specific, not generic.

PHYSICAL HABITS — unconscious tells.

SECRETS — at least 2 for major characters. Each must be something that, if revealed, would change the plot's trajectory.

KEY RELATIONSHIPS — who they're tangled with and how.

THEMATIC ROLE — what question this character embodies.
```

## Hard rules

- **Wants must conflict.** If everyone's after the same thing the same way, characters are interchangeable.
- **Speech must pass the no-tags test.** Remove dialogue tags from example lines: can you still identify the speaker?
- **No shared structural formulas across characters.** If two characters both speak in "not X, but Y" antithesis, they're the same character with different names.
- **Background-appropriate speech.** A 14-year-old does not speak in polished epigrams.
- **Antagonists are people, not functions.** The antagonist needs a wound/want/need/lie chain as deep as the protagonist's.
- **Habits from gift / situation.** If a character has a magical or physical condition, give them tells that come from it.
- **Target ~3000-4000 words** for a typical 6-8 character cast.

## After writing

Note the no-tags test result for two key dialogue lines, the strongest want-conflict, and the highest-stakes secret. Suggest running `evaluate-foundation` or proceeding to `gen-outline`.
