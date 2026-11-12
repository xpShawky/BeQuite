# Delivery QC checklist (M8 → `FINAL_QC_PASS`)

Most important first: **run the automated checks on every delivered file after encoding, look at a contact sheet of every section, watch the phone preview, and paste every command + output into the work's `evidence.md`.** `FINAL_QC_PASS` is recorded in `gates.md` only when every row below is PASS or n/a with a reason.

## A. Automated (per file: master, preview, each recut)

One command writes the evidence block:

```bash
python .claude/skills/bequite-render-pipeline/scripts/qc_report.py outputs/final/film_FINAL_16x9.mp4 \
       --expect-size 2560x1440 --expect-fps 60 --allow-black-tail 0.8 --evidence .bequite/work/<id>/evidence.md
python .claude/skills/bequite-render-pipeline/scripts/qc_report.py outputs/delivery/film_FINAL_9x16.mp4 --expect-size 1080x1920 --expect-fps 60
python .claude/skills/bequite-render-pipeline/scripts/qc_report.py outputs/previews/v7_720p.mp4 --no-audio        # silent preview
```

| Check | Command inside `qc_report.py` | Pass |
|---|---|---|
| format: size, fps, codec, pixel format | `ffprobe -show_entries format=…:stream=…` | as planned; `yuv420p`; same fps on every version |
| black frames | `blackdetect=d=0.2:pix_th=0.05` | none except intended head/tail fades (allow with `--allow-black-head/tail`); GPU OOM shows up here |
| frozen frames (optional) | `freezedetect` (`--freeze 2.0`) | none unintended (holds with drift are not frozen) |
| loudness after encode | `ebur128=peak=true` | −14 LUFS ±1 integrated (target owned by `bequite-sound-voice`) |
| true peak after encode | same | ≤ −1 dBTP |

Also: `ffprobe` duration matches the plan (±1 frame) and audio is 48 kHz stereo AAC.

## B. Visual (agent prepares, user judges)

| Check | How | Pass |
|---|---|---|
| **Motion DNA continuity on every section** | contact sheet at 1 fps (`contact_sheet.py --video … --every 1`) compared with the styleframes; look at the middle third especially | no off-DNA section, no generic filler, accent used only where it marks something |
| **banding** | stills of dark gradients at 100 %; 2K master from a 16-bit source | no visible rings |
| **phone readability** | 720p preview watched on a phone; every line held per the kinetic-type hold rule | every line readable twice; nothing meaningful under ~24 px at 1080p |
| safe zones (vertical) | stills against the platform's safe-zone overlay | no text in the bottom ~20 % / right edge UI zones |
| native resolution | zoomed UI/product frames at 100 % | sharp, no upscaling blur |
| smoothness | phone preview at full speed | user's verdict recorded in `review.md` |
| Arabic / RTL lines | stills of each line | joins intact, right-to-left reveals, nothing clipped (`.claude/skills/bequite-kinetic-type/references/arabic-rtl.md`) |

## B2. AI-tell QA (every AI-generated shot)

Reject the shot on any hit; regenerate or cut around it, don't patch in prompts. Record the selection ratio (generated vs kept) in `evidence.md`; professionals keep roughly 1 in 10 or fewer. Sources and the full list: `motion-library/CRAFT_RESEARCH.md` section 3.

- [ ] **Hands and bodies:** no merging fingers, wrong digit counts, joints bending wrong, impossible gaits in the background.
- [ ] **Text:** no gibberish or shifting in-scene text (put real text in as graphics instead).
- [ ] **Physics:** objects don't float, sink into surfaces or pass through each other; motion shows contact (feet, hands, props).
- [ ] **Clip ends:** trim the deceleration tail; no shot ends in a freeze or a camera that stops dead (cut about 0.5 s early).
- [ ] **Consistency across shots:** same product shape, colour, logo, character face and wardrobe in every shot.
- [ ] **Look:** not the stock AI look (golden-hour backlight + shallow depth of field + slow motion; flat uniform light; over-saturated or orange skin). One base grade for the whole film, then subtle grain.
- [ ] **Faces and voice:** no sudden reaction zooms, no slow-blinking "perfect skin" headshots; lips close on b/p/m; breaths reduced to natural, not loud or missing.
- [ ] **Sound:** music cuts and swells are tied to picture events, not a generic swell.

## C. Truth and rights

| Check | Pass |
|---|---|
| honesty table in `spec.md` re-checked against what the product does **today** | every claim still true |
| privacy list in `brief.md` | nothing on it appears in any frame (scan the contact sheets) |
| logos and brand marks | official files, not redrawn or AI-generated |
| licence ledger | one row per track, SFX pack, voice, font, AI asset; proof saved |
| AI labelling | platform labels planned where realistic AI video/audio is used |

## D. Delivery hygiene

- [ ] exactly one file named `FINAL` per version (`<film>_FINAL_16x9_2k.mp4`, `<film>_FINAL_9x16.mp4`); stale finals renamed or removed
- [ ] previews at the master's fps
- [ ] captions `.srt` present for every version with voice
- [ ] stems + WAV mix archived in `outputs/audio/`
- [ ] engine project saved (e.g. `.aep`, `.blend`, composition source) with the version number
- [ ] AE: caches purged after the final render (`aerender.js --purge`)
