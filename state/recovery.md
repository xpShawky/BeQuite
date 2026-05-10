# state/recovery.md

> **Resume from this file in a new session without chat history.** Updated end-of-every-task; refreshed every 5 minutes during long auto-mode runs.
>
> Master pattern (master §25). The recovery prompt at `prompts/recovery_prompt.md` references this file as the primary source. **Iron Law III** binding.

---

## Project

- **Name:** BeQuite
- **Owner:** Ahmed Shawky (xpShawky)
- **Mode (BeQuite-itself):** Safe Mode
- **Constitution version:** **1.2.0** (9 Iron Laws; Modes; Doctrines; Definition-of-done)
- **Active doctrines (BeQuite-itself):** library-package, cli-tool, mena-bilingual (full content lands v0.11.0)
- **12 Doctrines shipped for downstream projects:** default-web-saas, cli-tool, ml-pipeline, desktop-tauri, library-package, fintech-pci, healthcare-hipaa, gov-fedramp, ai-automation (v0.2.1), vibe-defense (v0.5.2; default for `audience: vibe-handoff`), mena-pdpl (v0.5.2; jurisdiction-branched Egypt/KSA/UAE), eu-gdpr (v0.5.2)

## Where we are

- **Build phase:** phase-3 — Reproducibility + economics (v0.7.0 + v0.7.1 done; v0.8.x next).
- **Sub-version in progress:** **v0.8.0** (next) — Multi-model routing live: AiProvider adapters (Anthropic + OpenAI + Google + DeepSeek + Ollama) + cost-aware routing.json schema + stop-cost-budget hook + receipts emit per model invocation.
- **Last green sub-version:** **v0.7.1** (Signed receipts — ed25519 keypair on init + sign-at-emission + `bequite verify-receipts` + `bequite keygen` + 9-test signing integration suite all passing; combined receipts+signing 19/19 green on Python 3.14).
- **Last successful commit (pending):** `feat(v0.7.1): Signed receipts — ed25519 keypair + sign-at-emission + bequite verify-receipts + 9-test signing suite`.
- **Last successful tag (pending):** **v0.7.1**.
- **Branch:** `main`.
- **Remote:** `origin = https://github.com/xpShawky/BeQuite.git` configured. **NOT pushed.** Push requires explicit owner authorization (Iron Law IV; one-way door).
- **Real git counts (post-v0.7.1, pre-commit):** ~23 commits, 18 tags pending, ~173+ tracked files.

## What is complete (verified by `git tag -l`)

