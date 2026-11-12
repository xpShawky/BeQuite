# AI video and image generation in a film

Most important first: **AI generation is for organic in-between shots, plates and look-dev — never for UI, text, logos, exact product geometry or anything the product claims.** Name the capability you need; pick a vendor per project after checking its *current* docs, price and commercial terms. Every paid generation is a ✋ stop (priced in `plan.md`, `RENDER_PLAN_APPROVED`, then a yes before spending).

## Capabilities (vendor-neutral)

| Capability | Use for | Typical limits |
|---|---|---|
| image → video / start-frame | animate a styleframe or render you control | short clips (seconds), drift after a few seconds |
| **start + end frame** ("frames to video") | bridge two frames you rendered yourself (best control) | lighting or perspective jumps between the two frames cause flicker |
| reference / "ingredients" consistency | keep one object or style across clips | consistency is never 100 % |
| video → video restyle | turn a plain 3D/graphic move into a photographic one, keep the motion | can change details you need fixed |
| HDR / high-bit-depth output (some vendors) | heavy grading/compositing | availability varies |
| image generation / editing | styleframes, start/end frames, background plates, props | text and logos still unreliable |
| vector output (some vendors) | icons and flat illustration as editable shapes | check licence of free tiers |
| text/image → 3D model | props and background objects | not for the hero product (topology, accuracy) |

## Rules

**Use AI for:** organic in-betweens that are expensive to simulate (cloth, liquids, particles, ribbons unfurling), bridges between two rendered frames, background plates, early look-dev and storyboards.

**Never for:** UI screens, logos, any text, exact device geometry, frame-accurate timing to music, people's likeness without consent.

**Hybrid recipe**
1. Design the start and end frames yourself (render, styleframe, or an edit of your own screenshot). AI only invents the motion between them.
2. Generate 6–10 variations at the cheapest/draft tier; re-render only the winner at high quality.
3. Bring the clip in as a **plate**, never as the final: stabilise, conform frame rate, track, then put the real UI, logo and type on top.
4. Grade it to the film's palette, match black levels, and lay the same grain over the whole film so AI and non-AI shots share one texture.
5. Keep AI shots short (1–3 s); cut before the model drifts or morphs. Add real imperfection (grain, slight distortion, matched motion blur).
6. Upscaling and frame interpolation are common sources of "AI-looking" artefacts; use sparingly.
7. Record every clip in the licence ledger (vendor, plan, date, terms URL).

**Disclosure:** platforms label realistic AI video and audio (some require it, some read embedded content credentials or watermarks automatically). Check each platform's current AI-label rule at M9; many generators embed an invisible watermark you cannot and should not strip.

## Landscape snapshot — dated, re-verify before use

As found in research notes dated 2026-09 to 2026-11 (`UNVERIFIED` unless re-checked in this session; lineups changed twice in Q3–Q4 2026):

- OpenAI's Sora video API and `sora-2*` models were removed on 2026-09-24 (official deprecations page). Do not plan around it.
- Google: Veo 3.1 *preview* models were removed from the Gemini API on 2026-10-22; the API points to a "Gemini Omni Flash" model (short clips, native audio, reference images, conversational edit/extend), with GA Veo 3.1 on Google's enterprise platform. The Imagen image models were replaced by the "Nano Banana" family. Google's consumer/pro video tool (Flow) had no official API found.
- Aggregators (several vendors in one subscription) and API hubs rotate their model lists (Kling, Seedance, Hailuo, Wan, Runway's own and third-party models were all listed at some point in 2026).
- Free tiers of many tools (video, voice, music, 3D) were **non-commercial** or watermarked; paid tiers usually added commercial rights. Open-weight models can carry licences that exclude regions or cap users.
- No model rendered small UI text or logos reliably.

The durable lesson: never hard-code a model. Write the capability in `plan.md`, list 2–3 candidate vendors with today's price and terms (with URLs and the date checked), and re-check at the moment of spending.
