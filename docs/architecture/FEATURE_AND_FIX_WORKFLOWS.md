# Feature & Fix workflows

**Status:** active
**Adopted:** 2026-05-11 (alpha.2 introduced 12-type feature router + 15-type fix router)
**Reference:** `.claude/commands/bq-feature.md`, `.claude/commands/bq-fix.md`

---

## Why dedicated workflows

Most BeQuite work falls into two patterns:

1. **Add a feature** — new capability for an existing project
2. **Fix a bug** — broken behavior somewhere in the project

Both deserve a structured workflow that classifies the work, activates the right specialist skills, and applies discipline (mini-spec → impl → test → log).

---

## /bq-feature — 12-type router

When you run `/bq-feature "title"`, the agent classifies the feature into one of 12 types and activates the matching skills:

| # | Type | Skills activated |
|---|---|---|
| 1 | Frontend UI | `bequite-frontend-quality`, `bequite-ux-ui-designer` |
| 2 | Backend API | `bequite-backend-architect`, `bequite-security-reviewer` |
| 3 | Database | `bequite-database-architect`, `bequite-backend-architect` |
| 4 | Auth | `bequite-security-reviewer`, `bequite-backend-architect` |
| 5 | Automation | `bequite-scraping-automation`, `bequite-backend-architect` |
| 6 | Scraping / Crawling | `bequite-scraping-automation` |
| 7 | Cloud / Deployment | `bequite-devops-cloud` |
| 8 | Admin panel | `bequite-frontend-quality`, `bequite-security-reviewer` |
| 9 | Dashboard | `bequite-frontend-quality`, `bequite-ux-ui-designer` |
| 10 | CLI | `bequite-backend-architect`, `bequite-testing-gate` |
| 11 | Integration | `bequite-backend-architect`, `bequite-security-reviewer` |
| 12 | Security | `bequite-security-reviewer` |

### Workflow

1. Get title (from argument or one question)
2. Classify (show classification + skills + ask "correct?")
3. Write mini-spec → `.bequite/plans/feature-<slug>.md` (What / Why / In scope / Out / Files / Acceptance / Test plan / Security / DevOps / Impl order)
4. Present + confirm
5. Implement per the order
6. Test + verify
7. Log + changelog entry

Quality gate: spec exists, user confirmed, files compile/typecheck, new test exists + passes, acceptance verified, CHANGELOG updated.

---

## /bq-fix — 15-type router

When you run `/bq-fix "what's broken"`, the agent classifies the problem into one of 15 types and activates the matching skills:

| # | Type | Skills activated |
|---|---|---|
| 1 | Frontend bug (visual/state) | `bequite-frontend-quality`, `bequite-problem-solver` |
| 2 | Backend bug (API/logic) | `bequite-backend-architect`, `bequite-problem-solver` |
| 3 | Database bug (query/data) | `bequite-database-architect`, `bequite-problem-solver` |
| 4 | Auth bug | `bequite-security-reviewer`, `bequite-backend-architect` |
| 5 | Build/compile | `bequite-problem-solver`, `bequite-testing-gate` |
| 6 | Test failure | `bequite-testing-gate`, `bequite-problem-solver` |
| 7 | Deployment/CI | `bequite-devops-cloud`, `bequite-problem-solver` |
| 8 | Performance regression | `bequite-problem-solver`, `bequite-backend-architect` |
| 9 | Security vulnerability | `bequite-security-reviewer` |
| 10 | Dependency/package | `bequite-problem-solver`, `bequite-project-architect` |
| 11 | Configuration/env | `bequite-devops-cloud`, `bequite-problem-solver` |
| 12 | Network/integration | `bequite-backend-architect`, `bequite-problem-solver` |
| 13 | Memory leak / resource | `bequite-problem-solver`, `bequite-backend-architect` |
| 14 | Race / async | `bequite-problem-solver`, `bequite-backend-architect` |
| 15 | Cross-browser / platform | `bequite-frontend-quality`, `bequite-problem-solver` |

### Workflow (reproduce-first)

1. Get the bug (from argument or question)
2. Classify (show classification + skills + ask "correct?")
3. **Reproduce** — no fix without reproduction
4. Capture exact error → `.bequite/logs/ERROR_LOG.md`
5. Write fix mini-spec → `.bequite/audits/FIX_<slug>.md`
6. Find root cause (5-whys; smallest change that removes the symptom)
7. Apply smallest patch
8. Add or update regression test (fails before, passes after)
9. Verify (reproduction now passes; new test passes; full suite green)
10. Log fix + update CHANGELOG if user-visible
11. Update `MISTAKE_MEMORY.md` if pattern is recurring

Quality gate: reproduction confirmed before any code change; smallest patch; regression test added; full suite green; no banned weasel words.

---

## Integration with auto-mode

`/bq-auto feature "..."` → dispatches to `/bq-feature`
`/bq-auto fix "..."` → dispatches to `/bq-fix`

Both continue by default; pause only at hard human gates.

## Anti-patterns

- ❌ Fix without reproduction ("I think I know what's wrong")
- ❌ Refactor during fix ("while I'm in here…")
- ❌ Multi-bug fix in one `/bq-fix` call (one bug per invocation)
- ❌ Feature without acceptance criteria
- ❌ Feature spec with weasel words ("should work", "probably handles edge cases")

## See also

- `.claude/commands/bq-feature.md` — full feature spec
- `.claude/commands/bq-fix.md` — full fix spec
- `.claude/skills/bequite-problem-solver/SKILL.md` — reproduce-first discipline
- WORKFLOW_GATES.md — which gates feature/fix update