| Tag | Module |
|---|---|
| v0.1.0 | Foundation: README + LICENSE + .gitignore + CHANGELOG + Constitution v1.0.0 + 6 Memory Bank templates + ADR template + Doctrine schema |
| v0.1.1 | 8 default Doctrines (default-web-saas / cli-tool / ml-pipeline / desktop-tauri / library-package / fintech-pci / healthcare-hipaa / gov-fedramp) |
| v0.1.2 | Master-file merge: two-layer architecture (Harness + Studio v2.0.0+); Constitution v1.0.1; ADR-008; CLAUDE.md + AGENTS.md; state/ + prompts/ + evidence/ scaffolds |
| v0.2.0 | Skill orchestrator (SKILL.md + 11 personas + routing.json + bequite.config.toml.tpl) |
| v0.2.1 | AI automation skill module (n8n / Make / Zapier / Temporal / Inngest expert + automation-architect 12th persona + ai-automation Doctrine + bundled skill at `skill/skills-bundled/ai-automation/`) |
| v0.3.0 | 10 hook scripts (deterministic gates) + template/.claude/settings.json + tests/integration/hooks/README.md |
| v0.4.0 | 12 master-aligned slash commands (discover / research / decide-stack / plan / implement / review / validate / recover / design-audit / impeccable-craft / evidence / release) |
| v0.4.1 | 7 BeQuite-unique slash commands (audit / freshness / auto / memory / snapshot / cost / skill-install) |
| v0.4.2 | `cli/bequite/audit.py` — Constitution + Doctrine drift detector + .github/workflows/audit.yml |
| v0.4.3 | `cli/bequite/freshness.py` — knowledge probe (npm/PyPI/crates.io/GitHub probes; 24h cache) + skill/references/package-allowlist.md |
| v0.5.0 | Python CLI thin wrapper (cli/pyproject.toml + __main__.py + commands.py + config.py + skill_loader.py + hooks.py); `bequite` + `bq` console scripts; 19 subcommands wired |
| v0.5.1 | **Article VIII Scraping** (Constitution v1.1.0; ADR-009): scraping-engineer 13th persona + skill/references/scraping-and-automation.md + pretooluse-scraping-respect.sh hook + watch-and-trigger template |
| v0.5.2 | **Article IX Cybersecurity** (Constitution v1.2.0; ADR-010): security-auditor + pentest-engineer + cve-watcher + disclosure-timer (4 new personas; total 17) + 3 hooks (pentest-authorization / no-malware / cve-poc-context) + scan-and-trigger template + RoE template + 3 Doctrines (vibe-defense / mena-pdpl / eu-gdpr) |
| v0.5.3 | URL casing fix (`xpshawky/bequite` → `xpShawky/BeQuite`); inflated-count corrections; remote configured |
| v0.6.0 | Verification gates: walkthrough templates (admin/user) + seed.spec.ts + playwright.config.ts + self-walk + smoke + skill/references/playwright-walks.md + cli/bequite/verify.py |
| v0.6.1 | Frontend Quality Module: vendored Impeccable bundle (.pinned-commit + ATTRIBUTION + SKILL.md + 3 reference files + commands/CATALOG.md + 4 marquee command dispatch contracts) + skill/templates/tokens.css.tpl + skill/references/frontend-stack.md + skill/references/frontend-mcps.md + axe-core gate (workflow tpl + a11y specs + playwright.config.ts axe-projects) + default-web-saas Doctrine v1.0.0 → v1.1.0 |
| v0.7.0 | Reproducibility receipts: cli/bequite/receipts.py (~510 lines, dataclass-based schema v1, sha256 hashing, chain-hash, validate-chain, replay-check, roll-ups by session/phase/day) + bequite cost local-first + bequite receipts {list,show,validate-chain,roll-up} Click group + tests/integration/receipts/ 10-test smoke suite (all passing on Python 3.14) |
| v0.7.1 | Signed receipts: cli/bequite/receipts_signing.py (ed25519 via cryptography lib; per-project keypair: private at .bequite/.keys/private.pem 0600 gitignored, public at .bequite/keys/public.pem 0644 committed; sign_dict + verify_dict + verify_receipts_directory + strict mode) + Receipt.signature additive field + ReceiptStore.write(sign_with=) opt-in signing + bequite verify-receipts [--strict] + bequite keygen + bequite init auto-keygen + 9-test signing suite (all passing); combined 19/19 receipts+signing green |

**Five working Python modules** (smoke-tested via `python -m`; help output prints):
- `python -m cli.bequite.audit` — rule-based, 7 rule packs
- `python -m cli.bequite.freshness --all`
- `python -m cli.bequite.verify` — 17-gate per-Mode matrix
- `python -m cli.bequite.receipts {emit,list,show,validate-chain,roll-up}` — chain-hashed receipts
- `python -m cli.bequite.receipts_signing {keygen,sign,verify}` — ed25519 keypair + sign + verify

## What is incomplete

The remaining sub-versions to v1.0.0:

