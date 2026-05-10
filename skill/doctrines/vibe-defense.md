---
name: vibe-defense
version: 1.0.0
applies_to: [vibe-handoff, ai-generated-code, audience-vibe-coder]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: vibe-defense v1.0.0

> Default Doctrine for projects with `audience: vibe-handoff`. Codifies the response to the Veracode 2025 GenAI Code Security Report finding: ~45% of AI-generated code has OWASP Top-10 issues (XSS 86% fail rate, log injection 88%, Java 72% fail). The 45% rate is the entire reason BeQuite exists; this Doctrine is the operational counter.
>
> Stacks cleanly with `default-web-saas` (UI rules) + `library-package` (semver/deps) + Article VIII (scraping when applicable) + Article IX (security baseline).

## 1. Scope

Projects authored primarily by an AI coding agent (Claude Code / Cursor / Codex / etc.) with minimal human review, intended to be handed off to a real engineer at the 70%-mark for production polish. The vibe-coder might be an engineer in a hurry, a non-engineer founder, or a Lovable/v0/Bolt refugee. The threat model: **the human reviewing this code is fast-moving and might miss what the AI got wrong.**

Auto-loaded by `bequite init <project> --audience=vibe-handoff` (or by setting `state/project.yaml::audience = vibe-handoff` directly).

## 2. Rules — extra-strict baseline

### Rule 1 — Block all HIGH SAST findings on merge

**Kind:** `block` (with 90d-expiring-ADR-override)
**Statement:** Any HIGH or CRITICAL Semgrep finding blocks PR merge. Override via ADR `ADR-SEC-OVERRIDE-<id>.md` documenting (a) why this finding is acceptable, (b) compensating controls, (c) `expires_at` ≤ 90 days. After expiry, finding re-blocks unless re-justified.
**Why:** vibe-coded apps' biggest risk is the developer not noticing the finding; default-block forces seeing.

### Rule 2 — Exact-pinned dep versions for production

**Kind:** `block`
**Statement:** Production dependencies (npm `dependencies`, PyPI `[project.dependencies]`, Cargo `[dependencies]`) MUST use exact version pins (`1.2.3`) for production. No `^1.2.3`, no `~1.2.3`, no `latest`, no `*`, no `>=1.2`. Lockfile committed. Dev dependencies (`devDependencies`) may use `^` or `~`.
**Check:** `bequite audit` parses `package.json` / `pyproject.toml` / `Cargo.toml`; flags non-exact prod deps.
**Why:** transitive supply-chain attacks (PhantomRaven 126 packages, Shai-Hulud ~700) exploit version-range ambiguity to slip in a backdoored minor patch.

### Rule 3 — RLS / RBAC deny-by-default

**Kind:** `block`
**Statement:** Database tables with user data start with deny-all RLS / RBAC; explicit allow rules per role. Migrations creating a new table without a policy → block.
**Check:** `bequite audit` parses migrations (Prisma / Drizzle / raw SQL); flags table-create without explicit policy in same migration or sibling.
**Why:** the most common authz breach is "we forgot to add a policy."

### Rule 4 — CSP locked-down by default

**Kind:** `block`
**Statement:** Content Security Policy header has no `'unsafe-inline'`, no `'unsafe-eval'`, no `*` source. Specific allow-lists. `frame-ancestors 'none'` unless explicit need.
**Check:** `bequite audit` parses `next.config.ts` / Hono middleware / Express helmet config; flags loose CSP.
**Why:** XSS at 86% fail rate per Veracode 2025; CSP is the defense-in-depth layer.

### Rule 5 — Secret-scan on every commit (not just PR)

**Kind:** `block`
**Statement:** `pretooluse-secret-scan.sh` (existing hook) runs as pre-commit hook, not just PreToolUse. Adds husky / pre-commit / lefthook config.
**Why:** vibe-coders don't always create PRs; some commit straight to main locally.

### Rule 6 — axe-core on every deploy (frontend Doctrines)

**Kind:** `block`
**Statement:** When `default-web-saas` (or fork) is active, axe-core a11y check runs on every deploy. Zero violations required.
**Check:** GitHub Actions workflow.
**Why:** vibe-coded UIs default to inaccessible; defense-in-depth.

### Rule 7 — Mandatory `bequite audit` clean before deploy

**Kind:** `block`
**Statement:** `bequite audit` exit code 0 is a deploy gate. Any unresolved Iron Law / Doctrine `block`-severity finding stops the deploy.
**Why:** Constitution drift accumulates fastest in vibe-coded projects.

### Rule 8 — Input validation everywhere — Zod / Pydantic / Valibot

**Kind:** `block`
**Statement:** Every API surface validates input via Zod / Pydantic / Valibot. No raw `req.body` consumption. Validation layer ALSO does output schema check (defense for OWASP LLM-08 vector / data exfiltration).
**Check:** `bequite audit` scans handlers; flags untyped body access.
**Why:** Veracode 2025 — Injection at 86%+ fail rate.

### Rule 9 — Auth via Better-Auth / Clerk / Supabase Auth — no custom

