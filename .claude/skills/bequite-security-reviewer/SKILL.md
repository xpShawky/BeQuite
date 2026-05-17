---
name: bequite-security-reviewer
description: Security review procedures — OWASP Web App Top 10 (2021/2025), OWASP LLM Top 10 (2025), supply-chain defense (PhantomRaven / Shai-Hulud), secrets handling, auth flow review, input validation, CORS / CSP, dependency CVE scanning, threat modeling, penetration-readiness. Loaded by /bq-plan, /bq-feature, /bq-fix, /bq-audit, /bq-review.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Bash
---

# bequite-security-reviewer — Skeptic mode

## Why this skill exists

Most security bugs aren't sophisticated. They're forgotten basics: hardcoded secret, missing input validation, CSRF token absent, leaky error message, dependency CVE that's been patched for 6 months.

This skill encodes the basics so they don't get forgotten.

For real penetration testing, hire a pentester (Cobalt.io, HackerOne, or independent). This skill makes the easy bugs disappear; it doesn't replace human red-teaming.

---

## OWASP Web App Top 10 (2021 stable, 2025 draft)

For each application, map controls:

| # | OWASP item | Common cause | Control |
|---|---|---|---|
| A01 | Broken Access Control | missing auth check on endpoints | enforce auth middleware on every route; deny-by-default |
| A02 | Cryptographic Failures | hardcoded secrets, weak hashing | env vars; bcrypt/scrypt/argon2 for passwords; TLS everywhere |
| A03 | Injection | string-concatenated SQL, XSS, command injection | parameterized queries; sanitize HTML on output; never `exec()` user input |
| A04 | Insecure Design | missing rate limit, missing CSRF token | rate limits; SameSite cookies; CSRF tokens on state-changing forms |
| A05 | Security Misconfiguration | dev mode in prod, verbose errors | env-specific configs; structured error responses |
| A06 | Vulnerable Components | outdated lib with CVE | Dependabot / Renovate; OSV scanner in CI |
| A07 | Identification + Auth Failures | brute-force, session fixation | rate-limit auth; rotate session on login; MFA option |
| A08 | Software + Data Integrity | unverified packages, unsigned releases | lockfile; package-signing where supported |
| A09 | Logging + Monitoring Failures | no logs, no alerts | structured logs; Sentry; uptime monitor |
| A10 | SSRF | server makes user-controlled URL fetches | allowlist outbound URLs; never let users specify internal IPs |

For each item in the project's plan / code, mark **covered** or **at-risk**.

---

## OWASP Top 10 for LLM Applications (2025 final)

For projects that include LLM features:

| # | LLM-specific risk | Control |
|---|---|---|
| LLM01 | Prompt Injection | sanitize user input before LLM; never let untrusted content become instructions |
| LLM02 | Insecure Output Handling | treat LLM output as untrusted; validate before executing / rendering |
| LLM03 | Training Data Poisoning | (mostly a vendor concern; verify training-data source if fine-tuning) |
| LLM04 | Model Denial of Service | rate-limit per user + cost ceilings; max context length enforcement |
| LLM05 | Supply Chain | verify model provider; pin model versions; check provider's terms |
| LLM06 | Sensitive Info Disclosure | never put secrets in prompts; never log full prompts in production |
| LLM07 | Insecure Plugin Design | for MCP / tool use — validate tool args; rate-limit; never give shell access to LLM |
| LLM08 | Excessive Agency | scope tool permissions; require human-in-the-loop for destructive ops |
| LLM09 | Overreliance | flag uncertainty in LLM outputs; let user audit / correct |
| LLM10 | Model Theft | API keys via OAuth / OIDC where possible; rotate; rate-limit |

---

## Supply-chain defenses (2025-2026 lessons)

### PhantomRaven (Aug-Oct 2025)

Threat: malicious npm packages with typo-squatted names.

Defense:
- Before `npm install <pkg>`, verify `<pkg>` exists on npmjs.com
- Cross-check against project allowlist (`references/package-allowlist.md`)
- For new deps not on allowlist → flag for user approval
- Audit `package.json` against `package-lock.json` (no phantom entries)

### Shai-Hulud (broader, 2025)

Threat: 700+ packages compromised via maintainer-account takeover.

Defense:
- Pin to exact versions for security-critical deps (auth, crypto, payments)
- Commit `package-lock.json` / `bun.lockb` / `pnpm-lock.yaml`
- Enable Dependabot or Renovate but auto-merge OFF
- 2FA on registry accounts (org-level requirement)

### Lockfile discipline