| Sub-version | Scope |
|---|---|
| **v0.8.0** (next) | Multi-model routing (cost-aware). Provider adapters in `cli/bequite/providers/{anthropic,openai,google,deepseek,ollama}.py`. Refresh `skill/routing.json` schema (phase + persona + model + reasoning_effort + fallback_model + max_input_tokens + max_output_tokens). Wire `stop-cost-budget.sh` hook for cost ceiling enforcement. Receipts emit per model invocation. Routing-test fixture proves Sonnet for implementer + Opus for reviewer. Cost-ceiling test. |
| v0.8.0 | Live multi-model AiProvider adapters (Anthropic + OpenAI + Google + DeepSeek + Ollama) |
| v0.8.1 | Pricing fetch + 24h cache + offline fallback |
| v0.9.0 | 3 example projects (bookings-saas Next/Hono/Supabase + ai-tool-wrapper CLI + tauri-note-app desktop) |
| v0.9.1 | E2E test harness (seven-phase + auto-mode + doctrine-loading) |
| v0.10.0 | Auto-mode state machine + safety rails + heartbeat |
| v0.10.1 | Auto-mode hardening (resume / parallel-task / idempotent) |
| v0.11.0 | MENA bilingual (Arabic Researcher, RTL tokens, Egyptian dialect, RTL Playwright walks) |
| v0.12.0 | Per-host adapters (AGENTS.md + .cursor/rules + .codex + .gemini + .windsurf + .clinerules + .kilocode + .continuerules + .aider) |
| v0.13.0 | Vibe-handoff exporters (spec-kit-zip + claude-code-skill formats) |
| v0.14.0 | Documentation (README + QUICKSTART + HOW-IT-WORKS + DOCTRINE-AUTHORING + HOSTS + AUTONOMOUS-MODE + SECURITY + MAINTAINER) |
| v0.15.0 | Release engineering (CI workflows + release.yml + versioning automation) |
| v1.0.0 | Final release |

## What failed last

Nothing structurally failed. Two minor session frictions worth noting:

1. **Edit-state mismatches** — when batching many file changes per turn, the harness's "have I read this file" tracking sometimes fell behind, causing some Edit calls to fail with "File has not been read yet." Workaround: explicit `Read` immediately before `Edit` for files modified earlier in the session. Several backfill commits resulted (chore commits to fix CHANGELOG / state files that didn't update with their feat commit).

2. **Inflated line-count claims** — earlier in session I quoted "30,000+ lines / 22,000+ lines" in status reports. Real git count is closer to 25k. Corrected in v0.5.3 (Article VI honest reporting). Going forward, run `git log --pretty=tformat: --numstat | awk '{a+=$1; s+=$2} END {print a, s}'` for real numbers; don't estimate.

## What evidence exists

Until v0.7.0 ships the receipts system, evidence is the git history + this file + the snapshots.

```
git log --oneline       # ~23 commits expected post-v0.7.1
git tag -l              # 18 tags expected (through v0.7.1)
find .bequite/memory/ skill/ template/ cli/ docs/ tests/ -type f | wc -l  # ~173+
```

Snapshots:
- `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md` — the approved plan ratified via ExitPlanMode (early session)
- `.bequite/memory/prompts/v1/2026-05-10_initial-brief.md` — original brief preserved
- `.bequite/memory/prompts/v2/2026-05-10_constitution-v1.2.0.md` + ADR-009 + ADR-010 (v0.5.2)
- `.bequite/memory/prompts/v3/` (this snapshot) — Constitution v1.2.0 + state/recovery.md + activeContext + progress + ADRs (taken pre-v0.6.1; v0.6.1 changes layered on top during this session)

## What is the next safe task

**Resume v0.8.0 — Multi-model routing (cost-aware).** Per the build plan §4 (`v0.8.0` row):

1. Refresh `skill/routing.json` schema with cost-aware fields per phase + persona: `model`, `reasoning_effort`, `fallback_model`, `max_input_tokens`, `max_output_tokens`. Existing routing.json (v0.2.0) had a basic shape; v0.8.0 makes it operational.
2. Implement provider adapters in `cli/bequite/providers/`:
   - `anthropic.py` (primary; uses `anthropic` SDK already in deps)
   - `openai.py` (planner alt; conditional on `bequite[openai]` extra; already declared in pyproject)
   - `google.py` (Gemini for free-tier doc gen; conditional on `bequite[google]` extra)
   - `deepseek.py` (cheap implementer; via OpenAI-compatible API)
   - `ollama.py` (offline mode; HTTP localhost)
3. `skill_loader.py` reads routing → picks model per call.
4. Cost ceiling: `bequite.config.toml::cost.session_max_usd` enforced via `stop-cost-budget.sh` hook.
5. Provider auth via env vars (already in `.gitignore`).
6. Receipts (v0.7.0 + v0.7.1) emit per model invocation — wire emit-on-call.
7. Add tests: routing-test fixture forces Sonnet for implementer + Opus for reviewer; cost-ceiling test (synthetic receipts summing past threshold trips the stop hook).
8. Bumps: `__init__.py` + `pyproject.toml` → `0.8.0`. CHANGELOG entry. State updates. Commit + tag.

