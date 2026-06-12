# Skill Registry (alpha.22 + orchestration update)

> **The compact routing index over all BeQuite skills.** Loaded FIRST by the Skill Router (token-cheap); full SKILL.md files load only after selection. **Single-source-of-truth rule:** detailed "when to use / when not / inputs / outputs / procedure" live in each SKILL.md — this registry holds ROUTING METADATA + terse pointers, never duplicated prose.
>
> **Refreshed by:** `/bq-skill-audit` (registry refresh is now step 1 of every audit run). **Last refreshed:** 2026-06-12 (alpha.22 — **30 skills** indexed; orchestrator added in the orchestration update; localization-rtl + guard-pass added earlier in alpha.22).
>
> **Discovery scope:** project `.claude/skills/bequite-*/` ✅ (30 found) · global `~/.claude/skills/` checked 2026-06-11 → **empty/not present on this machine**; only project skills indexed. Re-probe at each refresh.

Legend — **Cost** (token weight when fully loaded): L < 150 lines · M 150–300 · H > 300 or has references/. **Risk** (what damage misuse can do): L docs/advice · M writes project files · H touches security/prod/money domains. **Q** (quality status from last `/bq-skill-audit`): ✓ PASS · ~ improve-backlogged.

## Routing table (primary lookup)

| Skill | Domains | Trigger keywords / intents | Usual commands | Compatible with | Conflicts | Cost | Risk | Q |
|---|---|---|---|---|---|---|---|---|
| `anti-hallucination` | verification, claims, evidence | verify, prove, "is this true", done-claims, package check | review, verify, audit, red-team, writing strict | all (cross-cutting) | — | M | L | ✓ |
| `backend-architect` | backend, API | API, endpoint, queue, cache, rate limit, idempotency | plan, feature, fix | database-architect, security-reviewer | — | M | M | ✓ |
| `context-engineer` | context, memory, long tasks | multi-step, resume, compaction, "lost context", session | plan, implement, auto, recover | all (cross-cutting) | — | M | L | ✓ |
| `database-architect` | database, schema | schema, migration, index, N+1, transaction, RLS data | plan, feature, fix | backend-architect | — | M | **H** (migrations) | ✓ |
| `delegate-planner` | delegation, cost | delegate, cheap model, task pack, cross-session | auto/plan/assign/review delegate | researcher, frontier-coach | — | M | M | ✓ |
| `devops-cloud` | devops, deploy, infra | deploy, CI/CD, VPS, nginx, rollback, env vars, monitoring | plan, feature, verify, release | release-gate, security-reviewer | — | M | **H** (prod) | ✓ |
| `frontend-design-system` | frontend, UI/UX, visual identity | website, landing page, UI, redesign, cinematic, sections, design system | feature, fix, auto, uiux-variants, live-edit, audit, verify | ux-ui-designer, frontend-quality, live-edit (coordinates them) | — | **H** (master + references/) | M | ✓ |
| `frontend-quality` | UI slop detection | AI-looking, dead buttons, hidden text, contrast, mock data | audit, review, verify (UI present) | frontend-design-system (member) | — | L | L | ✓ |
| `frontier-reasoning-coach` | operating discipline (cross-cutting) | deep mode, delegate packs, drift symptoms, "be rigorous" | auto/plan deep, assign/review delegate, red-team, verify, skill-audit | all (governs HOW, not WHAT) | — | M | L | ✓ |
| `job-finder` | jobs, career | job, freelance, gig, remote work, apply | job-finder | make-money | — | M | L | ✓ |
| `live-edit` | frontend section edits | "make X less crowded", section, spacing, live edit | live-edit, auto live-edit | frontend-design-system (member) | — | M | M | ✓ |
| `make-money` | earning, business | make money, income, earning, side hustle, hidden gems | make-money | job-finder, product-strategist | — | M | L | ✓ |
| `multi-model-planning` | planning, second opinion | multi-model, second opinion, ChatGPT compare, debate | multi-plan | project-architect | — | M | L | ~ |
| `presentation-builder` | presentation, slides | slides, deck, PPTX, keynote, lecture, PDF→slides | presentation, auto presentation | ux-ui-designer, writing-dna (notes), researcher | — | **H** | M | ✓ |
| `problem-solver` | debugging | bug, broken, error, reproduce, root cause, bisect | fix | testing-gate, domain specialist | — | L | L | ~ |
| `product-strategist` | product, scope | MVP, persona, JTBD, scope, pricing, differentiation | clarify, scope, plan | project-architect | — | M | L | ✓ |
| `project-architect` | architecture, stack | stack choice, ADR, architecture, scale | plan, research, scope | all specialists | — | M | M | ✓ |
| `release-gate` | release, ship | release, version, tag, changelog, publish, ship | verify, release, changelog | devops-cloud, testing-gate | — | L | M | ✓ |
| `researcher` | research, evidence | research, compare, "what's best", competitors, verify package | research, plan (deep) | all (feeds everyone) | — | M | L | ✓ |
| `scraping-automation` | scraping, crawling, browser automation | scrape, crawl, automate site, monitor page | auto scraping/automation | backend-architect | — | M | M | ✓ |
| `security-reviewer` | security, prompt injection | vulnerability, auth review, OWASP, injection, secrets, CVE | plan, feature, fix, audit, review, red-team | anti-hallucination, devops-cloud | — | M | **H** | ✓ |
| `skill-auditor` | skill maintenance | skill audit, stale skills, pack health | skill-audit | anti-hallucination | — | M | L | ✓ |
| `testing-gate` | testing | test, coverage, pyramid, regression | test, feature, fix | all build skills | — | L | L | ✓ |
| `updater` | BeQuite maintenance | update BeQuite, refresh pack | update | — | — | M | M | ✓ |
| `ux-ui-designer` | UI/UX design, accessibility | design principles, typography, color, WCAG, a11y | plan, feature, audit (UI) | frontend-design-system (member) | — | M | L | ✓ |
| `workflow-advisor` | routing, orientation | "which command", "where to start", what next | suggest | — (read-only) | — | M | L | ✓ |
| `writing-dna` | writing, content, academic, brand voice | write in my style, human-quality, rewrite, blog, academic, voice | writing-dna, presentation (notes) | anti-hallucination (strict), researcher | — | M | L | ✓ |
| `localization-rtl` | Arabic, MENA, RTL, i18n | Arabic, Egypt, MENA, RTL, bilingual, translate app/course/site | course, feature, presentation, reference, live-edit, uiux-variants (auto-attach) | frontend-design-system, writing-dna, ux-ui-designer | — | M | L | ✓ |
| `guard-pass` | post-work quality gates, AI failure modes | after implementation/tests, before verify/release, AI-generated diff review | implement, feature, fix, test, review, verify, release (auto-attach) | anti-hallucination, testing-gate, skill-auditor | — | M | L | ✓ |
| `orchestrator` | global brain, conflict resolution, missing-capability | command/skill conflict, unclear next step, duplicated workflow, no capability fits | bequite, suggest, discover, plan, auto, implement, review, verify, skill-audit (auto-attach) | workflow-advisor, context-engineer | — | L | L | ✓ |

