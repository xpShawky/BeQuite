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

- **Build phase:** phase-2 — Verification + design module COMPLETE (covers v0.6.0 + v0.6.1; both shipped).
- **Sub-version in progress:** **v0.7.0** (next) — Reproducibility receipts: Pydantic-modeled receipt emitter + storage + chain-hash + cost roll-up.
- **Last green sub-version:** **v0.6.1** (Frontend Quality Module — vendored Impeccable + tokens.css.tpl + frontend-stack + frontend-mcps + axe gate + default-web-saas v1.1.0).
- **Last successful commit (pending):** `feat(v0.6.1): Frontend Quality Module — vendored Impeccable + tokens.css + frontend references + axe gate + default-web-saas v1.1.0`.
- **Last successful tag (pending):** **v0.6.1**.
- **Branch:** `main`.
- **Remote:** `origin = https://github.com/xpShawky/BeQuite.git` configured. **NOT pushed.** Push requires explicit owner authorization (Iron Law IV; one-way door).
- **Real git counts (post-v0.6.1, pre-commit):** ~21 commits, 16 tags pending, ~167+ tracked files.

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

**Three working Python modules** (smoke-tested via `python -m`; help output prints):
- `python -m cli.bequite.audit` — rule-based, 7 rule packs
- `python -m cli.bequite.freshness --all`
- `python -m cli.bequite.verify` — 17-gate per-Mode matrix

## What is incomplete

The remaining sub-versions to v1.0.0:

| Sub-version | Scope |
|---|---|
| **v0.7.0** (next) | Receipts JSON schema + emitter + storage at `.bequite/receipts/<sha>-<phase>.json`; Pydantic schema (version + session_id + phase + timestamp_utc + model + input{prompt_hash, memory_snapshot_hash} + output{diff_hash, files_touched} + tools_invoked[] + tests + cost + doctrine[] + constitution_version + parent_receipt); `bequite cost` reads receipts and rolls up. |
| v0.7.1 | ed25519 signing + `bequite verify-receipts` |
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
git log --oneline       # ~21 commits expected post-v0.6.1
git tag -l              # 16 tags expected (through v0.6.1)
find .bequite/memory/ skill/ template/ cli/ docs/ -type f | wc -l  # ~167+
```

Snapshots:
- `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md` — the approved plan ratified via ExitPlanMode (early session)
- `.bequite/memory/prompts/v1/2026-05-10_initial-brief.md` — original brief preserved
- `.bequite/memory/prompts/v2/2026-05-10_constitution-v1.2.0.md` + ADR-009 + ADR-010 (v0.5.2)
- `.bequite/memory/prompts/v3/` (this snapshot) — Constitution v1.2.0 + state/recovery.md + activeContext + progress + ADRs (taken pre-v0.6.1; v0.6.1 changes layered on top during this session)

## What is the next safe task

**Resume v0.7.0 — Reproducibility receipts.** Per the build plan §4 (`v0.7.0` row):

1. Author `cli/bequite/receipts.py` with a Pydantic model for the receipt schema.
2. Schema fields:
   - `version` (str, "1")
   - `session_id` (UUID)
   - `phase` (literal P0..P7)
   - `timestamp_utc` (ISO 8601)
   - `model` (object: name, reasoning_effort, fallback_model)
   - `input` (object: prompt_hash sha256, memory_snapshot_hash sha256)
   - `output` (object: diff_hash sha256, files_touched list)
   - `tools_invoked` (list of: name, args_hash sha256, exit code)
   - `tests` (object: command, exit, stdout_hash sha256)
   - `cost` (object: input_tokens, output_tokens, usd)
   - `doctrine` (list of active doctrines)
   - `constitution_version` (semver)
   - `parent_receipt` (sha256 chain pointer; null for first receipt of a session)
3. Storage: `.bequite/receipts/<sha>-<phase>.json` (sha is the receipt's own content-hash).
4. Update `bequite cost` to walk receipts and roll up by session / phase / day.
5. Emit a receipt at every phase transition (currently no-op since auto-mode lands v0.10.0; but the emitter is ready).
6. Add receipt-replay test that reconstructs prompt + memory state from receipt content.
7. Update `cli/bequite/__init__.py::__version__` → `0.7.0` and `cli/pyproject.toml::version` → `0.7.0`.
8. Update CHANGELOG, activeContext, progress, recovery; commit + tag v0.7.0.

Acceptance for v0.7.0: receipts emitted on every phase transition; `bequite cost --since v0.6.0` returns a roll-up; receipt-replay test reconstructs prompt + memory state from receipt content.

## Commands to run first (on resume)

```bash
# Orient
cat .bequite/memory/activeContext.md       # most-recent state
cat state/current_phase.md
cat state/recovery.md                       # this file

# Verify git state
git log --oneline | head -5
git tag -l                                  # expect 16 tags through v0.6.1
git status                                  # expect clean

# Smoke-test the three working Python modules
cd cli/
python -m bequite.audit --help
python -m bequite.freshness --help
python -m bequite.verify --help
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
12. `skill/references/*.md` — scraping + security + playwright-walks references + ai-automation bundled skill.
13. `cli/bequite/{audit,freshness,verify}.py` — three runnable Python modules.
14. `cli/bequite/{__main__,commands,config,skill_loader,hooks}.py` — CLI thin wrapper.

## Files to NOT touch

- `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief; immutable.
- `BeQuite_MASTER_PROJECT.md` — master file; immutable.
- `.bequite/memory/prompts/v1/*` + `v2/*` + `v3/*` — versioned snapshots; immutable history.
- `.bequite/memory/decisions/ADR-*.md` — accepted ADRs; supersede via NEW ADR, never edit.
- `.git/` — never.
- `.env*` — Iron Law IV; never read or write.

## Suggested next phase

Continue v0.7.0 → v0.7.1 → v0.8.0 → v0.8.1 → v0.9.0 → v0.9.1 → v0.10.0 → v0.10.1 → v0.11.0 → v0.12.0 → v0.13.0 → v0.14.0 → v0.15.0 → **v1.0.0** per the main plan at `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`. **13 sub-versions remain.**

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
