# DevOps & cloud safety

**Status:** active
**Adopted:** 2026-05-11 (alpha.2)
**Reference:** `.claude/skills/bequite-devops-cloud/SKILL.md`, AUTO_MODE_STRATEGY.md

---

## The principle

Production safety overrides convenience. When in doubt, pause.

Most outages come from one of five causes:
1. Env var missing / wrong in production
2. Migration deployed before backward-incompatible code
3. Manual server edit nobody else knew about
4. Missing rollback path
5. No monitoring → customer discovers the bug first

BeQuite's DevOps discipline encodes the patterns that prevent these and the **hard human gates** that block irreversible mistakes.

---

## Hard human gates (production-touching changes)

For projects with shared / production infrastructure, the agent **MUST pause** for explicit user confirmation at:

| # | Gate | Why |
|---|---|---|
| 1 | Destructive file deletion (`rm -rf` on tracked code) | Recovery requires git surgery |
| 2 | Database migration against shared / production DBs | Schema changes can lock tables / cause downtime |
| 3 | Production server change (SSH, systemd, firewall) | Each change can take prod down |
| 4 | VPS / Nginx / SSL change | Misconfigured TLS = customers see security warnings |
| 5 | Paid service activation | Spending money is irreversible |
| 6 | Secret / key handling (rotation, generation) | Wrong rotation = service outage |
| 7 | Changing auth / security model | Auth bugs cascade |
| 8 | Changing project architecture | Cross-cutting, expensive to revert |
| 9 | Deleting old implementation with active callers | Breaks unrelated code paths |
| 10 | Scope contradiction | Task contradicts locked SCOPE.md |

Plus 7 more in `/bq-auto` (cost / time ceilings, banned weasel words, 3-failure threshold, UI variant winner selection, release git push/tag, manual-approval flag).

The agent can:
- **Show** the user the command(s) to run
- **Plan** the change with a rollback path
- **Verify** the plan against tool neutrality + decision section requirements

The user runs the actual command.

---

## Environment hierarchy

Three at minimum:

| Env | What |
|---|---|
| **Local** | Developer's machine; `.env.local` |
| **Preview** | Per-PR deploy; same shape as production, different data + secrets |
| **Production** | Real users |

Optional fourth — staging — when team size > 3 or data migrations are common.

Rules:
- Same code on all environments (no env-specific branches in source)
- Different config (env vars, feature flags)
- Different data (never share prod data with preview)
- Different secrets (never share prod secrets with preview)

---

## CI gates (every PR)

Required:
- Lint
- Typecheck (`tsc --noEmit` / `mypy`)
- Unit tests
- Integration tests
- Build succeeds
- Lockfile unchanged OR explicitly approved

Optional (per project):
- E2E (Playwright)
- Bundle size check
- Lighthouse CI
- OSV / Snyk scan
- Accessibility (axe-core)

Block merge on any required gate failing.

---

## Deployment patterns

### Default: trunk-based + auto-deploy on main

- `main` is always deployable
- Merge to main → auto-deploy to production
- No long-lived feature branches

### When NOT to auto-deploy

- DB migration in the commit → require human approval
- Schema-breaking change → require human approval
- New env var required → require human approval (var must be set in production FIRST)
- Production-touching infra (Terraform, etc.) → require human approval

Configure your host (Vercel / Fly / Render / etc.) to pause production deploys after build, requiring a human click.

---

## Rollback strategy

Every release has a documented rollback. The three types:

1. **Code-only rollback** — `git revert <commit>` + redeploy. Fast.
2. **Code + reversible migration** — code revert + reverse migration. Plan the reverse before deploying forward.
3. **Code + forward-only migration** — can't reverse cleanly. Roll forward to a fix.

The hierarchy:
- **Always design migrations forward-only**
- **Always test rollback before deploying** (staging deploy → staging revert → confirm both work)

Document in `IMPLEMENTATION_PLAN.md` §14.

---

## Secrets discipline

