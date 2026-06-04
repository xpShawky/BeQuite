# Design DNA — Cadence (running-coach app landing)

**Status: locked** · Product type: SaaS landing (mobile-app-adjacent) · WCAG target: AA

The gate checks every section of `before-drifted.html` / `after-fixed.html` against this file.

## 1. Identity
- **Product:** Cadence — a running-coach app for amateurs training toward a race.
- **Audience:** weekend runners; calm, time-poor, slightly intimidated by "elite" fitness branding.
- **Emotional goal:** grounded + motivating, NOT hype. "You've got a plan; just run."
- **Brand adjectives:** grounded · steady · warm.
- **Scene sentence:** a runner lacing up at dawn on a quiet street, calm and focused before a long run.

## 2. Color (the contract)
Warm clay primary on warm tinted-neutral paper. **No purple/pink AI gradients.** Gray text never sits on the clay.

| Token | Value | Use | On-color |
|---|---|---|---|
| `--clay` | `#b14a2e` | primary brand / CTA / links | `--paper` |
| `--clay-700` | `#8f3a22` | hover/pressed | `--paper` |
| `--paper` | `#faf6f1` | page background (warm tinted white) | `--ink` |
| `--surface` | `#f3ece3` | alt section band / cards | `--ink` |
| `--ink` | `#2b2622` | body + headings | — |
| `--ink-soft` | `#6f655d` | secondary text **on paper/surface only** (≥4.5:1) | — |
| `--line` | `#e4d9cc` | hairline borders | — |

## 3. Typography
- **Display:** Fraunces (humanist soft-serif) — warmth so "grounded" reads human, not clinical. **Recorded reason; not Inter-by-default.**
- **Body:** Public Sans — clean, legible, neutral, pairs warm with Fraunces.
- Body ≥ 16px; measure 45–75ch; headings line-height 1.1–1.2, body 1.5–1.7.
- **All-caps only on ≤4-word labels at 0.04–0.08em tracking.** Never on multi-word titles. Never positive tracking on body.
- Headings are **sentence case**.

## 4. Spacing — 4/8 scale
`4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96`. Rhythm by contrast: 8–12 within a group, 48–96 between sections. No arbitrary values.

## 5. Radius
`--r-sm 8` / `--r-md 12` (cards/buttons) / `--r-lg 16`. **No radius ≥ 32px on cards.**

## 6. Components
- One button system (clay fill, `--paper` text, `--r-md`). One card depth — **no card-in-card**.
- Section format **varies** — not every section is a 3-up icon card grid.
- Real states; verb+object CTAs.

## 7. Motion
Exponential ease-out, no bounce/elastic; transform+opacity only; mandatory `prefers-reduced-motion`. (Demo is static-first, so this is mostly N/A but must not introduce noisy motion.)

## 8. Forbidden (the drift tells this product must never show)
purple/pink gradients · ALL-CAPS multi-word titles · wide letter-spacing on titles/body · gray-on-clay text · nested cards · identical generic 3-card grids · `border-radius ≥ 32px` on cards · arbitrary spacing · numbered `01/02/03` eyebrow markers as decoration · text overflow.
