# A kinetic-type film directed by ChatGPT

A 15-second BeQuite intro (1920x1080, 30 fps, 120 BPM, the `night-gold` preset), written entirely by ChatGPT as `bq-kinetic/1` JSON and built in After Effects by the BQ Kinetic panel. No one edited the JSON, and the film cost no Claude tokens.

| File | What it is |
|---|---|
| `film.json` | ChatGPT's round-5 film, exactly as it wrote it: four scenes (Research, Plan, Prove, the brand ending) |
| `rounds.jpg` | Each round's finished blocks, round 1 to round 5 |

## How it was made

1. ChatGPT (a reasoning model, high effort) got the six director files from `.claude/skills/bequite-kinetic-type/kinetic-engine/director/` and a short brief: the words, 15 s, 120 BPM with the first beat at 0.5 s, `night-gold`.
2. Its JSON went into the panel unchanged: **Check**, then **Build**, then **Contact sheet** (three frames per scene).
3. The panel's report and the sheet went back to ChatGPT. Each time it critiqued its own film in at most five timed points and sent a revised JSON.
4. After round 5 it answered "Ready to render."

What the rounds changed: the brand ending got stronger, words the brief banned were removed, and lines that were cropped were fixed. Every JSON passed the check with no errors on the first try. The rounds also exposed four engine problems, all fixed before round 5: overlapping words in mixed-size stacks, words touching during the push, the film running past its length, and a camera that came in too close.

## Build it yourself

1. Install the panel: copy `.claude/skills/bequite-kinetic-type/kinetic-engine/dist/BQ Kinetic.jsx` into After Effects' `Scripts/ScriptUI Panels` folder, allow scripts to write files (Preferences > Scripting & Expressions), and restart.
2. Open **Window > BQ Kinetic.jsx**, paste `film.json`, then press **Check** and **Build**.
3. The `night-gold` preset uses Google Sans Flex. If the font is missing, the panel falls back to the next font and says so.

To direct your own film, follow "Making a film" in [the engine's README](../../.claude/skills/bequite-kinetic-type/kinetic-engine/README.md).
