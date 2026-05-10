/**
 * tokens.css — Design tokens for {{PROJECT_NAME}}
 *
 * The single source of truth for design decisions. Every color / spacing /
 * typography / shadow / radius / motion / breakpoint value an interface uses
 * MUST resolve to one of these tokens (or a Tailwind class derived from them).
 *
 * Doctrine `default-web-saas` Rule 1 (block): no hardcoded values outside this file.
 * Doctrine `default-web-saas` Rule 2 (block): font-family declarations require a comment explaining WHY.
 *
 * Maintainer: {{MAINTAINER}}
 * Bundle:     skill/skills-bundled/impeccable/ (BeQuite v0.6.1+)
 * Last edit:  {{LAST_EDIT_DATE}}
 */

:root {
  /* ============================================================
   * 1. TYPOGRAPHY — recorded font choice (Doctrine Rule 2)
   *
   * REQUIRED: explain WHY this font fits this product. Acceptable
   * reasons: brand alignment, audience expectation, technical
   * constraint, density target, multi-locale support. The reason
   * must be one a senior designer would defend to a skeptic.
   *
   * Example reasons:
   *   "Inter — chosen for Linear/Vercel-style cleanliness in
   *    developer-tooling context; contrast carries hierarchy."
   *   "Geist — chosen for system-font-feel without IBM Plex's
   *    technical heaviness; pairs with Geist Mono semantically."
   *   "Tajawal + Inter — chosen for MENA-bilingual support;
   *    Tajawal renders Arabic with cleaner line-height than
   *    fallback system Arabic fonts."
   * ============================================================ */
  --font-sans: "{{FONT_SANS}}", "Helvetica Neue", system-ui, sans-serif; /* {{FONT_SANS_REASON}} */
  --font-mono: "{{FONT_MONO}}", "SF Mono", "Menlo", "Consolas", monospace; /* {{FONT_MONO_REASON}} */
  --font-display: var(--font-sans); /* override only with a recorded reason */

  /* Type scale — keep to ≤ 5 levels per principle (principles.md::1) */
  --text-display: 2.5rem;     /* 40px — hero / landing */
  --text-h1: 2rem;            /* 32px — page title */
  --text-h2: 1.5rem;          /* 24px — section title */
  --text-h3: 1.25rem;         /* 20px — sub-section */
  --text-body: 1rem;          /* 16px — default reading */
  --text-small: 0.875rem;     /* 14px — secondary copy */
  --text-caption: 0.75rem;    /* 12px — captions, badges */

  --leading-tight: 1.2;
  --leading-snug: 1.4;
  --leading-normal: 1.6;
  --leading-relaxed: 1.8;

  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;

  /* ============================================================
   * 2. COLOR — three-color system per principle (principles.md::3)
   *
   * Primary (brand), neutral scale (text + surfaces), accent.
   * System-state colors (success / warning / danger / info) are
   * not "more colors" — they encode meaning, not aesthetic.
   *
   * Light theme defaults; dark-theme overrides at the bottom.
   * ============================================================ */

  /* Brand primary */
  --color-primary-50:  #f3f8ff;
  --color-primary-100: #e2eeff;
  --color-primary-200: #c5dcff;
  --color-primary-300: #a3c4ff;
  --color-primary-400: #6699ff;
  --color-primary-500: #2563eb; /* primary brand */
  --color-primary-600: #1e51c8;
  --color-primary-700: #173f9b;
  --color-primary-800: #112d6e;
  --color-primary-900: #0a1c47;

  /* Neutral scale */
  --color-neutral-0:   #ffffff;
  --color-neutral-50:  #fafafa;
  --color-neutral-100: #f5f5f5;
  --color-neutral-200: #e5e5e5;
  --color-neutral-300: #d4d4d4;
  --color-neutral-400: #a3a3a3;
  --color-neutral-500: #737373;
  --color-neutral-600: #525252;
  --color-neutral-700: #404040;
  --color-neutral-800: #262626;
  --color-neutral-900: #171717;
  --color-neutral-1000: #000000;

  /* Accent (use sparingly — single accent per screen at most) */
  --color-accent-500: {{ACCENT_500_HEX}}; /* {{ACCENT_REASON}} */

  /* System state */
  --color-success-bg:    #dcfce7;
  --color-success-fg:    #14532d;
  --color-success-border:#86efac;

  --color-warning-bg:    #fef3c7;
  --color-warning-fg:    #78350f;
  --color-warning-border:#fcd34d;

  --color-danger-bg:     #fee2e2;
  --color-danger-fg:     #7f1d1d;
  --color-danger-border: #fca5a5;

  --color-info-bg:       #dbeafe;
  --color-info-fg:       #1e3a8a;
  --color-info-border:   #93c5fd;

  /* Semantic surfaces (light theme) */
  --color-bg:           var(--color-neutral-0);
  --color-bg-subtle:    var(--color-neutral-50);
  --color-bg-muted:     var(--color-neutral-100);
  --color-fg:           var(--color-neutral-900);
  --color-fg-subtle:    var(--color-neutral-700);
  --color-fg-muted:     var(--color-neutral-500);
  --color-border:       var(--color-neutral-200);
  --color-border-strong:var(--color-neutral-300);

  /* Skeleton */
  --color-skeleton-bg: var(--color-neutral-100);
  --color-skeleton-shimmer: var(--color-neutral-200);

  /* ============================================================
   * 3. SPACING SCALE — strict 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128
   * (principles.md::4). No arbitrary values.
   * ============================================================ */
  --space-0:    0;
  --space-1:    0.25rem;  /* 4px  */
  --space-2:    0.5rem;   /* 8px  */
  --space-3:    0.75rem;  /* 12px */
  --space-4:    1rem;     /* 16px */
  --space-6:    1.5rem;   /* 24px */
  --space-8:    2rem;     /* 32px */
  --space-12:   3rem;     /* 48px */
  --space-16:   4rem;     /* 64px */
  --space-24:   6rem;     /* 96px */
  --space-32:   8rem;     /* 128px */

  /* ============================================================
   * 4. RADIUS — keep to ≤ 4 levels (anti-patterns.md::14)
   * ============================================================ */
  --radius-none: 0;
  --radius-sm:   0.25rem; /* 4px */
  --radius-md:   0.5rem;  /* 8px */
  --radius-lg:   0.75rem; /* 12px */
  --radius-xl:   1rem;    /* 16px */
  --radius-full: 9999px;

  /* ============================================================
   * 5. SHADOW — restrained, semantic (focus / hover / elevated)
   * ============================================================ */
  --shadow-none:    none;
  --shadow-sm:      0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md:      0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg:      0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-focus:   0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-primary-500);
  --shadow-focus-danger: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-danger-fg);

  /* ============================================================
   * 6. MOTION — eased, restrained (principles.md::5; Doctrine Rule 6)
   * NEVER bounce / elastic / back. Doctrine `default-web-saas` Rule 6 blocks them.
   * ============================================================ */
  --duration-instant:  75ms;
  --duration-fast:     150ms;
  --duration-base:     200ms;
  --duration-slow:     300ms;
  --duration-deliberate: 500ms;

  --ease-linear:  linear;
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);   /* feel: snappy, decelerating */
  --ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in:      cubic-bezier(0.4, 0, 1, 1);

  /* ============================================================
   * 7. BREAKPOINTS — mobile-first (Doctrine Rule 7)
   * ============================================================ */
  --bp-sm: 640px;   /* small phones */
  --bp-md: 768px;   /* tablets */
  --bp-lg: 1024px;  /* small laptop */
  --bp-xl: 1280px;  /* desktop */
  --bp-2xl: 1440px; /* wide */

  /* ============================================================
   * 8. Z-INDEX — semantic, ≤ 8 levels
   * ============================================================ */
  --z-base:      0;
  --z-raised:    10;
  --z-dropdown:  100;
  --z-sticky:    200;
  --z-overlay:   300;
  --z-modal:     400;
  --z-popover:   500;
  --z-toast:     600;
  --z-tooltip:   700;
}

