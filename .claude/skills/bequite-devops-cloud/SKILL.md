---
name: bequite-devops-cloud
description: DevOps + cloud procedures — CI/CD pipelines, preview deploys, rollback strategy, env-var management, secrets discipline, monitoring + alerting, cost ceilings, IaC patterns, server/VPS safety, database migration approval, blue-green + canary, runbooks. Hard human gates for production-touching changes. Loaded by /bq-plan, /bq-feature, /bq-verify, /bq-release.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Bash
---

# bequite-devops-cloud — production safety

## Why this skill exists

Most outages come from one of five causes:
1. Env var missing / wrong in production
2. Migration deployed before backward-incompatible code
3. Manual server edit nobody else knew about
4. Missing rollback path
5. No monitoring → discovered by customer first

This skill encodes the patterns + hard gates that prevent these.

**Production safety overrides convenience.** When in doubt, pause.

---

## Environment hierarchy

Three at minimum:
- **Local** — developer's machine; `.env.local`
- **Preview** — per-PR deploy; same shape as production, different data
- **Production** — real users

Optional fourth:
- **Staging** — pre-production with real-shape data; useful when team > 3 or data migrations are common

Rules:
- Same code on all environments (no env-specific branches in source)
- Different config (env vars, feature flags)
- Different data (never share prod data with preview)
- Different secrets (never share prod secrets with preview)

---

## CI gates (every PR)

Required:
- Lint (eslint, ruff, clippy)
- Typecheck (tsc, mypy, cargo check)
- Unit tests
- Integration tests
- Build succeeds
- Lockfile unchanged OR explicitly approved

Optional (per project):
- E2E tests (Playwright walks)
- Bundle size check (size-limit)
- Lighthouse CI for web pages
- OSV / Snyk security scan
- Accessibility scan (axe-core)

Block merge on:
- Any required gate failing
- Lockfile changed without approval label

---

## Preview deploys

Every PR gets a preview URL:
- Same build process as prod
- Different DB (per-PR or shared preview DB)
- Different env vars (preview-tier, e.g. test Stripe keys)
- Auto-cleanup after PR closes

Vercel does this natively. For self-host:
- Cloudflare Pages does this
- Render does this
- DIY: GitHub Actions + ephemeral container + ngrok / tunnel

---

## Production deployment

### Default: trunk-based + auto-deploy on main

- `main` is always deployable
- Merge to main → auto-deploy to production
- No long-lived feature branches

### When NOT to auto-deploy

- Database migration in this commit → require human approval
- Schema-breaking change → require human approval
- New env var required → require human approval (var must be set in production FIRST)
- Production touching infra (Terraform changes, etc.) → require human approval

### Approval-gated deploys (Vercel + similar)

Configure: deploys to production paused after build, require human click.

For zero-trust shops: every prod deploy is human-approved.

---

## Rollback strategy

Every release has a rollback plan documented. The three rollback types:

1. **Code-only rollback** — `git revert <commit>` and redeploy. Fast, safe IF no DB migration.

2. **Code + reversible migration** — code revert + reverse migration script. Plan the reverse before deploying forward.

3. **Code + forward-only migration** — can't reverse cleanly. Roll forward to a fix (don't try to roll back the DB).

The hierarchy:
- **Always design migrations forward-only** (per `bequite-database-architect`)
- **Always test rollback path before deploying** — at minimum, deploy the change to staging, then deploy the revert to staging, confirm both work

Document in IMPLEMENTATION_PLAN §14.

---

## Env var management

### Per environment
- Local: `.env.local` (gitignored)
- Preview: host's preview env vars (Vercel, Netlify, etc.)
- Production: host's production env vars

### Template file (committed)
`.env.example` lists every required var with a comment explaining what it does:
```
# Postgres connection string (Supavisor transaction-mode for serverless)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Better-Auth secret — 32+ random chars
AUTH_SECRET=

# Resend API key for email delivery
RESEND_API_KEY=
```

### Adding a new var
Order matters:
1. Add to `.env.example`
2. Add to production secrets store
3. Add to preview secrets store
4. Then merge the code that reads it

If you skip step 2 or 3, prod / preview breaks on deploy.

### Secret rotation
- Quarterly minimum
- Immediately after suspected leak
- Immediately after engineer offboarding
- Documented in `SECURITY.md`

---

## Monitoring + alerting

The three pillars (also in `bequite-backend-architect` §observability):

### Errors → Sentry
- Free tier: 5K errors/month
- Configure `beforeSend` to scrub PII
- Set up Slack / email alerts on new error types
- Triage daily; ignore < error_count_p99 baseline

### Uptime → Better Stack / Pingdom / Uptime Robot
- Probe every 60s from 3+ regions
- Alert if 2+ regions fail (avoid one-region flakes)
- Status page automatic (Better Stack does this)

### Logs → Axiom / Datadog / host-native
- Structured JSON
- 30-day retention minimum
- Search before guessing — don't fix bugs by intuition

