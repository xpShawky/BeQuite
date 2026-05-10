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

- **Build phase:** phase-4 (Examples + e2e harness) complete; **Phase-1 docs for two new feature modules shipped v0.9.2**. Next phase: phase-5 (Auto-mode + Multi-Model Planning impl + CLI Auth stubs + MENA + host adapters; v0.10.0–v0.13.0).
- **Sub-version in progress:** **v0.10.0** (next) — Auto-mode state machine (one-click P0→P7). Then v0.10.5 multi-model manual-paste MVP (per ADR-012) + v0.10.6 CLI auth stubs (per ADR-011) + v0.10.7 auto-mode hardening.
- **Last green sub-version:** **v0.9.2** (Phase-1 docs for ADR-011 CLI Authentication + ADR-012 Multi-Model Planning; 2 strategy docs + 1 requirements doc + 3 new personas; no new Iron Laws).
- **Last successful commit (pending):** `feat(v0.9.2): Phase-1 docs — ADR-011 CLI Auth + ADR-012 Multi-Model Planning + 2 strategy docs + 1 requirements doc + 3 personas`.
- **Last successful tag (pending):** **v0.9.2**.
- **Branch:** `main`.
- **Remote:** `origin = https://github.com/xpShawky/BeQuite.git` configured. **NOT pushed.** Push requires explicit owner authorization (Iron Law IV; one-way door).
- **Real git counts (post-v0.9.2, pre-commit):** ~28 commits, 23 tags pending, ~210+ tracked files.

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
| v0.8.0 | Multi-model routing live: cli/bequite/providers/{__init__,anthropic,openai,google,deepseek,ollama}.py (AiProvider Protocol + Completion dataclass + 5 graceful-degrading adapters with hard-coded May-2026 pricing fallback) + cli/bequite/router.py (select_route + dispatch + fallback resolution) + cli/bequite/cost_ledger.py (writes .bequite/cache/cost-ledger.json so existing stop-cost-budget.sh hook is operational) + bequite route {show,list,providers} + bequite ledger {show,reset} CLI groups + 15-test router integration suite (all passing); combined 34/34 receipts+signing+router green |
| v0.8.1 | Live pricing fetch (best-effort): cli/bequite/pricing.py (~330 lines, cache + 24h TTL + offline fallback + WebFetch best-effort live extraction with regex paragraph parser) + skill/references/pricing-table.md (vendored May-2026 snapshot covering 5 model providers + hosting + auth + database) + provider adapters' estimate_cost_usd consults cache before hard-coded fallback + bequite pricing {show,list,refresh} Click group + 14-test integration suite (all passing); combined 48/48 receipts+signing+router+pricing green |
| v0.9.0 | Three example projects scaffolded + spec'd: examples/01-bookings-saas (Doctrine default-web-saas; full README + ADR-001 stack with per-rule Doctrine compliance + spec.md with 4 flows + phases.md with 7-phase decomposition + HANDOFF.md with engineer + non-engineer sections); examples/02-ai-tool-wrapper (Doctrine cli-tool; README + ADR-001 reusing BeQuite providers/); examples/03-tauri-note-app (Doctrine desktop-tauri; README + ADR-001 with brief reconciliations applied — NOT Stronghold/altool/EV cert/relic). Honest scope per Article VI: scaffolds + walkthroughs, not production code |
| v0.9.1 | E2E test harness: tests/integration/e2e/test_seven_phase_walk.py (8 tests for CLI surface; subprocess wrapper inherits parent env; UTF-8 with errors=replace for Windows compat) + test_doctrine_loading.py (8 tests for Doctrine structural invariants; tolerant Rules-section regex) + .github/workflows/examples-e2e.yml (3 jobs: python-suite × 4 Python versions + example-scaffolds + audit-self + pr-comment summary). Combined integration suite green: 10+9+15+14+8+8 = 64/64 |
| v0.9.2 | Phase-1 docs for two new feature modules per Ahmed's "add two major features" prompt: ADR-011 CLI Authentication (`.bequite/memory/decisions/ADR-011-cli-authentication.md`; device-code login MVP; Python keyring storage; CI-mode separate from human login) + ADR-012 Multi-Model Planning (`.bequite/memory/decisions/ADR-012-multi-model-planning.md`; manual-paste MVP; Parallel mode default; Claude Opus 4.7 default judge; browser-session reuse of consumer subscriptions NOT recommended) + `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md` + `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md` + `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md` + 3 new personas at `skill/agents/{multi-model-planning-orchestrator,model-judge,red-team-reviewer}.md` (total persona count → 20). Master-doc updates: CLAUDE.md + AGENTS.md (paths) + Constitution preamble (v0.9.2 update line) + activeContext + progress (roadmap reshape). No new Iron Laws — operational frameworks. |