/* ============================================================
 * Dark theme overrides (when [data-theme="dark"] is set)
 * ============================================================ */
[data-theme="dark"] {
  --color-bg:           var(--color-neutral-900);
  --color-bg-subtle:    var(--color-neutral-800);
  --color-bg-muted:     var(--color-neutral-700);
  --color-fg:           var(--color-neutral-50);
  --color-fg-subtle:    var(--color-neutral-200);
  --color-fg-muted:     var(--color-neutral-400);
  --color-border:       var(--color-neutral-700);
  --color-border-strong:var(--color-neutral-600);

  --color-skeleton-bg:  var(--color-neutral-800);
  --color-skeleton-shimmer: var(--color-neutral-700);

  /* System-state surfaces in dark theme */
  --color-success-bg: #14532d;
  --color-success-fg: #dcfce7;

  --color-warning-bg: #78350f;
  --color-warning-fg: #fef3c7;

  --color-danger-bg:  #7f1d1d;
  --color-danger-fg:  #fee2e2;

  --color-info-bg:    #1e3a8a;
  --color-info-fg:    #dbeafe;

  --shadow-focus:     0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-primary-400);
}

/* ============================================================
 * RTL / mena-bilingual additions
 * Active when html[dir="rtl"] is set (typically locale ar-*).
 * Doctrine `mena-bilingual` v0.11.0+.
 * ============================================================ */
[dir="rtl"] {
  /* Mirror logical-property defaults; most layouts use logical
     properties (margin-inline-start, padding-inline-end) which
     mirror automatically. Only add mirror-specific overrides
     for icon-direction / arrow-direction values here. */

  /* Arabic-friendly font stack — overrides --font-sans when RTL.
     Tajawal: clean, geometric, designed for screens.
     Cairo: warmer, well-paired with Inter.
     Readex Pro: high x-height, good for dense interfaces.
     Pick one and document why above the override. */
  --font-sans: "Tajawal", "Cairo", "Readex Pro", "{{FONT_SANS}}", system-ui, sans-serif;

  /* Slightly larger body sizing for Arabic legibility. */
  --text-body: 1.0625rem; /* 17px — Arabic glyphs benefit from ~1pt extra */
  --leading-normal: 1.7;  /* slightly more leading for Arabic */
}

/* ============================================================
 * Reduced-motion (a11y)
 * ============================================================ */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 0ms;
    --duration-fast: 0ms;
    --duration-base: 0ms;
    --duration-slow: 0ms;
    --duration-deliberate: 0ms;
  }
}
