# Design DNA — worked example: ClinicFlow

> Purpose: a fully filled, ship-ready Design DNA for the **ClinicFlow marketing landing page**, used as a reference pattern for the `bequite-frontend-design-system` skill. The staff dashboard inherits this DNA but carries its own page-level overrides (see § 19).

**Status: locked** · Version 1.0 · Scope: `clinicflow.com` marketing landing (public)
Doctrine: `default-web-saas` · WCAG target: **AA** (marketing) — see sibling `../references/design-continuity-checklist.md` for the gate this DNA is checked against.

Related files:
- `../SKILL.md` — owning skill
- `../references/design-continuity-checklist.md` — the gate every section is verified against
- `./section-map-example.md` — the section map this DNA is applied across (hero → footer)
- `../references/product-type-rules.md` — the product-type row this DNA follows
- (in a real project, the values below export to the project's own `tokens.css`)

---

## 1. Product identity

| Field | Value |
|---|---|
| Product | ClinicFlow — clinic booking platform |
| This surface | Marketing landing page (public, conversion-focused) |
| Sibling surface | Staff dashboard (internal, task-focused) — own overrides in § 19 |
| Product type | SaaS landing (marketing) |
| Audience | Clinic owners, practice managers, front-desk decision-makers |
| Primary job-to-be-done | "Show me this is a calm, trustworthy system my staff can run without training." |
| Brand adjectives | trustworthy · calm · efficient |
| Anti-adjectives | hype-y · playful · futuristic · clinical-cold |
| Conversion goal | Book a demo / start free trial |

---

## 2. Voice and tone

| Trait | Rule |
|---|---|
| Reading level | Plain, grade 8–9. No jargon stacks ("HIPAA-aligned scheduling middleware"). |
| Sentence shape | Short. One idea per sentence. Active voice. |
| Pronoun | "your clinic", "your front desk" — second person. |
| Forbidden words | revolutionary, seamless, cutting-edge, unleash, supercharge, game-changing, AI-powered (as a headline) |
| Headline style | Sentence case. Outcome-led ("Fewer no-shows. Calmer front desk."). |
| Numbers | Concrete and earned ("Reminders cut no-shows ~30%* — *based on pilot clinics"). No invented precision. |

---

## 3. Color system (OKLCH)

Brand core is a **calm clinical teal**. Backgrounds are **tinted neutrals** (a hair of teal in the gray), never pure `#FFFFFF` slabs. **No purple/pink AI gradients anywhere.**

### 3.1 Brand teal ramp

| Token | OKLCH | Use | Paired on-color |
|---|---|---|---|
| `--teal-50` | `oklch(0.97 0.02 195)` | tint wash, hover bg | `--ink-900` |
| `--teal-100` | `oklch(0.93 0.04 195)` | subtle fills, chips | `--ink-900` |
| `--teal-200` | `oklch(0.86 0.07 194)` | borders on tint | `--ink-900` |
| `--teal-500` | `oklch(0.62 0.12 192)` | accents, icons, links | `--paper-0` |
| `--teal-600` | `oklch(0.55 0.12 192)` | **primary brand / primary button** | `--paper-0` |
| `--teal-700` | `oklch(0.47 0.11 192)` | button hover, pressed | `--paper-0` |
| `--teal-800` | `oklch(0.39 0.09 193)` | deep accent, dark band | `--paper-0` |

### 3.2 Tinted neutrals

| Token | OKLCH | Use | Paired on-color |
|---|---|---|---|
| `--paper-0` | `oklch(0.99 0.004 195)` | page background (teal-tinted white) | `--ink-900` |
| `--surface-1` | `oklch(0.975 0.006 195)` | cards, raised surfaces | `--ink-900` |
| `--surface-2` | `oklch(0.95 0.008 195)` | alt section band | `--ink-900` |
| `--line` | `oklch(0.90 0.01 195)` | hairline borders / dividers | n/a |
| `--ink-500` | `oklch(0.55 0.015 200)` | secondary text (on paper only) | n/a |
| `--ink-700` | `oklch(0.40 0.02 205)` | strong secondary text | n/a |
| `--ink-900` | `oklch(0.22 0.02 210)` | primary body + headings | n/a |

### 3.3 Semantic

| Token | OKLCH | Use |
|---|---|---|
| `--success` | `oklch(0.58 0.11 150)` | confirmed, available |
| `--warn` | `oklch(0.74 0.13 75)` | attention (rare on marketing) |
| `--danger` | `oklch(0.55 0.16 27)` | errors only |
| `--focus-ring` | `oklch(0.55 0.12 192)` | keyboard focus = teal-600, 2px + 2px offset |

### 3.4 Contrast proof (WCAG 2.2 AA — see § 13)

| Pair | Ratio | Floor | Pass |
|---|---|---|---|
| `--ink-900` on `--paper-0` | ~13.8:1 | 4.5:1 body | yes |
| `--ink-700` on `--paper-0` | ~8.6:1 | 4.5:1 body | yes |
| `--ink-500` on `--paper-0` | ~4.6:1 | 4.5:1 body | yes (body floor only) |
| `--paper-0` on `--teal-600` (button text) | ~5.1:1 | 4.5:1 body | yes |
| `--teal-600` link on `--paper-0` | ~4.7:1 | 4.5:1 body | yes |
| `--focus-ring` vs adjacent | ~3.2:1 | 3:1 UI | yes |

> Rule: `--ink-500` is for body on paper backgrounds ONLY. **Never gray text on teal.** On any teal fill, text is `--paper-0` or `--ink-900` — never a mid-gray (forbidden, § 18).

---

## 4. Typography

Fonts are deliberate picks with recorded reasons — **not "Inter by default"** (Iron Law / Doctrine).

| Role | Font | Recorded reason |
|---|---|---|
| Display / headings | **Fraunces** (humanist soft-serif, optical sizing) | Adds warmth + character so "calm + trustworthy" reads human, not sterile-clinical. Optical sizing keeps large headings friendly. Variable font = one file. |
| Body / UI | **Public Sans** (US gov humanist sans) | Clean, highly legible, neutral, open-license, built for civic/medical-adjacent readability. Chosen over Inter because it pairs warmer with Fraunces and avoids the generic-AI-landing look. |
| Numeric / data | Public Sans `tnum` (tabular figures) | Aligns prices, stats, demo times. |

### 4.1 Type scale (rem · 1rem = 16px)

| Token | Size | Line-height | Weight | Font | Use |
|---|---|---|---|---|---|
| `--fs-display` | 3.5rem | 1.05 | 560 | Fraunces | hero H1 |
| `--fs-h2` | 2.25rem | 1.15 | 540 | Fraunces | section titles |
| `--fs-h3` | 1.5rem | 1.2 | 600 | Public Sans | card titles |
| `--fs-lead` | 1.25rem | 1.55 | 400 | Public Sans | hero subhead |
| `--fs-body` | 1.0625rem (17px) | 1.6 | 400 | Public Sans | body (≥16px floor) |
| `--fs-small` | 0.9375rem (15px) | 1.5 | 400 | Public Sans | captions, footnotes |
| `--fs-label` | 0.8125rem (13px) | 1.4 | 600 | Public Sans | eyebrow labels |

### 4.2 Type rules

- Body ≥ 16px everywhere. `--fs-body` is 17px.
- Headings line-height 1.1–1.2; body 1.5–1.7.
- Measure: body 60ch, lead 50ch — within 45–75ch.
- All-caps **only** on eyebrow labels (≤ 4 words) at `letter-spacing: 0.08em` (within 0.05–0.12em). **Feature/card titles are never all-caps** (forbidden, § 18).
- No wide tracking on body or headings (drift symptom).

---

## 5. Spacing scale (4 / 8 pt)

| Token | px | Use |
|---|---|---|
| `--s-1` | 4 | icon-to-label gap |
| `--s-2` | 8 | inline gaps, chip padding |
| `--s-3` | 12 | tight stack |
| `--s-4` | 16 | default element gap |
| `--s-6` | 24 | card padding |
| `--s-8` | 32 | block gap |
| `--s-12` | 48 | sub-section gap |
| `--s-16` | 64 | section padding (mobile) |
| `--s-24` | 96 | section padding (desktop) |

> All spacing snaps to the 4/8 grid. No `13px`, `27px`, `arbitrary` values (drift symptom).

---

## 6. Radius scale

| Token | px | Use |
|---|---|---|
| `--r-sm` | 8 | inputs, chips, small buttons |
| `--r-md` | 12 | buttons, cards |
| `--r-lg` | 16 | feature cards, media |
| `--r-xl` | 24 | hero media, modal |
| `--r-pill` | 999 | tags, avatars |

> One radius family. Calm = consistent corners. No mixing sharp + pill in the same group.

---

## 7. Elevation / shadow

| Token | Value | Use |
|---|---|---|
| `--e-0` | none | flat sections on `--paper-0` |
| `--e-1` | `0 1px 2px oklch(0.22 0.02 210 / 0.06)` | resting cards |
| `--e-2` | `0 4px 12px oklch(0.22 0.02 210 / 0.08)` | raised / hover |
| `--e-focus` | `0 0 0 2px --paper-0, 0 0 0 4px --focus-ring` | keyboard focus |

> Shadows are tinted with `--ink-900` hue (not pure black) so they sit calm, not harsh.

---

## 8. Borders / dividers

- Hairlines: `1px solid --line`.
- Section separation prefers **tinted background bands** (`--surface-2`) over heavy rules.
- No double borders, no border + shadow + tint stacked on one card (busy = drift).

---

## 9. Iconography

| Field | Value |
|---|---|
| Set | Lucide (single weight, 1.75px stroke) — candidate chosen for calm, uniform line weight |
| Size | 20px inline / 24px feature |
| Color | `--teal-600` on paper; `--paper-0` on teal |
| Rule | Line icons only. **No emoji as bullets or feature markers** (forbidden, § 18). No mixed icon sets. |

---

## 10. Imagery / illustration

- Photography: real clinic environments, soft natural light, calm. No stock "doctor pointing at floating UI".
- Tint overlay allowed: `--teal-800` at ≤ 12% for cohesion.
- Illustration: flat, 2-tone (teal + ink), thin line. No 3D blobs, no gradient mesh.
- **Never animate `<img>` on hover** (zoom/scale) — jitter reads anxious, contradicts "calm" (forbidden, § 18).

---

## 11. Components — canonical patterns

| Component | Spec |
|---|---|
| Primary button | `--teal-600` bg, `--paper-0` text, `--r-md`, 16px/24px padding, hover `--teal-700`, focus `--e-focus` |
| Secondary button | transparent bg, `--teal-600` text + 1.5px `--teal-600` border, hover `--teal-50` bg |
| Eyebrow label | `--fs-label`, all-caps, `0.08em`, `--teal-700`, ≤ 4 words |
| Feature card | `--surface-1`, `--r-lg`, `--s-6` padding, `--e-1`, icon + H3 (sentence case) + body |
| Pricing card | **single flat card per tier on a shared band** — NOT a card inside a card (forbidden, § 18) |
| Input | `--r-sm`, `--line` border, focus → `--focus-ring` + `--e-focus` |
| Touch targets | ≥ 44×44pt (Apple HIG) / 48×48dp (Android); never below WCAG 24×24px floor; ≥ 8dp spacing between targets |

---

## 12. Motion

| Rule | Value |
|---|---|
| Feedback (hover, press) | 100–150ms |
| State change (toggle, reveal) | 200–300ms |
| Layout / section reveal | 300–500ms |
| Exit duration | ~75% of entrance |
| Easing | exponential ease-out `cubic-bezier(0.16, 1, 0.3, 1)` family |
| Animate | `transform` + `opacity` only |
| Banned | bounce, elastic, overshoot (contradicts "calm") |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` → all transitions ≤ 0.01ms, no transform reveals |
| Reveal safety | content fully visible if JS/animation fails (no `opacity:0` left stuck) |
| Image hover | none — never scale/zoom `<img>` |

---

## 13. Accessibility target (WCAG 2.2 AA)

| Requirement | Floor | This DNA |
|---|---|---|
| Body text contrast | 4.5:1 | met (§ 3.4) |
| Large text (≥18px / 14px bold) | 3:1 | met |
| UI components / focus | 3:1 | met (focus ring) |
| Touch targets | 24×24px CSS floor; 44pt/48dp targets | met (§ 11) |
| Focus visible | always | `--e-focus` 2px + 2px offset |
| Reduced motion | mandatory fallback | § 12 |

> Marketing surface targets **AA**. The dashboard leans **AAA (7:1 body / 4.5:1 large)** on critical actions — see § 19.

---

## 14. Layout / grid

| Field | Value |
|---|---|
| Container max | 1200px, `--s-6` side gutters mobile |
| Grid | 12-col, 24px gutter desktop |
| Section rhythm | `--s-24` (96px) top/bottom desktop, `--s-16` (64px) mobile |
| Breakpoints | 640 / 768 / 1024 / 1280 |
| Section alternation | `--paper-0` → `--surface-2` → `--paper-0` band rhythm |

---

## 15. Section inventory (hero → footer)

| # | Section | Background | Continuity anchor |
|---|---|---|---|
| 1 | Hero | `--paper-0` | Fraunces H1, teal-600 primary CTA |
| 2 | Trust bar (clinic logos) | `--surface-2` | grayscale logos, uniform height |
| 3 | Problem ("no-show chaos") | `--paper-0` | sentence-case H2, 60ch body |
| 4 | Features (3-up) | `--surface-2` | feature cards, Lucide icons, sentence-case H3 |
| 5 | How it works (3 steps) | `--paper-0` | numbered, tabular figures |
| 6 | Pricing (3 tiers) | `--surface-2` | flat single cards, no nesting |
| 7 | Testimonial | `--paper-0` | one clinic, real photo |
| 8 | Final CTA | `--teal-800` band | `--paper-0` text, no gray-on-teal |
| 9 | Footer | `--surface-2` | hairline dividers, `--fs-small` |

> Drift check: every section reuses the same tokens above. Middle sections (4–6) are the highest drift risk — verified against `../references/design-continuity-checklist.md`.

---

## 16. Continuity anchors (must repeat in every section)

1. Same teal ramp — accents are always `--teal-500/600/700`, never a new hue.
2. Same two fonts — Fraunces (display) + Public Sans (everything else).
3. Same 4/8 spacing and `--r-md`/`--r-lg` radii.
4. Same button styles (§ 11) — no bespoke per-section buttons.
5. Sentence-case headings throughout.
6. Tinted neutrals — no pure-white slab appears mid-page.

---

## 17. Allowed patterns

- Tinted-neutral band alternation for section rhythm.
- Teal accent on icons, links, primary CTA, eyebrow labels.
- Soft tinted shadows (`--e-1` / `--e-2`).
- Flat single-tier pricing cards on a shared band.
- All-caps eyebrow labels (≤ 4 words, 0.08em).
- Calm fade + small `translateY` reveals (transform/opacity, ease-out).

---

## 18. Forbidden patterns (calm clinical product)

| Forbidden | Why it breaks ClinicFlow |
|---|---|
| Purple→pink AI gradients | Reads "generic AI demo", destroys clinical trust |
| Nested pricing cards (card-in-card) | Visual noise; contradicts "calm + efficient" |
| ALL-CAPS feature/card titles | Shouty; all-caps reserved for ≤4-word eyebrows |
| Emoji bullets / emoji feature markers | Unprofessional for a medical-adjacent product |
| Gray text on teal fills | Fails contrast + reads muddy; use `--paper-0` or `--ink-900` |
| Animating `<img>` on hover | Jitter contradicts "calm"; never |
| Bounce / elastic motion | Playful tone, off-brand |
| Wide letter-spacing on body/headings | Classic AI-drift symptom |
| Arbitrary spacing (13px, 27px) | Breaks the 4/8 grid |
| Pure `#FFFFFF` slab backgrounds | Use tinted `--paper-0` for warmth |
| New accent hue per section | Identity loss = the core problem this DNA solves |

---

## 19. Dashboard overrides (sibling surface — separate locked DNA expected)

The staff dashboard inherits this DNA's tokens but applies page-level overrides. Recorded here so the two surfaces stay coherent without copy-pasting hype tone into an internal tool.

| Aspect | Marketing (this file) | Staff dashboard override |
|---|---|---|
| Density | airy, large rhythm | compact (`--s-3`/`--s-4` rhythm, denser tables) |
| Type scale | display-led (Fraunces 3.5rem) | utility-led; Fraunces only on page titles, Public Sans dominant |
| Contrast target | AA | **AAA on critical actions** (confirm/cancel booking): body 7:1, large 4.5:1 |
| Color use | teal as accent + brand | teal reserved for primary actions + active nav; status uses semantic ramp |
| Motion | reveal-on-scroll allowed | feedback-only (100–150ms); no scroll reveals in a work tool |
| Imagery | clinic photography | none — data + icons only |
| Touch targets | 44pt | 44pt minimum, 48dp on tablet check-in kiosks |

> Action: the dashboard ships its own `design-dna.md` at its surface, referencing this file as parent. This file does **not** govern dashboard layout.

---

_Locked. Changes require a new version bump and re-running the Design Continuity Gate against all sections in § 15._