Acceptance for v0.8.0: routing-test green; cost-ceiling test green; receipts confirm correct model choice per phase.

## Commands to run first (on resume)

```bash
# Orient
cat .bequite/memory/activeContext.md
cat state/current_phase.md
cat state/recovery.md

# Verify git state
git log --oneline | head -5
git tag -l                                  # expect 18 tags through v0.7.1
git status                                  # expect clean

# Smoke-test the five working Python modules
cd cli/
python -m bequite.audit --help
python -m bequite.freshness --help
python -m bequite.verify --help
python -m bequite.receipts --help
python -m bequite.receipts_signing --help

# Run the v0.7.0 + v0.7.1 test suites
PYTHONIOENCODING=utf-8 python ../tests/integration/receipts/test_receipts_smoke.py    # 10/10
PYTHONIOENCODING=utf-8 python ../tests/integration/receipts/test_signing_smoke.py     # 9/9
```

## Files to inspect before editing (Iron Law III)

For any agent resuming this build:

1. `.bequite/memory/constitution.md` — Iron Laws v1.2.0 + Modes + Doctrines + Definition-of-done.
2. `.bequite/memory/{projectbrief, productContext, systemPatterns, techContext, progress}.md`.
3. `.bequite/memory/decisions/ADR-008-master-merge.md` + `ADR-009-article-viii-scraping.md` + `ADR-010-article-ix-cybersecurity.md`.
4. `state/project.yaml`, `state/current_phase.md`, this `state/recovery.md`, `state/task_index.json`, `state/decision_index.json`.
5. `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief (preserved verbatim; immutable).
6. `BeQuite_MASTER_PROJECT.md` — master file (introduced mid-session, post-v0.1.1; preserved).
7. `docs/merge/MASTER_MD_MERGE_AUDIT.md` — the merge plan.
8. `skill/SKILL.md` — orchestrator entry.
9. `skill/agents/*.md` — 17 personas.
10. `skill/doctrines/*.md` — 12 Doctrines.
11. `skill/hooks/*.sh` — 14 hooks.
12. `skill/references/*.md` — scraping + security + playwright-walks + frontend-stack + frontend-mcps + package-allowlist references + ai-automation + impeccable bundled skills.
13. `cli/bequite/{audit,freshness,verify,receipts}.py` — four runnable Python modules.
14. `cli/bequite/{__main__,commands,config,skill_loader,hooks}.py` — CLI thin wrapper.
15. `tests/integration/receipts/test_receipts_smoke.py` + `test_signing_smoke.py` — 19-test combined suite for v0.7.0 + v0.7.1 (all passing on Python 3.14).

## Files to NOT touch

- `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief; immutable.
- `BeQuite_MASTER_PROJECT.md` — master file; immutable.
- `.bequite/memory/prompts/v1/*` + `v2/*` + `v3/*` — versioned snapshots; immutable history.
- `.bequite/memory/decisions/ADR-*.md` — accepted ADRs; supersede via NEW ADR, never edit.
- `.git/` — never.
- `.env*` — Iron Law IV; never read or write.

## Suggested next phase

Continue v0.8.0 → v0.8.1 → v0.9.0 → v0.9.1 → v0.10.0 → v0.10.1 → v0.11.0 → v0.12.0 → v0.13.0 → v0.14.0 → v0.15.0 → **v1.0.0** per the main plan at `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`. **11 sub-versions remain.**

After v1.0.0: pause. Layer 2 Studio (v2.0.0+) is a separate plan that requires Ahmed's authorization to begin (see ADR-008 / docs/merge/MASTER_MD_MERGE_AUDIT.md Bucket D).

## One-way doors that always pause

Per Iron Law IV + plan §11/12. Auto-mode never auto-runs:

- `git push` to remote (any branch).
- `git push --force` (any).
- PyPI publish.
- npm publish.
- `terraform apply` against shared infra.
- DB migrations against shared DBs.
- Generating publishable press / blog content.
- Scraping MENA channels (Twitter/X / Telegram) — Ahmed seeds the list at v0.11.0.

Each of these requires explicit owner approval per session.

## Last heartbeat

`2026-05-10` — end of v0.6.0 + memory snapshot before v0.6.1.