**Kind:** `block`
**Statement:** Authentication uses Better-Auth (MIT, self-host) or Clerk (free 50k MAU 2026) or Supabase Auth. Custom session / cookie / JWT auth requires explicit `ADR-SEC-OVERRIDE-AUTH.md` with security-reviewer sign-off.
**Why:** rolling-your-own-auth is the most common breach surface; vibe-coders are most likely to roll their own.

### Rule 10 — Rate limiting on all public endpoints

**Kind:** `block`
**Statement:** Public endpoints (no auth required) MUST have rate limiting. Approved patterns: Upstash Redis sliding window / Cloudflare Rate Limiting / framework-native (Hono rate-limit middleware, FastAPI slowapi).
**Check:** `bequite audit` scans for `app.get('/api/*')` / handlers without rate-limit middleware in scope.
**Why:** vibe-coded MVPs go viral and get DDoS'd; baseline rate-limit is cheap insurance.

### Rule 11 — No `.env` reads in code

**Kind:** `block` (cross-references Iron Law IV)
**Statement:** Code MUST NOT contain `fs.readFile('.env*')`, `open('.env*')`, etc. Use the framework's env loader.
**Why:** vibe-coded apps occasionally do this and accidentally bundle the file.

### Rule 12 — CSRF protection on state-changing endpoints

**Kind:** `block`
**Statement:** POST / PUT / PATCH / DELETE on session-cookie-authenticated routes require CSRF token (double-submit, SameSite=Strict cookies, or framework-native CSRF middleware).
**Check:** `bequite audit` flags state-changing handlers without CSRF middleware in scope.

### Rule 13 — All passwords hashed with Argon2id (not bcrypt by default)

**Kind:** `recommend`
**Statement:** When custom auth is used (despite Rule 9), passwords hashed with Argon2id (preferred 2026) or bcrypt (cost ≥ 12).
**Check:** `bequite audit` greps for `crypto.pbkdf2` / weak hashes.

### Rule 14 — Cookie flags hardened

**Kind:** `block`
**Statement:** Session cookies set with `Secure; HttpOnly; SameSite=Lax` (or `Strict` if no cross-site flow). No cookies without flags.

### Rule 15 — Logging excludes PII / CHD / PHI

**Kind:** `block`
**Statement:** Application logs do NOT contain PII / CHD / PHI / passwords / tokens. Approved: opaque user IDs, request IDs, durations, exit codes. NOT approved: emails, phone numbers, full request bodies.
**Check:** `bequite audit` scans logger configs + log statements.
**Why:** log files leak via S3 misconfiguration; exposure of this data triggers GDPR / HIPAA / PDPL breach notification.

## 3. Stack guidance

### Frontend (vibe-handoff specific)

| Choice | Rationale |
|---|---|
| Next.js (App Router) | Best vibe-coder ergonomics; built-in CSP support; React Server Components reduce client-side attack surface |
| shadcn/ui | Copy-paste; full ownership; avoids supply-chain risk of "themed component library that ships its own deps" |

### Backend

| Choice | Rationale |
|---|---|
| Hono | Smallest; built-in Zod adapter; rate-limit middleware native |
| Next.js API routes | When solo-dev; deploy to Vercel; built-in CSP |

### Database + auth

| Choice | Rationale |
|---|---|
| Supabase | Postgres + Auth + RLS + Storage in one; SOC 2 / ISO 27001; deny-by-default RLS by convention |
| Better-Auth | If self-host preferred; 2FA / passkeys / orgs / RBAC |

### Hosting

| Choice | Rationale |
|---|---|
| Vercel + Supabase | Smallest-ops; vibe-coder-friendly; built-in WAF (Vercel Firewall) |

## 4. Verification (Phase 6 gates added by this Doctrine)

`bequite verify` adds:

1. **All 15 Doctrine rules** scanned by `bequite audit` and clean.
2. **Lite scanner stack** green (Trivy + Semgrep + OSV + secret-scan).
3. **axe-core** zero violations.
4. **Rate-limit smoke test** — 100 rapid requests to public endpoint; expect HTTP 429.
5. **CSP header verified live** via `curl -I` and inspected.
6. **Cookie flags verified live** via response inspection.
7. **CSRF token verified** on state-changing endpoint.
8. **harden-on-deploy gate** green.

## 5. Examples and references

- Veracode 2025 GenAI Code Security Report — https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/
- OWASP Top 10 (Web App) — https://owasp.org/www-project-top-ten/
- OWASP LLM Top 10 (2025) — https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- PhantomRaven supply-chain attack (Koi Security 2025).
- Better-Auth — https://better-auth.com/
- Clerk — https://clerk.com/

## 6. Forking guidance

- `vibe-defense-strict` — bumps Rule 1 threshold to MEDIUM+ block (default is HIGH+); for high-stakes vibe-handoffs.
- `vibe-defense-frontend-only` — drops Rules 8-14 (backend-specific); for frontend-only vibe-coded projects.
- `vibe-defense-mena` — overlays `mena-pdpl` Doctrine for region-specific compliance.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. 15 rules. Default for audience: vibe-handoff projects.
```
