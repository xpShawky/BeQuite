# Tech Context: BeQuite

> Technology choices, pinned versions, dev setup, operational constraints. Mirrors `pyproject.toml` (authoritative); this file is the human-readable summary.

---

## 1. Stack at a glance

| Layer | Choice | Version | ADR | Doctrine source |
|---|---|---|---|---|
| Skill format | Anthropic SKILL.md | spec 2025-10-02 | n/a (standard) | library-package |
| CLI runtime | Python | 3.11+ | ADR-001-stack (drafting) | cli-tool |
| CLI build | hatchling | latest stable | ADR-001-stack | cli-tool |
| CLI args | click | latest stable | ADR-001-stack | cli-tool |
| Claude API | anthropic (Python SDK) | latest stable | ADR-001-stack | library-package |
| Pretty CLI output | rich | latest stable | ADR-001-stack | cli-tool |
| HTTP | httpx | latest stable | ADR-001-stack | library-package |
| Validation | pydantic | v2 | ADR-001-stack | library-package |
| TOML parsing | tomli | bundled in 3.11+ via tomllib | n/a | n/a |
| Receipts (signing) | cryptography (ed25519) | latest stable | ADR-001-stack | library-package |
| Hooks | bash 4+ (POSIX subset where portable) | n/a | ADR-001-stack | cli-tool |
| Distribution | PyPI via uvx/pipx | n/a | ADR-001-stack | library-package |
| npm thin shell | TBD (downloads Python on first run) | v0.15.0 | (future ADR) | library-package |
| CI | GitHub Actions | latest | (template) | library-package |
| Tests (Python) | pytest | latest | ADR-001-stack | library-package |
| Tests (e2e) | playwright | @playwright/mcp@latest | (referenced for examples) | default-web-saas (downstream) |
| Lint (Python) | ruff | latest | ADR-001-stack | cli-tool |
| Format (Python) | black or ruff format | latest | ADR-001-stack | cli-tool |
| Lint (Markdown) | markdownlint | latest | (template) | library-package |

**Note: BeQuite-itself does not bundle a frontend stack.** The Doctrines we ship for downstream projects (default-web-saas, mena-bilingual, …) reference the corrected stack matrix (post the §2 reconciliations in our build plan). BeQuite-itself is a CLI + Markdown skill + bash hooks.

## 2. Pinned versions (authoritative — copy from manifests)

`pyproject.toml` will be authored in v0.5.0. Until then, this file lists the *intended* pins; mismatches between this file and `pyproject.toml` are an Article III violation surfaced by `bequite audit`.

```
# Intended pins (drafted; authoritative version lives in cli/pyproject.toml from v0.5.0):
python    >= 3.11
click     >= 8.1
anthropic >= 0.40
rich      >= 13.7
httpx     >= 0.27
pydantic  >= 2.7
cryptography >= 42
pytest    >= 8.0
ruff      >= 0.5
```

## 3. Local dev setup

Until v0.5.0 ships the CLI, `make`-style dev commands are not yet wired. The current dev surface is just file editing + `git`.

```bash
# 1. Prerequisites (post-v0.5.0)
python --version    # >= 3.11
git --version       # >= 2.40

# 2. Bootstrap (post-v0.5.0)
git clone https://github.com/xpshawky/bequite
cd bequite
uvx --from . bequite --version

# 3. Run tests (post-v0.5.0)
uvx --from . pytest tests/

# 4. Self-audit (post-v0.4.2)
uvx --from . bequite audit
```

## 4. Environment variables

Listed by purpose. Reference `.env.example` for the schema (created in v0.5.0).