### Custom metrics
- Stripe revenue → daily Slack post
- Sign-up conversion → daily Slack post
- p95 latency by route → weekly review

Use Discord / Slack webhook for low-noise alerts; PagerDuty for actual on-call (only if you have an on-call rotation).

---

## Cost ceilings

Every production deployment has a cost ceiling.

### Per-service ceilings
- Vercel function execution: alert at 80% of plan
- Database storage: alert at 80%
- Email sending volume: alert at 80%
- LLM API spend: hard cap (cut off requests beyond)

### Per-user ceilings
For LLM features: max tokens per user per day. Don't let one user burn $1000 of API spend.

### Per-job ceilings
Background jobs: max duration, max memory. Kill jobs that exceed.

---

## IaC patterns

For v1, prefer:
- **Vercel CLI + dashboard** — for Vercel-hosted projects
- **fly.toml** — for Fly.io
- **Terraform** — for AWS/GCP/Azure if multi-resource
- **Pulumi** — for TypeScript-native IaC

Avoid:
- Manually clicking through cloud dashboards (drift accumulates)
- Custom shell scripts (no idempotency, no plan)
- Premature Kubernetes (almost never needed in v1)

For Terraform:
- Commit state? **Never** — use remote state (Terraform Cloud / S3+DynamoDB)
- Run `plan` in PR; `apply` after human approval
- Never `terraform destroy` without explicit human confirmation

---

## Server / VPS safety (hard human gate)

For projects touching their own server / VPS (not managed platforms):

### Hard human gates — never auto-execute

- SSH into production server
- `rm -rf` anywhere on production filesystem
- `systemctl stop/restart/disable` of production services
- Edits to `/etc/` config
- User add / delete on server
- Firewall rule changes
- DNS record changes
- TLS certificate operations

**The agent MUST pause and ask the user to run these themselves.** The agent can show the command; the user runs it.

### Acceptable agent actions on a VPS

- Read logs via SSH (`tail`, `journalctl`) for debugging
- Read service status (`systemctl status`)
- Read disk / memory (`df`, `free`, `top`)
- Read network state (`ss`, `netstat`) — without making changes

---

## Database migration approval (hard human gate)

For projects with a shared DB (preview + prod both touching it, OR multiple developers):

### Migrations against shared / production DB

**Pause for human approval before:**
- Any migration that's been generated but not reviewed
- Any migration with `DROP`, `ALTER COLUMN TYPE`, `RENAME`
- Any migration during business hours (define per project)
- Migration > 1 minute estimated duration

The agent can:
- Generate the migration
- Test against a fresh local DB
- Test rollback path
- Print the command for the user to run

The user runs the actual `migrate up` against production.

### Migrations against feature-branch DB (per-PR)

Auto-run is fine. Each PR gets its own scratch DB.

---

## Deployment runbooks

Every project ships a deployment runbook at `docs/runbooks/DEPLOY.md`:

```markdown
# Deploy runbook

## Pre-deploy
- [ ] All CI green on the commit
- [ ] CHANGELOG.md `[Unreleased]` reviewed
- [ ] Migration (if any) reviewed
- [ ] Env vars (if new) set in production
- [ ] Rollback plan written

## Deploy
1. Tag: `git tag v<X.Y.Z>`
2. Push tag: `git push origin v<X.Y.Z>`
3. CI builds + publishes
4. Monitor Sentry for 30 minutes

## Rollback (if needed)
1. `git revert <commit>`
2. Re-deploy

## Post-deploy
- [ ] Sentry error rate within baseline
- [ ] Uptime monitor green
- [ ] Spot-check critical user flow
- [ ] Update status page if user-visible
```

---

## When activated by /bq-plan

Write §12 (deployment + DevOps) in detail:
- Environment hierarchy
- CI gate list
- Deployment trigger (auto on main vs approval-gated)
- Rollback strategy per change type
- Monitoring stack
- Cost ceilings
- Runbook outline

---

## When activated by /bq-verify

Run the deploy-readiness checklist:
- All CI gates pass
- Lockfile committed
- Env vars documented in `.env.example`
- Migration reviewed (if present)
- Rollback path verified

---

## When activated by /bq-release

Coordinate with `bequite-release-gate`:
- Bump version per semver
- Move CHANGELOG `[Unreleased]` → `[vX.Y.Z]`
- Print git commands
- Hard gate: user runs `git push` and `git tag` themselves
- Never auto-push tags
- Never auto-deploy from /bq-release

---

## When activated by /bq-fix

DevOps bug types:
- **Deployment / CI bug** → check workflow YAML, runner logs, env vars
- **Configuration / env bug** → check var name typos, path separators (Windows vs Unix), permission bits
- **Server / VPS issue** → diagnose only; do NOT modify; print commands for user

---

## What this skill does NOT do

- Manage production database content (use `bequite-database-architect`)
- Real incident response (out of scope; use a runbook + page on-call)
- Cost optimization beyond ceilings (use a FinOps consultant for serious bills)
- Cloud architecture certification (AWS / GCP / Azure cert prep is out of scope)
