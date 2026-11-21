# Route G: a multimodal model in the user's browser

Claude cannot hear or watch. Gemini takes video as input: Google's docs say it samples 1 frame per second by default together with the audio track and per-second timestamps, and warn that rapid motion or quick scene changes can be missed. Run in the user's own browser, the video streams from YouTube to Google, not to this machine, and costs no Claude tokens beyond the prompt and the answer.

Ask first, once per machine: which browser and profile, which Google account, and whether this route is allowed. Record the answers and the test result in `.bequite/state/CAPABILITIES.md`. On another person's machine nothing here is assumed.

## G1: Google AI Studio (aistudio.google.com)

1. New chat. Pick the strongest model not marked "Paid" (2026-11-21: `gemini-4-neon`). Thinking: High.
2. Turn **Grounding with Google Search off** for the prompt, so the answer can only come from the video.
3. Prompt box `+` → "YouTube Video" → paste the URL. The dialog also offers Start Time, End Time, FPS (default 1) and "Agentic video understanding". Use a clip range for a long video when only part matters; raise FPS only for fast-cut questions.
4. The attachment shows its token cost (measured: 23,446 for 224 s; 130,021 for 1,238 s; about 105 per second).
5. Paste a template below, run (Ctrl+Enter), read the answer from the page text.
- Free-tier limits from the docs: public YouTube videos only; up to 8 hours of YouTube video per day.
- Seen: "Model isn't available right now" on a long video: rerun once a minute later.
- Chats may be "Temporary" (not saved). Do not enable Drive or claim API credits without the user's yes.

## G2: Gemini app (gemini.google.com)

Paste "Watch this video: URL" plus the template. Accepts several URLs in one message. Measured differences: it misread a filename the AI Studio model read exactly, called a logo frame "blank black", and in a three-video T4 table it left every timestamp cell empty. Use G2 for gist and structure, or when G1 is out of quota; check exact values. The app's sidebar shows the user's other chats: read only the response element, never record the sidebar.

## The watch-or-transcript test (once per route and model)

Ask about things only the picture shows, at moments the speech does not describe: a filename on a timeline, the colour of an object, the end card, a value under the cursor. Fetch those moments locally (L2b, 3 s at 720p) and compare. Pass: matches. Fail: that route reads the transcript only; use it for words, never for visuals.

Results on the owner's machine (2026-11-21):

| Route | Model | Score | Notes |
|---|---|---|---|
| G1 AI Studio | gemini-4-neon | 5 of 5 exact | read a 75-character filename never spoken; wrote UNSURE where the frame was unreadable; times within 1 s |
| G2 Gemini app | "Neon" | 3 of 5 exact, 1 misread, 1 wrong | still clearly watches (described unspoken visuals) |

## Templates (copy, fill the brackets)

**T1 Full breakdown.** "Watch this whole video. Report with a timestamp on every point: 1) what it is about in two lines; 2) the first 3 seconds, word for word (in the original language, then English) and what is on screen; 3) the structure as timestamped beats; 4) every on-screen text with its time (keep the original script); 5) visuals: shot sizes, camera moves, colour, graphics; 6) editing: number of cuts, average shot length, transitions used and where; 7) sound: music style and energy changes, effects, silence, and which cuts land on beats; 8) the call to action; 9) three things worth copying and three to avoid. If you are not sure about something, write UNSURE."

**T2 Technique from a tutorial.** "In this tutorial, extract the exact steps to make [the effect]: for each step the timestamp, the menu path or shortcut, every value or setting shown on screen, and what changes in the picture. Do not fill gaps from general knowledge; write NOT SHOWN where the video does not show it. End with a compact table: effect, property, keyframe values, easing."

**T3 Format measurement.** "Measure this video as data: total length; time of every cut (list); shot size per shot; on-screen caption style (case, position, words per caption); where the hook ends; music tempo if you can tell; how the video ends. Numbers and timestamps only."

**T4 Research across videos.** "Watch these videos: [1..5]. List every claim about [topic] with the video number, the speaker, the timestamp and a short quote. Then: where they agree, where they contradict, and what evidence each gives (platform statement with source shown, their own data with numbers shown, or nothing). If you are not sure, write UNSURE."

**T5 Ad breakdown.** "Break down this ad: the offer, the hook (first 2 s), the proof shown, the call to action, length, format, product shots with timestamps, the text on screen, and the emotional turn."

**Watch test.** "Answer only from what you see in the attached video's picture, not from its speech. If you cannot see it, write UNSURE. Give a timestamp for each answer. 1) At [t1], what exactly is shown [where]? 2) At [t2], what text is written on [element]? ... 5) Describe the very last frame."

## Rules

- Gemini's answer is a claim. Relay it as "Gemini (route G1) says", check what you act on, mark the rest `UNVERIFIED:`.
- Measured on this machine: spoken values came back exact; unspoken on-screen values 7 of 8 exact in one tutorial (one wrong). So: spoken values need a caption check, on-screen values need a frame check.
- Route G does not replace measurement: it wrote UNSURE for cut counts and misjudged pause lengths. Use L3 `--study` for numbers.