### Never commit
- `.env*` files
- Hardcoded API keys
- Database / OAuth / Stripe credentials anywhere in repo

### Where to store
- Local dev: `.env.local` (gitignored)
- CI: GitHub Actions Secrets / GitLab CI Variables
- Production: host's secrets manager
- Multi-environment teams: Doppler or 1Password Secrets Automation (candidates per tool neutrality)

### Rotation
- Quarterly minimum
- Immediately after suspected leak / engineer offboarding
- Documented in `SECURITY.md`

### Scanning

PreToolUse-style scan for AWS keys, GitHub tokens, Slack tokens, Stripe, generic secret patterns. Tools: trufflehog, gitleaks (candidates).

---

## Monitoring (the 3 pillars)

| Pillar | Recommended candidates (not defaults) |
|---|---|
| **Errors** | Sentry, GlitchTip, Honeybadger |
| **Uptime** | Better Stack, Pingdom, Uptime Robot |
| **Logs** | Axiom, Datadog, host-native |
| **Traces** | OpenTelemetry (vendor-neutral) |

Per tool neutrality, every name is a candidate. Pick what fits the project.

---

## Cost ceilings

Every production deployment has cost ceilings:

- Per-service: alert at 80% of plan
- Per-user (LLM): max tokens per user per day; hard cap on runaway loops
- Per-job: max duration, max memory; kill jobs that exceed

Document in `IMPLEMENTATION_PLAN.md` §12.

---

## IaC (Infrastructure as Code)

For v1, prefer the simplest tool that fits:
- Vercel CLI + dashboard (Vercel projects)
- `fly.toml` (Fly.io)
- Terraform (multi-resource AWS/GCP/Azure) — per tool neutrality, a candidate
- Pulumi (TypeScript-native) — candidate

Avoid:
- Manually clicking through cloud dashboards (drift accumulates)
- Custom shell scripts (no idempotency, no plan)
- Premature Kubernetes (almost never needed in v1)

For Terraform: commit state? **Never** — use remote state. Run `plan` in PR; `apply` after human approval. **Never** `terraform destroy` without explicit user OK.

---

## Server / VPS safety

For projects touching their own server / VPS:

### Hard human gates — never auto-execute

- SSH into production server
- `rm -rf` on production filesystem
- `systemctl stop/restart/disable` on production services
- Edits to `/etc/` config
- User add / delete on server
- Firewall rule changes
- DNS record changes
- TLS certificate operations

The agent can **read** (logs via SSH, service status, disk / memory) for debugging. It cannot **modify** without user OK.

---

## Database migration approval

For projects with shared DBs (preview + prod, or multiple developers):

### Pause before
- Any migration not yet reviewed
- Any migration with `DROP`, `ALTER COLUMN TYPE`, `RENAME`
- Any migration during business hours
- Migrations > 1 minute estimated

The agent can:
- Generate the migration
- Test against a fresh local DB
- Test the rollback path
- Print the command for user to run

The user runs the actual `migrate up` against production.

---

## Deployment runbook (template)

Every project ships `docs/runbooks/DEPLOY.md`:

```markdown
# Deploy runbook

## Pre-deploy
- [ ] All CI green
- [ ] CHANGELOG `[Unreleased]` reviewed
- [ ] Migration (if any) reviewed
- [ ] Env vars (new) set in production
- [ ] Rollback plan written

## Deploy
1. git tag v<X.Y.Z>
2. git push origin v<X.Y.Z>
3. CI builds + publishes
4. Monitor Sentry for 30 min

## Rollback
1. git revert <commit>
2. Re-deploy

## Post-deploy
- [ ] Error rate within baseline
- [ ] Uptime monitor green
- [ ] Smoke test critical flow
- [ ] Status page updated if user-visible
```

---

## See also

- `.claude/skills/bequite-devops-cloud/SKILL.md` — full skill spec
- AUTO_MODE_STRATEGY.md — 17 hard human gates
- ADR-002 — mandatory workflow gates
- TOOL_NEUTRALITY.md — IaC / monitoring / secrets tools are candidates
