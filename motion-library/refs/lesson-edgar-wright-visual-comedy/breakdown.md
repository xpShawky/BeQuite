# Edgar Wright: How to Do Visual Comedy (Every Frame a Painting): lesson

**File:** `inbox/New/Edgar Wright - How to Do Visual Comedy.mp4` · **Source:** Every Frame a Painting (Tony Zhou, Taylor Ramos), https://www.youtube.com/watch?v=3FOzD4Sfgag · **Length:** ~7:46 · **Studied from:** transcript (`frames/transcript.md`) + frame checks (`frames/check/sheet.jpg`, `items.jpg`, `hotfuzz_montage.jpg`) + ffmpeg scene detection on the travel montage.
**Category:** craft lesson (picture and sound as joke delivery; staging; cut rhythm)

## What it teaches
A beat (a joke, a reveal, a claim) lands harder when picture and sound deliver it, not dialogue. Wright uses the edge of the frame, camera moves, transitions, sound effects, music and light as delivery tools. For a launch film, "joke" reads as "beat": every claim should be delivered by an image event and a sound event, not by the voice or the type alone.

## Lessons (with timestamps)
| # | Time | Lesson | Example used |
|---|---|---|---|
| 1 | 00:21–00:56 | When every beat is carried by dialogue in static close-ups, the film is not using cinema. Picture and the full range of sound (not only speech) should carry the beat. | Unnamed contemporary American comedies (montage) |
| 2 | 01:16–01:43 | The lazy montage: every shot pans left to right, obvious landmarks, helicopter footage, upbeat music to keep people awake. Know the cliché so you can avoid it. | Described, not shown as a single film |
| 3 | 01:43–02:20 (montage measured 01:42.4–01:58.9) | The inventive travel montage. Measured: about 24 cuts in 16.5 s. It opens on holds of 2.2–2.7 s, accelerates to 0.13–0.5 s shots (01:47.2–01:52.8), then eases back to 1.0–1.5 s. It is bookended by two close-ups of a TAXI roof sign: a lit yellow London sign at the start, a dim white one at the end (where we came from, where we are going). The hero always faces forward or right, so screen direction carries the journey. A phone's signal bars drop between two inserts (leaving civilisation). Music down, SFX up, so each cut lands as a jolt. | *Hot Fuzz*: London to Sandford |
| 4 | 02:25–03:02 | Staging in depth: put the important information in the frame while the characters ignore it, so the audience discovers it. Do not hide it in a two-frame insert. | *Shaun of the Dead*: the news on TV in the background |
| 5 | 03:03–03:35 | Replace a dialogue scene with a visual gag that says the same thing. | Wright scene vs a talky version |
| 6 | 03:35–04:50 | The frame is the instrument: things popping into frame, leaving frame, a zoom, a crane up, a pan can each deliver the beat. What is out of frame matters as much as what is in it (Scorsese line, 04:34). | Bordwell-derived examples |
| 7 | 05:15 | **Things entering frame** in a surprising way. | Wright films |
| 8 | 05:27 | **People leaving frame** in a surprising way (the empty frame is the punchline). | Wright films |
| 9 | 05:39 | **There and back again**: the camera moves away and returns; something has changed. | *Shaun of the Dead* |
| 10 | 06:08 | **Matching scene transitions**: the last action of one scene is matched by the first of the next. | Wright films |
| 11 | 06:20 | **The perfectly timed sound effect**: the cut and the sound land on the same frame. | *Scott Pilgrim* and others |
| 12 | 06:38 | **Action synchronised to the music**: movement and cuts on the beat. | *Shaun of the Dead* |
| 13 | 06:52 | **Super-dramatic lighting cues**: the light snaps to a dark or spot look on a single line. | *Scott Pilgrim* (frames) |
| 14 | ~07:15 | Item 8, label inferred from frames (a garden fence collapse/jump): **fence gags**, a physical gag repeated and paid off. UNVERIFIED wording. | *Shaun of the Dead* |
| 15 | ~07:28 | Bonus item 9, label UNVERIFIED (frames show several characters pointing in sync). | *Hot Fuzz* (frames) |

## How each lesson applies to a 30–60 s launch film (BeQuite, "the most powerful AI harness")
- **#1, #5:** never let a type card or VO line be the only carrier of a claim. "Gates catch it" should be an event: a broken commit falls into frame and a gate snaps shut on it, with a clack.
- **#3 (the montage):** the "plan → build → verify → ship" pipeline as a 10–15 s travel montage. Bookend it on the same object in two states (a red failing check at the start, the same check green at the end, framed identically). Keep one screen direction (everything moves left to right, the way progress reads). Pull the music down and let SFX (keys, clicks, gate clacks) drive the fastest stretch.
- **#4:** put proof in the background of UI shots (test counts ticking, a log scrolling with "PASS") while the foreground does the hero action. Viewers who pause find it.
- **#7, #8:** the frame edge is the cheapest reveal tool in AE: UI cards and type pop in from outside the frame on a beat; the hook can end with an object leaving frame and an empty beat before the title.
- **#9:** a camera move off the messy repo and back, and it is clean: before/after without a split screen.
- **#10, #11, #12:** match the exit of one scene to the entry of the next, and put a designed sound on that exact frame.
- **#13:** a lighting snap (the whole UI goes dark, one spot on the logo) for the turn line.

## What to try in the lab
1. **Bookend montage, 8 s:** same framing of one status chip at the start (red) and end (green), 12–16 cuts between, shot lengths 2.2 → 0.15–0.4 → 1.2 s. Measure with `film_study.py` and compare the curve with the Hot Fuzz numbers above.
2. **Enter / exit frame on a beat:** a card enters from frame edge with a strong ease-out, the hit SFX 1–2 frames before the landing; then an exit leaving an empty frame for 6–10 frames before the next cut. Judge whether the empty frame reads as intentional.
3. **There and back:** a 3D camera pan off a messy terminal and back to a clean one, with the swap hidden in the blur.

## Open questions / UNVERIFIED
- The exact on-screen labels for items 8 and 9 were not read from the title cards (the transcript is silent there); labels above are inferred from frames.
- Film attributions for items 7–13 are from frames, not captions.
