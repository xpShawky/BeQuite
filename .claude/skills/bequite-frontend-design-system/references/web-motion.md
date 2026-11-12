# Web motion: cinematic scroll, depth and 3D that stay fast on phones

Load this for any site with scroll animation, pinned scenes, frame sequences, video, 3D or "Apple product page" storytelling. It pairs with `cinematic-ui-checklist.md` (when motion is worth it at all) and `visual-qa-checklist.md` (how to look at the result). It sets the targets and adds the `PERF_BUDGET_PASS` gate.

Sources: a real project post-mortem (a scroll-storytelling site that was slow on phones: about 3.3 MB before the first scroll, 95 unsized images, a scroll handler that re-measured 34 elements per event, a canvas loop that never stopped), plus web.dev Core Web Vitals, MDN scroll-driven animations, the View Transitions API, and the React Three Fiber performance guide. Library sizes are UNVERIFIED until checked on the registry in the session.

---

## 1. The motion grammar (what makes it feel premium)

Pick a few of these per site and keep them consistent. Taste goes in the `Motion taste profile` block of `.bequite/design/DESIGN_DNA.md` so it survives sessions.

| Pattern | What it is | Good for | Cheapest way to build |
|---|---|---|---|
| Scroll-scrubbed story | progress of the scroll drives a scene (product pours, rotates, assembles) | product launches, food/retail, hardware | pre-rendered frame sequence or a short-GOP video scrubbed on one canvas |
| Pinned chapter | a section sticks while its content changes | features one by one, before/after | CSS `position: sticky` + scroll-driven animation |
| Travelling object | one object carries across chapters (a light, a line, the product) | tying many features into one story | one fixed layer whose transform follows scroll progress |
| Cut-out depth | product cut-outs in front of / behind giant type | premium feel without 3D | layered PNG/AVIF cut-outs, transform + opacity only |
| Chapter colour handoff | each chapter owns a colour; header and accents follow | brands with several moods | CSS custom properties switched by scroll position |
| Write-on / mask reveal | logo or headline drawn or revealed | intros, section titles | SVG stroke or clip-path; ≤ 1.2 s, never hides the headline |
| Video inside type or logo | footage plays inside a mask | hero moments | one muted `playsinline` clip with a poster; mask stays still |
| Real 3D | a model the user can rotate or that reacts | configurators, real 3D products | WebGL/WebGPU only when a pre-render can't do it (see §4) |

Restraint rules: one hero effect per screen; motion explains the product, never decorates; content first. If removing the animation loses no meaning, it is decoration.

## 2. Choosing the technique (tool-neutral, cheapest first)

1. **CSS scroll-driven animations** (`animation-timeline: view()` / `scroll()`): Baseline in all major browsers since October 2026. No JavaScript, runs off the main thread. Keep a static fallback via `@supports`.
2. **View Transitions** for page and state changes (same-document is Baseline; cross-document support still varies).
3. **One coalesced scroll reader** (rAF + ticking flag; all reads, then all writes; sizes cached on resize) when progress must drive a canvas or many layers.
4. **A motion library** (GSAP + ScrollTrigger is now free and has official agent skills; Motion/Framer Motion in React) only when 1–3 are not enough. Justify it with the 10 decision questions and count its bytes.
5. **WebGL / WebGPU** (three.js, React Three Fiber, Spline exports) last. WebGPU still needs a WebGL2 fallback.

Smooth-scroll libraries (Lenis and similar) are optional; never make content unreadable without them.

## 3. Mobile performance budget (first load, Lighthouse mobile + a real mid-range phone)

| Metric | Budget |
|---|---|
| LCP / INP / CLS (75th percentile, mobile) | ≤ 2.5 s / ≤ 200 ms / ≤ 0.1 |
| TBT (lab) | ≤ 200 ms |
| Bytes before the first scroll | ≤ 500 KB compressed; whole page ≤ 1.5 MB before lazy sections |
| JavaScript (own + libraries) | ≤ 100 KB gzip for a motion landing page |
| Hero image / any other image | ≤ 150 KB / ≤ 120 KB on mobile, AVIF or WebP, ≤ 2× rendered size |
| Logos and icons | SVG, or ≤ 20 KB raster |
| Fonts | ≤ 2 families, ≤ 4 faces, ≤ 200 KB woff2; Arabic subset |
| Video | ≤ 1 MB mobile encode, poster required, `muted playsinline` |
| Scroll frame sequence | mobile ≤ 90 frames at ≤ 720p, ≤ 1.5 MB; load progressively, only near the viewport |
| 3D model | ≤ 1 MB (Draco/Meshopt + KTX2), ≤ 100k triangles, DPR ≤ 1.5 on mobile |
| Scrolling | ≥ 55 fps sustained, no frame > 50 ms; ≤ 4 ms of script per scroll frame |

