# Command Clutter Review (alpha.14)

**Run date:** 2026-05-17
**Total commands:** 45 (1 menu + 44 `bq-*`)
**Goal:** Should any command be merged, demoted to skill-only, demoted to roadmap, or rejected? Keep BeQuite lightweight.

---

## 1. Scoring methodology

For each command, score on:
- **Utility:** how often a real user needs it
- **Distinctness:** does it do something a sibling command doesn't?
- **Discipline:** is it a workflow gate, or a productivity tool?
- **Maintenance cost:** how much spec drift does it create per alpha?

Categories:
- 🟢 **Keep** — clear utility + distinct + low maintenance
- 🟡 **Document better** — utility OK; description / docs need work
- 🟠 **Merge / promote to skill** — useful capability but doesn't deserve its own slash command
- 🔴 **Reject / demote to roadmap** — not yet earning its place

---

## 2. Per-command verdict

### Root + orientation (4) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bequite` | 🟢 keep | Gate-aware menu. Core navigation. |
| `/bq-help` | 🟢 keep | Full command reference. Distinct from `/bequite`. |
| `/bq-now` | 🟢 keep | One-line status. Faster than `/bequite`. |
| `/bq-explain` | 🟢 keep | Plain-English explainer. Useful for onboarding / handoff. |

### P0 Setup (6) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-init` | 🟢 keep | Sets up `.bequite/` scaffold. Essential. |
| `/bq-mode` | 🟢 keep | Mode selector. Drives the whole workflow shape. |
| `/bq-new` | 🟢 keep | New Project entry. Sets mode + queues questions. |
| `/bq-existing` | 🟢 keep | Existing Audit entry. Sets mode + queues questions. |
| `/bq-discover` | 🟢 keep | Inspects repo; writes DISCOVERY_REPORT.md. |
| `/bq-doctor` | 🟢 keep | Environment health. Distinct from discover. |

### P1 Framing (6) — all 🟢 keep (one note)

| Command | Verdict | Notes |
|---|---|---|
| `/bq-clarify` | 🟢 keep | 3-5 high-value questions. Essential discipline. |
| `/bq-research` | 🟢 keep | 11-dimension research. Core capability. |
| `/bq-scope` | 🟢 keep | IN/OUT/NON-GOALS lock. Disciplinary. |
| `/bq-spec` | 🟢 keep | One-page Spec Kit-compatible spec. Useful interop. |
| `/bq-plan` | 🟢 keep | Full implementation plan. Core. |
| `/bq-multi-plan` | 🟡 document better | Manual-paste workflow; users may not know when to invoke. |

### P2 Build (5) — 4 🟢, 1 🟠

| Command | Verdict | Notes |
|---|---|---|
| `/bq-assign` | 🟢 keep | Atomic task list. Essential. |
| `/bq-implement` | 🟢 keep | Per-task implementation. Workhorse. |
| `/bq-feature` | 🟢 keep | 12-type router for adding features. |
| `/bq-fix` | 🟢 keep | 15-type router for fixes. Reproduce-first. |
| `/bq-add-feature` | 🟠 **deprecate as alias for `/bq-feature`** | Legacy; superseded in alpha.2. Mark deprecated in alpha.14; redirect users. |

### P3 Quality (4) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-test` | 🟢 keep (with repair) | Test runner + missing-test writer. **Repair:** add gate-refusal logic. |
| `/bq-audit` | 🟢 keep | 10-area audit. Distinct from review. |
| `/bq-review` | 🟢 keep | Per-file diff review. |
| `/bq-red-team` | 🟢 keep | Adversarial review. 8 angles. |

### P4 Release (3) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-verify` | 🟢 keep | Full local verification matrix. Core. |
| `/bq-release` | 🟢 keep | Release prep. Prints commands; user pushes. |
| `/bq-changelog` | 🟢 keep | Keep-a-Changelog discipline. |

### P5 Memory (3) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-memory` | 🟢 keep | Snapshot read/write. |
| `/bq-recover` | 🟢 keep | Resume after break. Critical. |
| `/bq-handoff` | 🟢 keep | HANDOFF.md generator. |

### Phase orchestrators (7) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-p0` … `/bq-p5` | 🟢 keep | Phase walkers. Each maps to a phase. Useful for users who want one-shot phase execution without going to full auto. |
| `/bq-auto` | 🟢 keep | Full autonomous runner. Most powerful command in the system. |

### UI / UX (2) — both 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-uiux-variants` | 🟢 keep | Generate 1-10 isolated UI directions. |
| `/bq-live-edit` | 🟢 keep | Section-mapped frontend edits. |

