---
description: Environment health check — Node / Python / Docker / package managers / ports / scripts / env files / CI. Reports blockers and the next recommended command.
---

# /bq-doctor — environment health

You are checking that the local environment can actually build + run this project. Surfaces missing tools, missing env files, port conflicts, and install-clarity issues.

## Step 1 — Read DISCOVERY_REPORT.md

If it doesn't exist, suggest `/bq-discover` first and exit early.

Otherwise, read its "Stack detected" + "Apps detected" + "Package managers" + "Ports" sections.

## Step 2 — Probe required tools

For each tool the discovered stack needs, check whether it's on PATH.

Use the **Bash** tool with `command -v <tool>` (the only shell exception — single tool probes are safe).

Cross-reference what's needed:

| Stack | Tools required |
|---|---|
| Node-based (any) | `node`, `npm` (or `pnpm` / `yarn` per package manager detected) |
| Python | `python` or `python3`, `pip` |
| Rust | `cargo`, `rustc` |
| Go | `go` |
| Bun runtime in package.json | `bun` |
| Docker compose present | `docker` + daemon reachable |
| Playwright in deps | `npx playwright --version` |

Note version for each tool found. Warn if version is below documented minimum (e.g. Node < 20 for Next.js 15).

## Step 3 — Probe ports

For each port DISCOVERY_REPORT.md listed (e.g. 3000, 3001, 3002), check whether it's currently bound.

Use Bash: `netstat -ano | grep ':3000 '` on Windows or `lsof -i :3000` on Unix. Note PID if bound. Don't kill anything — just report.

## Step 4 — Check env-var clarity

- If `.env.example` exists → read it, list the env vars expected.
- If `.env.example` is missing BUT code references `process.env.X` or `os.environ.get("Y")` (Grep) → flag as a risk: "App reads env vars but no .env.example".
- Do NOT read `.env` itself.

## Step 5 — Check scripts clarity

For Node projects, read `package.json::"scripts"`:

- Are `dev`, `start`, `build`, `test` defined?
- Any cryptic scripts (heavy shell incantations) without comments?

For Python projects:

- Is there a clear `pip install -e .` path? `requirements.txt` resolved?
- Are tests discoverable via `pytest`?

## Step 6 — Check README usefulness

Specifically: does README answer these questions?

- How to install
- How to run dev
- How to test
- How to build

Score each: present / partial / missing.

## Step 7 — Check CI

Look in `.github/workflows/`, `.gitlab-ci.yml`, etc.

- Is there a CI workflow that runs the test command on push?
- Is there a CI workflow that runs install + build?

## Step 8 — Write the report

Print to chat AND write `.bequite/audits/DOCTOR_REPORT.md`:

```markdown
# Doctor Report

**Generated:** <ISO 8601 UTC>
**Probed against:** <one-line stack summary from PROJECT_STATE.md>

## 1. Required tools

| Tool | Status | Version | Notes |
|---|---|---|---|
| node | OK | v24.12.0 |  |
| npm | OK | 11.9.0 |  |
| docker | OK | 29.1.3 | daemon: running |
| bun | MISSING |  | needed for studio/api; install: irm bun.sh/install.ps1 \| iex |
...

## 2. Ports

| Port | State | Bound by (PID) | Notes |
|---|---|---|---|
| 3000 | free |  |  |
| 3001 | in-use | 18856 | likely running dev server |
...

## 3. Environment variables

- `.env.example`: present / missing / partial
- App references: count
- Risk: <description>

## 4. Scripts (package.json or equivalent)

- `dev`: <one-liner> (clarity: clear / cryptic)
- `start`: <one-liner>
- `build`: <one-liner>
- `test`: <one-liner>

## 5. README usefulness

| Section | Status |
|---|---|
| Install | present / partial / missing |
| Run | ... |
| Test | ... |
| Build | ... |

## 6. CI

- Platform: <GitHub Actions / etc. / none>
- Test runs on push: yes / no
- Build runs on push: yes / no

## 7. Docker (if present)

- Dockerfile: present / no
- docker-compose.yml: present / no
- Heavy or light: <judgment based on services count + image sizes>

## 8. Blockers (must fix before building)

1. <e.g. "bun not installed — required for studio/api">
2. <...>

## 9. Recommendations

1. <e.g. "Add .env.example for the env vars referenced in src/lib/db.ts">
2. <...>

## 10. Recommended next command

- If blockers exist: `/bq-fix` for each one
- If only recommendations: `/bq-clarify` or `/bq-plan`
- If everything is clean: `/bq-plan`
```

## Step 9 — Update state

- `.bequite/state/PROJECT_STATE.md` — append the environment snapshot
- `.bequite/state/LAST_RUN.md` — `/bq-doctor` + timestamp
- `.bequite/logs/AGENT_LOG.md` — append

## Step 10 — Report back

Print to chat:

```
✓ Doctor complete

Tools required: <count> · OK: <count> · MISSING: <count>
Ports: <count probed> · free: <count> · in-use: <count>
Blockers: <count>

Full report: .bequite/audits/DOCTOR_REPORT.md

Next: </bq-fix or /bq-clarify or /bq-plan based on blocker count>
```

## Rules

- Only one shell-tool exception: probing `command -v <tool>` (or Windows `where.exe`) + `netstat`/`lsof` for port checks. No other shell commands during doctor.
- Do NOT install missing tools — report only.
- Do NOT touch `.env`.

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/state/PROJECT_STATE.md`
- `package.json`, `pyproject.toml`, `.env.example`, `README.md`, CI workflow files

## Memory files this command writes

- `.bequite/audits/DOCTOR_REPORT.md` (new)
- `.bequite/state/PROJECT_STATE.md` (updated — env snapshot section)
- `.bequite/state/LAST_RUN.md` (updated)
- `.bequite/logs/AGENT_LOG.md` (appended)

## Usual next command

- Blockers present → `/bq-fix`
- Recommendations only → `/bq-clarify`
- All clean → `/bq-plan`
