# Frontend stack reference (verified May 2026)

> Library list for Doctrine `default-web-saas` and forks. Each entry includes license + maintenance freshness + the project tier where it fits. Cross-checked by `bequite freshness` before any stack ADR signs.
>
> Cross-references:
> - Doctrine: `skill/doctrines/default-web-saas.md`
> - Tokens template: `skill/templates/tokens.css.tpl`
> - Bundled design skill: `skill/skills-bundled/impeccable/`
> - Stack matrix (multi-doctrine): `skill/references/stack-matrix.md` (v0.14.0+)

## Component layer

### Tier 1 — primary

| Library | License | Last release | Notes |
|---|---|---|---|
| **shadcn/ui** v3+ | MIT | rolling | Copy-paste components; full ownership; built-in registry MCP since v3. **Default for new web SaaS.** |
| **Radix UI** primitives | MIT | rolling | Underlying primitives shadcn ships on top of. Use directly when shadcn is too opinionated. |
| **HeadlessUI** | MIT | active | Tailwind-team primitives; alternative to Radix when on Tailwind-only stack. |

### Tier 2 — themed / animated

| Library | License | Last release | Notes |
|---|---|---|---|
| **tweakcn** | MIT | active | Visual theme editor → JSON → drop into shadcn. Use to derive `tokens.css` from a brand. |
| **Aceternity UI** | MIT | active | Animated / accent components (gradient cards, parallax sections). Avoid as default — selection bias toward AI-default look. |
| **Magic UI** | MIT | active | Animation-heavy; subset useful for marketing (not admin). |
| **Origin UI** | MIT | active | Form-heavy components (multi-step forms, complex selectors). |

### Tier 3 — generative MCPs

| MCP | Auth | Notes |
|---|---|---|
| **shadcn Registry MCP** (built into shadcn CLI v3+) | none | Primary MCP for adding shadcn components by name. No separate install. |
| **21st.dev Magic MCP** (`@21st-dev/magic`) | API key required | "/ui" prompt → multiple variations. Use for *unfamiliar* component shapes (e.g. an unusual data-vis combo). Document key in env. |
| **context7 MCP** (Upstash) | none (free tier) | Version-pinned docs lookup. Pair with stack ADR to confirm any chosen library is indexed. |

## Framework layer

| Framework | License | When to pick | When NOT to pick |
|---|---|---|---|
| **Next.js (App Router)** | MIT | Full-stack with SEO + edge; default for unknown | Non-React teams |
| **Remix** | MIT | Form-heavy, RR-routing-aware | Static-first (use Astro) |
| **Astro** | MIT | Content / blog / mostly-static | Heavy interactive dashboards |
| **SvelteKit** | MIT | Smallest bundles, animation-heavy | Massive React-talent pool needed |
| **Nuxt** | MIT | Vue teams | React teams |
| **React + Vite** | MIT | SPA dashboards (no SEO need) | When SEO matters |
| **Plain HTML/CSS/JS** | n/a | True static sites; landing pages | Anything stateful |

## Styling layer

| Tool | License | When to pick |
|---|---|---|
| **Tailwind CSS** v4+ | MIT | Default. Pairs with `tokens.css`. |
| **CSS Modules** | n/a (built-in) | Component-scoped CSS without Tailwind. |
| **Vanilla CSS + tokens.css** | n/a | Brand sites, marketing pages, spec-perfect renders. |
| **CSS-in-JS (Emotion / styled-components)** | MIT | Legacy projects; new projects should prefer Tailwind. |
| **Panda CSS** | MIT | Type-safe CSS-in-JS without runtime. New stable. |

## Type-safety layer

| Library | License | Notes |
|---|---|---|
| **Zod** | MIT | Default for runtime validation. Doctrine `default-web-saas` Rule 11. |
| **Valibot** | MIT | Smaller bundle than Zod; same API shape. |
| **TypeScript** | Apache-2.0 | Default. Always strict-mode. |

## Data fetching layer

| Library | License | When to pick |
|---|---|---|
| **TanStack Query (React Query)** v5+ | MIT | Default for client-side data. Cache, retry, optimistic. |
| **SWR** | MIT | Lightweight alternative; less feature-rich. |
| **tRPC** | MIT | When backend is Node and TS-end-to-end is desirable. |
| **Hono RPC** | MIT | When backend is Hono. Smaller than tRPC. |

## State management

| Library | License | When to pick |
|---|---|---|
| **Zustand** | MIT | Default for client state. Small, no boilerplate. |
| **Jotai** | MIT | Atom-based; React-Three-Fiber-friendly. |
| **TanStack Query cache** | MIT | Server state — don't duplicate into local state. |
| **Redux Toolkit** | MIT | Legacy projects; not recommended new. |

