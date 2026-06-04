---
description: Add Feature workflow with type router. Classifies the feature (frontend / backend / database / auth / etc.) and activates the right specialist skills. Replaces bq-add-feature.
---

# /bq-feature — Add Feature workflow

## Purpose

Add a new feature to an existing project, safely. **Identifies the feature type** (12 categories) and activates the matching specialist skills.

## When to use it

- Existing project (`.git/` + manifests present)
- You want to add ONE feature
- Mode = Add Feature (or you're using this as the mode-entry shortcut)

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/audits/DISCOVERY_REPORT.md` (if exists; else suggest `/bq-discover` first)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists)

## Files to write

- `.bequite/state/CURRENT_MODE.md` → "Add Feature" if not already
- `.bequite/plans/feature-<slug>.md` — feature mini-spec
- `.bequite/tasks/CURRENT_TASK.md` (the feature becomes the active task)
- `.bequite/state/OPEN_QUESTIONS.md` (any unresolved)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. Get the feature title

If user typed `/bq-feature` alone:
> "Describe the feature in one sentence."

If `/bq-feature "csv export on bookings page"` — use the argument.

### 2. Classify the feature type

Ask the model (silently) to classify into one of:

| # | Type | Activates skill(s) |
|---|---|---|
| 1 | **Frontend UI** | `bequite-frontend-quality`, `bequite-ux-ui-designer` |
| 2 | **Backend API** | `bequite-backend-architect`, `bequite-security-reviewer` |
| 3 | **Database** | `bequite-database-architect`, `bequite-backend-architect` |
| 4 | **Auth** | `bequite-security-reviewer`, `bequite-backend-architect` |
| 5 | **Automation** | `bequite-scraping-automation`, `bequite-backend-architect` |
| 6 | **Scraping / Crawling** | `bequite-scraping-automation` |
| 7 | **Cloud / Deployment** | `bequite-devops-cloud` |
| 8 | **Admin panel** | `bequite-frontend-quality`, `bequite-security-reviewer` |
| 9 | **Dashboard** | `bequite-frontend-quality`, `bequite-ux-ui-designer` |
| 10 | **CLI** | `bequite-backend-architect`, `bequite-testing-gate` |
| 11 | **Integration** | `bequite-backend-architect`, `bequite-security-reviewer` |
| 12 | **Security** | `bequite-security-reviewer` |

Print the classification + which skills will be active. Ask: "Correct? (y/N + correction)"

### 3. Write the mini-spec

Save to `.bequite/plans/feature-<slug>.md` (slug from title):

```markdown
# Feature: <title>

**Generated:** <date>
**Type:** <classification>
**Active skills:** <list>

## What
(2-3 sentences)

## Why
(1 sentence)

## In scope
- ...

## Out of scope
- ...

## Files this will touch
| File | Action |
|---|---|

## Acceptance criteria
(specific + testable + no weasel words)

## Test plan
- Unit: ...
- Integration: ...
- E2E: ... (if UI)

## Security considerations (from bequite-security-reviewer)
- ...

## DevOps considerations (from bequite-devops-cloud, if deployment-touching)
- ...

## Implementation order
1. ...
2. ...
3. ...
```

### 4. Present + confirm

Show user the mini-spec. Wait for "yes" or corrections.

### 5. Implement

Once confirmed, implement per the order in §3.
- Read files first
- Make minimal changes per file
- Run tests after each material change
- Update `.bequite/tasks/CURRENT_TASK.md` with progress

### 6. Test + verify

Run the test plan from the spec. Run a quick `/bq-test` subset.

### 7. Log + changelog

- `.bequite/logs/CHANGELOG.md` `[Unreleased]` `### Added` entry
- `.bequite/logs/AGENT_LOG.md` entry

## Output format

```
✓ Feature added — <title>

Type:         <classification>
Active skills:<list>
Spec:         .bequite/plans/feature-<slug>.md
Files:        <count> touched
Tests:        <pass / total>
Acceptance:   <one-line confirmation>

Next: /bq-review (review the change) or /bq-verify (full gates)
```

## Quality gate

- Mini-spec exists at `.bequite/plans/feature-<slug>.md`
- User confirmed the spec
- All implementation files compiled / typechecked
- New test exists + passes
- Acceptance criterion verified by running it
- CHANGELOG `[Unreleased]` updated
- New code matches `.bequite/state/PROJECT_DNA.md` conventions + dependency direction (alpha.18 — no off-convention spaghetti; follow the exemplar files it names)
- Any new package verified in-session — registry + age + downloads + publisher + lockfile — before import (alpha.18; `bequite-anti-hallucination`)
- For multi-file features: a File-Responsibility Map exists before tasks (`bequite-context-engineer`); failing-test-first for logic; completion report pastes command output (no weasel words)

## Failure behavior

- Type-classification wrong → user corrects → re-route
- Mini-spec rejected → revise → re-present
- Implementation hits a blocker → mark `[!]` blocked → log → exit
- Test fails after implementation → roll back via git stash → log error → exit

## Usual next command

- `/bq-review` — formal review of the change
- `/bq-test` — broader test pass
- `/bq-verify` — full gate matrix before shipping
- `/bq-changelog` — sharpen the CHANGELOG entry

---

## Design Continuity Gate (alpha.17 — UI-typed features)

For features classified Frontend UI / Admin panel / Dashboard (types 1 / 8 / 9), this command activates `bequite-frontend-design-system` and runs the **Design Continuity Gate** so the feature holds the same quality across **every** section — not just the first one built.

**Before implementing UI:**
- Read `.bequite/design/DESIGN_DNA.md` (gate `DESIGN_DNA_LOCKED`). If missing/placeholder, fill + lock it first — every section is judged against it.
- Pick the product type → apply `.claude/skills/bequite-frontend-design-system/references/product-type-rules.md` (do NOT default to "cinematic SaaS landing").
- Add each section to `.bequite/uiux/SECTION_MAP.md` with acceptance criteria.

**While implementing:** build section-by-section — build a section → check it against the DNA → continue. Don't build the whole surface then hope. Re-read `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` between sections.

**Before "done":**
- Run the Design Continuity Gate → `.bequite/design/DESIGN_CONTINUITY_REPORT.md` (no BLOCKER/HIGH drift; close the quality cliff between weakest and strongest section).
- Run Visual QA → `.bequite/audits/VISUAL_QA_REPORT.md` (render it; never claim a visual PASS you didn't see).
- Set `DESIGN_CONTINUITY_PASS` + `VISUAL_QA_DONE`. Log any `[fe][design]` lesson to `MISTAKE_MEMORY.md`.

**Effort awareness:** low/medium → compact heuristic check; high → full per-section; xhigh/Ultracode → per-section critique + browser visual QA + final polish.

Spec: `docs/architecture/DESIGN_CONTINUITY_GATE.md`. Map: `.bequite/design/FRONTEND_SKILL_MAP.md`.

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, or design system this command might add as part of a feature is a CANDIDATE, not a default.**

If the feature mini-spec requires a new tool / library / dep, the spec must include a decision section before `/bq-implement` runs.

**Do not write in the mini-spec:** "Add Drizzle."
**Write:** "Drizzle is one candidate. Compared against [alternatives]; chosen because [reasons]; risk [X]; rollback [Y]."

The 10 decision questions every new dep must answer:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

For each new dep, embed a short decision section in the feature mini-spec (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan). For features touching auth, payments, or DB schema, use a full ADR.

**Do not auto-install new deps.** Adding a dependency requires explicit justification per the 6-point implementation rule: needed, justified, compatible, not over-complex, has test plan, has rollback path.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
