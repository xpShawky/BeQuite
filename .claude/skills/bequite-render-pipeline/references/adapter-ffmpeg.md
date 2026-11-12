# Adapter: ffmpeg (study, preview, reframe, captions, mux, encode)

Most important first: **ffmpeg is the agent's eyes and scissors in every pipeline: frames for review, small previews for the phone, real recuts, captions, the final mux and the QC measurements.** All commands below ran on ffmpeg 8.0.1 in this pack (synthetic test media) unless marked. Windows paths in filter arguments need the drive colon escaped (`C\:/fonts/x.ttf`).

## Studying a film (reference or our own render)

```bash
# 1 fps contact sheet of the whole film (30 tiles per sheet; numbered sheets for longer films)
ffmpeg -i ref.mp4 -vf "fps=1,scale=480:-1,tile=6x5" sheet_1fps_%02d.png
# 4 fps sheets for fast moments (a 200 ms pop falls between 1 fps samples)
ffmpeg -ss 12 -t 6 -i ref.mp4 -vf "fps=4,scale=480:-1,tile=6x4" sheet_4fps_%02d.png
# every frame of one 3 s moment, to read an effect
ffmpeg -ss 12 -t 3 -i ref.mp4 -vf "fps=15,scale=960:-1" f_%03d.png
# hard cuts vs continuous moves (try 0.35 and 0.2)
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.35)',showinfo" -an -f null - 2>&1 | grep pts_time
# rhythm: motion energy (mean frame difference) at 5 samples per second
ffmpeg -i ref.mp4 -vf "fps=5,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -an -f null - 2>&1 | grep YAVG
# a 25 % speed copy for model-assisted analysis (state the factor in the prompt)
ffmpeg -i ref.mp4 -vf "setpts=4*PTS" -af "atempo=0.5,atempo=0.5" ref_25pct.mp4
# crop the screen out of a phone-filmed "POV" post (measure x,y,w,h on a still first)
ffmpeg -i pov.mp4 -vf "crop=w:h:x:y,scale=1280:-2" screen_only.mp4
```

Labelled sheets from chosen times: `python .claude/skills/bequite-render-pipeline/scripts/contact_sheet.py sheet.png --video film.mp4 --every 1.0 --cols 6`.

## Previews for review (cheap, phone-sized)

```bash
# 720p at the MASTER's fps (don't drop 60 → 30 silently), a few MB per minute
ffmpeg -i master.mov -vf "scale=-2:720:flags=lanczos" -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p \
       -c:a aac -b:a 128k -movflags +faststart preview_720p.mp4
# one still / cover frame
ffmpeg -ss 31.6 -i master.mov -frames:v 1 cover_16x9.png
```

## Masters and mux

```bash
# silent picture + mastered mix → delivery master (grain-friendly settings fight banding)
ffmpeg -i film_picture.mov -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 15 -tune grain -pix_fmt yuv420p \
       -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart film_FINAL_16x9.mp4
# PNG sequence → video
ffmpeg -framerate 60 -i f_%05d.png -c:v libx264 -crf 15 -pix_fmt yuv420p film.mp4
```

Re-measure loudness on the encoded file after muxing (`qc_report.py` or `bequite-sound-voice` `master.py --measure-only`).

## Recuts per platform

**Best: a real recut** — re-render each scene at the new aspect from the engine with type re-laid out (`.claude/skills/bequite-motion-director/references/delivery-and-social.md`). ffmpeg covers the cases where framing allows it:

```bash
# 9:16 centre crop (only when the subject and text sit in the centre third; check stills first)
ffmpeg -i master.mp4 -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a copy film_9x16_crop.mp4
# moving crop (reframe follows the subject): x as an expression of time, e.g. pan between two positions
ffmpeg -i master.mp4 -vf "crop=ih*9/16:ih:'if(lt(t,10),200,if(lt(t,12),200+(t-10)*300,800))':0,scale=1080:1920" -c:a copy film_9x16_pan.mp4
# 1:1 and 4:5 centre crops
ffmpeg -i master.mp4 -vf "crop=ih:ih,scale=1080:1080" -c:a copy film_1x1.mp4
ffmpeg -i master.mp4 -vf "crop=ih*4/5:ih,scale=1080:1350" -c:a copy film_4x5.mp4
# "stacked" 9:16 fallback (only with the user's yes): film centred on the film's own stage colour; add hook/CTA in the engine or with drawtext
ffmpeg -i master.mp4 -filter_complex "[0:v]scale=1080:-2:flags=lanczos[f];color=c=0x141414:s=1080x1920:r=60[bg];[bg][f]overlay=(W-w)/2:(H-h)/2:shortest=1[v]" \
       -map "[v]" -map 0:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k film_9x16_stacked.mp4
```

Hook text and CTA pills on a stacked version use the film's accent, font and corner radius (a square box in a different colour broke the film's system in the worked example). `drawtext` needs `fontfile=` and avoids colons in text; prefer adding them in the engine.

## Captions

```bash
# side-car: deliver captions.srt next to the video (from bequite-sound-voice check_take.py --srt)
# burn-in (vertical versions; feeds autoplay muted) with libass, which shapes complex scripts
ffmpeg -i film_9x16.mp4 -vf "subtitles=captions.srt:force_style='FontName=<family>,FontSize=18,MarginV=120'" -c:a copy film_9x16_captions.mp4
```

For Arabic, use an Arabic-capable font in `force_style`; the subtitles filter ran with an Arabic line in this pack, but correct joining was **not visually verified** — check one burned frame. `drawtext` shapes Arabic only when ffmpeg was built with text-shaping support (UNVERIFIED per machine).

## Audio helpers

```bash
ffmpeg -i film.mp4 -vn -af "ebur128=peak=true" -f null -        # loudness + true peak (summary at the end)
ffmpeg -i film.mp4 -vn -ac 2 -ar 48000 audio.wav                 # extract audio
```

Avoid `-ss` before `-i` on some TTS WAVs (mis-seeks); decode and slice instead (the sound scripts do this).
