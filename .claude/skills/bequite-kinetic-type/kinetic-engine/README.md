# BQ Kinetic

Kinetic-typography films in After Effects, directed by ChatGPT, with no code written by anyone and no Claude tokens spent per film.

ChatGPT plays the director. It writes the film as a small JSON scene description (`bq-kinetic/1`). The BQ Kinetic panel inside After Effects checks that JSON, builds the film (text layers, the word push, a following camera with motion blur, slams, exits) and makes a contact sheet. ChatGPT looks at the sheet and revises its own film. Two or three rounds are usually enough.

## What is in this folder

| Path | What it is |
|---|---|
| `dist/BQ Kinetic.jsx` | The After Effects panel, one file (engine included). This is what you install. |
| `director/` | The six knowledge files for ChatGPT: `DIRECTOR_INSTRUCTIONS.md`, `SCHEMA.md`, `GRAMMAR.md`, `PRESETS.md`, `EXAMPLES.md`, `TELLS.md`. |
| `engine/bq_kinetic.jsx` | The engine source (ExtendScript, ASCII only). |
| `panel/panel_ui.jsx` | The panel source. |
| `tools/make_panel.py` | Joins engine + panel into `dist/BQ Kinetic.jsx`. Run it after any change. |
| `tests/` | Test films and the harness (`case.py` builds a test in After Effects, renders it with aerender and makes a contact sheet with ffmpeg). |

## Set up the director (once)

1. In ChatGPT, create a Project (or a custom GPT) named "BQ Director".
2. Paste the text of `director/DIRECTOR_INSTRUCTIONS.md` into the project's instructions.
3. Upload all six files from `director/` to the project's files.
4. Use a reasoning model with high effort; the director needs to count beats.

Without a project, attaching the six files to the first message of a chat works too; that is how the first test ran.

## Install the panel (once)

1. Copy `dist/BQ Kinetic.jsx` into the After Effects folder `Scripts/ScriptUI Panels` (Windows: `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Scripts\ScriptUI Panels`).
2. In After Effects: Preferences > Scripting & Expressions > tick "Allow Scripts to Write Files and Access Network".
3. Restart After Effects and open Window > BQ Kinetic.jsx. Dock it wherever you like.

To try it without installing, use File > Scripts > Run Script File and pick `dist/BQ Kinetic.jsx`.

The `night-gold` preset uses Google Sans Flex (static instances), `ink-green` uses Montserrat, `paper` uses Geist. A missing font falls back to the next one on the list and the panel says so.

## Making a film

1. Give ChatGPT the brief: the words or the idea, the platform and length, the music tempo and its first beat, the preset.
2. Copy ChatGPT's whole reply into the panel and press **Build**. (Press **Check** first if you only want to see errors.)
3. Press **Contact sheet**. The panel saves a 12-frame PNG in a `BQ Kinetic sheets` folder next to your project (or on the desktop for an unsaved project).
4. Press **Copy report**, paste it into ChatGPT and attach the sheet. ChatGPT critiques its own film (at most five points, each with a time) and sends a revised JSON.
5. Repeat from step 2. When you are happy, render from the Render Queue (the panel adds an H.264 item when the box is ticked).

Every build is one undo step, and each round lands in its own project folder, so earlier rounds stay to compare.

## What the engine can and cannot do

It can: words landing whole on the beat, the push (a new word appears beside the last one and the row slides to stay centred), stacks of small words, two-colour brand words, a camera that follows the newest word and pulls back to the whole block, slams with a flash, cut / fade / whip-up exits, three presets, 16:9 and 9:16, 24 to 60 fps, a music file laid under the film.

It cannot (yet): Arabic or other right-to-left scripts, images, icons or shapes, per-letter animation.

## Test record

The first end-to-end test (21 Nov 2026, ChatGPT with high effort, a 15 s BeQuite intro, night-gold, 120 BPM) ran five rounds. Every JSON ChatGPT wrote passed the check with no errors and built without a single edit. Its own critiques of the sheets caught the real problems (the brand ending too weak, the client's banned words, cropped lines), and in round 5 it answered "Ready to render." The final film is `build/gpt_final/gpt_final.mp4`; `build/chatgpt_director_rounds.jpg` shows each round's finished blocks.

The test also improved the engine: mixed-size stacks no longer overlap, words never overlap during the push, the film ends exactly on time, the camera stays closer to the whole block (it used to crop lines), static scenes start centred, and the contact sheet samples three frames per scene so no hero word falls between two frames.