**Seven working Python modules** (smoke-tested; help / CLI output exercised):
- `python -m cli.bequite.audit` — rule-based, 7 rule packs
- `python -m cli.bequite.freshness --all`
- `python -m cli.bequite.verify` — 17-gate per-Mode matrix
- `python -m cli.bequite.receipts {emit,list,show,validate-chain,roll-up}` — chain-hashed receipts
- `python -m cli.bequite.receipts_signing {keygen,sign,verify}` — ed25519 keypair + sign + verify
- `python -m cli.bequite route show --phase P5 --persona reviewer` — multi-model routing inspection (v0.8.0)
- `python -m cli.bequite.pricing {show,list,refresh}` — live pricing fetch + cache (v0.8.1)

Plus `bequite route {show,list,providers}` + `bequite ledger {show,reset}` + `bequite pricing {show,list,refresh}` Click commands.

## What is incomplete

The remaining sub-versions to v1.0.0:

| Sub-version | Scope |
|---|---|
| **v0.10.0** (next) | Auto-mode state machine. `cli/bequite/auto.py` orchestrator with INIT → P0_RESEARCH → P1_STACK → P2_PLAN → P3_PHASES → P4_TASKS → P5_IMPLEMENT (per-task loop) → P6_VERIFY → P7_HANDOFF → DONE plus BLOCKED/FAILED/PAUSED states. Per-phase commit (atomic). Skeptic gate at every phase boundary (≥1 kill-shot). Safety rails: hard cost ceiling (default $20), wall-clock ceiling (default 6h), 3 consecutive Implementer failures threshold, banned-word check (already in stop-verify-before-done.sh hook), hook-block respect (no auto-override), one-way-door operations always pause. Failure replay: `.bequite/replays/<timestamp>/`. Heartbeat: `activeContext.md` every 5 min. CLI flags: `--feature`, `--max-cost-usd`, `--max-wall-clock-hours`, `--phases <subset>`, `--mode slow|fast|auto`, `--on-failure pause|abort|continue-with-warning`, `--no-skeptic` (debug only). |
| v0.10.5 | Multi-model planning Phase-3 (manual-paste mode working) per ADR-012: cli/bequite/multi_model.py (render_prompt + compare + merge + extract_final_plan) + cli/bequite/providers/manual_paste.py (ManualPasteProvider conforming to AiProvider Protocol) + bequite plan --multi-model + bequite models {list,configure,roles,compare,merge} Click groups + ≥4 prompt templates + 10-test integration suite. End-to-end manual-paste run on examples/01-bookings-saas as proof-of-life. |
| v0.10.6 | CLI auth Phase-2 (command stubs that gracefully degrade until auth server stands up) per ADR-011: bequite auth {login,logout,whoami,status,refresh} commands + Python `keyring` integration for OS keychain storage (with file fallback) + offline-mode (`BEQUITE_OFFLINE=true`) + CI-mode (`BEQUITE_API_KEY` + `BEQUITE_CI_MODE=true`) + sessionstart-load-auth.sh hook + 8-test integration suite. |
| v0.10.7 | Auto-mode hardening (was v0.10.1 in original plan; renumbered v0.9.2): resume from BLOCKED, parallel-task fan-out per AkitaOnRails 2026 N>5 rule, idempotent reruns, state persistence at .bequite/auto-state/<session>.json, integration with v0.10.5 multi-model planning + v0.10.6 auth. |
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
git log --oneline       # ~28 commits expected post-v0.9.2
git tag -l              # 23 tags expected (through v0.9.2)
find .bequite/memory/ skill/ template/ cli/ docs/ tests/ examples/ -type f | wc -l  # ~210+
```

Snapshots:
- `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md` — the approved plan ratified via ExitPlanMode (early session)
- `.bequite/memory/prompts/v1/2026-05-10_initial-brief.md` — original brief preserved
- `.bequite/memory/prompts/v2/2026-05-10_constitution-v1.2.0.md` + ADR-009 + ADR-010 (v0.5.2)
- `.bequite/memory/prompts/v3/` (this snapshot) — Constitution v1.2.0 + state/recovery.md + activeContext + progress + ADRs (taken pre-v0.6.1; v0.6.1 changes layered on top during this session)

## What is the next safe task

**Resume v0.10.0 — Auto-mode state machine.** Per the build plan §4 (`v0.10.0` row) and §5 (auto-mode design):

1. Author `cli/bequite/auto.py`:
   - State machine class with states: INIT, P0_RESEARCH, P1_STACK, P2_PLAN, P3_PHASES, P4_TASKS, P5_IMPLEMENT, P6_VERIFY, P7_HANDOFF, DONE, BLOCKED, FAILED, PAUSED.
   - Per-phase contract: enter with memory + receipts + previous-phase output; exit only when artifact + Skeptic kill-shot answered + verify-gate passed + receipt emitted + commit landed.
   - State persistence at `.bequite/auto-state/<session>.json` so `bequite auto resume <session>` reloads cleanly (v0.10.1 hardens this path).
2. Safety rails:
   - Hard cost ceiling — `bequite.config.toml::cost.session_max_usd` (default $20). Reads `cli/bequite/cost_ledger.py` (v0.8.0 wired). On exceed: pause + write `.bequite/cache/cost-override.json` requirement.
   - Hard wall-clock ceiling — default 6h.
   - 3 consecutive Implementer failures on same task → BLOCKED.
   - Banned-word check — uses existing `stop-verify-before-done.sh` hook (v0.3.0).
   - Hook-block respect — never auto-override (Article IV).
   - One-way-door operations always pause: PyPI publish, npm publish, git push to main, force push, terraform apply, DB migrations against shared DBs.
3. Failure replay: capture state to `.bequite/replays/<timestamp>/` on BLOCKED/FAILED.
4. Heartbeat: write `activeContext.md` every 5 min during long phases.
5. CLI flags: `--feature`, `--max-cost-usd`, `--max-wall-clock-hours`, `--phases <subset>`, `--mode slow|fast|auto`, `--on-failure pause|abort|continue-with-warning`, `--no-skeptic` (debug only).
6. Add e2e test `tests/integration/auto/test_auto_mode_smoke.py` — drives auto-mode through P0-P7 with all real backends mocked; asserts: phase-by-phase commits, receipts emitted, state persistence, cost-ceiling trip path, banned-word trip path.
7. Bumps: `__init__.py` + `pyproject.toml` → `0.10.0`. CHANGELOG. State. Commit + tag.

Acceptance for v0.10.0: `bequite auto --feature add-health-endpoint --max-cost-usd 5` runs to DONE on the bookings-saas example (in mocked-backend mode); cost stays under $5; receipts emitted at every phase. Planted Article-V violation correctly trips BLOCKED.

After v0.10.0: v0.10.1 (auto-hardening) → v0.11.0 (MENA) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0**. **8 sub-versions remain.**

## Commands to run first (on resume)

```bash
# Orient
cat .bequite/memory/activeContext.md
cat state/current_phase.md
cat state/recovery.md