- ALWAYS commit lockfile
- ALWAYS install with frozen lockfile in CI (`npm ci`, `bun install --frozen-lockfile`, `pnpm install --frozen-lockfile`)
- Never `npm install` in production deployments — only `npm ci`

---

## Secrets handling

### Never commit:
- `.env*` files (gitignore them)
- Hardcoded API keys in code
- Stripe / OAuth / database credentials anywhere in repo

### Where to store:
- **Local dev**: `.env.local` (gitignored)
- **CI**: GitHub Actions Secrets / GitLab CI Variables / etc.
- **Production**: host's secrets manager (Vercel env vars, AWS Secrets Manager, Doppler, Infisical)
- **Multi-environment teams**: Doppler or 1Password Secrets Automation

### Rotation
- Document each secret's rotation policy in `SECURITY.md`
- Rotate quarterly minimum
- Rotate immediately after a leak / suspected leak / engineer offboarding

### Scanning

PreToolUse hook: scan diffs for secret-shaped strings:
- AWS keys: `AKIA[0-9A-Z]{16}`
- GitHub tokens: `gh[pousr]_[A-Za-z0-9_]{36,}`
- Slack tokens: `xox[baprs]-[A-Za-z0-9-]+`
- Stripe: `sk_(test|live)_[A-Za-z0-9]{24,}`
- Generic: `(api|secret|password|token|jwt)[-_]?(key|token)?[\s]*=[\s]*['""][^'""]+`

Block commits matching these patterns unless explicitly allowlisted.

Tools: `trufflehog`, `gitleaks` (both have CI integrations).

---

## Auth flow review

### Sign-up
- Email verification required (or social provider)
- Rate-limited (5 / 15min per IP)
- No "user already exists" leak — always "if account exists, we sent an email"
- Password requirements: 12+ chars, no other complexity rules (NIST 2017+)

### Sign-in
- Rate-limited (5 / 15min per account + per IP)
- Generic error message ("invalid credentials") regardless of cause
- Session rotation on login (new session ID)
- Optional MFA (TOTP via `otplib`; SMS only as fallback)

### Sign-out
- Server-side session invalidation (not just client-side cookie clear)

### Password reset
- Time-limited token (15 min max)
- Single-use
- Email to the address ON FILE (never let user specify a different email)
- Generic error message ("if account exists, email sent")

### Session management
- HttpOnly cookies
- Secure flag (HTTPS only)
- SameSite=Lax (default) or Strict (for sensitive apps)
- Reasonable lifetime (7-30 days for low-sensitivity, 1 day for high)
- Refresh tokens stored server-side, never in localStorage

Recommended 2026 stacks:
- **Better-Auth** — open source, modern, TypeScript-native
- **Clerk** — managed, 50K MAU free, fastest setup
- **Auth0** — enterprise; expensive but proven
- **Supabase Auth** — built in if you're on Supabase
- **NextAuth (next-auth v5)** — fine for Next.js-only

Avoid:
- Custom auth (only if you have a strong reason)
- Firebase Auth for new projects (Google may sunset; complex pricing)

---

## Input validation discipline

Every public API endpoint:
- Validates body, query, path params with Zod / Valibot / Pydantic
- Bounds numeric inputs (no `parseInt(id)` without max)
- Length-limits strings (no unbounded text fields)
- MIME-type checks file uploads
- Content-type matches extension on uploads
- HTML sanitizes any user-provided HTML (DOMPurify on output, not input)

Never:
- Trust client validation alone
- Use `eval()` / `Function()` on user input
- Pass user input to shell (`exec`, `spawn` with string args)

---

## CORS + CSP

### CORS
- Allow specific origins, not `*` for credentialed requests
- For public APIs (no credentials), `*` is fine
- `Access-Control-Allow-Credentials: true` requires explicit origin (not `*`)

### CSP (Content Security Policy)
Strict default:
```
default-src 'self';
script-src 'self' 'wasm-unsafe-eval';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
connect-src 'self' https://api.yourservice.com;
frame-ancestors 'none';
form-action 'self';
base-uri 'self';
```

Loosen only when needed, with documented reason.

---

## CVE scanning in CI

For each release:
- **OSV scanner** — npm, Python, Go, Rust, more
- **npm audit** / **bun audit** / **pip-audit** as fallback
- **Snyk** — commercial, deeper analysis (free tier exists)

Block merge on:
- Critical severity, unpatched
- High severity, patched > 30 days ago

Warn on:
- Medium severity
- High severity, recently patched (< 30 days)

---

## Threat modeling (one-page version)

