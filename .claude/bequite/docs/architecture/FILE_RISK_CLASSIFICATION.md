# File Risk Classification (alpha.19)

> **Third enforcement surface for file-edit safety.** Hooks catch destructive SHELL ops + secret strings; hard human gates catch named risky ACTIONS; this classification catches risky FILE EDITS that would otherwise pass through the Edit/Write tools silently. Tunable per-project rules live in `.bequite/state/FILE_RISK_RULES.md`.

**Status:** active · **Adopted:** alpha.19 (Fable Strengthening Pass)
**Enforced at:** execution contract step 7 · `/bq-auto` continuation logic · `/bq-review` + `/bq-red-team` (flag high-tier diffs for extra scrutiny)

---

## The three tiers

### Tier R3 — CONFIRM (hard human gate, even in auto mode)

Editing, creating, or deleting any of these requires explicit user confirmation first:

| Category | Path / pattern examples |
|---|---|
| Env + secrets | `.env*` · `secrets.*` · `*credentials*` · key/cert files (`*.pem`, `*.key`, `id_rsa*`) |
| Auth + security model | auth middleware/config · session handling · password/token logic · RLS policies · permission/role definitions |
| Database migrations | `migrations/**` · schema-change SQL · seed scripts touching prod data |
| Production deploy | deploy scripts targeting prod · `nginx*.conf` · systemd units · `Dockerfile`/`docker-compose*` in deploy context |
| CI/CD | `.github/workflows/**` · pipeline configs (these run arbitrary code on push) |
| Payments | payment-provider integration code · webhook secret handling · pricing/billing logic |
| Cloud credentials | provider config with account identifiers · IAM/policy files |
| Mass destruction | deleting any file with active callers · mass refactors (>10 files in one action) · deleting `.bequite/` or `.claude/` content |

**Behavior:** pause → show the intended diff → state the risk category → wait for user yes. In auto mode this is a hard gate (it joins the 17).

### Tier R2 — ANNOUNCE (proceed, but say so explicitly first)

Package manager configs (`package.json` deps section, lockfiles, `pyproject.toml`) · build configs (`tsconfig`, `vite.config`, webpack) · routing tables · public API signatures · `.gitignore` · install scripts. **Behavior:** state "editing R2 file <path> because <reason>" in the visible output before the edit; include in report.

### Tier R1 — NORMAL

Everything else: source, tests, docs, styles, BeQuite memory templates. Standard contract discipline (smallest safe change, DNA conformance, verification).

---

## Rules of application

1. Classification is by **content role, not just filename** — a file named `utils.ts` containing session-token logic is R3.
2. **Reading** any tier is unrestricted (except secrets — never print secret VALUES into chat/logs; reference by key name).
3. Tier check happens BEFORE the edit (contract step 7), not after.
4. False-positive escape hatch: the user can lower a specific path's tier in `FILE_RISK_RULES.md` (per-project), never in this doc (pack-wide).
5. Hooks remain the machine layer for shell ops; this classification governs the agent's Edit/Write behavior — together they close the "risky change via file edit" gap identified in the Fable audit (finding H3).
