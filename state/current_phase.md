# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-1` — Core domain + CLI (master §23 framing)
- **Sub-version:** Just tagged `v0.4.1`. Next: `v0.4.2` (bequite audit Python implementation).
- **Last green sub-version:** `v0.4.1` (BeQuite-unique commands; committed + tagged 2026-05-10)
- **Mode:** Safe Mode (master §4)
- **Active doctrines:** `library-package`, `cli-tool`, `mena-bilingual`
- **Constitution version:** `v1.0.1`

## What this sub-version is doing

`v0.2.0` is the **Skill orchestrator**. The brain of the harness.

Completed in this commit:
- ✅ `skill/SKILL.md` — Anthropic Skills frontmatter (name, description ≤1024 chars, allowed-tools), orchestrator persona, 7-phase router, mode selector (Fast/Safe/Enterprise), 19-command surface (master's 12 + BeQuite's 7 unique), routing matrix reference, hooks reference, auto-mode reference, banned-weasel-words enforcement.
- ✅ 11 persona files at `skill/agents/`: product-owner, research-analyst, software-architect, frontend-designer (Impeccable-loaded for frontend Doctrines), backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist, **skeptic** (adversarial twin — BeQuite's unique addition).
- ✅ `skill/routing.json` — default model routing matrix per phase + persona. Anthropic primary; OpenAI / Google / DeepSeek / Ollama as fallback per provider abstraction. Aider architect mode pattern (cheap writes + frontier review). AkitaOnRails 2026 split-only-when-genuinely-parallel rule encoded.
- ✅ `skill/templates/bequite.config.toml.tpl` — per-project config schema. mode, audience, doctrines, scale_tier, compliance, locales, safety_rails, routing overrides, providers (env-var-only), freshness, receipts, evidence, memory, hosts, skills, telemetry, mena_bilingual.
- ✅ `template/.claude/skills/bequite/README.md` — fresh-project skill-install target (`bequite skill install` v0.12.0 will populate). Documents the copy-not-symlink decision.

## Next sub-version

After `v0.2.0`: **`v0.3.0` — Hooks (deterministic gates)**.

Tasks for v0.3.0:
1. `skill/hooks/pretooluse-secret-scan.sh` — regex for API keys, JWTs, AWS access patterns. Exit 2.
2. `skill/hooks/pretooluse-block-destructive.sh` — Tier-3 commands (rm -rf, terraform destroy, DROP DATABASE, git push -f, git reset --hard). Exit 2.
3. `skill/hooks/pretooluse-verify-package.sh` — diff new imports vs registry. PhantomRaven defense. Exit 2.
4. `skill/hooks/posttooluse-format.sh` — auto-format (prettier/biome/black/ruff/clippy).
5. `skill/hooks/posttooluse-lint.sh` — warn-only lint.
6. `skill/hooks/stop-verify-before-done.sh` — banned-weasel-words check + incomplete-task check. Exit 2.
7. `skill/hooks/sessionstart-load-memory.sh` — preload Memory Bank + active ADRs + state/recovery.md.
8. `skill/hooks/sessionstart-cost-budget.sh` — load cost ceiling.
9. `tests/integration/hooks/` — fixtures + assertions per hook.
10. `template/.claude/settings.json` — hooks wired for fresh-project.

## Open questions (none blocking v0.1.2)

- E1 — GitHub org / repo name (`xpshawky/bequite` default; confirm before remote push, no remote configured)
- E2 — PyPI package name + ownership (will block v0.5.0 release)
- E3 — Studio (v2.0.0+) timing (after v1.0.0 ships, default)
- E4 — Telemetry policy (off entirely; pending ADR-002 in v0.7.0)
- E5 — Doctrine distribution model (separate org for community; pending in v0.12.0)
- E6 — MENA bilingual Researcher seeds (Ahmed seeds list at v0.11.0)
- E7 — Codex 5.5 review-mode role (review-only default; pending v0.8.0)

None of these block v0.1.2 → v0.5.x progress.

## Cost / wall-clock telemetry (this session)

Receipts ship in v0.7.0; until then, telemetry is best-effort.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
