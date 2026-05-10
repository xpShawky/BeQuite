---
adr_id: ADR-014-iron-law-x-operational-completeness
title: Iron Law X — Operational completeness; Constitution v1.2.0 → v1.3.0
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
constitution_version: 1.2.0   # decided UNDER 1.2.0; output is 1.3.0
related_articles: [II, VI, X]
related_doctrines: [default-web-saas, vibe-defense, ai-automation]
---

# ADR-014: Iron Law X — Operational completeness

> Status: **accepted** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

The signature failure mode of AI vibe-coding (per Ahmed's lived experience): the agent reports "feature added" or "bug fixed" — but the change is **committed but not operational**. Examples:

- Backend route added → committed → but the dev server wasn't restarted, so the route 404s.
- Frontend env var changed → committed → but Next.js build wasn't refreshed, so the old value is bundled.
- Docker compose service edited → committed → but `docker compose up -d --build` never ran, so the running container is the old one.
- Database migration written → committed → but `alembic upgrade head` (or `prisma migrate deploy`) never ran, so the schema is unchanged.
- Frontend component added a new API call → committed → but the backend route doesn't exist yet, so it 500s on first click.
- React component edited → committed → but Vite HMR is stale; user reloads to find the same broken state.
- Dependency added to package.json → committed → but `npm install` never ran, so import fails at runtime.
- nginx config edited → committed → but `nginx -s reload` never ran.

Article II (Verification before completion) covers tests passing. But "tests pass" ≠ "operationally live" — a test against the un-restarted server might pass on the unchanged route while the new route 404s in production. Article VI (Honest reporting) requires "what was tested" but doesn't explicitly demand "the running system reflects the change."

The vibecoder's correct expectation: **when BeQuite says "added", they should be able to use it immediately, without restart-the-build / recompose-docker / re-migrate-DB friction.**

## Decision

Add **Article X — Operational completeness** to the Constitution as an Iron Law. Bump Constitution `1.2.0 → 1.3.0` (minor; additive only — no Iron Law removed or relaxed).

### Article X — Operational completeness

> When the agent reports a change as complete, the running system **must reflect the change**. The agent is responsible for the post-edit operational steps:
>
> 1. **Build refresh.** If the change requires a build step (next build / vite build / cargo build / tsc / docker build / etc.), the build MUST be re-run before reporting completion. If the build fails, the work is NOT complete.
> 2. **Service restart.** If the change touches a running service (web server, API server, worker, queue consumer, docker compose stack, k8s deployment), the service MUST be restarted (or the agent MUST verify hot-reload took effect) before reporting completion.
> 3. **Wire-up confirmation.** If a backend endpoint is added or changed, the agent MUST hit the endpoint and verify the response (curl / fetch from a test) before reporting completion. If a frontend component calls a new endpoint, the agent MUST verify the call succeeds end-to-end.
> 4. **Migration applied.** Database schema changes mean the migration MUST run against the current dev DB before reporting completion. Production migrations are one-way doors (Article IV); pause + ask.
> 5. **Dependencies installed.** When `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` is edited, the matching install command MUST run (and lockfile commit) before reporting completion.
> 6. **Config refreshed.** Environment variables, nginx configs, systemd units, etc. MUST be hot-reloaded or the service restarted before reporting completion.
> 7. **Cache busted.** If a CDN or browser cache is in front of the change, the cache MUST be invalidated (or the resource fingerprinted) before reporting completion.

### Banned report patterns (Article VI extension)

The agent is FORBIDDEN to use these phrasings when the named follow-up step is the user's responsibility:

- ❌ "Added the route — restart your server to use it"
- ❌ "Updated the schema — run the migration"
- ❌ "Edited the config — rebuild the docker image"
- ❌ "Installed the package — run `npm install`"
- ❌ "Changed the env — restart the dev server"
- ❌ "Ready once you redeploy"

If the agent CANNOT complete the operational step (e.g. it's a one-way door, or it requires credentials the agent doesn't have, or the service is on a remote host the agent can't reach), the agent MUST:
1. Pause + report exactly what the user must do
2. NOT report the change as complete
3. Stay in `BLOCKED` state until the user signals completion

### When the operational step IS a one-way door (Article IV)

Per Article IV, certain operations always pause for human approval:
- Production deploy (`vercel --prod`, k8s prod cluster, etc.)
- Production DB migration
- Force push to protected branch
- Public package publish (PyPI, npm)

For these, Article X requires the agent to **prepare** the change such that the human's single approval action delivers an operationally-complete result. Specifically:
- Local dev environment is fully restarted + verified.
- Staging environment (if exists) is operationally complete.
- The single human action is well-documented (e.g. "Run `pnpm deploy:prod` after reviewing the staging URL").

### Hook implementation (lands v0.16.x+)

A new PostToolUse hook `posttooluse-operational-check.sh` runs after Edit/Write operations on:
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`
- `next.config.*` / `vite.config.*` / `astro.config.*`
- `docker-compose.yml` / `Dockerfile` / `dockerfile`
- `nginx.conf` / `*.conf`
- DB migration files
- env files (per Article IV — never read; but their existence-changes are flagged)

The hook prints a checklist of operational steps required and exit-code-1 (advisory). It does NOT block (Article X is the agent's responsibility, not a hook gate). Auto-mode (v0.10.0+) reads the checklist and runs each step automatically before phase exit.

### Existing hook impact

`stop-verify-before-done.sh` (v0.3.0) already enforces banned-weasel-words on completion messages. v0.16.x+ extends its forbidden-phrase list with the Article X banned report patterns above.

## Self-attestation

For every "change complete" report, the agent appends:

```markdown
## Operational completeness (Article X)

- [x] Build refresh: <command run + exit code> OR (n/a — no build needed)
- [x] Service restart: <command run> OR (n/a — service auto-reloads)
- [x] Wire-up confirmed: <test command + status>
- [x] Migration applied: <command run> OR (n/a — no migration)
- [x] Dependencies installed: <command run> OR (n/a — no dep change)
- [x] Config refreshed: <command run> OR (n/a — no config change)
- [x] Cache busted: <command run> OR (n/a — no cache layer)

The running system reflects this change. The vibecoder can use it immediately.
```

When ANY box is unchecked AND not-`n/a`, the agent MUST NOT report the change as complete.

## Constitution amendment summary

- **Constitution version:** 1.2.0 → 1.3.0 (additive only).
- **New Iron Law:** Article X — Operational completeness.
- **Modified hook:** `stop-verify-before-done.sh` extends banned-phrase list (v0.16.x+).
- **New hook:** `posttooluse-operational-check.sh` (v0.16.x+).
- **Auto-mode integration:** auto-mode reads the operational checklist + runs each step automatically before phase exit (v0.16.x+).

## Status: accepted (2026-05-10)

Implementation:
- v0.16.0: Constitution amendment text + ADR + self-attestation pattern documented.
- v0.16.1+: Hook extension + new posttooluse hook + auto-mode integration.

## Cross-references

- Constitution: `.bequite/memory/constitution.md`
- Article II (Verification before completion): same file
- Article VI (Honest reporting): same file
- Article IV (Security & destruction — one-way doors): same file
- Existing hooks: `skill/hooks/`
- Auto-mode: `cli/bequite/auto.py`