## Form layer

| Library | License | When to pick |
|---|---|---|
| **React Hook Form** | MIT | Default. Pair with Zod resolver. |
| **TanStack Form** | MIT | When TanStack Query is already loaded; consistent API. |
| **Conform** | MIT | Server-action-aware; pairs well with Remix / Next App Router. |

## Auth layer (per Doctrine `default-web-saas` Rule 9)

| Library | License | When to pick | When NOT to pick |
|---|---|---|---|
| **Better-Auth** | MIT | Self-hosted, ownership, 2FA / passkeys / orgs / RBAC | Need pre-built billing |
| **Clerk** | proprietary | Speed > ownership; free 50k MAU as of 2026 | Need data residency control |
| **Supabase Auth** | Apache-2.0 | When on Supabase | Not on Supabase |
| **Auth0 / WorkOS** | proprietary | Enterprise SSO / SAML | Pre-PMF cost-sensitive |

## Accessibility layer

| Library | License | Use |
|---|---|---|
| **axe-core** (Deque) | MPL-2.0 | CI gate. Doctrine Rule 8. |
| **axe-playwright** | MIT | Wrapper to run axe-core in Playwright walks. |
| **eslint-plugin-jsx-a11y** | MIT | Lint-time a11y catches; doesn't replace runtime axe. |
| **react-aria** (Adobe) | Apache-2.0 | When building from-scratch components needing full a11y. |

## i18n layer (when mena-bilingual is loaded)

| Library | License | Use |
|---|---|---|
| **next-intl** | MIT | Next.js + App Router default. |
| **i18next** | MIT | Framework-agnostic; mature. |
| **lingui** | MIT | Compile-time messages; smallest runtime. |

## Testing layer

| Library | License | Use |
|---|---|---|
| **Playwright** + **@playwright/test** | Apache-2.0 | Default e2e. Doctrine Rule 12. Pair with `axe-playwright`. |
| **Vitest** | MIT | Unit + component tests. |
| **Testing Library** (React/Vue/Svelte) | MIT | Component-level tests with user-perspective queries. |
| **MSW** | MIT | Network mocking in tests. |
| **Storybook** | MIT | Component preview + visual regression baseline. Pairs with `live` Impeccable command. |

## Performance / build

| Tool | License | Use |
|---|---|---|
| **Vite** | MIT | Default bundler. |
| **Turbopack** (Next) | MIT | When on Next.js — built-in. |
| **rspack** | MIT | Webpack-API-compatible; faster. Migration path for old Webpack projects. |
| **Lighthouse CI** | Apache-2.0 | Performance budget gate in CI (Doctrine `default-web-saas` Rule 8 stacks here). |

## Observability layer

| Tool | License | Use |
|---|---|---|
| **Sentry** | BSL-1.1 / FSL-1.1 (recent) | Error tracking. Note license shift since 2023; review for self-hosting needs. |
| **PostHog** | MIT | Product analytics + feature flags + session replay. |
| **OpenTelemetry-JS** | Apache-2.0 | Vendor-neutral instrumentation. |

## License-flag callouts

These are flagged in `bequite freshness` because they affect commercial closed-source distribution:

- **Sentry SDK** — recent license shifts (BSL/FSL). **Self-hosted Sentry** is fine; SaaS is fine; redistribution may not be. Read the current license before bundling.
- **Aceternity UI / Magic UI / Origin UI** — MIT but components are *style-heavy*; verify each component you use isn't a 1:1 copy of a copyrighted design. A senior frontend-designer should audit selections.
- **Inter font** — OFL (SIL Open Font License) — fine. **Geist** — MIT. **SF Pro** — Apple license, NOT for non-Apple-platform self-hosting in production webfonts; use Inter / Geist instead.
- **Tajawal / Cairo / Readex Pro (Arabic)** — OFL — fine for embedding.

## Cross-references

- **Bundled design skill:** `skill/skills-bundled/impeccable/` — applies on top of any of these.
- **Doctrine:** `skill/doctrines/default-web-saas.md` — codifies which of these are required vs recommended.
- **Tokens template:** `skill/templates/tokens.css.tpl` — what every layered design tool reads.
- **Freshness probe:** `cli/bequite/freshness.py` — re-checks last-release dates + license + CVE freshness before signing the stack ADR.
- **Stack matrix (cross-doctrine):** `skill/references/stack-matrix.md` (lands in v0.14.0).