## Per-skill detail pointers

For every skill: **when to use / when NOT to use / required inputs / expected outputs / memory reads / memory writes** are canonical in `.claude/skills/bequite-<name>/SKILL.md` (§When-to-use, §When-NOT, §Quality-gate sections — present in all 27 per the alpha.15 repair, verified alpha.19 seed audit). The router loads the routing table above for selection; it opens SKILL.md only for SELECTED skills.

Memory-write hotspots worth knowing at routing time (so writeback step plans correctly):
- frontend-design-system → `design/DESIGN_DNA`, `DESIGN_CONTINUITY_REPORT`, `uiux/SECTION_MAP`, `state/FRONTEND_CONTEXT_SUMMARY`, `audits/VISUAL_QA_REPORT`
- writing-dna → `writing/*` (5 files) · presentation-builder → `presentations/*` (9 files)
- guard-pass → `audits/GUARD_PASS_REPORT.md` · localization-rtl → writes into the active workflow's artifacts (no own dir)
- delegate-planner → `tasks/DELEGATE_*` + `audits/DELEGATE_REVIEW_REPORT`
- researcher → `research/<DOMAIN>_RESEARCH_REPORT` · anti-hallucination → `research/EVIDENCE_LOG`
- job-finder / make-money → `jobs/*` / `money/*` · skill-auditor → `audits/SKILL_QUALITY_AUDIT` + **this registry**
- context-engineer → `state/{PROJECT_DNA,WORKING_NOTES,CONTEXT_SUMMARY}`

## Review metadata

| Field | Value |
|---|---|
| Skills indexed | 27 |
| Last full review | 2026-06-11 (alpha.19 seed audit + alpha.21 registry refresh) |
| Quality summary | 28 ✓ PASS (3 new alpha.22 skills baselined PASS 2026-06-12 — SKILL_AUDIT_ALPHA_22_BASELINE.md; live-invocation validation pending) · 2 ~ (problem-solver thin example, multi-model-planning stale phasing — backlogged) |
| Next refresh due | next `/bq-skill-audit` run, or when a skill is added/removed |

**Maintainer rule:** adding or removing a skill without updating this registry in the same commit is a drift violation (caught by `/bq-skill-audit`).
