---
description: Inspect the repo before planning. Writes .bequite/audits/DISCOVERY_REPORT.md with detected stack, apps, entry points, ports, docs, tests, risks, missing information.
---

# /bq-discover — repo discovery

You are inspecting the repository to understand WHAT IT IS before any planning happens. The output is the foundation for every later command.

## Step 1 — Scan the repo

Use Glob + Read + Grep (NOT shell `find` or `grep`):

### Manifests + package managers

- `package.json` → Node project. Note `"scripts"`, `"dependencies"`, `"devDependencies"`, `"engines"`.
- `pyproject.toml` / `requirements.txt` / `setup.py` → Python.
- `Cargo.toml` → Rust.
- `go.mod` → Go.
- `composer.json` → PHP.
- `Gemfile` → Ruby.
- Multiple = monorepo or polyglot. Note each.

### Code structure

- Top-level dirs (`src/`, `lib/`, `app/`, `apps/`, `packages/`, `cmd/`, `internal/`, etc.)
- `pages/` or `app/` (Next.js / Nuxt / SvelteKit) → web framework
- `routes/` (Hono / Express / FastAPI conventions)
- `tests/` or `__tests__/` or `spec/` → test layout

### Infrastructure

- `Dockerfile`, `docker-compose.yml`, `.dockerignore` → containerized
- `.github/workflows/*.yml` → GitHub Actions
- `.gitlab-ci.yml`, `.circleci/`, `azure-pipelines.yml` → other CI
- `terraform/`, `infra/`, `k8s/` → IaC

### Configuration

- `.env.example`, `.env.local.example` → expected env vars (DO NOT read `.env` itself)
- `tsconfig.json`, `eslint.config.*`, `biome.json`, `.prettierrc*` → JS/TS tooling
- `mypy.ini`, `pyproject.toml::[tool.ruff]` → Python tooling
- `playwright.config.*`, `vitest.config.*`, `jest.config.*` → JS test runners
- `pytest.ini`, `conftest.py` → Python test config

### Documentation

- `README.md` (read fully)
- `docs/`, `documentation/`, `wiki/`
- `CHANGELOG.md`, `RELEASES/`
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
- `HANDOFF.md`, `ARCHITECTURE.md`, `DECISIONS.md` / `adr/`

## Step 2 — Sniff the runtime

Look for entry-point clues:

- `package.json::"main"`, `"module"`, `"bin"`, `"scripts.dev"`, `"scripts.start"`, `"scripts.build"`, `"scripts.test"`
- `pyproject.toml::[project.scripts]`, `[tool.poetry.scripts]`, `__main__.py`, `manage.py`
- Cargo: `Cargo.toml::[[bin]]`
- Go: `main.go`, `cmd/*/main.go`

## Step 3 — Find ports + URLs

Grep for `:3000`, `:8000`, `:8080`, `:5173`, `localhost:`, `127.0.0.1:`. Note any port the project clearly uses.

## Step 4 — Find tests

- `package.json::"scripts.test"` → the canonical test command
- `*.test.{js,ts,tsx}`, `*.spec.{js,ts,tsx}` → JS tests
- `test_*.py`, `*_test.py` → pytest discovery
- `*_test.go` → Go tests

## Step 5 — Risk surface

Note anything risky from a "vibe coder reading this fresh" perspective:

- README is missing OR clearly stale
- No `.env.example` but `.env` referenced in code
- No tests directory
- No CI
- Many `// TODO`, `FIXME`, `XXX` comments (Grep + count)
- Dependencies with `^0.x.x` or `^0.0.x` versions (pre-1.0 → fragile)
- `node_modules/` committed (bad)
- Secrets in source (search for `api_key =`, `password =`, `AKIA`, `sk_live_`, etc. — DO NOT print full values)
- Lockfile missing
- Multiple package managers (yarn.lock + package-lock.json + pnpm-lock.yaml) — pick-one needed

## Step 6 — Write DISCOVERY_REPORT.md

Author `.bequite/audits/DISCOVERY_REPORT.md`:

