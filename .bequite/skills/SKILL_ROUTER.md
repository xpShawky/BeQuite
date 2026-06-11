# Skill Router (alpha.20)

> The domain map + selection algorithm. Read AFTER `SKILL_REGISTRY.md`. Strategy: `docs/architecture/AUTO_SKILL_ROUTING_STRATEGY.md`.

## Domain → skill map

| Domain | Primary skill(s) | Usual companions |
|---|---|---|
| frontend / UI/UX / visual identity / branding | **frontend-design-system** (coordinates ux-ui-designer + frontend-quality + live-edit) | testing-gate · context-engineer (multi-section) |
| presentation | **presentation-builder** | ux-ui-designer · writing-dna (speaker notes) · researcher (sources) · frontend-design-system (HTML decks) |
| writing / content / brand voice | **writing-dna** | anti-hallucination (strict) · researcher (factual claims) |
| academic writing | **writing-dna (strict)** + **researcher** | anti-hallucination · EVIDENCE_LOG mandatory |
| security / auth review | **security-reviewer** | anti-hallucination · testing-gate · FILE_RISK rules · devops-cloud (if infra) |
| prompt injection / agent safety | **security-reviewer** (LLM Top-10 + red-team angle 10) | anti-hallucination · context-engineer (memory-poisoning review) |
| backend / API | **backend-architect** | database-architect · security-reviewer · testing-gate |
| database | **database-architect** | backend-architect · devops-cloud (migrations = R3 gate) |
| devops / deploy / release-ship | **devops-cloud** + **release-gate** | testing-gate · security-reviewer |
| automation / scraping / crawling / browser automation | **scraping-automation** | backend-architect · security-reviewer (politeness + legality) |
| data analysis | **researcher** + **database-architect** (data modeling) | product-strategist (data-to-insight) |
| research | **researcher** | anti-hallucination · domain specialist for the topic |
| business / make-money | **make-money** | product-strategist · researcher |
| job finding | **job-finder** | writing-dna (pitches) |
| testing | **testing-gate** | problem-solver (failing tests) |
| documentation | context-engineer + writing-dna (long-form) | — |
| product strategy | **product-strategist** | project-architect · researcher |
| debugging / fix | **problem-solver** + per-bug-type specialist | testing-gate |
| new feature | per 12-type router in `/bq-feature` | testing-gate · context-engineer |
| existing project audit | researcher + security-reviewer + frontend-quality (if UI) | anti-hallucination |
| new project build | **project-architect** + product-strategist | per-discovery specialists |
| delegation / cost control | **delegate-planner** | researcher (phase 1) |
| BeQuite self-maintenance | **updater** / **skill-auditor** | anti-hallucination |

## Selection algorithm

```
1. classify(request, command, files, mode, phase, memory, risk, output_type) → domains[]
2. for each domain: add primary skill(s) from map
3. apply cross-cutting auto-attach (anti-hallucination on claims · testing-gate on code
   · context-engineer on >1 session or >5 files · security-reviewer on R3 paths
   · frontend-design-system on >1 UI section)
4. apply mode sizing (fast=smallest safe · deep=broader · token-saver=lazy-load
   · delegate=names skills in task pack)
5. arbitrate (master beats member · specialist beats generalist · 2-skill cap on trivial)
6. emit Skill Selection section (selected + reasons; notable not-selected + reasons)
7. load only selected SKILL.md files
8. at writeback: append SKILL_USAGE_LOG entry
```

## Worked routings (canonical examples)

**"Build a cinematic animated landing page"** → frontend-design-system (coordinator: ux-ui-designer + frontend-quality + live-edit) · testing-gate · context-engineer (multi-section) · [brand assets present? → brand extraction via design-system DNA flow]. Not selected: security-reviewer (no R3 paths).

**"Build a restaurant ordering app"** → product-strategist · project-architect · frontend-design-system · backend-architect · database-architect · testing-gate · [release-gate when shipping].

**"Rewrite this to sound like a real human and match this style"** → writing-dna · [brand exists? + brand voice via DNA profile] · [source material? → strict mode + anti-hallucination] · [factual claims? → researcher]. *Goal = human-quality + fidelity, never detector evasion.*

**"Write a literature review from these papers"** → writing-dna (strict) · researcher · anti-hallucination (citation fidelity → EVIDENCE_LOG) · academic-integrity constraints from writing-dna ethics.

**"Create a beginner YouTube lecture presentation about BeQuite"** → presentation-builder · ux-ui-designer · writing-dna (script/notes register) · [HTML deck? → frontend-design-system] · researcher (source handling) · brand identity via DESIGN_DNA.

**"Review my auth flow for vulnerabilities"** → security-reviewer · anti-hallucination (evidence per finding) · testing-gate · FILE_RISK R3 awareness · devops-cloud if deploy configs touched. Output: severity-tagged findings, each `file:line`-cited.

**"Test this agent workflow against prompt injection"** → security-reviewer (angle 10: injection vectors, tool-permission review, memory poisoning) · anti-hallucination · context-engineer (memory-poisoning surface).

## Output block template (every non-trivial command)

```
Skill Selection:
- Selected: bequite-<skill> — <one-line reason tied to the task>
- Selected: bequite-<skill> — <reason>
- Not selected: bequite-<skill> — <reason it was considered and skipped>
```

## Notes

- "Professional Expert", "Security Lab", "Prompt Injection Lab" intents route to **security-reviewer + anti-hallucination (+ deep mode)** — those labels are compositions, not separate skills (see GAME_CHANGER tracker).
- Explicit user skill choice overrides routing; log the override.
