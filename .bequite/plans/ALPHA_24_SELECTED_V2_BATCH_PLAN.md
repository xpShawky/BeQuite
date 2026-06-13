# Alpha.24 Selected-V2 + P1 Batch Plan

**Run:** 2026-06-13 · Deep Mode · **Model: claude-opus-4-8** (user's `/model` command set this; user's text said "fable 5" — conflict reported, executing on the harness-selected model, logged honestly). No live trials this pass.

## Shape decisions (FEATURE_TYPE_TAXONOMY applied)

| Selected item | Shape | Why | ID |
|---|---|---|---|
| Automation + bots | **command** `/bq-automation` (bot = `bot` profile, not a separate command) | distinct workflow + 10-artifact set + tool-neutral engine; reuses merged legacy automation content | C12 |
| AI Service Business Builder | **merged into `/bq-offer`** (`business-system`/`agency`/`service-business` modes) | orchestrates existing offer chain — a command would duplicate `/bq-offer`; user-approved merge | (C11 ext) |
| Workflow Export | **argument** `/bq-handoff workflow-export` + spec + `.bequite/exports/` | export is a handoff variant; no standalone command needed; secret-scan gate | (W5.3 arg) |
| Release Template | **argument** `/bq-release template` + spec + `.bequite/templates/` | already in the launch-kit family (alpha.22); now built | (W4.2 arg) |
| Local Business Digitizer | **command** `/bq-local-business` | distinct recurring MENA-SMB workflow + 10-artifact set + local context that doesn't fit inside offer/automation alone | C13 |
| Brand Kit Generator | **command** `/bq-brand-kit` | distinct creative workflow + 13-artifact set + research-driven non-generic identity | C14 |
| Community Pack | **command** `/bq-community` | shared by ≥3 parents (course/launch/brand) — one home beats 3 duplicated args | C15 |
| Recording-to-assets | **command** `/bq-recording` (workflow/spec-first; tools optional) | distinct media-intake workflow; dedup strategy is the core IP | C16 |
| Starting Path Advisor | **command** `/bq-start` | distinct advisory workflow + 12-artifact set; user-approved | C17 |
| Course Architect | **strengthen `/bq-course`** (no new skill) | spec/command enrichment; skill deferred until live use proves reuse | (C5 ext) |

**New skills:** **+1** `bequite-automation-engineer` (merged from legacy `automation-architect` + `ai-automation` bundled refs — satisfies Part 2 merge + Part 5 build) → **31 skills**. No other new skills (brand/community/recording/start/local-business reuse existing skills).
**New commands:** 6 (C12–C17) → **59 active commands** + 1 alias.

## Deferred (stay parked, descriptions improved in MASTER §E)

`/bq-data-product` · Agent Pack Generator · App Store Launch Kit · cross-agent adapters/wrapper · any heavy media runtime beyond the recording workflow/spec · any provider API integration · any new app/dashboard/studio.

## Files to create/update (high level)

**P1:** P1_SKILL_PATCH_AUDIT · patch problem-solver + multi-model-planning skills · LEGACY_SKILL_FOLDER_AUDIT + `skill/README.md` deprecation pointer · HIGH_RISK_COMMAND_TEST_CASES + HIGH_RISK_COMMAND_HARDENING_AUDIT · OKAY_COMMAND_TIGHTENING_AUDIT.
**Builds:** 6 command files + 7 specs (AUTOMATION_ENGINE, WORKFLOW_EXPORT, RELEASE_TEMPLATE, LOCAL_BUSINESS, BRAND_KIT_ENGINE, COMMUNITY_PACK, RECORDING_TO_ASSETS, STARTING_PATH_ADVISOR) + offer/handoff/release/course extensions + 1 new skill.
**Memory scaffolds** (dir + README pointer per established pattern; files created on first run): `.bequite/{automation,exports,templates,local-business,brand,community,recordings,start}/`.
**Sync:** ID map · both routers · SKILL_REGISTRY/ROUTER/USAGE_LOG · ORCHESTRATION_MAP · MASTER · README · commands.md · catalog · CLAUDE.md · installers (8 new dirs) · changelog/agent-log/last-run/version → alpha.24.

## Risks & mitigations

- **Command-count growth (53→59):** all 6 are user-selected, each passes the standalone test (distinct workflow + artifacts), bots/business-system/export/template correctly kept as profiles/args not commands. Anti-bloat honored where it applies.
- **Recording heavy-runtime risk:** spec-first, tools OPTIONAL + tool-dependent, no yt-dlp/ffmpeg/Whisper installed or required by default; transcript-first; no ToS-violating downloads. Mitigated.
- **Legacy merge risk:** merge only unique useful content (automation refs) into ONE new skill; everything else legacy-marked, nothing deleted. Mitigated.
- **Dependency risk:** zero installs; all tool lists are candidates per tool-neutrality. Mitigated.

## No-heavy-runtime plan

Every new command outputs markdown plans/blueprints only. Automation/recording name tools as candidates (official-API-first), never install. No provider keys, no daemons, no DB.

## Rollback plan

Pure additive markdown pass — `git revert` the release commit restores prior state; no migrations, no destructive ops. Legacy `skill/` untouched except an added README pointer.

## Acceptance criteria

Per the prompt's Part 16 + the `/bq-start` addendum criteria — verified in the final report against repo files.

## Verification commands

`ls .claude/commands/*.md | wc -l` (expect 60 files = 59 active + 1 alias) · `ls -d .claude/skills/bequite-*/ | wc -l` (expect 31) · `bash -n scripts/install-bequite.sh` · PowerShell ParseFile on ps1 · grep stale-count sweep.
