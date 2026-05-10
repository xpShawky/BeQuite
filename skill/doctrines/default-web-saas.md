---
name: default-web-saas
version: 1.0.0
applies_to: [web-saas, frontend]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: default-web-saas v1.0.0

> The default Doctrine BeQuite ships for web SaaS projects with a frontend. Loaded by `.bequite/bequite.config.toml::doctrines = ["default-web-saas"]`. Stacks with `mena-bilingual` cleanly when both are loaded (mena-bilingual adds RTL + Arabic; default-web-saas governs the rest of UI/UX).

## 1. Scope

Web applications with a user-facing frontend, primarily Next.js / Remix / SvelteKit / Astro deployed to a Vercel / Cloudflare / Render / Fly tier appropriate to scale. Covers UI rules, design tokens, accessibility gates, frontend stack ordering, and the verification suite (Playwright walks).

**Does NOT cover:** pure CLI tools (use `cli-tool`), ML training pipelines (use `ml-pipeline`), desktop apps (use `desktop-tauri`), library packages (use `library-package`).

## 2. Rules

### Rule 1 — Tokens-only design
**Kind:** `block`
**Statement:** No hardcoded `font-family`, `color`, `background-color`, `border-color`, `box-shadow` outside `tokens.css` / `tokens.json`. Tailwind classes that bypass tokens (e.g. `bg-[#7c3aed]` or `text-[16px]`) are forbidden.
**Check:** `bequite audit` greps non-token color/font/spacing usage in CSS/TSX/Tailwind classes; flags violations.
**Why:** prevents the AI-default purple-to-blue gradient + Inter-font slop.

### Rule 2 — Recorded design choice
**Kind:** `block`
**Statement:** The font stack must be a deliberate choice recorded in `tokens.css` with a one-line comment explaining *why* this font fits this product. Inter is *allowed* but only with a recorded reason ("we want Linear/Vercel cleanliness" is acceptable; "the AI suggested it" is not).
**Check:** `bequite audit` greps for `font-family` declarations without an adjacent comment.
**Why:** softer than an outright ban (Linear, Vercel, Stripe use Inter beautifully); harder than no rule.

### Rule 3 — Component sourcing order
**Kind:** `recommend`
**Statement:** When a UI need arises, source from this list in order, dropping to the next only when nothing above fits:
1. **shadcn/ui** (base components, copy-paste, full ownership)
2. **tweakcn** (theme generator → custom JSON → drop into shadcn)
3. **Aceternity UI / Magic UI / Origin UI** (animated/accent components when needed)
4. **21st.dev Magic MCP** (`/ui` slash → multiple variations from prompt)
5. **Custom** (only when nothing above fits)
**Check:** advisory only; not enforced.
**Why:** the brief's component-sourcing order; reduces from-scratch component-building.

### Rule 4 — No nested cards
**Kind:** `block`
**Statement:** A `.card` / `[role="region"]` MUST NOT contain another `.card` / `[role="region"]` within itself. Use sections, dividers, or layout grids instead.
**Check:** `bequite audit` parses TSX and Vue templates; flags nested `.card` / role="region".
**Why:** the AI-slop tell.

### Rule 5 — No gray-on-color
**Kind:** `block`
**Statement:** Text on a coloured background (anything other than `bg-white` / `bg-black` / pure tokens) MUST meet WCAG AA contrast (≥ 4.5:1 for body text, ≥ 3:1 for large text). Gray text on coloured backgrounds is forbidden.
**Check:** `axe-core` gate in CI; fails the build on contrast violation.
**Why:** the AI-slop tell + accessibility.

### Rule 6 — No bounce / elastic easing
**Kind:** `block`
**Statement:** Animations MUST use linear / ease-out / cubic-bezier easings. `bounce`, `elastic`, `back` easings are forbidden in production code.
**Check:** `bequite audit` greps for `bounce` / `elastic` / `cubic-bezier(.*1.0\d*,.*\)` (overshoot detection).
**Why:** the AI-slop tell.

### Rule 7 — Mobile + desktop parity from day 1
**Kind:** `block`
**Statement:** Every page MUST work at **360 px and 1440 px** viewports. Touch targets ≥ 44 × 44 px. The Playwright walks (Rule 12) include both viewports.
**Check:** Playwright walks with viewport overrides.
**Why:** mobile-last is a regression you pay for over and over.

### Rule 8 — axe-core gate
**Kind:** `block`
**Statement:** axe-core runs in CI on every PR; zero violations is required for merge.
**Check:** GitHub Actions workflow.
**Why:** WCAG AA isn't optional.

### Rule 9 — Auth via Better-Auth or Clerk or Supabase Auth
**Kind:** `recommend`
**Statement:** Authentication uses **Better-Auth** (MIT, self-hosted, 2FA / passkeys / orgs / RBAC) or **Clerk** (when speed > ownership; free tier 50k MAU as of 2026) or **Supabase Auth** (when on Supabase). Custom session / cookie / JWT auth requires an explicit ADR.
**Check:** advisory; the ADR is the gate.
**Why:** rolling-your-own auth is the most common breach surface; OWASP Top 10 web (Broken Access Control, Cryptographic Failures).

