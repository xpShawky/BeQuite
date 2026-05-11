# BeQuite MVP — Lightweight scope (v3.0.0-alpha.1)

**Status:** authored 2026-05-11
**Companion:** ADR-001 (`docs/decisions/ADR-001-lightweight-skill-pack-first.md`)

This spec defines exactly what v3.0.0-alpha.1 ships. Out-of-scope items are deferred to v3.1+ or paused indefinitely.

---

## 1. In scope (v3.0.0-alpha.1 ships)

### File deliverables

| Path | Status | Description |
|---|---|---|
| `.claude/commands/bequite.md` | ✅ | Root /bequite menu |
| `.claude/commands/bq-help.md` | ✅ | Full command reference |
| `.claude/commands/bq-init.md` | ✅ | Initialize BeQuite in a repo |
| `.claude/commands/bq-discover.md` | ✅ | Inspect repo → DISCOVERY_REPORT.md |
| `.claude/commands/bq-doctor.md` | ✅ | Env health → DOCTOR_REPORT.md |
| `.claude/commands/bq-clarify.md` | ✅ | 3-5 high-value questions |
| `.claude/commands/bq-research.md` | ✅ | Library + freshness verification → RESEARCH_REPORT.md |
| `.claude/commands/bq-scope.md` | ✅ | IN / OUT / NON-GOALS → SCOPE.md |
| `.claude/commands/bq-plan.md` | ✅ | IMPLEMENTATION_PLAN.md |
| `.claude/commands/bq-multi-plan.md` | ✅ | Manual-paste multi-model planning |
| `.claude/commands/bq-assign.md` | ✅ | Plan → atomic TASK_LIST.md |
| `.claude/commands/bq-implement.md` | ✅ | One task at a time |
| `.claude/commands/bq-add-feature.md` | ✅ | Mini-cycle for one feature |
| `.claude/commands/bq-fix.md` | ✅ | Reproduce → root cause → patch → test |
| `.claude/commands/bq-test.md` | ✅ | Run + write tests |
| `.claude/commands/bq-audit.md` | ✅ | Full project audit |
| `.claude/commands/bq-review.md` | ✅ | Review current changes |
| `.claude/commands/bq-red-team.md` | ✅ | Adversarial Skeptic review |
| `.claude/commands/bq-verify.md` | ✅ | Full gate matrix |
| `.claude/commands/bq-release.md` | ✅ | Release prep |
| `.claude/commands/bq-changelog.md` | ✅ | CHANGELOG hygiene |
| `.claude/commands/bq-memory.md` | ✅ | Read / write BeQuite memory snapshots |
| `.claude/commands/bq-recover.md` | ✅ | Resume after session break |
| `.claude/commands/bq-handoff.md` | ✅ | Generate HANDOFF.md |
| `.claude/skills/bequite-project-architect/SKILL.md` | ✅ | Stack + ADR + scale-tier procedures |
| `.claude/skills/bequite-problem-solver/SKILL.md` | ✅ | Reproduce-first + 5-whys + bisect |
| `.claude/skills/bequite-frontend-quality/SKILL.md` | ✅ | 10 principles + 15 AI-slop patterns + Impeccable |
| `.claude/skills/bequite-testing-gate/SKILL.md` | ✅ | Test pyramid + contract tests + snapshot rules |
| `.claude/skills/bequite-release-gate/SKILL.md` | ✅ | CI parity + semver + CHANGELOG + signing |
| `.claude/skills/bequite-scraping-automation/SKILL.md` | ✅ | Article VIII + polite mode + 2026 tool catalog |
| `.claude/skills/bequite-multi-model-planning/SKILL.md` | ✅ | 5 modes + manual paste + tie-break order |
| `.bequite/state/PROJECT_STATE.md` (template) | ✅ | |
| `.bequite/state/CURRENT_PHASE.md` (template) | ✅ | |
| `.bequite/state/LAST_RUN.md` (template) | ✅ | |
| `.bequite/state/DECISIONS.md` (template) | ✅ | |
| `.bequite/state/OPEN_QUESTIONS.md` (template) | ✅ | |
| `.bequite/logs/AGENT_LOG.md` (template) | ✅ | |
| `.bequite/logs/CHANGELOG.md` (template) | ✅ | |
| `.bequite/logs/ERROR_LOG.md` (template) | ✅ | |
| `.bequite/prompts/{user_prompts,generated_prompts,model_outputs}/` | ✅ | |
| `.bequite/{audits,plans,tasks}/` | ✅ | |
| `scripts/install-bequite.ps1` | ✅ | Windows installer |
| `scripts/install-bequite.sh` | ✅ | macOS / Linux installer |
| `README.md` | ✅ | Rewritten — leads with skill pack |
| `CLAUDE.md` | ✅ | Shortened |
| `docs/decisions/ADR-001-lightweight-skill-pack-first.md` | ✅ | The reset ADR |
| `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` | ✅ | End-user install runbook |
| `docs/runbooks/USING_BEQUITE_COMMANDS.md` | ✅ | Per-command practical guide |
| `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` | ✅ | This architecture |
| `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md` | ✅ | THIS document |
| `.bequite/audits/DIRECTION_RESET_AUDIT.md` | ✅ | Keep/pause/delete inventory |

### Behavior contracts

