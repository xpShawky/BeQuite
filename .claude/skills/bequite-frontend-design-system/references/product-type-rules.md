# Product-Type Rules

Not every project is a cinematic SaaS landing page. **Detect the product type first** (record it in `DESIGN_DNA.md` §1), then design *for that type*. The Design Continuity Gate judges sections against the type's row here — a dense dark finance dashboard and an airy wellness app are both correct for their type.

> Adapted from the UI-UX-Pro-Max reasoning model (researched reference: `ui-ux-pro-max-notes.md`). Tool-neutral: the named styles/colors are **candidates**, not mandates — pick what fits the brand and record why.

## How to use

1. Classify the product into the closest row.
2. Apply its pattern / density / color mood / typography mood / trust level / motion / CTA / mobile + a11y level.
3. Honor the **decision rules** (conditional branches) and **anti-patterns** (hard rejects).
4. For anything not listed: reason from the nearest analog + the 10 decision questions.

## The headline cross-cutting rule

**Trust domains — banking, fintech, healthcare, government, legal, B2B/enterprise — must reject "AI purple/pink gradients," playful styles, and glassmorphism overuse.** Trust-first beats trendy. This is the single most portable, high-value guardrail.

## Per-type rules

| Product type | Recommended pattern | Density | Color mood | Typography mood | Trust | Motion | CTA style | Anti-patterns (reject) | Mobile / A11y |
|---|---|---|---|---|---|---|---|---|---|
| **SaaS landing** | Hero + Features + Social proof + CTA | Medium | Trust blue + 1 accent; tinted neutrals | Modern sans, clear hierarchy | Med-high | Restrained, purposeful | One primary "Start free"-style, specific | excessive animation, dark-by-default, 5-col feature grids | Mobile-first; AA |
| **SaaS dashboard** | App shell + KPI cards + tables/charts | Medium-high | Calm base + status colors | Functional sans | Med | Subtle state transitions | Toolbar actions, primary per view | landing-page styling, decorative gradients | Responsive; AA |
| **Admin panel** | Sidebar nav + data tables + forms | High | Neutral + semantic status | Functional, compact | Med | Minimal | Row actions, bulk actions | marketing fluff, low info density | AA; keyboard-first |
| **Financial dashboard** | Data-dense dashboard, real-time | High | Dark (OLED) bg + red/green alerts + trust blue | Precise sans, tabular numerals | High | Real-time number anim only | Clear, confirm destructive | light-mode-default, slow render, **AI purple/pink** | High-contrast; AA+ |
| **Fintech / crypto / banking** | Trust & authority + feature | Medium | Navy + trust blue + gold | Precise, single-family ok | Very high | Minimal | Security-forward, clear fees | playful design, unclear fees, **AI purple/pink** | AA; security UX |
| **Medical / healthcare** | Social-proof + clear flows | Medium | Calm blue + health green | Accessible, generous | Very high | Gentle (breathing if meditation) | Book/Start care, reassuring | bright neon, motion-heavy, **AI purple/pink** | **WCAG-AAA**; large targets |
| **Government / public** | Minimal & direct | Medium | Professional blue + high contrast | Plain, legible | Very high | Avoid motion | Direct ("Apply", "Pay") | ornate, low contrast, motion | **WCAG-AAA**; keyboard-nav |
| **Legal services** | Trust & authority + minimal | Medium | Navy + gold + white | Serif authority + sans body | Very high | Minimal | Consult / case results | outdated look, hidden credentials, AI gradients | AA; readable |
| **E-commerce** | Feature-rich showcase | Medium-high | Brand primary + success green (+ urgency) | Clear, product-forward | Med-high | Hover product reveals (not image-scale) | Add to cart, urgency where honest | flat-without-depth, text-heavy, low-quality imagery | Mobile-first; AA |
| **E-commerce luxury / premium brand** | Storytelling + showcase | Low-medium | Black + gold + white; minimal accent | High-contrast serif display | High | Slow, refined | Discreet, premium | cheap visuals, fast/playful animation | Mobile-first; AA |
| **Marketplace** | Search + listings + trust signals | Medium-high | Neutral + brand accent + trust badges | Clear, scannable | High | Subtle | List/Buy/Contact; safety-forward | generic listings, missing trust/safety | Mobile-first; AA |
| **Restaurant / food-ordering** | Hero-centric + conversion | Medium | Warm (orange/red/brown) | Appetite-forward display + clean body | Med | Light, appetizing | Order / Reserve | low-quality imagery, cluttered menu | Mobile-first; AA |
| **Booking app** | Hero + availability + social proof | Medium | Calm + clear CTA | Friendly, legible | Med-high | Subtle confirmations | Book now, clear date/availability | hidden pricing, confusing calendar | Mobile-first; AA |
| **Developer tool** | Docs-forward + code samples | Medium | Dark or neutral; restrained accent | Mono + clean sans; single-family ok | High | Minimal | Install/Get key; copyable | marketing fluff over substance, fake metrics | AA; keyboard |
| **AI product** | Interactive demo + minimal chrome | Low-medium | Neutral + restrained accent (purple OK *only if* genuine brand) | Clean, modern | Med-high | Conversational feedback | Try it / Demo on your data | heavy chrome, slow feedback, "Powered by AI" badge | AA |
| **Content platform** | Editorial + reading-first | Low | Neutral + 1 accent; high readability | Editorial serif/sans pairing | Med | Minimal (reading-safe) | Subscribe / Read | cluttered chrome over content, ad-heavy | Mobile-first; AA; measure 45–75ch |
| **Internal business tool** | Function-first shell + forms/tables | High | Neutral + semantic | Compact functional | Med | None-minimal | Direct verbs | over-design, animation, decoration | AA; keyboard |
| **Automation dashboard** | Real-time monitoring + controls | High | Dark + status colors | Functional, tabular | High | Status pulse only | Run/Stop/Configure; confirm destructive | ornate, no filtering, slow render | High-contrast; AA |

## Style "Do Not Use For" guardrails (from styles research)

- **Claymorphism / Neumorphism (soft)** — ✗ finance, medical, legal, formal corporate.
- **Brutalism / Neubrutalism** — ✗ corporate, trust domains; ✓ creative/portfolio.
- **Motion-driven / Liquid glass** — ✗ data dashboards, low-power devices.
- **Glassmorphism** — only rare + purposeful; ✗ as a default everywhere.
- **Data-dense** — ✓ BI/finance/enterprise; ✗ marketing/consumer landing.

## Decision-rule examples (conditional, not one fixed answer)

- E-commerce → liquid-glass *if* luxury; urgency colors *if* conversion-focused.
- Finance → dark mode *if* dashboard; light *if* marketing site.
- Healthcare → red-alert colors *if* medication; breathing motion *if* meditation.
- Portfolio → brutalism *if* creative; reduce-motion *if* minimal.

## Output

The chosen type + its applied rules belong in `DESIGN_DNA.md` (§1 product type, plus the palette/type/motion/a11y sections it drives). The continuity gate reads them back.