| Variable | Required | Purpose | Where to obtain |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | optional (CLI dispatch only) | Claude API access for non-Claude-Code hosts | https://console.anthropic.com |
| `OPENAI_API_KEY` | optional (multi-model) | OpenAI fallback in routing.json | https://platform.openai.com |
| `GOOGLE_API_KEY` | optional (Gemini for cheap doc gen) | Routing.json fallback | https://aistudio.google.com |
| `BEQUITE_LOG_LEVEL` | optional | `debug` / `info` / `warn` / `error` | n/a |
| `BEQUITE_COST_CEILING_USD` | optional | Override the per-session cost cap | n/a |
| `BEQUITE_TELEMETRY` | optional | `off` (default) / `receipts-only` / `full` (opt-in via ADR-002) | n/a |

## 5. External services

| Service | Auth method | Rate limit | Status page | Incident channel |
|---|---|---|---|---|
| Anthropic Claude API | API key (Bearer) | per Anthropic plan | https://status.anthropic.com | https://anthropic.com/contact |
| PyPI (registry) | n/a (read-only for freshness) | no | https://status.python.org | n/a |
| npm registry | n/a (read-only for freshness) | no | https://status.npmjs.org | n/a |
| GitHub (Actions, Releases) | GH Actions OIDC for release | per GH plan | https://www.githubstatus.com | https://support.github.com |
| Context7 MCP | Upstash | per Upstash plan | https://status.upstash.com | https://upstash.com/contact |

## 6. Dev-tool constraints

- **Node version:** N/A for BeQuite-itself; downstream Doctrines specify (e.g. `default-web-saas` pins to current LTS).
- **Python version:** `>= 3.11` (for `tomllib` standard-library TOML support; `pyproject.toml::requires-python`).
- **Rust version:** N/A for BeQuite-itself; `desktop-tauri` Doctrine references for downstream.
- **OS targets:** Linux, macOS, Windows. Path handling via `pathlib`.
- **Browser targets:** N/A for BeQuite-itself.
- **Editor extensions:** none required; recommended via `.vscode/extensions.json` post-v0.14.0.

## 7. The freshness contract

`bequite freshness` runs against this stack on every `bequite stack` and quarterly via CI. A package is "fresh" iff:

- Last commit < 6 months
- No unfixed criticals (OSV scan)
- The vendor pricing tier this project assumed still exists
- Not in a recorded supply-chain incident (PhantomRaven, Shai-Hulud, Sept-8 attack, …)

When a package fails freshness, the project receives a freshness-warning receipt and the stack ADR enters `status: requires-review`.

**Last freshness sweep:** none yet (probe ships in v0.4.3; first sweep will run on the BeQuite repo itself in CI starting v0.4.3).
**Failures:** none yet.

## 8. Known stale advice (post brief reconciliation)

The original brief — preserved at `BEQUITE_BOOTSTRAP_BRIEF.md` — contained advice that was correct in 2024 but stale by May 2026. The corrections we apply throughout BeQuite's templates and references:

- **Aider architect mode** is "frontier reasoner plans, cheap editor emits diffs" (the brief had it reversed).
- **Tauri Stronghold** is deprecated and being removed in v3 — use OS keychain plugins instead.
- **EV cert + relic for Windows** is no longer optimal — use **OV cert + AzureSignTool**; EV no longer gives SmartScreen reputation boost since Aug 2024.
- **macOS notarization** uses `xcrun notarytool`, not `altool`.
- **Spec-Kit ships 9 commands today**, not 16 (we extend, not replicate).
- **Roo Code** is shutting down May 15, 2026 — replace with Kilo Code in host lists.
- **shadcn registry MCP** is built into shadcn CLI v3+.
- **Clerk free tier** is now 50k MAU (was 10k).
- **Vercel Pro** can extend timeout to 800s (not a hard 300s cap).
- **Supavisor** has replaced PgBouncer on Supabase.
- **PhantomRaven** (Koi Security, Aug-Oct 2025) is the proper name for the 126-package npm hallucination attack.
- **Veracode 2025** confirms the 45% OWASP figure; the "~14 vulns/MVP" is not in the report and is dropped.
- **Impeccable** has ~26.6k stars (not 19k) and 23 commands (not 18).
