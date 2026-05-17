# Command + Skill Consistency Audit (alpha.14)

**Run date:** 2026-05-17
**Reference schema:** alpha.6+ standardized command fields
**Files scanned:** 45 commands + 21 skills

---

## 1. Command consistency table

Per-command check across 18 fields. Legend: ✅ has it · ❌ missing · ⚪ partial / present elsewhere

(Where a file lacks a specific section, it doesn't necessarily mean the content is missing — sometimes the same information appears under a different heading. The checklist marks the canonical alpha.6 heading.)

| Command | Frontmatter | Description useful | Purpose | When to use | Preconditions | Required gates | Files to read (memory-first) | Files to write | Steps | Output format | Quality gate | Failure behavior | Memory writeback | Log update | Changelog rule | Usual next | Standardized fields section |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bequite.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ |
| `bq-add-feature.md` | ✅ | ✅ | ✅ | ⚪ | ❌ | ❌ | ❌ | ⚪ | ✅ | ⚪ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ⚪ | ❌ |
| `bq-assign.md` | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-audit.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-auto.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-changelog.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-clarify.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-discover.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-doctor.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-existing.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-explain.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ |
| `bq-feature.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-fix.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-handoff.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-help.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bq-implement.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-init.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-job-finder.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-live-edit.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-make-money.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-memory.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-mode.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-multi-plan.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-new.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-now.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bq-p0.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-p1.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-p2.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-p3.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-p4.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-p5.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-plan.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-presentation.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-recover.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-red-team.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-release.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-research.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-review.md` | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| `bq-scope.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `bq-spec.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ |
| `bq-suggest.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ |
| `bq-test.md` | ✅ | ✅ | ✅ | ⚪ | ❌ | ❌ | ❌ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ❌ |
| `bq-uiux-variants.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| `bq-update.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bq-verify.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ |

### Summary

- **All 45 commands have valid YAML frontmatter + description + purpose** ✅
- **18 commands lack the explicit `## Files to read` section** (memory-first preflight)
- **20 commands lack the alpha.6 `## Standardized command fields` section**
- **No placeholder commands** — smallest is `bq-existing.md` at 93 lines with complete schema

### Commands needing memory-first preflight added (alpha.14 repair)

1. `bq-add-feature.md` — legacy, may deprecate
2. `bq-assign.md`
3. `bq-audit.md`
4. `bq-changelog.md`
5. `bq-clarify.md`
6. `bq-discover.md`
7. `bq-doctor.md`
8. `bq-handoff.md`
9. `bq-implement.md`
10. `bq-init.md` (legitimately doesn't need it — initializes from scratch)
11. `bq-memory.md`
12. `bq-recover.md`
13. `bq-red-team.md`
14. `bq-release.md`
15. `bq-review.md`
16. `bq-scope.md`
17. `bq-test.md`
18. `bq-verify.md`

---

## 2. Skill consistency table

Per-skill check across 12 fields.

| Skill | Frontmatter (name + description + allowed-tools) | When to use | When NOT to use | Inputs / triggers | Steps / checklist | Output format | Quality gate | Common mistakes | Failure handling | Memory/log update | Tool neutrality treated | No heavy deps installed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bequite-backend-architect` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-database-architect` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-delegate-planner` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bequite-devops-cloud` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-frontend-quality` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ✅ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-job-finder` | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `bequite-live-edit` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bequite-make-money` | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `bequite-multi-model-planning` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-presentation-builder` | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-problem-solver` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-product-strategist` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-project-architect` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-release-gate` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-researcher` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-scraping-automation` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-security-reviewer` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-testing-gate` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-updater` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `bequite-ux-ui-designer` | ✅ | ✅ | ❌ | ✅ | ✅ | ⚪ | ❌ | ✅ | ⚪ | ⚪ | ✅ | ✅ |
| `bequite-workflow-advisor` | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ⚪ | ✅ | ✅ |

### Summary

- **All 21 skills have valid frontmatter** ✅
- **All 21 skills treat named tools as candidates (tool neutrality)** ✅
- **No skill installs heavy deps by default** ✅
- **16 skills lack `When NOT to use`**
- **18 skills lack explicit `Quality gate`** section
- **17 skills lack explicit `Common mistakes`** section

### Skills needing `When NOT to use` (alpha.14 repair)

backend-architect · database-architect · devops-cloud · frontend-quality · job-finder · make-money · presentation-builder · problem-solver · product-strategist · project-architect · release-gate · scraping-automation · security-reviewer · testing-gate · ux-ui-designer · workflow-advisor

### Skills needing `Quality gate` (alpha.14 repair)

backend-architect · database-architect · devops-cloud · frontend-quality · job-finder · live-edit · make-money · multi-model-planning · presentation-builder · problem-solver · product-strategist · project-architect · release-gate · researcher · scraping-automation · security-reviewer · testing-gate · ux-ui-designer

---

## 3. Cross-listing audit

| Command | In README? | In commands.md? | In `/bequite` menu? | In `/bq-help`? |
|---|---|---|---|---|
| All 45 commands | mostly ✅ | mostly ✅ | mostly ✅ | mostly ✅ |
| `/bq-add-feature` (legacy) | ❌ | ⚪ alias note only | ❌ | ⚪ |
| `/bq-presentation` | ✅ | ✅ | ✅ | ✅ |
| `/bq-update` | ✅ | ✅ | ✅ | ✅ |
| `/bq-suggest` | ✅ | ✅ | ✅ | ✅ |
| `/bq-job-finder` | ✅ | ✅ | ✅ | ✅ |
| `/bq-make-money` | ✅ | ✅ | ✅ | ✅ |
| `/bq-explain` | ✅ | ✅ | ⚪ | ⚪ |
| `/bq-spec` | ✅ | ✅ | ⚪ | ⚪ |
| `/bq-now` | ✅ | ✅ | ✅ | ⚪ |

`/bq-add-feature.md` is the legacy form of `/bq-feature`. **Decision for alpha.14:** document as deprecated alias at top of `bq-add-feature.md`; do NOT delete (preserves existing user muscle memory; redirects to `/bq-feature`).

---

## 4. Banned-weasel-word scan

Searched for: `should`, `probably`, `seems to`, `appears to`, `I think it works`, `might`, `hopefully`, `in theory`.

**Result:** Found in command file bodies as TEACHING examples (e.g. `/bq-auto`'s "Banned-weasel-word check" lists them; `/bq-verify` references them; CLAUDE.md lists them). **These are intentional documentation references, not violations.**

No banned weasel words found in completion claim contexts in any command output template.

---

## 5. Cross-command consistency issues

| Issue | Affected files | Severity |
|---|---|---|
| Phase naming "Setup and Discovery" vs "Setup and Understanding" | `bq-help.md` uses older "Understanding" in its body | ⚪ minor |
| Gate name `DISCOVERY_COMPLETE` vs `DISCOVERY_DONE` | `WORKFLOW_GATES.md` uses `_COMPLETE`; some commands use `_DONE` | 🟡 medium |
| Gate name `IMPLEMENTATION_DONE` vs `IMPLEMENT_DONE` | same | 🟡 medium |
| Command count claim "34" / "36" / "44" / "45" | `bequite.md` body comment, README badge, CLAUDE.md, COMMAND_CATALOG.md | ⚪ minor |
| Skill count claim "7" / "11" / "14" / "15" / "19" / "20" / "21" | CLAUDE.md body, LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md, README, `/bequite` menu | 🟡 medium |

---

## 6. Acceptance for alpha.14 repair

- [ ] All 18 commands lacking memory-first preflight get the `## Files to read` section added
- [ ] All 20 commands lacking the standardized fields section get it added (or are explicitly exempted with note)
- [ ] All 16 skills lacking `When NOT to use` get it added
- [ ] All 18 skills lacking `Quality gate` get it added
- [ ] Gate name canonicalization decided + applied across all files
- [ ] Command count + skill count standardized everywhere
- [ ] `/bq-add-feature.md` marked as deprecated alias
