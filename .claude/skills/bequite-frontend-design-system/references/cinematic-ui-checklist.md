# Cinematic / 3D / Animated UI Checklist

> Purpose: advanced visual experiences (motion, 3D, parallax, scroll storytelling) earn their place ONLY when the product needs them — never force cinematic or 3D on every project.

Sibling references: `design-dna.md` (brand identity), `motion-timing.md` (full timing tables), `accessibility-gates.md` (WCAG numbers), `product-type-rules.md` (marketing vs dashboard), `ai-slop-anti-patterns.md` (purple/pink gradient bans).

---

## 0. "Should we even do this?" gate

Answer ALL of these BEFORE building any cinematic / 3D / heavy-animated surface. If it does not earn its place, do not build it.

| Question | Pass condition | If fail |
|---|---|---|
| Business fit | The motion/3D advances a real goal (explain a product, build trust, demo a physical object). | Cut it. |
| Conversion impact | Animation helps the user act, or is neutral. It does not delay the CTA or hide content. | Cut or simplify. |
| User distraction risk | The user can still focus on the primary task / content. | Reduce scope to one accent. |
| Content readability | Text stays legible during and after motion; no contrast loss over moving backgrounds. | Static background; isolate motion. |
| Audience + context | Matches product type + Doctrine. Medical-adjacent / dashboard surfaces stay calm. | Drop cinematic on internal/critical screens. |
| Maintenance cost | The team can maintain the asset (poly budget, libraries, license). | Use a simpler technique. |

ClinicFlow application:
- Marketing landing: ONE orchestrated hero reveal + a calm scroll-triggered "how booking works" sequence. Justified — builds trust, explains the flow. Brand stays calm clinical teal; no purple/pink AI gradients.
- Staff dashboard: NO cinematic, NO 3D. Motion limited to functional feedback (100-150ms) and state transitions (200-300ms). Critical actions lean AAA (7:1 body / 4.5:1 large) and must never depend on animation to be usable.

---

## 1. Mandatory considerations before building

Tick every row. A blank row blocks the build.

| Area | Requirement |
|---|---|
| Performance — frame budget | Hold 60fps (16.7ms/frame); never drop below 30fps on target devices. |
| Performance — GPU | Composite on GPU. Animate `transform` + `opacity` only. No layout thrash. |
| Mobile fallback | Define a lighter or static path for phones / low-power devices. Test on real mid-range hardware. |
| `prefers-reduced-motion` | Mandatory `@media (prefers-reduced-motion: reduce)` fallback — remove or replace motion with an instant state. |
| Loading time | Heavy assets lazy-loaded; first contentful paint not blocked by 3D/video. |
| Accessibility | Motion is decorative, not informational. Focus order, contrast, and touch targets (44x44pt / 48x48dp / 24x24 CSS px floor, ≥8dp gap) hold during and after motion. |
| Content readability | Body ≥16px, measure 45-75ch, line-height 1.5-1.7 body / 1.1-1.2 headings. No text trapped behind moving layers. |
| Progressive enhancement | Base experience works with zero JS / zero WebGL. Motion/3D is added on top. |
| Fallback states | If WebGL / JS / video fails, a static poster + readable content remain. |

---

## 2. Motion craft rules

| Rule | Spec |
|---|---|
| Feedback timing | 100-150ms (hover, press, toggle). |
| State timing | 200-300ms (open/close, tab switch). |
| Layout timing | 300-500ms (large reveals, page-level). |
| Exit duration | ~75% of the entrance duration. |
| Easing | Exponential ease-out only — `cubic-bezier(0.16, 1, 0.3, 1)` family. NO bounce, NO elastic. |
| Animatable props | `transform` + `opacity` ONLY. Never animate `width` / `height` / `top` / `left` / `margin`. |
| Scroll triggers | Use Intersection Observer. Never raw scroll-event listeners. |
| `will-change` | Use sparingly, on the few elements about to animate; remove after. Not blanket. |
| Stagger budget | Total stagger ≤500ms; the sequence must not feel slow. |
| Reveal-safety | Never gate content visibility on a class-triggered transition — content is visible by default; motion enhances. If the class never lands, content still shows. |
| Images on hover | Never animate an `<img>` on hover (no scale/zoom that causes jank or layout shift). |

---

## 3. 3D specifics

| Rule | Spec |
|---|---|
| Lazy-load | Load heavy 3D assets only when in/near viewport; never block first paint. |
| Poly / texture cap | Cap polygon count and texture resolution to the target device budget; compress textures. |
| Static poster | Ship a static poster / fallback image that renders identically in layout before and if 3D fails. |
| Reduced motion | Under `prefers-reduced-motion: reduce`, offer a STILL render — no auto-rotate, no idle motion. |
| Mobile / low-power degrade | Provide a degrade path: lower LOD, fewer lights, or fall back to the static poster on weak GPUs. |
| Tool neutrality | Any named engine/library (Three.js, R3F, Spline, GLTF tooling, etc.) is a CANDIDATE — research, compare, justify, and pick per the 10 decision questions. Never auto-install. |

---

## 4. Performance budget alignment

Accessibility and performance pull in the SAME direction here:

- Respecting `prefers-reduced-motion` also removes GPU/CPU overhead — one rule serves both users and the frame budget.
- A static poster fallback is both the a11y path AND the low-power path.
- Lazy-loading heavy assets improves loading time AND keeps the main thread free for input.
- Animating only `transform` + `opacity` avoids layout/paint cost AND avoids jank that hurts users with vestibular sensitivity.

Treat the a11y fallback as the performance fallback. Build the lighter path first, layer the rich path on top.

---

## 5. Pre-ship checklist (tick before shipping ANY cinematic / 3D / animated surface)

- [ ] Section 0 gate passed — the experience earns its place (business fit + conversion + distraction + readability).
- [ ] 60fps held on a real mid-range mobile device; no drop below 30fps.
- [ ] Only `transform` + `opacity` animated; no `width`/`height`/`top`/`left`.
- [ ] Easing is exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)` family); no bounce/elastic.
- [ ] Timings within bands: 100-150 / 200-300 / 300-500ms; exit ≈75% of entrance.
- [ ] Scroll work uses Intersection Observer, not scroll listeners.
- [ ] `will-change` is targeted and removed after use; total stagger ≤500ms.
- [ ] `prefers-reduced-motion: reduce` fallback verified (motion removed/instant; 3D shows a still).
- [ ] Content is visible WITHOUT the animation (reveal-safety): disable JS and confirm the page reads.
- [ ] WebGL/video failure tested — static poster + readable content remain.
- [ ] No `<img>` animated on hover.
- [ ] Mobile / low-power degrade path tested (lower LOD or static poster).
- [ ] Heavy 3D/video lazy-loaded; first contentful paint not blocked.
- [ ] Text legibility holds during + after motion (body ≥16px, measure 45-75ch, contrast AA 4.5:1 / large 3:1; AAA where the Doctrine requires).
- [ ] Touch targets and focus order unchanged by motion (44x44pt / 48x48dp / 24x24 CSS px floor, ≥8dp gap).
- [ ] Brand identity preserved (no purple/pink AI gradient drift; ClinicFlow stays calm clinical teal).

---

> One well-orchestrated experience beats scattered animations everywhere.
