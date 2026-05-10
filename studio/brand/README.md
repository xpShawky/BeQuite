# BeQuite Brand System

> Single source of truth for visual design across all three Studio surfaces (`marketing`, `dashboard`, `api`).

## Color palette (gold + black)

The brand is **black-first with gold as the only accent**. Yellow is never the background.

| Token | Hex | Use |
|---|---|---|
| `--gold-primary` | `#E5B547` | Logo mark, primary CTA, character highlights |
| `--gold-bright` | `#F2C76A` | Hover state, active glints |
| `--gold-deep` | `#B8861E` | Pressed state, deep accents |
| `--black-pure` | `#000000` | Primary background |
| `--black-stage` | `#0A0A0A` | Cards, lifted surfaces |
| `--black-velvet` | `#141414` | Hover surfaces |
| `--silver` | `#D4D4D4` | Wordmark, secondary text |
| `--white-pure` | `#FFFFFF` | Hero text peaks |

Full token set: `tokens.css` + machine-readable `tokens.json`.

## Type

- **Display + body:** Geist (Vercel; Apple-inspired without the SF-Pro license issue).
- **Mono:** Geist Mono (pairs with the terminal-prompt mark in the logo).
- **Type scale is responsive-clamped** — see `tokens.css` `--text-*`.

## Motion

- **Easing:** `--ease-cinematic` (Apple-flavored ease-out: `cubic-bezier(0.16, 1, 0.3, 1)`).
- **Never bouncy / elastic / back** (Doctrine `default-web-saas` Rule 6).
- **Reduced-motion respected** — all durations zero when `prefers-reduced-motion: reduce`.

## Logo + character

| Asset | File | Use |
|---|---|---|
| Hero zen + mark | `raw/01-hero-zen-with-mark.png` | Marketing hero composition |
| Character zen pose | `raw/02-character-zen.png` | Idle / loading state |
| Character pointing pose | `raw/03-character-pointing.png` | "Look here" / call-to-attention |
| Hero wordmark + character | `raw/04-hero-wordmark-character.png` | Above-the-fold marketing hero alt |
| Logo horizontal lockup | `raw/05-logo-horizontal.png` | Nav bars, footers, favicons |
| Studio dashboard mock | `raw/06-studio-dashboard-mock.png` | Information-architecture target for `studio/dashboard/` |

## Usage rules

1. **Never put gold on gold.** Gold is always over black.
2. **Never put silver text on gold.** Silver is for over-black readability; on gold use black.
3. **The astronaut character is the personality anchor** — every chapter should feature it (zen pose during quiet moments; pointing during call-to-action).
4. **Tokens-only** (Doctrine Rule 1). No hardcoded hex / rgb anywhere outside this folder.
5. **Mark + wordmark sizing rule:** the mark height = wordmark x-height × 1.4 in horizontal lockups.

## License + attribution

The astronaut character + chat-bubble-prompt mark + "BeQuite" wordmark are original assets owned by Ahmed Shawky (xpShawky). The 6 ranked PNGs in `raw/` were generated via ChatGPT image generation with Ahmed's direction.

Geist + Geist Mono fonts are MIT-licensed by Vercel.

The whole brand system is MIT-licensed alongside BeQuite itself.

## Cross-references

- ADR-013 (Studio v2 architecture): `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- Doctrine `default-web-saas` (governs UI rules): `../../skill/doctrines/default-web-saas.md`
- Marketing site (consumes this): `../marketing/`
- Dashboard (consumes this): `../dashboard/`