# Verify git state
git log --oneline | head -5
git tag -l                                  # expect 20 tags through v0.8.1
git status                                  # expect clean

# Smoke-test the seven working Python modules
cd cli/
python -m bequite.audit --help
python -m bequite.freshness --help
python -m bequite.verify --help
python -m bequite.receipts --help
python -m bequite.receipts_signing --help
python -m bequite route providers           # provider availability probe
python -m bequite.pricing list              # pricing table

# Run the combined integration suite (48/48 expected)
PYTHONIOENCODING=utf-8 python ../tests/integration/receipts/test_receipts_smoke.py    # 10/10
PYTHONIOENCODING=utf-8 python ../tests/integration/receipts/test_signing_smoke.py     # 9/9
PYTHONIOENCODING=utf-8 python ../tests/integration/router/test_router_smoke.py        # 15/15
PYTHONIOENCODING=utf-8 python ../tests/integration/pricing/test_pricing_smoke.py      # 14/14
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
15. `tests/integration/receipts/{test_receipts_smoke,test_signing_smoke}.py` + `tests/integration/router/test_router_smoke.py` + `tests/integration/pricing/test_pricing_smoke.py` — 48-test combined suite for v0.7.0 + v0.7.1 + v0.8.0 + v0.8.1 (all passing on Python 3.14).

## Files to NOT touch

- `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief; immutable.
- `BeQuite_MASTER_PROJECT.md` — master file; immutable.
- `.bequite/memory/prompts/v1/*` + `v2/*` + `v3/*` — versioned snapshots; immutable history.
- `.bequite/memory/decisions/ADR-*.md` — accepted ADRs; supersede via NEW ADR, never edit.
- `.git/` — never.
- `.env*` — Iron Law IV; never read or write.

## Suggested next phase

Continue v0.10.0 → v0.10.5 → v0.10.6 → v0.10.7 → v0.11.0 → v0.12.0 → v0.13.0 → v0.14.0 → v0.15.0 → **v1.0.0** per the main plan at `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md` and the v0.9.2 reshape. **9 sub-versions remain (added 2 for new feature modules per Ahmed's request).**

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
