---
name: bequite-devops-cloud
description: Use when a task touches CI workflows, deploys, environments, env vars and secrets, containers, infrastructure code, monitoring, cost limits, a VPS or server, or a production migration, or when a build or deploy fails. Hardens CI (SHA pins, least-privilege tokens, OIDC), gates production behind human approval, and keeps every change reversible.
last_verified: 2026-11-21
sources:
  - https://docs.github.com/en/actions/reference/security/secure-use (read 2026-11-21) SHA pins, token scope, script injection, OIDC
  - https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments (read 2026-11-21) required reviewers, env secrets
  - https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction (read 2026-11-21) moved tag leaked secrets
  - https://docs.docker.com/build/building/best-practices/ (read 2026-11-21) multi-stage, digests, non-root
  - https://dora.dev/guides/dora-metrics/ (read 2026-11-21) five delivery metrics
  - https://sre.google/workbook/canarying-releases/ (read 2026-11-21) canary vs control
  - https://12factor.net/config (read 2026-11-21) config in the environment
allowed-tools: Read, Glob, Grep, Bash, WebFetch, WebSearch
---

# bequite-devops-cloud

Most outages trace back to five things: a missing env var, a migration that outran the code, a hand edit on a server, no way back, and nobody watching. CI adds a sixth: the pipeline itself holds the keys. This skill hardens the pipeline and puts a human between the agent and production.

## When to use

- `/bq-plan`: environments, CI gates, deploy trigger, rollback, monitoring, cost ceilings.
- `/bq-feature`: a new env var, service, job, container or workflow file.
- `/bq-verify`: deploy readiness. `/bq-release`: with `bequite-release-gate`.
- `/bq-fix`: CI failures, config bugs, server issues (diagnose only on servers).

Not for: schema design (`bequite-database-architect`), app-level security review (`bequite-security-reviewer`), version and changelog (`bequite-release-gate`).

## Procedure

1. **Read the pipeline.** Every workflow file, the deploy config, `.env.example`, Dockerfiles. List each job's trigger, permissions, secrets used and third-party actions.
2. **Harden CI** (`references/ci-hardening.md`): third-party actions pinned to a full commit SHA with the tag in a comment; `permissions:` read-only at the top, raised per job; no `pull_request_target` that checks out PR code; event text passed through `env:`, never inline in `run:`; cloud access through OIDC, not stored keys.
3. **Environments.** Local, preview, production (staging when the team or the data needs it). Same code, different config and data; production secrets live only in the production environment, released after its protection rules (required reviewer, branch pattern).
4. **Env vars in order.** Add to `.env.example` with a comment, then to production, then to preview, then merge the code that reads it. A missing var fails at boot with a clear message, not at first use.
5. **Containers**, if the project uses them (never added by default): multi-stage build, base image pinned by digest with a bot to bump it, non-root `USER`, `.dockerignore`, regular rebuild with `--pull`.
6. **Deploy and rollback.** Each change type has a written path back: code only = redeploy the previous build; code plus forward-only migration = roll forward with a fix. Risky changes go out as a canary compared against the control on error rate and latency.
7. **Watch.** Errors, uptime from more than one region, structured logs, and the five DORA metrics (lead time, deploy frequency, failed-deploy recovery time, change fail rate, rework rate) if the team tracks delivery.
8. **Cost ceilings.** Alerts at 80% of each plan limit; hard per-user caps on LLM spend; max duration for jobs.
9. **Production and servers are hard human gates** (`references/prod-safety.md`): the agent reads and prints, the user runs.
10. **Evidence**: the workflow lines before and after, a CI run link or local `act`-style dry run if available, the deploy checklist ticked.

## Worked example (real audit of this repo, 2026-11-21)

```
$ grep -nE "uses:|permissions|contents:|pull_request_target" .github/workflows/*.yml
ci.yml:12       contents: read
ci.yml:19,29,45 uses: actions/checkout@v4          ci.yml:20 uses: actions/setup-python@v5
release.yml:11  contents: write                    release.yml:17-18 checkout@v4, setup-python@v5
$ git ls-remote https://github.com/actions/checkout refs/tags/v4      -> 11d5960a326750d5838078e36cf38b85af677262
$ git ls-remote https://github.com/actions/setup-python refs/tags/v5  -> a26af69be951a213d495a4c3e4e4022e16d87065
```

Findings: 7 `uses:` lines pinned by movable tag (the tj-actions incident shows why that matters); `release.yml` grants `contents: write` to the whole workflow; no `pull_request_target`; no event text inlined in `run:`. Proposed change, for the owner of the workflow files to apply:

```yaml
permissions: {}                      # top level
jobs:
  release:
    permissions: { contents: write } # only the job that creates the release
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4 (resolved 2026-11-21)
```

## Quality gate

- Every third-party action is SHA-pinned or listed as an accepted exception with a reason.
- Every job's token permissions are stated; none is broader than the job needs.
- Every new env var is in `.env.example` and in each environment before the code that reads it merges.
- Every production-touching step has a rollback line and an approval point.
- The report shows commands and output; nothing is called "deployed" without the platform's own status.

## Boundaries

- Never run production deploys, server commands that change state, DNS, TLS, firewall or production migrations. Print them; the user runs them.
- Never print or paste secret values; reference them by name.
- Docker, Kubernetes, Terraform and hosting platforms are candidates chosen with the ten questions. Do not add any of them by default.

## References (load on demand)

- `references/ci-hardening.md`: workflow checklist with examples, OIDC, environments, artifact caching.
- `references/prod-safety.md`: server and VPS gates, migration approval, deploy runbook template, cost ceilings.
