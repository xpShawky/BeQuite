---
description: Skill quality loop — audit all BeQuite skills for bloat, shallowness, duplication, missing sections (output format / quality gate / memory rules / failure handling), stale counts, and oversized activation descriptions. Reports by default; edits only on user approval. Writes SKILL_QUALITY_AUDIT.md.
---

# /bq-skill-audit — the self-evolving skill quality loop

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

You are **BeQuite's skill auditor**. Skills must not stagnate: counts drift, descriptions bloat past activation-matching limits, sections go missing as the pack grows. This command institutionalizes the structural review that previously happened ad-hoc.

## When to use it

- Every 2–3 alpha releases, or after adding ≥2 skills
- When a skill misfires (activated wrongly / failed to activate)
- Before a stable release

## When NOT to use it

- Auditing the PROJECT's code (use `/bq-audit`) · auditing commands (covered by the alignment-audit pattern) · mid-feature work

## Required previous gates

`BEQUITE_INITIALIZED` · orthogonal workflow (maintenance — doesn't change mode/phase)

## Execution (per COMMAND_EXECUTION_CONTRACT)

### 1–2. Preflight + gates
Core pack + `MEMORY_INDEX.md` + previous `SKILL_QUALITY_AUDIT.md` (compare against last run).

### 3–6. Scope: all `.claude/skills/bequite-*/SKILL.md` (or `only=<skill>` argument)

### 7a. Registry refresh

Before per-skill checks, refresh `.bequite/skills/SKILL_REGISTRY.md`:
- Glob `.claude/skills/bequite-*/` and probe `~/.claude/skills/` (document if inaccessible/empty)
- Add rows for new skills · remove rows for deleted skills · update Cost/Risk/Q columns
- **Drift check:** registry rows vs live dirs must match 1:1; any mismatch is a HIGH finding
- **Orphan check:** every skill referenced by ≥1 command (cross-check `SKILL_USAGE_LOG.md` — a skill never selected in 90 days is an archive candidate)
- **Routing-defect scan:** SKILL_USAGE_LOG entries marked over-/under-triggered → router map fix proposals
- Update the "Last refreshed" header + review-metadata table

### 7b. The audit checks (per skill)

| Check | Threshold / rule |
|---|---|
| **Bloat** | SKILL.md > ~400 lines → split candidate (move depth to `references/` per master-skill pattern) |
| **Shallowness** | < ~60 lines or no worked procedure → deepen or merge candidate |
| **Duplication** | overlapping purpose with another skill → merge/role-split proposal |
| **Frontmatter** | valid `name` + `description` + `allowed-tools`; description ≤ ~300 chars, trigger-focused |
| **Required sections** | When to use · When NOT to use · Quality gate · failure handling · output format (where the skill produces artifacts) · memory/log rules (where relevant) |
| **Tool neutrality** | named tools framed as candidates |
| **Cross-listing** | skill referenced by ≥1 command; counts in orchestrator / CLAUDE.md / README / catalog match reality |
| **Staleness** | references to gone files, old counts, superseded modes |

### 8. Verification
Every finding carries `file:line` evidence (citation-or-strike per anti-hallucination). Findings without evidence are struck.

### 9. Report → `.bequite/audits/SKILL_QUALITY_AUDIT.md`
Per skill: PASS / findings list (severity-tagged) + verdict (keep / improve / merge / split / archive). Summary table + top-5 repair list.

**Default mode is REPORT-ONLY.** Apply repairs only when the user says so (`apply=true` or explicit follow-up) — prevents audit-churn. Exception: objectively-broken frontmatter (invalid YAML) may be fixed inline with a note.

### 10–11. Writeback (LAST_RUN · AGENT_LOG · CHANGELOG if edits applied) → next command (usually: user reviews report, then `/bq-skill-audit apply=true` for approved items)

## Skills activated

`bequite-skill-auditor` (owner) · `bequite-anti-hallucination` (evidence discipline)

## Failure behavior

Skill dir unreadable → list + skip + note · ambiguous merge call → propose both options, user decides · >20 findings → rank, fix top 5 first

## Usual next command

User reviews `SKILL_QUALITY_AUDIT.md` → `/bq-skill-audit apply=true` for approved repairs → `/bq-update` consumers pick up improvements next refresh

## Drift inputs

- **Drift inputs:** also reads `.bequite/commands/COMMAND_ID_MAP.md` + `COMMAND_ROUTER.md` + `NEXT_COMMAND_LOG.md` — flags: commands missing IDs, router routes to nonexistent commands, recommendations that are always ignored (demote) or follow-ups users run unrecommended (add).

## Next Command Recommendations

Per contract step 12: router block per `COMMAND_ROUTER.md` (typically: fixes on approval → W4.1 `/bq-verify drift` to confirm).
