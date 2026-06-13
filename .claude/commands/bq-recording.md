---
description: Recording-to-Assets (C16). Turn long videos/lectures/webinars/meetings into structured knowledge — clean summary, chapter map, notes, action items, content-repurposing ideas, searchable knowledge pack. Transcript-first; extracts visual keyframes ONLY on meaningful change (no frame-by-frame, no duplicate talking-head screenshots). Workflow/spec-first — heavy tools are OPTIONAL and tool-dependent, none installed by default, no ToS-violating downloads.
---

# /bq-recording — video/recording → knowledge assets (C16)

Full spec: `docs/specs/RECORDING_TO_ASSETS.md`. Follows the 12-step contract. Skills: researcher + knowledge (C4 pack) + anti-hallucination + localization-rtl (Arabic). **Not a heavy runtime:** transcript-first; tools optional + tool-dependent; nothing installed by default; never download video in violation of platform terms — prefer user-provided transcript/video or official export.

## Syntax

```
/bq-recording "<YouTube URL | local video | audio | transcript file | subtitle file>"
```
Core use: a 6–8h lecture → clean summary + chapter map + study notes + action items + repurposing ideas + searchable pack (not just clips/captions).

## Steps (after contract steps 1–7)

1. **Source intake** — `SOURCE_INTAKE.md`: classify input (URL/video/audio/transcript/subtitle/meeting). **Transcript-first:** if subtitles/transcript exist, use them; if not, mark **transcription required** (optional tool: Whisper-class — tool-dependent, not installed). Never invent a transcript.
2. **Transcript** — `TRANSCRIPT.md`: clean filler, preserve meaning + order; align to timestamps.
3. **Visual extraction (the core IP)** — `VISUAL_KEYFRAMES.md` + `DEDUPLICATION_STRATEGY.md`: extract screenshots **only on meaningful visual change** (slide/keyframe detection), NOT frame-by-frame. Separate talking-head motion from real slide/visual change (perceptual-hash / scene-detection thresholds — optional tools: ffmpeg/scenedetect, tool-dependent). Deduplicate near-identical frames; attach timestamps; map frames → transcript sections. This is what prevents massive duplicated screenshots + token waste.
4. **Reconstruct** — `CHAPTER_MAP.md` + `KNOWLEDGE_NOTES.md` + `ACTION_ITEMS.md`: remove filler, keep real meaning + order, identify chapters/repeated points/examples/claims-needing-verification. Notes good enough to replace watching when appropriate. `CONTENT_REPURPOSING.md` (posts/shorts/threads from the material).
5. **Quality** — `OUTPUT_PACKAGE.md` + `QUALITY_REPORT.md` + `TOOL_DECISION.md`: source map (timestamp · transcript segment · keyframe-if-any · summary · confidence); mark low-confidence; **do not pretend to have watched the video if only the transcript was used**; distinguish personal learning notes from republishing (no improper use of copyrighted content). `NEXT_STEPS.md`.

## Tool note (candidates, never defaults; re-verify before use)

subtitle extraction · yt-dlp (only where legally appropriate + ToS-compliant) · ffmpeg · scene detection · keyframe extraction · OCR on slides · transcript alignment · Whisper-class transcription · local/cheap multimodal models (Gemini/Gemma-class) · perceptual hashing · screenshot-difference thresholds. **All optional + tool-dependent. Nothing installed by default.** Prefer user-provided transcript/official export.

## Writes

`.bequite/recordings/{SOURCE_INTAKE,TRANSCRIPT,CHAPTER_MAP,VISUAL_KEYFRAMES,DEDUPLICATION_STRATEGY,KNOWLEDGE_NOTES,ACTION_ITEMS,CONTENT_REPURPOSING,OUTPUT_PACKAGE,TOOL_DECISION,QUALITY_REPORT,NEXT_STEPS}.md` (first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical)

Required next: **C4 `/bq-knowledge build`** (turn notes into a searchable pack) or **C5 `/bq-course`** (recording → course outline). Set: C2 `/bq-writing-dna repurpose` (content from the material) · C1 `/bq-presentation` (notes → deck). Do not run yet: any frame-by-frame extraction or ToS-violating download — both are explicitly refused.
