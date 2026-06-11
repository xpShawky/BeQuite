---
name: bequite-skill-auditor
description: Skill-pack quality discipline — structural review of all BeQuite skills for bloat, shallowness, duplication, missing required sections, stale counts, and activation-description quality. Evidence-cited findings; report-only by default; merge/split/archive proposals. Invoked by /bq-skill-audit.
allowed-tools: Read, Glob, Grep, Edit, Write
---

# bequite-skill-auditor — keep the pack healthy

## Purpose

A skill pack rots in predictable ways: descriptions bloat past activation-matching usefulness, new skills overlap old ones, counts in docs drift from reality, sections added by one repair pass get omitted by the next feature. This skill encodes the structural review so it's repeatable, not heroic.

## The healthy-skill profile

- Frontmatter: valid `name`/`description`/`allowed-tools`; description ≤ ~300 chars, written as ACTIVATION TRIGGERS (when should this load?) not marketing
- Body: 60–400 lines; depth beyond that goes to `references/` (master-skill pattern, alpha.17)
- Required sections present: purpose · when to use · when NOT to use · procedure/checklist · output format (artifact-producing skills) · quality gate · common mistakes · failure handling · memory/log rules (where relevant)
- Tool neutrality language present where tools are named
- Referenced by ≥1 command; reflected in workflow-advisor's knowledge + repo counts

## The skill-tier model

| Tier | Role | Example |
|---|---|---|
| Master / coordinator | owns a domain, coordinates members, holds references/ | frontend-design-system |
| Specialist | one domain's deep procedure | backend-architect, security-reviewer |
| Cross-cutting | applies to many workflows | context-engineer, anti-hallucination |
| Capability | powers one user-facing command | presentation-builder, writing-dna, job-finder |

Audit rule: a skill drifting across tiers (specialist accumulating coordination logic) is a split candidate.

## Severity model

- **HIGH** — broken frontmatter · skill orphaned (no command references it) · direct duplication
- **MEDIUM** — missing required section · description > 300 chars · stale facts (wrong counts, gone files)
- **LOW** — style drift, thin examples, minor bloat

## Evidence discipline

Every finding: `skill:line` + quoted evidence. No evidence → struck (anti-hallucination citation-or-strike). Compare with previous SKILL_QUALITY_AUDIT to show trend (improving / stable / degrading).

## When NOT to use this skill

Project-code audits (`/bq-audit`) · single-skill quick fix the user already specified (just edit it) · command-file audits (alignment-audit pattern)

## Quality gate

- [ ] All skills enumerated (Glob, not memory)
- [ ] Every finding evidence-cited; none struck silently
- [ ] Verdicts limited to: keep / improve / merge / split / archive — each with one-line rationale
- [ ] Report-only honored unless user approved edits
- [ ] Writeback done (LAST_RUN, AGENT_LOG; CHANGELOG only if edits applied)

## Common mistakes

Auditing from memory instead of reading files · proposing merges that erase a distinct activation trigger · "improving" prose style instead of structure (churn) · fixing findings inline in report-only mode · forgetting to update counts in workflow-advisor/README/CLAUDE.md after an approved merge

## Failure handling

Unreadable skill → skip + note · tie between merge/split options → present both · audit reveals a COMMAND problem → note it for the alignment audit, don't fix out-of-scope
