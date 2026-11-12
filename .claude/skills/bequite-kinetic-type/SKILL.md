---
name: bequite-kinetic-type
description: 'Kinetic typography (text that moves) for films, promos, explainers, reels and animated web sections. Chooses a different treatment per line from its meaning (blur-in write-on, mask slide-up, directional smear, scale punch, word to icon swap, letter pop, swap in place, recolour sweep, inline icon, typing), owns reading-time and readability rules, and covers Arabic / RTL kinetic type (connected script, right-to-left reveals, kashida, mixed-direction lines, fonts). Implementable in After Effects, HTML/CSS/JS/GSAP, Remotion or any engine. Use whenever text has to animate, or when someone says the text animation feels cheap, static, monotone, too fast, too slow or "not smooth", or asks for Apple / Spotify / keynote-style type.'
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-kinetic-type — text is a graphic, not a caption

Each line gets a treatment chosen for **what it says**, it is written on the rhythm of the voice, it stays on screen long enough to read twice, and nothing is ever fully static. This skill owns the treatment chooser and the reading-time rules. Easing and smoothness live in `bequite-motion-director` (`.claude/skills/bequite-motion-director/references/motion-grammar.md`); engine set-up lives in `bequite-render-pipeline`.

## When to use / when not to use

**Use:** any moving text in a film or animated page — headlines, voice-over lines on screen, feature lists, UI callouts, end cards, Arabic or bilingual titles; diagnosing "cheap / monotone / not smooth / unreadable" type.

**Do not use:** static typography and type scales for UI (that is `bequite-ux-ui-designer` / `bequite-frontend-design-system`); subtitles/captions files (produced by `bequite-sound-voice`, styled here only if burned in).

## Choose a treatment per line (by meaning)

Never repeat the same treatment on consecutive lines. Details, parameters and per-engine notes: `references/toolbox.md`.

| The line… | Treatment |
|---|---|
| headline / turning point ("There's a better way.") | **blur-in write-on** by character: blur → sharp, small rise, scale 82 → 100, soft trailing bounce |
| calm editorial statement | **mask slide-up** by word from a baseline mask |
| energy, speed, "easy" | **directional smear**: word travels in with heavy horizontal blur, lands with 2–4 % overshoot |
| one emphasis word | **scale punch** (1.25 → 1) and/or a **recolour sweep** to the accent; failure = red + punch + tiny shake |
| a list or alternatives ("in size → in style") | **swap in place**: one slot, the line re-centres, the new word rides the glide |
| a concept that has an icon | **word → icon swap** (word collapses into a pill, morphs to an icon) or an **inline icon** that grows inside the sentence |
| product / brand moment | **letter pop** with a light shine; or a match cut from punctuation/shape into the logo |
| a chat, search or command | real **typing** with a caret |
| a visual property ("stretched", "square", "misaligned") | **do it to the word** (stretch it, box it, knock its letters out of line) |
| a quote or comment | left-aligned (start-aligned) like a real comment, written on the speech rhythm |
| names a place in the UI | underline/outline drawn while the word is written |

## Timing and readability (the single home for these numbers)

- **Write a sentence in ~0.5–0.65 s** (0.8–1.3 s felt slow; much faster felt rushed). Swaps glide in ~0.3–0.35 s.
- **Hold after it lands: max(1 s, 0.35 s × words + 0.5 s); × 1.5 when the line is not also spoken.** It must be readable twice. Single-word bursts may go to 5–7 frames per word (≈ 0.2 s), one word at a time only.
- Reading pace reference: ~160–180 words per minute for lines; ≤ 6 words on screen at once.
- **Write on the voice:** a word lands as it is spoken; keep the voice's pauses visible.
- **No empty waits** (an empty card, a pause before the key word) and **no monotone** (every line rising word by word was rejected as "not smooth").
- **Nothing static:** a slow push/drift (0.5–1 %, ~2 % scale over the hold) while a line holds.
- **Exits matter:** unwrite (units lift away into blur in reading order) or a motivated whip — never pop off on a hold.
- Text sits on empty space, never over a busy object; at phone size, nothing meaningful under ~24 px on a 1080p master (`.claude/skills/bequite-motion-director/references/style-system.md`).

## Type system rules

One family, two weights max; follow the font's own tracking guidance (many grotesks ≈ −2 % on display sizes; **never track Arabic**). Accent on ~5–8 % of the frame; red only for failure. "Wrong fonts" only where the meaning *is* wrong fonts. Overshoot a little on arrivals; springs only on things that land.

## Arabic / RTL

Connected scripts are animated by **word** or whole glyph cluster, never by single letter; reveals run right → left; no decorative kashida; mixed Arabic/Latin lines need bidi isolation. Full rules: `references/arabic-rtl.md` (pairs with `bequite-localization-rtl`).

## Building it

| Engine | Where |
|---|---|
| After Effects (script-built) | `type.jsx` in `bequite-render-pipeline` assets — function map in `references/engine-recipes.md` |
| Browser / HTML-to-video (Remotion, HyperFrames, frame capture) | `assets/kinetic.js` (dependency-free Web Animations API; RTL-safe) + `assets/kinetic-demo.html` |
| GSAP, CSS-only, Remotion `interpolate`/`spring`, Blender, Resolve | `references/engine-recipes.md` |

Study references at 4 fps contact sheets and write per line: entrance, emphasis, exit, duration (`.claude/skills/bequite-motion-director/references/studying-references.md`).

## Files this skill writes

Into the active work folder `.bequite/work/<id>/`: the **treatment column** of the beat sheet in `spec.md` (one treatment + timing per line), type tokens in `spec.md` § Motion DNA, test stills/contact sheets of type moments in `outputs/previews/`, and a note per type change in `log.md`.

## Evidence rule

A type pass is checked on stills/contact sheets at the beat times and on a phone-size preview; the commands and outputs go to `evidence.md`. Readability claims ("holds long enough") cite the formula result per line. Smoothness is the user's verdict in `review.md`, not an agent claim.