### Opportunity (alpha.8) (3) — all 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-suggest` | 🟢 keep | Workflow advisor. Read-only. |
| `/bq-job-finder` | 🟢 keep | Real work opportunities. Distinct from money. |
| `/bq-make-money` | 🟢 keep | Earning opportunities. Distinct from jobs. |

### Maintenance (alpha.10) (1) — 🟢 keep

| Command | Verdict | Notes |
|---|---|---|
| `/bq-update` | 🟢 keep | BeQuite self-update. Essential as the system evolves. |

### Creative + Content (alpha.13) (1) — 🟢 keep (with repair)

| Command | Verdict | Notes |
|---|---|---|
| `/bq-presentation` | 🟢 keep | Premium PPTX/HTML builder. **Repair:** wire to MISTAKE_MEMORY; add Quality gate + When NOT to use to skill. |

---

## 3. Summary

| Verdict | Count | Commands |
|---|---|---|
| 🟢 Keep | **42** | All but those below |
| 🟡 Document better | 1 | `/bq-multi-plan` (clarify when to invoke) |
| 🟠 Merge / promote / deprecate | 1 | `/bq-add-feature` → deprecate as alias |
| 🔴 Reject | 0 | none |

**Net:** 45 commands → 44 active commands after alpha.14 (counting `/bq-add-feature` as deprecated alias, not active).

---

## 4. Skills that should NOT become commands

The system has 21 skills. **None should be promoted to a top-level slash command.** Skills are invoked by commands; they don't need their own user-facing command. The current ratio (44 commands / 21 skills) is healthy.

Anti-pattern to avoid: `/bq-frontend-quality` or `/bq-security-reviewer` as top-level slash commands. These capabilities are correctly delivered through `/bq-audit`, `/bq-review`, `/bq-fix`, `/bq-feature` etc., which activate the relevant skill.

---

## 5. Features that should stay as roadmap

From `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`:

| Feature | Status | Stay as roadmap? |
|---|---|---|
| Bot Maker | roadmap only | ✅ Yes — too broad; needs scope work; will be `/bq-build-bot` or merged into `/bq-feature` automation type |
| Website change monitor | roadmap only | ✅ Yes — niche; consider as a skill activated by `/bq-feature automation` |
| Scraping product factory | partial (skill exists) | ✅ Skill exists; no command yet (correct — invoked via `/bq-auto scraping`) |
| Lead finder | roadmap only | ✅ Yes |
| Report generator | roadmap only | ✅ Yes |
| QA bot | roadmap only | ✅ Yes |
| Decision support | roadmap only | ✅ Yes |
| Lecture builder | roadmap only | ⚠ Now partially covered by `/bq-presentation` (alpha.13) — re-scope roadmap |
| Academic writing | roadmap only | ⚠ Partially covered by `/bq-research` + `/bq-presentation` — re-scope |
| Marketing campaign builder | roadmap only | ✅ Yes |
| Course builder | roadmap only | ⚠ Partially covered by `/bq-presentation` |
| Support bot | roadmap only | ✅ Yes |
| Sales agent | roadmap only | ✅ Yes |
| Medical / pharmacy assistant | roadmap only | ✅ Yes (requires regulated doctrine) |
| Style cloner / persona simulator | roadmap only | ✅ Yes — handled by `/bq-multi-plan` partially |
| Auto documentation builder | roadmap only | ⚠ Partially covered by `/bq-handoff` + `/bq-explain` |

**Repair:** alpha.14 — update `FEATURE_EXPANSION_ROADMAP.md` to mark items now partially covered by alpha.13 + reorganize remaining roadmap entries.

---

## 6. Recommendation

**BeQuite at alpha.13 is at a clean equilibrium.** 44 active commands + 21 skills + 4 operating modes + 6 workflow modes + 6 phases is comprehensive without bloat.

Going forward, the system should:

1. **Hold the line on command count.** New features should:
   - First try as skill activations from existing commands
   - Then try as keyword-routed sub-types of existing commands (like `/bq-fix`'s 15-type router)
   - Only finally as a new slash command, and only if it's a major workflow

2. **Use `/bq-suggest` as the discovery layer** — users don't need to memorize 44 commands; they describe their situation and `/bq-suggest` routes them.

3. **Track command additions in MODE_HISTORY** — if a command isn't used for 6+ months, candidate for removal in a major version.

4. **Discipline restoration in alpha.14** — establish the global feature-addition rule. Don't add features that haven't gone through discover→research→scope→plan→tasks.

---

## 7. Acceptance for alpha.14

- [ ] `/bq-add-feature.md` marked as deprecated alias (clear note at top redirecting to `/bq-feature`)
- [ ] `/bq-multi-plan.md` "When to use" section sharpened
- [ ] No new commands added in alpha.14
- [ ] `FEATURE_EXPANSION_ROADMAP.md` updated to reflect alpha.13 partial coverage of lecture/academic/course builders
