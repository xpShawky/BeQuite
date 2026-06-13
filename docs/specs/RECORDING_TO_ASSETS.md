# Recording-to-Assets — `/bq-recording` (C16) — alpha.24

Turn long videos/lectures/webinars/meetings into structured knowledge. Command: `bq-recording.md`. Skills: researcher + (C4 knowledge) + anti-hallucination + localization-rtl. **Workflow/spec-first; heavy tools OPTIONAL + tool-dependent; nothing installed by default; no ToS-violating downloads.**

## The core problem it solves

A 6–8h video → clean summary + chapter map + study notes + action items + repurposing ideas + searchable pack (not just short clips/captions). The hard part is **visual extraction without waste**: frames repeat, talking-head motion creates false "changes," and frame-by-frame extraction explodes tokens + storage.

## Outputs — `.bequite/recordings/`

SOURCE_INTAKE · TRANSCRIPT · CHAPTER_MAP · VISUAL_KEYFRAMES · DEDUPLICATION_STRATEGY · KNOWLEDGE_NOTES · ACTION_ITEMS · CONTENT_REPURPOSING · OUTPUT_PACKAGE · TOOL_DECISION · QUALITY_REPORT · NEXT_STEPS.

## Workflow

1. **Source intake** — URL/video/audio/transcript/subtitle/meeting. **Transcript-first:** use subtitles/transcript if present; else mark *transcription required* (optional Whisper-class tool); never invent.
2. **Visual extraction** — screenshots ONLY on meaningful visual change (slide/keyframe detection); separate talking-head motion from real change (perceptual hashing / scene-detection thresholds — optional ffmpeg/scenedetect); dedupe near-identical frames; timestamps; map frames→transcript.
3. **Reconstruct** — remove filler, preserve meaning + order; chapters; repeated points; examples; claims-needing-verification; notes good enough to replace watching when appropriate.
4. **Quality** — source map (timestamp · segment · keyframe-if-any · summary · confidence); mark low-confidence; **never claim to have watched the video if only the transcript was used**; distinguish personal learning notes from republishing (no improper copyrighted-content use).

## Tools (candidates, never defaults; re-verify; nothing installed)

subtitle extraction · yt-dlp (legal + ToS-compliant only) · ffmpeg · scene detection · keyframe extraction · slide OCR · transcript alignment · Whisper-class transcription · local/cheap multimodal (Gemini/Gemma-class) · perceptual hashing · screenshot-diff thresholds. **No heavy dependency by default; prefer user-provided transcript/official export.** **Built alpha.24 — NOT live-tested.**