### Rule 10 — Authz: deny-by-default
**Kind:** `block`
**Statement:** Database tables start with **deny-all** RLS / RBAC and explicit allow rules per role. Any table without an explicit policy is forbidden.
**Check:** `bequite audit` parses Supabase migrations / Drizzle schema; flags tables without policy.
**Why:** the most common authz breach is "we forgot to add a policy."

### Rule 11 — Input validation everywhere
**Kind:** `block`
**Statement:** Every API surface validates input via **Zod** / **Pydantic** / **Valibot**. No raw `req.body` consumption.
**Check:** `bequite audit` scans handlers; flags untyped body access.
**Why:** OWASP Top 10 web (Injection, Insecure Design).

### Rule 12 — Playwright walks: admin + user
**Kind:** `block`
**Statement:** Every project ships `tests/walkthroughs/admin-walk.md` and `tests/walkthroughs/user-walk.md`. The `bequite verify` runner traverses every route in the sitemap as both roles, captures console errors, captures 4xx/5xx from API.
**Check:** `bequite verify` exit code.
**Why:** the verification gate the brief demands.

### Rule 13 — No reads of `.env*`
**Kind:** `block`
**Statement:** Code MUST NOT contain `fs.readFile('.env*')`, `open('.env*')`, or equivalent. Environment variables are loaded by the framework / runtime.
**Check:** PreToolUse hook + `bequite audit`.
**Why:** Article IV (security & destruction).

### Rule 14 — CSP / HSTS / X-Frame-Options scaffolded
**Kind:** `recommend`
**Statement:** `next.config.ts` / Hono middleware scaffolds Content Security Policy, HSTS, X-Frame-Options at init.
**Check:** `bequite audit` checks for the scaffold.
**Why:** OWASP Top 10 web (Security Misconfiguration).

## 3. Stack guidance

When the Architect writes the stack ADR for a project loaded with this Doctrine, this is the starting menu. **Run `bequite freshness` before signing the ADR.**

### Frontend
| Choice | When |
|---|---|
| Next.js (App Router) | Full-stack with SEO + edge; default for unknown |
| Remix | Form-heavy, RR-routing-aware |
| Astro | Content / blog / mostly-static |
| SvelteKit | Smallest bundles, animation-heavy |
| Nuxt | Vue teams |
| React + Vite | SPA dashboards (no SEO need) |
| Plain HTML/CSS/JS | True static sites |

### Backend
| Choice | When |
|---|---|
| Hono on Bun/Node | Smallest, edge-friendly |
| Fastify | Node teams who want speed without extra learning |
| NestJS | Large teams; opinionated DI |
| FastAPI | Python ML colocation |

### Database
| Choice | When |
|---|---|
| Supabase | Postgres + Auth + Storage + Realtime; SOC 2 / ISO 27001 |
| Neon | Pure Postgres, branching, scale-to-zero |
| Turso | SQLite at edge; 5 GB free |
| Convex | Reactive TS-native; small write-throughput ceiling |
| PlanetScale | Serious scale; no free tier |

### Auth
| Choice | When |
|---|---|
| Better-Auth | MIT, self-hosted, 2FA / passkeys / orgs / RBAC |
| Clerk | Speed > ownership; free 50k MAU as of 2026 |
| Supabase Auth | When on Supabase |
| Auth0 / WorkOS | Enterprise SSO / SAML |

### Hosting
| Choice | When |
|---|---|
| Vercel | Next.js default; Pro extends timeout to 800 s |
| Cloudflare Pages/Workers | Cheapest at scale |
| Render / Fly.io / Railway | Always-on workers + private networks |

### Pooling (per-tenant)
- **PgBouncer** on Neon / RDS / self-host
- **Supavisor** on Supabase (replaced PgBouncer there)

## 4. Verification

`bequite verify` runs the following additional gates for projects loaded with this Doctrine:

1. **Playwright walks** — admin-walk + user-walk at viewport 360 + 1440.
2. **Smoke** — `curl` every public endpoint; expect 200/401/403 per spec.
3. **axe-core** — accessibility gate.
4. **Secret scan** — repository content + the build output.
5. **CSP / HSTS check** — actual headers from a running server.
6. **`bequite audit`** — Iron Laws + this Doctrine's rules.

## 5. Examples and references

- shadcn/ui: https://ui.shadcn.com/
- tweakcn: https://tweakcn.com/
- Aceternity UI: https://ui.aceternity.com/
- 21st.dev Magic: https://21st.dev/
- context7: https://github.com/upstash/context7
- Better-Auth: https://better-auth.com/
- Clerk: https://clerk.com/pricing
- Supabase: https://supabase.com/pricing
- OWASP Top 10 (Web): https://owasp.org/www-project-top-ten/
- WCAG AA: https://www.w3.org/WAI/WCAG2AA-Conformance

## 6. Forking guidance

Common forks:
- **Plain-shadcn** — drop the Magic MCP recommendation when offline-only.
- **Frontend-only** — drop the database/auth rules when decoupled from backend.
- **Marketing-only** — drop the auth + RLS rules; keep design tokens + axe-core.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: default-web-saas@1.0.0`.
4. Document changes in a `## Changes` section.
5. Load via `.bequite/bequite.config.toml::doctrines = ["<your-name>"]`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–14 ratified. Stack matrix reflects May 2026 reality (post brief reconciliation).
```