## 4. Rules (each has a check)

**Loading**
1. Every `<img>` has `width`/`height` (or `aspect-ratio`) and `decoding="async"`; `loading="lazy"` unless in the first viewport. The LCP image gets `fetchpriority="high"` and is never lazy. *Check:* Lighthouse "explicit width and height" = 0 failures.
2. Responsive images: `srcset`/`sizes`, AVIF → WebP via `<picture>`. *Check:* Lighthouse "properly size images" passes.
3. No base64 images except tiny icons; never ship the same bytes twice. *Check:* HTML < 100 KB.
4. Fonts: no CSS `@import`, no JS-injected font links on the real page; preload the display face; `font-display: swap`. Font pickers and debug bars are prototype tools; remove them. *Check:* fonts requested in the first round trip.
5. Scripts `defer` / `type="module"`; no unused libraries. *Check:* DevTools Coverage, unused JS < 30%.
6. Video: poster, mobile encode, short GOP (`-g 1`–`6`) when scrubbed; no autoplay with reduced motion or Save-Data. *Check:* `ffprobe` keyframes, attribute grep.

**Animating**
7. Animate only `transform` and `opacity` (`filter` only on small static elements). Never `top/left/width/height/margin`, `mask-*` or `backdrop-filter` per frame. *Check:* Performance panel shows no Layout/Paint inside scroll frames.
8. Scroll-linking: CSS scroll timelines first, else one rAF-coalesced reader or a vetted library. Never one rAF per scroll event. *Check:* no "forced reflow" warnings.
9. Every scene and loop starts near the viewport and stops when out (IntersectionObserver). No forever `requestAnimationFrame`. *Check:* scrolled away, scripting ≈ 0.
10. Pinned sections use `svh` / `dvh`, not raw `vh`; resize handlers debounced and ignore URL-bar height changes.
11. Many moving pieces: cap counts on mobile, bake shadows into sprites (no `drop-shadow` on dozens of images), or draw the scene on one canvas.
12. `will-change` only on what is animating now; remove it after.

**Content first**
13. Content is readable without JS and before any intro finishes. Intros ≤ 1.2 s, skippable, never hide the headline or CTA.
14. `prefers-reduced-motion: reduce` handled in CSS **and** JS: scrubs jump to the end state, loops stop, video shows its poster.

**Device tiers** (choose at runtime with cheap signals, no fingerprinting)
15. **full** (desktop / high-end) · **lite** (phones: fewer pieces, smaller frame sets, no backdrop blur, pre-rendered depth instead of WebGL) · **static** (reduced motion, Save-Data, `deviceMemory ≤ 2` or `hardwareConcurrency ≤ 4`: posters and simple fades). Lite is the default on phones.
16. A "3D look" defaults to pre-rendered depth (Blender / After Effects / AI video → frame sequence or cut-outs). Runtime 3D needs a reason, a poster, lazy init, a paused render loop off-screen, and a static fallback.

**Done means measured**
17. **Performance pass** before "done": Lighthouse mobile summary (LCP / CLS / TBT + total bytes), a Performance trace at CPU 4× while scrolling every scrubbed section, and one real phone, or an explicit `UNVERIFIED: no device`. Record it in the work's `evidence.md` and the Performance table of `.bequite/audits/VISUAL_QA_REPORT.md`; set `PERF_BUDGET_PASS` in the work's `gates.md`.
18. Test the link the client will actually open (host, tunnel or preview URL) with compression and caching on, not only `localhost`.
19. A user saying "it's slow on my phone" is a bug: log it in the work's `log.md`, fix it with `/bq-fix`, and add the prevention rule to `MISTAKE_MEMORY.md`.

## 5. Tools to see and measure (any available tier)

Built-in browser pane (local previews, screenshots, resize to a phone viewport) · Claude in Chrome (real sites, console, network, GIF recording of the scroll) · Lighthouse CLI or DevTools · computer use for a native browser or device mirror. Prefer what is already available; never auto-install.
