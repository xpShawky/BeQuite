# The learning orchestra

How the motion director keeps getting better between films: every film studied, every technique tried, every result (worked or failed) is written down the moment it happens, so nothing is relearned and every plan can offer real options ("we could do 1, 2 or 3; here is where each comes from and what it costs").

Three loops, one library (`motion-library/`):

| Loop | Input | Output | Command |
|---|---|---|---|
| **Study** | a film in `inbox/New/` | `refs/<slug>/breakdown.md`, INDEX row, new or updated techniques | `/bq-motion study <file|folder>` |
| **Lab** | a technique marked `untested` | `lab/NNN-slug/notes.md` + a test render, technique status updated | `/bq-motion lab <technique>` |
| **Plan** | a brief | 2-3 directions built only from studied refs and tested techniques | `/bq-motion` M1-M2 |

## 1. The crew (roles the director calls on)

The director is one agent wearing several hats in order. Each hat looks at the same film for different things, and writes its own lines in the breakdown.

| Role | Watches for | Writes into | Craft skill |
|---|---|---|---|
| **Director** | the one feeling, story shape, hook, where it breathes, the ending | breakdown §1-2, §5 | `bequite-motion-director` |
| **Editor** | cut rhythm, shot lengths per act, match cuts, J/L cuts, cuts on action, where the cuts accelerate or stop | §3 beat sheet, §4 transitions/pacing | `references/motion-grammar.md` |
| **Sound designer** | music entry and drops, BPM, hits on cuts, whooshes and risers, silences, the mix level | §4 sound | `bequite-sound-voice` |
| **Voice director** | voice gender and register, words per minute, pauses, where the line lands against the cut | §4 sound | `bequite-sound-voice` |
| **Graphic / motion designer** | layout grid, colour system, shape language, UI morphs, guide elements | §4 colour/background | `references/style-system.md` |
| **Typographer** | typefaces, treatment per line, hold times, type in 3D | §4 typography | `bequite-kinetic-type` |
| **DP / 3D artist** | lens, camera moves, light sweeps, materials, macro, product turns | §4 camera | `references/3d-and-filmed-look.md` |
| **AI-video generalist** | which shots could be generated, which would read as AI | §7 + technique notes | `references/ai-generation.md` |
| **QA** | AI tells, loudness, readability on a phone | §7 | `bequite-render-pipeline` QC B2 |

## 2. Study loop (per film)

1. **Measure** (local, cheap, no tokens): `.claude/skills/bequite-motion-director/scripts/film_study.py VIDEO refs/<slug>/frames` gives cuts, shot lengths, camera labels, match-cut candidates, loudness, tempo, onsets, silences and what the sound does at each cut. `.claude/skills/bequite-motion-director/scripts/transcribe.py` (faster-whisper, GPU when present) gives the voice lines. `.claude/skills/bequite-motion-director/scripts/director_sheet.py` joins them into one shot-by-shot table with voice pace and pitch.
2. **Look** only where the numbers point: `shots.jpg` (one tile per shot), `matches.jpg` (before|after pairs), `timeline.png` (cuts over the sound). Open more frames only for moments the sheet flags.
3. **Long films** (keynotes, lessons): read the transcript and the chapters first; study the minutes that matter (opening, product films, transitions), not the whole thing. A second model (Gemini on YouTube, for example) can point at the key moments; its answer is a pointer, checked against the measured film.
4. **Write** `refs/<slug>/breakdown.md` from `motion-library/TEMPLATE.md`, every claim tied to a timestamp. Quote at most a short line of a voice-over; never paste the script.
5. **Catalogue**: every technique seen goes into `motion-library/TECHNIQUES.md` (new row, or one more "seen in" for an existing one). Add or update the INDEX row and the directions menu.
6. **Move** the film from `inbox/New/` to `inbox/old/`. `New/` ends empty.

Measured labels are pointers, not verdicts: a "graphic-match" tag must be confirmed on `matches.jpg` before it goes into a breakdown.

## 3. Lab loop (per technique)

A technique is only `proven` once we have made it ourselves and it looked right.

1. Pick an `untested` technique from `TECHNIQUES.md` (or one a plan needs).
2. Research how pros build it (official docs, tutorials); write the hypothesis and the recipe in `motion-library/lab/<NNN-slug>/notes.md` before touching the tool.
3. Build the smallest test in the cheapest tool that can do it (ffmpeg or code, then After Effects via the ExtendScript bridge, Premiere, Blender, Resolve, Google Flow), at preview quality.
4. Measure the test with `film_study.py` and compare it with the reference numbers (did our match cut register as `position-locked`? does our hit land within ±70 ms of the cut?). Look at the frames.
5. Write the result: `worked` / `partly` / `failed`, why, the exact settings, the render path, time spent, credits spent. A failure is kept: it saves the next attempt.
6. Update the technique status in `TECHNIQUES.md` (`untested` → `proven` / `partly` / `failed, see lab/NNN`).

Lab rules: preview renders only; paid generation credits only inside the ceiling the owner set; never overwrite the owner's projects (work in `lab/`); stop after 3 failed attempts on one technique and write what blocked it.

## 4. Plan loop (how the library pays off)

At M1, the director reads `INDEX.md` and `TECHNIQUES.md` and proposes 2-3 directions, each as: the feeling, the structure, 3-5 techniques (with status: proven ones are cheap and safe, untested ones carry a lab cost), the reference timestamps that show it, tools and rough effort. The owner picks; the choice and the reason go into the work `log.md` and, when the owner rejects something, into `MISTAKE_MEMORY.md` so the next plan does not offer it again.

## 5. Write-back, always

| When | Write |
|---|---|
| a film studied | breakdown + INDEX + TECHNIQUES + move to `old/` |
| a lab test done | `lab/NNN/notes.md` + TECHNIQUES status |
| a lesson (something failed, the owner disliked something) | `.bequite/state/MISTAKE_MEMORY.md` |
| a session ends | `.bequite/logs/AGENT_LOG.md`, `.bequite/state/LAST_RUN.md` |