1. **Install:** one-line PowerShell / bash. Refuses to overwrite memory without `--force`. Copies files only. No package install.
2. **`/bequite` root menu:** reads state, classifies project, recommends next 3 commands, prints full command map.
3. **Every command:** has YAML `description:`, step-by-step procedure, declared reads + writes, declared next command.
4. **Every skill:** has Anthropic Skills SKILL.md frontmatter (name, description, allowed-tools).
5. **Memory:** every command that takes action updates `.bequite/state/LAST_RUN.md` + appends `.bequite/logs/AGENT_LOG.md`.
6. **Banned weasel words:** enforced by commands (especially `/bq-implement`, `/bq-verify`, `/bq-release`). Listed in CLAUDE.md.

---

## 2. Out of scope (v3.1+)

| Item | Target |
|---|---|
| Codex / Cursor / Antigravity slash-command compatibility | v3.1 |
| Per-Doctrine skill bundles (bequite-fintech-pci, bequite-healthcare-hipaa, ...) | v3.2 |
| Skill marketplace / community skills | v3.3 |
| Hooks for blocking destructive ops (carry over from v2.x line) | v3.1 |
| BeQuite GitHub integration (Issues + PRs from commands) | v3.x+ |
| Multi-project orchestration (`/bq-portfolio` for tracking N projects) | v3.x+ |

---

## 3. NON-GOALS (will not ship)

- A web dashboard for BeQuite itself
- A localhost server for BeQuite itself
- A database for BeQuite memory (filesystem only)
- A built-in auth system
- Docker / containers as a dependency for the skill pack
- Heavy frontend (React, Vue, Svelte) as a dependency for the skill pack
- Provider API integrations (OpenAI / Anthropic / etc.) as a dependency
- 3D models (Blender / R3F) as a dependency
- A package on npm or PyPI for the skill pack (it's a folder of markdown files, not an installable package)

---

## 4. Acceptance criteria for v3.0.0-alpha.1 ship

- [x] All 24 slash command files exist with valid YAML frontmatter
- [x] All 7 skill files exist with valid SKILL.md format
- [x] `.bequite/` template files have real content (not "TODO" placeholders)
- [x] `scripts/install-bequite.{ps1,sh}` exist
- [x] `README.md` leads with the skill-pack install command
- [x] `CLAUDE.md` shortened to point at the new structure
- [x] `docs/decisions/ADR-001-lightweight-skill-pack-first.md` exists
- [x] `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` exists
- [x] `docs/runbooks/USING_BEQUITE_COMMANDS.md` exists
- [x] `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` exists
- [x] `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md` (this file) exists
- [x] `.bequite/audits/DIRECTION_RESET_AUDIT.md` exists with full keep/pause/delete inventory
- [x] No heavy default dependencies introduced
- [x] No Docker / database / frontend / API required for the skill pack
- [x] All work committed to main + ready for push

**Pending:**

- [ ] Live verification inside Claude Code (user task — paste `/bequite` into Claude Code, confirm menu renders)
- [ ] Tag `v3.0.0-alpha.1` (user-gated; not auto-tagged)
- [ ] Decision: delete heavy assets (studio/, docker-compose.yml, ...) or keep paused. **User-gated.** Default: keep paused.

---

## 5. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| User invokes `/bequite` in Claude Code; nothing happens (command not picked up) | low | high | Test inside Claude Code; verify YAML frontmatter parses. |
| `/bq-implement` runs ahead without acceptance criteria → produces low-quality work | medium | medium | Commands enforce reading TASK_LIST.md first; refuse to run without an approved task |
| Skill pack feels "too prescriptive" — users want to skip steps | medium | low | Runbook (`USING_BEQUITE_COMMANDS.md` §"When to break the rules") documents safe ways to skip |
| Two install paths (skill pack + Python CLI) confuse users | medium | low | README leads with skill pack; CLI is "optional supplemental" footnote |
| Studio later gets deleted; user regrets it | low | medium | All heavy assets kept on disk in `studio/` per DIRECTION_RESET_AUDIT — deletion requires explicit approval |

---

## 6. Verification (post-ship, user-side)

What a real user does to verify v3.0.0-alpha.1 works:

```
1. Open an existing project in Claude Code (not BeQuite itself)
2. Run: irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
3. Confirm output: "BeQuite installed" with summary of files copied
4. In Claude Code, type: /bequite
5. Expect: the menu renders showing project state + recommended next 3 commands
6. Type: /bq-init
7. Expect: state files materialize at .bequite/state/
8. Type: /bq-discover
9. Expect: .bequite/audits/DISCOVERY_REPORT.md appears with detected stack
10. Type: /bq-help
11. Expect: full command reference grouped by phase
```

If any of those fail, that's a v3.0.0-alpha.2 bug to fix.

---

## 7. What NOT to claim until verified

Article VI honest reporting:

- I (the agent that authored this) **have not run `/bequite` inside a live Claude Code session** against this content. The files are structurally correct (YAML frontmatter validates, SKILL.md format matches Anthropic Skills spec, memory template files have real content), but the actual command-dispatch behavior is unverified.
- I have **not pushed this to a fresh project + tested the installer end-to-end** post-this-commit. The PowerShell + bash installer scripts are written; they have not been live-run from `raw.githubusercontent.com`.

User-verification step closes both gaps. Until then, v3.0.0 is "alpha" honestly.
