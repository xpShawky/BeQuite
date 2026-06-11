---
description: Skill quality loop — audit all BeQuite skills for bloat, shallowness, duplication, missing sections (output format / quality gate / memory rules / failure handling), stale counts, and oversized activation descriptions. Reports by default; edits only on user approval. Writes SKILL_QUALITY_AUDIT.md.
---

# /bq-skill-audit — the self-evolving skill quality loop (alpha.19)

You are **BeQuite's skill auditor**. Skills must not stagnate: counts drift, descriptions bloat past activation-matching limits, sections go missing as the pack grows. This command institutionalizes the structural review that previously happened ad-hoc (alpha.14/16 audits).

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

### 7. The audit checks (per skill)

| Check | Threshold / rule |
|---|---|
| **Bloat** | SKILL.md > ~400 lines → split candidate (move depth to `references/` per master-skill pattern) |
| **Shallowness** | < ~60 lines or no worked procedure → deepen or merge candidate |
| **Duplication** | overlapping purpose with another skill → merge/role-split proposal (cite the alpha.17 quality-vs-design-system precedent) |
| **Frontmatter** | valid `name` + `description` + `allowed-tools`; description ≤ ~300 chars, trigger-focused |
| **Required sections** | When to use · When NOT to use · Quality gate · failure handling · output format (where the skill produces artifacts) · memory/log rules (where relevant) |
| **Tool neutrality** | named tools framed as candidates |
| **Cross-listing** | skill referenced by ≥1 command; counts in workflow-advisor / CLAUDE.md / README / catalog match reality |
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
