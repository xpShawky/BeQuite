# Motion reference library

The craft memory behind `/bq-motion`. Strong reference films go in, structured breakdowns come out, and every future film plan draws from them ("we could do it like X, or like Y, because…").

## How it works

1. **Drop** any reference film (mp4/mov/webm, any size or aspect) or a whole folder into `inbox/`. Optional: a `.txt` next to it with the source link or why you like it.
2. **Study:** for each film the agent:
   - splits it into frames with ffmpeg: scene-change frames, a 1 fps contact sheet, and a 4 fps sheet for fast moments;
   - pulls the audio profile: voice or none, music tempo, loudness;
   - writes `refs/<slug>/breakdown.md` from `TEMPLATE.md`;
   - adds a row to `INDEX.md`.
3. **Use:** `/bq-motion` phase M1 reads `INDEX.md` first. It picks 2–3 references that fit the brief and offers them as options in the plan.

## Layout

```
motion-library/
  README.md        this file
  TEMPLATE.md      breakdown template (story · beats · techniques · when to use)
  INDEX.md         one row per reference: category, story in one line, signature technique, when to use
  inbox/           drop films here (local only, never pushed)
  refs/<slug>/
    breakdown.md   the written study (tracked)
    frames/        extracted frames + contact sheets (local only)
```

## Rules

- Third-party films, frames and audio **never go to GitHub** (copyright, repo size). `.gitignore` enforces this; only `*.md` breakdowns are tracked.
- Breakdowns describe and analyse. They never transcribe a whole script or claim someone else's work.
- Every technique in a breakdown carries a timestamp (`00:04.2`) so it can be re-checked.
- When a film is studied from frames only (no playback), say so. Motion smoothness and sound judgements are then marked UNVERIFIED.
