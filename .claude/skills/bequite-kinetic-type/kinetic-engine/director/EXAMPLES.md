# Three complete films

Each example shows the brief, the plan, the JSON, what the contact sheet showed, the critique and the fix. Copy the habits, not the words.

---

## Example 1: a brand line (night-gold, 16:9, 120 BPM)

**Brief.** "BeQuite, the most powerful AI harness right now." Music at 120 BPM, first beat at 0.5 s. About 5 seconds.

**Plan.**
- One scene, four rows. Hero: "now." (XL, accent, slam) on beat 6 after a full-beat breath (nothing lands on beat 5).
- The brand opens on beat 0 in two colours; "the / most" is a small stack beside it on beats 1 and 1.5.
- "powerful" alone on beat 2; "AI harness" as a half-beat pair (3, 3.5); "right" on 4.
- Exit with a whip because a second scene would follow.

```json
{
  "version": "bq-kinetic/1",
  "title": "BeQuite intro",
  "format": { "width": 1920, "height": 1080, "fps": 30 },
  "tempo": { "bpm": 120, "first_beat": 0.5 },
  "style": "night-gold",
  "scenes": [
    {
      "rows": [
        [ { "parts": [ { "text": "Be" }, { "text": "Quite", "accent": true } ], "size": "XL", "beat": 0 },
          { "stack": [ { "text": "the", "beat": 1 }, { "text": "most", "beat": 1.5 } ] } ],
        [ { "text": "powerful", "size": "L", "beat": 2 } ],
        [ { "text": "AI", "size": "L", "beat": 3 }, { "text": "harness", "size": "L", "beat": 3.5 } ],
        [ { "text": "right", "size": "L", "beat": 4 }, { "text": "now.", "size": "XL", "accent": true, "slam": true, "beat": 6 } ]
      ],
      "hold_beats": 3,
      "exit": "whip-up"
    }
  ]
}
```

**Contact sheet.** 0.6 s BeQuite alone, centred. 1.0 s "the" lands small to its right. 1.5 s "most" under it. 1.9 s "powerful" lands below and the camera has moved down with it. 2.3 to 3.1 s "AI harness", then "right"; each row slides to stay centred and the camera follows with motion blur. 3.5 s "now." slams in gold with a flash. 4.0 s the whole block, settled. 4.8 s the block whips up, blurred.

**Critique and fix.**
1. 1.9 s: "powerful" lands only half a beat after "most", so the stack (the joke of the line) never gets a moment alone. Land "powerful" half a beat later (2.5).
2. 2.7 s: "AI harness" and "right" are three L words in a row; "right" is a connector here. Make it M so "now." dominates.

Revised rows: `"powerful"` beat 2.5; `"right"` size M. Everything else unchanged.

---

## Example 2: a tutorial hook (ink-green, 16:9, 120 BPM)

**Brief.** "Animating text like this can be challenging, but this tutorial will help you. How to do that." About 9 seconds.

**Plan.**
- Three scenes with three different rhythms: a dense run (scene 1), a building line (scene 2), a slow payoff (scene 3).
- Scene 1 hero: "challenging" (L, accent) on beat 4 after a breath.
- Scene 2 hero: "you" (accent) on beat 4.
- Scene 3: three slow words, "that" slams on beat 3.

```json
{
  "version": "bq-kinetic/1",
  "title": "Kinetic hook",
  "tempo": { "bpm": 120, "first_beat": 0.5 },
  "style": "ink-green",
  "scenes": [
    {
      "rows": [
        [ { "text": "animating", "size": "M", "beat": 0 }, { "text": "text", "size": "L", "accent": true, "beat": 0.5 } ],
        [ { "text": "like", "size": "XL", "beat": 1 }, { "stack": [ { "text": "this", "beat": 1.5 }, { "text": "can be", "beat": 2 } ] } ],
        [ { "text": "challenging", "size": "L", "beat": 4 } ]
      ],
      "hold_beats": 2,
      "exit": "whip-up"
    },
    {
      "rows": [
        [ { "text": "but", "size": "L", "beat": 0 }, { "stack": [ { "text": "this", "beat": 0.5 }, { "text": "tutorial", "beat": 1 } ] } ],
        [ { "text": "will", "size": "M", "beat": 1.5 }, { "text": "help", "size": "L", "beat": 2 } ],
        [ { "text": "you", "size": "XL", "accent": true, "beat": 4 } ]
      ],
      "hold_beats": 2,
      "exit": "cut"
    },
    {
      "rows": [
        [ { "text": "how", "size": "L", "beat": 0 } ],
        [ { "text": "to do", "size": "L", "beat": 1 } ],
        [ { "text": "that", "size": "XL", "accent": true, "slam": true, "beat": 3 } ]
      ],
      "hold_beats": 3,
      "camera": "static",
      "exit": "fade"
    }
  ]
}
```

**Contact sheet.** Scene 1 builds a dense, justified block; "challenging" lands alone on the last row. Scene 2 snaps in after a cut. Scene 3 is framed whole; "that" slams in mint.

**Critique and fix.**
1. Scene 1: "text" is accented and "challenging" is not, but "challenging" is the hero. Move the accent to "challenging".
2. Scene 3: `static` with only three words feels like a slide. Use `follow`, so the camera travels down the three words, then pulls back on the slam.

---

## Example 3: a manifesto Reel (paper, 9:16, 100 BPM)

**Brief.** A 9:16 Reel: "Plan first. Prove it. Then ship." Music at 100 BPM, first beat at 0.4 s. About 8 seconds.

**Plan.**
- Three short scenes, one idea each; a beat at 100 BPM is 0.6 s.
- Scene 1 and 2: two words each, the second word is the hero.
- Scene 3: "Then" small, "ship." slams; the only accent of the film.
- Portrait frame: one or two words per row so the block stays tall and narrow.

```json
{
  "version": "bq-kinetic/1",
  "title": "Plan Prove Ship",
  "format": { "width": 1080, "height": 1920, "fps": 30 },
  "tempo": { "bpm": 100, "first_beat": 0.4 },
  "style": "paper",
  "scenes": [
    {
      "rows": [ [ { "text": "Plan", "size": "XL", "beat": 0 } ], [ { "text": "first.", "size": "L", "beat": 1 } ] ],
      "hold_beats": 2,
      "exit": "cut"
    },
    {
      "rows": [ [ { "text": "Prove", "size": "XL", "beat": 0 } ], [ { "text": "it.", "size": "L", "beat": 0.5 } ] ],
      "hold_beats": 3,
      "exit": "cut"
    },
    {
      "rows": [ [ { "text": "Then", "size": "M", "beat": 0 } ], [ { "text": "ship.", "size": "XL", "accent": true, "slam": true, "beat": 2 } ] ],
      "hold_beats": 3,
      "exit": "fade"
    }
  ]
}
```

**Contact sheet.** Each scene is a tall two-word block centred on warm off-white; "ship." lands orange with a flash.

**Critique and fix.**
1. Scenes 1 and 2 have nearly the same rhythm. Scene 2 is the urgent one: keep "it." on 0.5 (a quick hit) and give scene 1 a slower landing for "first." on beat 1.5.
