# Lessons from the BeQuite hero film (work 0001, 2026-11-12 to 11-15)

What the owner corrected and what broke, so the next film starts past them. Each item: what happened, the rule now.

## Direction (the owner's eye)

- **Generic reads as AI.** A first 3D character (Blender) "reads generic"; beige/green palettes and a cursor-block character were rejected as generic. Rule: start from the owner's own references and his own character sheet; trace it ("like tracing paper") before inventing.
- **Flat drawings were rejected** in favour of the real object (a real MacBook model, credited, with the logo visible).
- **No brown world.** A warm "dark" Blender world (0.03, 0.022, 0.012) made the laptop look brown. Rule: the camera sees black; reflections see a studio.
- **Measure the reference before matching it.** Our type was thicker and shinier than Apple's: measured stroke 48.3 px vs Apple's 28.4 px, metal p90 221 (bluish) vs 200 (neutral). Fixed by a narrower width and weight and a matte neutral metal (stroke 32-34 px, p90 ~205).
- **Kinetic type (v14):** type follows the light or the laptop's angles; the brand word first; whole words that push, not typing; less zoom; every step checked to fit the shot (`bequite-kinetic-type/references/kinetic-study.md`).
- **Frames before video.** The owner asked for stills and storyboards before any video spend; it saved credits and caught direction errors early.

## Tools and pipeline

- **AI video credits:** shots generated at 8 s cost 24 credits each until the owner flagged the waste; set the length per shot from the edit. A frame picker sorted by "Recent" swapped two frames; two links (24 credits) were lost. Rule: zoom on the frame preview before every submit.
- **Flow flagged "unusual activity"** once (a page script hook plus fast clicks). Rule: no script hooks on the page, human-paced clicks, re-read coordinates per layout.
- **After Effects scripting:** `float` is a reserved word in ES3; variable fonts silently fall back to serif in text layers (use static fonts); many async `saveFrameToPng` calls crashed AE (save one frame, poll for the file); drive `aerender` from Python with an argument list, not bash string loops; AE Glow "Original Colors" turns warm gold to lemon yellow (build glows from blurred Screen-mode copies).
- **AE one-shot runs:** a script that leaves the project modified blocks `AfterFX -r` at a hidden "Save changes?" dialog; close the project without saving at the end of every probe.
- **Blender lights** shine along local -Z (aim with rotation x = -(90 + tilt)); fit a gobo's diagonal inside the cone (about 0.82) or the cone crops it.
- **Review sheets:** sample per scene (first word, half built, finished), not evenly spaced.

Sources: work 0001's log and the mistake memory in the BeQuite repo's private working memory; this page is the shippable summary.