For v1, write a one-page threat model in IMPLEMENTATION_PLAN §11:

```markdown
## Threat model

### Assets
- User data (PII per GDPR / CCPA / PDPL)
- Auth credentials
- Payment data (if PCI scope)
- Customer-uploaded files

### Threats (STRIDE)
- Spoofing: <how attacker impersonates a user; control: MFA, session rotation>
- Tampering: <how data gets modified in transit; control: HTTPS, signed cookies>
- Repudiation: <how user denies an action; control: audit log per write>
- Information disclosure: <leak vectors; control: no PII in logs, generic errors>
- Denial of service: <DoS vectors; control: rate limits, Vercel Firewall>
- Elevation of privilege: <how to gain admin; control: deny-by-default, role checks>

### Trust boundaries
- Browser → app (untrusted input)
- App → DB (trusted; SQL injection prevention via parameterized queries)
- App → 3rd party (trusted by config; outbound allowlist for SSRF)

### Out of scope for v1
- Defenses against state-level actors (out of league for solo founders)
- Real-time intrusion detection (use a SIEM later)
```

---

## When activated by /bq-plan

Write §11 (security) in the plan:
- OWASP Top 10 mapping (which items apply, how covered)
- Threat model (one-page STRIDE)
- Secret handling per environment
- Auth flow specifics
- Rate limits per endpoint

---

## When activated by /bq-feature

For each feature touching auth, payments, PII, file uploads:
- Run the OWASP checklist for the relevant categories
- Add rate limit if new public endpoint
- Validate inputs (Zod schema)
- Audit log the action

---

## When activated by /bq-fix

Security-specific bug types:
- **Security vulnerability** → highest priority; fix smallest patch; rotate any leaked secret; add regression test
- **Auth bug** → audit the surrounding flow; bad auth bugs come in families

---

## When activated by /bq-audit

Run the comprehensive security audit:
1. Scan repo for hardcoded secrets (trufflehog / gitleaks)
2. Scan deps for CVEs (osv-scanner)
3. Verify lockfile present + committed
4. Check `.gitignore` covers `.env*`
5. Read every API route — does it have auth middleware?
6. Read every form — does it have CSRF token?
7. Check error responses — do they leak stack traces?
8. Verify rate limits on auth endpoints

Flag findings by severity (Critical / High / Medium / Low).

---

## When activated by /bq-review

For each diff:
- New API route → has auth + rate limit?
- New user input → validated server-side?
- New secret → handled via env / secrets manager?
- New dependency → on allowlist? On OSV scanner?
- New SQL → parameterized?
- New HTML output → sanitized?

---

## What this skill does NOT do

- Real penetration testing (hire a pentester)
- Compliance certification (SOC 2, ISO 27001 — hire auditors)
- Incident response (use `engineering:incident-response` skill if available)
- Forensic analysis (out of scope)

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (Better-Auth, Clerk, Auth0, NextAuth, Supabase Auth, trufflehog, gitleaks, OSV scanner, Snyk, Dependabot, Renovate, Doppler, Infisical, AWS Secrets Manager, DOMPurify, Zod, Valibot, Pydantic, otplib, etc.) is an EXAMPLE, not a mandatory default.**

The OWASP coverage map + supply-chain defenses + secrets discipline + auth flow controls are **universal security rules**. Specific tool picks are candidates per project.

**Do not say:** "Use Better-Auth."
**Say:** "Better-Auth is one candidate for self-hosted auth. Compare against Clerk (managed), Supabase Auth (built-in if on Supabase), NextAuth/Auth.js, or Auth0 (enterprise) based on this project's hosting, scale, team expertise, and budget. Use it only if it fits."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## When NOT to use this skill (alpha.15)

- The task at hand doesn't touch this skill's domain — defer to the right specialist skill
- A faster / simpler skill covers the same need — pick the simpler one and document why
- The skill's core invariants don't apply to the current project (e.g. regulated-mode rules on a prototype)
- The command that would activate this skill is already running with another specialist that fits better

If unsure, surface the trade-off in the command's output and let the user decide.

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected (not just glanced at)
- [ ] No banned weasel words in any completion claim — `should`, `probably`, `seems to`, `appears to`, `might`, `hopefully`, `in theory`
- [ ] Any tool / library / framework added during this run has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met (or honestly reported as PARTIAL / FAIL)
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended for the run
- [ ] Memory state files (LAST_RUN, WORKFLOW_GATES, CURRENT_PHASE) updated when gate state changed

If any item fails, do not claim done — report PARTIAL with the specific gap.
