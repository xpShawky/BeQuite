# Active Context: BeQuite

> The most-edited file in `.bequite/memory/`. Updated at the end of every task. Phase-snapshotted at the end of every phase.

---

## Now (last edited: 2026-05-10)

- **Active feature:** `BeQuite v1.0.0` (the build of BeQuite itself)
- **Active phase:** `phase-1` — Core domain + CLI (master §23 framing)
- **Active sub-version:** v0.4.1 just tagged. Eight sub-versions tagged this session: v0.1.0 → v0.4.1.
- **Active mode:** `auto` (Ahmed authorised autonomous execution; safety rails per `state/project.yaml::safety_rails`)
- **Project mode (BeQuite-itself):** Safe Mode (newly named per Constitution v1.0.1)
- **Skeptic gate state:** `cleared` — merge audit + ADR-008 reviewed; Constitution amendment rationale recorded
- **Last green sub-version:** `v0.1.1` (Doctrines pack — 8 doctrines committed + tagged 2026-05-10)
- **Constitution version:** `v1.0.1` (just amended — patch bump from v1.0.0; ADR-008-master-merge)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual`
- **Cost-ceiling status:** session-default ($20 USD); not yet tracked (receipts ship in v0.7.0)
- **Wall-clock-ceiling status:** session-default (6 h); not yet tracked

## What I'm doing right now

`v0.2.0` Skill orchestrator. `skill/SKILL.md` written (Anthropic Skills frontmatter; orchestrator persona; 7-phase router; mode selector for Fast/Safe/Enterprise; 19-command surface). 11 personas authored at `skill/agents/` (master's 10 + Skeptic). `skill/routing.json` encodes model + reasoning-effort per phase/persona, with provider abstraction. `bequite.config.toml.tpl` defines per-project config schema. `template/.claude/skills/bequite/` wired for `bequite skill install`. About to commit + tag `v0.2.0`, then proceed to `v0.3.0` (Hooks).

Earlier in session: v0.1.2 master-file merge — `BeQuite_MASTER_PROJECT.md` (2858 lines) was introduced mid-session by Ahmed, post-`v0.1.1` tag. Senior-architect call: do not discard 5800+ lines of v0.1.0/v0.1.1 work; instead **two-layer architecture** (Harness now, Studio v2.0.0+).

Adopted into v0.1.2 (this commit):
- Master merge audit at `docs/merge/MASTER_MD_MERGE_AUDIT.md`.
- Root `CLAUDE.md` + `AGENTS.md` (master §11, §12).
- `state/` files (project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json) — master §10.2 pattern.
- `prompts/` directory (7 prompt packs: master, discovery, research, stack_decision, implementation, review, recovery) — master §10.4 pattern.
- `evidence/README.md` — master §3.6, §10.3, §21 pattern.
- `ADR-008-master-merge.md` capturing the decision.
- Constitution v1.0.0 → v1.0.1 patch amendment: Modes section (Fast/Safe/Enterprise from master §4), command-safety three-tier (master §19.4), prompt-injection rule (master §19.5), three-level definition-of-done (master §27), state/ files reference in Article III. Additive only. Both `skill/templates/constitution.md.tpl` and `.bequite/memory/constitution.md` updated.
- `README.md` — added two-layer architecture section + status table.
- `CHANGELOG.md` — added v0.1.1 + v0.1.2 entries.
- `BeQuite_MASTER_PROJECT.md` — now tracked.

Personas decision: master's 10 named roles + Skeptic + FrontendDesign-Impeccable = 12 personas total. To be authored in `v0.2.0`.

Slash commands decision: master's 12 names + BeQuite's 7 unique extras = 19 commands total. To be authored in `v0.4.0`–`v0.4.3`.

Next: stage all v0.1.2 files; commit with conventional-commits message; tag `v0.1.2`. Then proceed to `v0.2.0` (Skill orchestrator).

## Open questions (none blocking v0.1.2)

- [ ] E1 — GitHub org / repo name (`xpshawky/bequite` default; confirm before remote push, no remote configured)
- [ ] E2 — PyPI package name + ownership (will block v0.5.0 release)
- [ ] E3 — Studio (v2.0.0+) timing (after v1.0.0 ships, default)
- [ ] E4 — Telemetry policy (off entirely; pending ADR-002 in v0.7.0)
- [ ] E5 — Doctrine distribution model (separate org for community; pending in v0.12.0)
- [ ] E6 — MENA bilingual Researcher seeds (Ahmed seeds list at v0.11.0)
- [ ] E7 — Codex 5.5 review-mode role (review-only default; pending v0.8.0)

None of these block v0.1.2 → v0.5.x progress.

## Blockers

| Blocker | Why it blocks | Owner | Mitigation |
|---|---|---|---|
| (none) | | | |

## Next 3 things I'll do

1. Commit + tag `v0.2.0` (Skill orchestrator + 11 personas + routing + config TOML + skill-install template).
2. Begin `v0.3.0` (Hooks): 8 deterministic-gate shell scripts + integration test fixtures + template/.claude/settings.json.
3. Begin `v0.4.0` (Slash commands wave 1: master's 12 names) immediately after v0.3.0.

## Heartbeat (auto-mode only)

- Last heartbeat: 2026-05-10 (this update)
- Last receipt: none (receipts ship in v0.7.0)
- Last commit: `50ebfe6 feat(v0.1.1): doctrines pack — 8 default Doctrines for project-type rules`
- Pending commit: v0.1.2 (master-merge)

## Recent decisions (last 8)

```
2026-05-10  ADR-008 accepted: two-layer architecture; Constitution v1.0.0 → v1.0.1 patch amendment.
2026-05-10  Personas merge: master's 10 + Skeptic + FrontendDesign-Impeccable = 12. (DEC-007)
2026-05-10  Slash commands merge: master's 12 + BeQuite's 7 unique = 19. (DEC-008)
2026-05-10  Master file scope deferred: TypeScript monorepo + DB + web UI → Studio v2.0.0+.
2026-05-10  Iron Laws layered (7 articles); Doctrines forkable. (DEC-003)
2026-05-10  Skill-first distribution; CLI is thin Python wrapper. (DEC-002)
2026-05-10  Engineer-first v1; vibe-handoff seeded into artifact discipline. (DEC-001)
2026-05-10  Full v1 power from day 1 (15 sub-versions, autonomous execution authorised by Ahmed). (DEC-004)
```
