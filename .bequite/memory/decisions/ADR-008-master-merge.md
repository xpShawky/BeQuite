---
adr_id: ADR-008-master-merge
title: Master file merge — two-layer architecture and Constitution v1.0.0 → v1.0.1 amendment
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
superseded_by: null
constitution_version: 1.0.0          # the version this ADR was decided UNDER
related_articles: [I, II, III, IV]
related_doctrines: []
---

# ADR-008: Master file merge — two-layer architecture and Constitution v1.0.0 → v1.0.1 amendment

> Status: **accepted** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

`BeQuite_MASTER_PROJECT.md` (2858 lines) was introduced mid-session, after `v0.1.1` had been committed and tagged under the contract ratified via `ExitPlanMode`. The master file is structurally consistent with the original `BEQUITE_BOOTSTRAP_BRIEF.md` but prescribes a substantially wider implementation: a TypeScript pnpm + Turborepo monorepo with Next.js dashboard, NestJS API, Postgres + Prisma, Worker, Redis + BullMQ, Docker Compose, k6 load tests, OpenTelemetry traces. The original direction (skill-first Markdown + Python CLI + repo template) is the current build.

Ahmed instructed: "merge anything useful and continue work." Senior-architect call required.

The full reconciliation analysis is at `docs/merge/MASTER_MD_MERGE_AUDIT.md`. This ADR captures the decision.

## Decision

**Two-layer architecture.** BeQuite is built in two layers sharing one brain:

- **Layer 1 — Harness** (current; v0.1.0 → v1.0.0). SKILL.md + Python CLI + repo template. Markdown + Python 3.11+ + bash hooks. Distributable via `uvx`/`pipx`. Source of truth.
- **Layer 2 — Studio** (v2.0.0+). Next.js dashboard + NestJS API + Worker + Postgres. TypeScript pnpm + Turborepo. Reads what Layer 1 writes; the visual surface.

Layer 2 is **planned**, not started. After v1.0.0 ships and Ahmed authorises.

**Constitution v1.0.0 → v1.0.1 amendment** — patch bump. Additive only:

1. Adds **Modes section** (Fast / Safe / Enterprise) per master §4. Modes are project-complexity tiers; orthogonal to Doctrines.
2. Adds **command-safety three-tier classification** (safe / needs approval / dangerous) per master §19.4. Wired into PreToolUse hooks (v0.3.0) + auto-mode safety rails (v0.10.0).
3. Adds **prompt-injection rule** per master §19.5. External content (web pages, GitHub issues, Reddit, dependency READMEs, error messages) treated as untrusted; never overrides BeQuite operating rules.
4. Adds **three-level definition-of-done** (feature / phase / release) per master §27. Cross-referenced from Article II.
5. Adds **`state/` files reference** to Article III's SessionStart reads. Memory Bank is durable cross-session brain; `state/` is current operational state. Both required.

**Personas** — adopt master's 10 named roles (product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist) **+ keep Skeptic as #11 + add FrontendDesign-Impeccable as #12**. 12 personas total.

**Slash commands** — adopt master's 12 names (`/discover`, `/research`, `/decide-stack`, `/plan`, `/implement`, `/review`, `/validate`, `/recover`, `/design-audit`, `/impeccable-craft`, `/evidence`, `/release`) **+ keep BeQuite's unique extras** (`/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`). 19 commands total.

## Rationale

The master file is genuinely useful. Adopting it wholesale would discard ~5800 lines of v0.1.0 + v0.1.1 work that was ratified via `ExitPlanMode` and is structurally aligned with Ahmed's earlier four ratified fork answers (engineer-first / skill-first / layered Constitution / full-power v1).

The two-layer architecture honours the master's ambition (full-stack web UI for non-engineers; visual phase board; database for project history) **without** abandoning the wedge that justifies BeQuite over Spec-Kit / BMAD / Cline / Superpowers / Lovable / v0 / Bolt:

- Skill-first portability across 25+ hosts.
- The vibe-to-handoff niche.
- Receipts (cryptographic proof) on top of evidence (filesystem proof).
- Knowledge-freshness probe defending against stack rot.
- Skeptic adversarial twin distinct from Reviewer.
- MENA bilingual support as v1.

The Constitution amendment is patch-bump (v1.0.0 → v1.0.1) because it is **purely additive**. No Iron Law removed or relaxed.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| **A. Wholesale switch to master's monorepo stack** | Master is more ambitious; UI is more familiar | Discards 5800+ lines of v0.1.0/v0.1.1; breaks the ratified ExitPlanMode contract; conflicts with skill-first decision; 6+ month timeline | Disregards the work-in-flight and the vibe-to-handoff wedge |
| **B. Reject the master entirely** | Stays purely on the original brief + plan | Ignores genuinely useful master additions (modes, recovery prompt, persona names, command-safety classification, common-gaps audit) | The master has real value; rejecting it wholesale would be lazy |
| **C. Two-layer architecture (THIS ADR)** | Both directions honoured; no work discarded; wedge preserved; master's UI ambition lands as v2.0.0+ | More moving parts to track | None significant |

Option C selected.

## Consequences

### Positive

- v0.1.0 + v0.1.1 work preserved; no rework.
- Master's useful additions (modes, recovery, personas, commands, common-gaps) baked into v0.1.2 + later sub-versions.
- Studio (Layer 2) becomes a credible v2.0.0+ deliverable that reads what the harness writes — single source of truth.
- The vibe-to-handoff wedge (the unoccupied niche) preserved.

### Negative

- Two-layer means two sub-version trees (v0.x.0 → v1.0.0 for Layer 1, v2.x.0+ for Layer 2). Adds some cognitive load.
- Until Layer 2 ships, the master's web-UI ambitions are deferred. Some users may want the dashboard sooner.
- Some master claims (TypeScript everywhere) become Layer-2-only; users who prefer TS over Python for the harness will have to wait until they want Studio.

### Constitutional impact

- Patch bump v1.0.0 → v1.0.1.
- No Iron Law removed or relaxed.
- New material in Constitution: Modes section, command-safety classification, prompt-injection rule, three-level def-of-done, state/ files reference.

### Refactoring path

If we ever decide Layer 2 should subsume Layer 1 (e.g. fold the CLI into the Studio's worker), it's a **major-version** ADR (v3.x.0+) requiring explicit Iron Law amendment to the distribution discipline.

## Verification

- ✅ `docs/merge/MASTER_MD_MERGE_AUDIT.md` exists and is complete (Buckets A / B / C / D / E classified).
- ✅ `CLAUDE.md` and `AGENTS.md` at repo root reference the new structure.
- ✅ `state/` files written (project.yaml, current_phase.md, recovery.md, indexes).
- ✅ `prompts/` written (master, discovery, research, stack_decision, implementation, review, recovery).
- ✅ `evidence/README.md` written.
- ✅ Constitution v1.0.0 → v1.0.1 amendment applied to both `skill/templates/constitution.md.tpl` AND `.bequite/memory/constitution.md`.
- ✅ Receipt for v0.1.2 (forthcoming when v0.7.0 ships) will reference this ADR.

## References

- Related ADRs: ADR-001-stack (drafting in v0.5.0)
- External docs: master file at `BeQuite_MASTER_PROJECT.md`; original brief at `BEQUITE_BOOTSTRAP_BRIEF.md`
- Plan snapshot: `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`
- Memory Bank entries: `.bequite/memory/systemPatterns.md::ADR index`, `.bequite/memory/progress.md::Decisions made`

## Amendments

```
2026-05-10 — initial draft + accepted in same session per Ahmed's "merge anything useful and continue work" instruction.
```