```markdown
# Discovery Report

**Generated:** <ISO 8601 UTC>
**Repo path:** <absolute path>
**Stack detected:** <e.g. Next.js 15 + TypeScript + Tailwind v4; Node 20+; pnpm>

## 1. Project shape

(2-3 sentences explaining what this project is, based on README + structure.)

## 2. Apps detected

| App | Path | Stack | Entry point | Status |
|---|---|---|---|---|
| <app-1> | <path> | <stack> | <entry> | <healthy / unknown> |
...

## 3. Package managers

- Primary: <npm / pnpm / yarn / poetry / cargo / etc.>
- Lockfile: <present + sane | missing | conflicting>

## 4. Run / build / test commands

| Action | Command | Notes |
|---|---|---|
| Install | <e.g. pnpm install> |   |
| Dev | <e.g. pnpm dev>     |   |
| Build | <e.g. pnpm build> |   |
| Test | <e.g. pnpm test>   |   |
| Lint | <e.g. pnpm lint>   | (optional) |
| Typecheck | <e.g. tsc --noEmit> | (optional) |

## 5. Ports used

- <port>: <service>

## 6. Documentation

- README: <present + useful | present + stale | missing>
- CHANGELOG: <yes / no>
- docs/: <described structure>
- Other docs noted: <list>

## 7. Tests

- Framework: <vitest / jest / playwright / pytest / etc.>
- Test directory: <path>
- Test count: <approximate, by Glob count of test files>

## 8. CI

- Platform: <GitHub Actions / GitLab / CircleCI / none>
- Workflow files: <list>

## 9. Infrastructure

- Docker: <Dockerfile + docker-compose | no>
- IaC: <terraform / k8s manifests / none>

## 10. Risks / smells

- (Bulleted list of items from Step 5)

## 11. Missing information (asks for /bq-clarify)

- (Bulleted list of things we couldn't determine and need the user to clarify)

## 12. Architecture guess

(2-4 sentences: based on the file layout + manifests, what's the system architecture? Get it close, mark as "guess" — `/bq-clarify` will confirm.)

## 13. Recommended next command

- If risks/smells were found → `/bq-audit` for the full picture
- If everything looks healthy → `/bq-doctor` for environment health
- If many things are unclear → `/bq-clarify` to ask the user 3-5 questions
```

## Step 7 — Update state

After writing the report:

1. Update `.bequite/state/PROJECT_STATE.md` with the detected stack + apps.
2. Update `.bequite/state/CURRENT_PHASE.md` — still Phase 0, but note "discovery complete".
3. Update `.bequite/state/LAST_RUN.md` to `/bq-discover` + timestamp + outcome.
4. Append a line to `.bequite/logs/AGENT_LOG.md`.

## Step 8 — Report back

Print to chat:

```
✓ Discovery complete

Stack:    <one-liner summary>
Apps:     <count>
Ports:    <list>
Tests:    <count> tests via <framework>
Risks:    <count> items flagged

Full report: .bequite/audits/DISCOVERY_REPORT.md

Next:  /bq-doctor          environment health check
       /bq-clarify         ask user about <count of missing-info items>
       /bq-audit           full project audit (if risks were flagged)
```

## Rules

- Use Read / Glob / Grep tools. Do NOT run shell commands.
- Do NOT read `.env`, `.env.local`, or any file with `secret` / `private` / `key` in the name (you may note its EXISTENCE without reading content).
- Do NOT make any code changes during discovery.
- Be specific: say "Next.js 15.5.18" not "React app".
- Be honest: if you can't determine something, list it in section 11.

## Standardized command fields (alpha.6)

**Phase:** P0 — Setup and Discovery
**When NOT to use:** completely empty folder with no source code — use `/bq-new` instead.
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:**
- `DISCOVERY_REPORT.md` written with all 11 sections
- Stack detected (or explicitly marked "unknown")
- Risks + missing-info surfaced
- Marks `DISCOVERY_DONE ✅`
**Failure behavior:**
- No manifests + no source → write minimal report; suggest `/bq-new`
- Read fails on a file → skip + note in report; don't abort the whole discover
**Memory updates:** Sets `DISCOVERY_DONE ✅`. Writes `DISCOVERY_REPORT.md`.
**Log updates:** `AGENT_LOG.md` entry with summary.

## Memory files this command reads

- All package manifests
- README.md
- CLAUDE.md
- All `.bequite/state/*.md`

## Memory files this command writes

- `.bequite/audits/DISCOVERY_REPORT.md` (new)
- `.bequite/state/PROJECT_STATE.md` (updated)
- `.bequite/state/CURRENT_PHASE.md` (updated)
- `.bequite/state/LAST_RUN.md` (updated)
- `.bequite/logs/AGENT_LOG.md` (appended)

## Usual next command

- `/bq-doctor` if discovery was clean
- `/bq-clarify` if discovery left questions
- `/bq-audit` if discovery flagged risks
