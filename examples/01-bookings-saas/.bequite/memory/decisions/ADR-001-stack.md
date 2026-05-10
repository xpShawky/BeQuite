---
adr: 001
title: Stack decision for example-01-bookings-saas
status: accepted
date: 2026-05-10
deciders: BeQuite v0.9.0 author
supersedes: null
superseded_by: null
---

# ADR-001 — Stack for `01-bookings-saas`

## Context

The BeQuite example demonstrates `default-web-saas` Doctrine end-to-end. Stack must:
- Match Doctrine Rules 1–14.
- Pass `bequite freshness` (no rotted candidates).
- Hit the small-SaaS scale tier (5,000 MAU; Pro tiers acceptable).
- Be hand-runnable by a second engineer reading only this ADR + HANDOFF.

## Decision

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router) |
| UI | shadcn/ui v3+ + tweakcn-derived `tokens.css` + Tailwind v4 |
| Backend | Hono on Bun |
| Database | Supabase (Postgres + RLS) |
| Auth | Better-Auth (primary); Clerk as alternate (Doctrine Rule 9) |
| Hosting | Vercel (web) + Supabase (db) |
| Pooling | Supavisor (Supabase-bundled) |
| Validation | Zod |
| Forms | React Hook Form + Zod resolver |
| Server state | TanStack Query v5 |
| Client state | Zustand |
| i18n | next-intl |
| Testing | Playwright + Vitest + axe-playwright |
| Observability | Sentry (review license; self-hosted in v1.x) + PostHog |
| CI | GitHub Actions (lint + typecheck + tests + axe + smoke) |

## Rationale per layer

**Next.js (App Router).** Default for unknown stacks per Doctrine. App Router is now stable since 2024; React Server Components handle the bulk of admin views well; client components scope to interactive flows. Edge-runtime middleware for auth gating.

**Hono on Bun.** Edge-friendly TS backend; smallest dependency tree among Bun-targeting frameworks. Pairs with Next.js as either a co-located `apps/api` or a separate Vercel function. Hono RPC keeps types end-to-end without a separate tRPC layer.

**Supabase.** Postgres + Auth + Storage + Realtime in one tier. SOC 2 / ISO 27001. RLS deny-by-default fits Doctrine Rule 10. Free tier covers prototyping (500MB DB); Pro tier ($25/mo) covers small SaaS up to ~8GB. Supavisor replaces PgBouncer for transaction-mode pooling.

**Better-Auth.** MIT-licensed, self-hosted, 2FA + passkeys + orgs + RBAC. Doctrine Rule 9 lists it first; Clerk is the alternate when speed > ownership matters more (free tier 50k MAU as of 2026 is generous). For this example, we choose Better-Auth to demonstrate ownership-first; the alternate path is one ADR amendment away.

**Vercel.** Default Next.js host; Pro tier extends function timeout to 800s (configurable up from 300s default). Edge functions for auth middleware. Hobby tier is a hard 300s — won't suit production-grade webhooks.

**Zod everywhere.** Every API surface — POST/PUT/PATCH bodies, query params, env vars, server actions — validates via Zod. Doctrine Rule 11. Pairs with React Hook Form on the client (zod resolver) for type-safe forms.

**TanStack Query v5 for server state.** Caches server reads; tracks mutation lifecycle; handles optimistic updates + rollback. Pairs with Hono RPC types so cache keys are typed.

**Zustand for client state.** Smaller than Redux Toolkit; no boilerplate. Use only for genuinely-client state (UI flags, form drafts); server data lives in TanStack Query cache.

**next-intl.** App-router-aware i18n; supports static + dynamic locales. Sets up cleanly to layer `mena-bilingual` Doctrine on top later.

**Playwright + axe-playwright.** Doctrine Rule 12 (admin + user walks) + Rule 8 (axe-core gate). The walkthrough templates at `../../skill/templates/tests/walkthroughs/{admin,user}-walk.md.tpl` are the source.

## Alternatives considered

- **Remix instead of Next.js.** Equally good; chose Next.js for SEO / Vercel default. Remix is the alt for form-heavy admin tools; this example has both, so Next.js wins for breadth.
- **Neon instead of Supabase.** Pure Postgres, branching, scale-to-zero. Wins for branching workflows; loses for built-in auth + storage. We chose Supabase to keep auth + storage in one platform.
- **Clerk instead of Better-Auth.** Free 50k MAU is generous; Clerk wins for speed-to-prod. We chose Better-Auth to demonstrate ownership; Clerk is one ADR amendment away.

## Consequences

- **Positive:** typed end-to-end (Zod schemas shared client+server). Auth ownership. Clear scaling path (Vercel Pro + Supabase Pro both within $50/mo).
- **Negative:** Bun's runtime divergence from Node (some npm packages don't load cleanly on Bun). Mitigation: track Bun's ecosystem-compat list quarterly; fall back to Node if needed.
- **Risk:** Sentry's BSL/FSL license shift since 2023. Mitigation: review per `skill/references/frontend-stack.md::License-flag callouts` before bundling; self-host or swap to OpenTelemetry-only if license becomes a problem.

## Doctrine compliance

- Rule 1 (tokens-only): tokens.css + Tailwind config-extended-from-tokens. PASS.
- Rule 2 (recorded font choice): `tokens.css` carries the comment. PASS.
- Rule 3 (component sourcing order): shadcn/ui first; Magic MCP for unknowns. PASS.
- Rule 4 (no nested cards): enforced by `bequite audit`. PASS.
- Rule 5 (no gray-on-color): axe-playwright gate. PASS.
- Rule 6 (no bounce/elastic): tokens.css has only ease-out / ease-in-out. PASS.
- Rule 7 (mobile + desktop parity): Playwright walks at viewport 360 + 1440. PASS.
- Rule 8 (axe-core gate): wired via skill/templates/.github/workflows/axe.yml.tpl. PASS.
- Rule 9 (Better-Auth / Clerk / Supabase Auth): chose Better-Auth. PASS.
- Rule 10 (deny-by-default RLS): enforced in Supabase migrations. PASS.
- Rule 11 (input validation everywhere): Zod. PASS.
- Rule 12 (Playwright walks admin + user): scaffolded. PASS.
- Rule 13 (no .env reads): `process.env` only via Next.js / Hono runtime. PASS.
- Rule 14 (CSP / HSTS / X-Frame-Options): Next.js middleware scaffolded. PASS.

## Status: accepted (2026-05-10)
