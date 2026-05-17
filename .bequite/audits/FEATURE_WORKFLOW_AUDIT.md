# Feature Workflow Audit (alpha.14)

**Run date:** 2026-05-17
**Audit goal:** For every feature shipped alpha.1 → alpha.13, verify it went through the proper BeQuite workflow.

---

## 1. The reference workflow

A new BeQuite feature should travel through these 15 steps:

1. Add feature request to memory (`OPEN_QUESTIONS.md` or `FEATURE_EXPANSION_ROADMAP.md`)
2. Run discovery (`/bq-discover` if context unclear)
3. Run research (`/bq-research` — 11 dimensions; minimum 3 for fast mode)
4. Define scope (`/bq-scope` → `SCOPE.md`)
5. Create plan (`/bq-plan` → `IMPLEMENTATION_PLAN.md`)
6. Break into tasks (`/bq-assign` → `TASK_LIST.md`)
7. Implement command / skill / docs / memory (`/bq-implement` or `/bq-feature`)
8. Update README
9. Update commands.md
10. Update `/bequite` root menu
11. Update `/bq-help`
12. Update command catalog (`docs/specs/COMMAND_CATALOG.md`)
13. Update agent log (`.bequite/logs/AGENT_LOG.md`)
14. Update changelog (`docs/changelogs/CHANGELOG.md`)
15. Verify command + skill consistency (`/bq-verify`)

---

## 2. Per-feature workflow trace

### F1. Lightweight pack core direction (v3.0.0-alpha.1)

| Step | Status | Evidence |
|---|---|---|
| 1. Request to memory | ✅ | `BEQUITE_BOOTSTRAP_BRIEF.md` is the request artifact |
| 2. Discovery | ✅ | `DIRECTION_RESET_AUDIT.md` |
| 3. Research | ✅ | Multiple research reports in `.bequite/memory/` |
| 4. Scope | ✅ | ADR-001 documents scope |
| 5. Plan | ✅ | `MVP_LIGHTWEIGHT_SCOPE.md` |
| 6. Tasks | ⚪ | Implicit in commit sequence |
| 7. Implement | ✅ | 36 command files + 14 skill files authored |
| 8-14. Docs/menu/help/catalog/log/changelog | ✅ | All updated |
| 15. Verify | ⚪ | No formal `/bq-verify` run (the verify command didn't exist yet) |

**Verdict:** ✅ Properly worked through the workflow.

---

### F2. `/bq-add-feature` (legacy)

| Step | Status |
|---|---|
| 1-6 | ❌ skipped |
| 7. Implement | ✅ |
| 8-14 | ⚪ partial |
| 15. Verify | ❌ |

**Verdict:** 🟡 process gap — superseded by `/bq-feature` in alpha.2. `bq-add-feature.md` still on disk as legacy.

**Repair:** alpha.14 — mark explicitly as deprecated; redirect to `/bq-feature`.

---

### F3. 7 specialist skills (alpha.2)

`bequite-researcher`, `bequite-product-strategist`, `bequite-ux-ui-designer`, `bequite-backend-architect`, `bequite-database-architect`, `bequite-security-reviewer`, `bequite-devops-cloud`

| Step | Status |
|---|---|
| 1-6 | ⚪ informal; skills designed during conversation |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** 🟡 informal process; outcome solid; skills have valid Anthropic Skills format.

---

### F4. Tool neutrality (ADR-003, alpha.3)

| Step | Status |
|---|---|
| 1-2 | ✅ surfaced by user observation |
| 3. Research | ⚪ |
| 4. Scope | ✅ ADR-003 |
| 5. Plan | ⚪ |
| 6. Tasks | ⚪ |
| 7. Implement | ✅ principle + decision template added |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** ✅ Principles-level addition; ADR is the scope/plan.

---

### F5. `/bq-uiux-variants` + `/bq-live-edit` (alpha.4)

| Step | Status |
|---|---|
| 1-3 | ⚪ |
| 4. Scope | ✅ `UIUX_VARIANTS_STRATEGY.md` + `LIVE_EDIT_STRATEGY.md` |
| 5. Plan | ⚪ embedded in strategy docs |
| 6. Tasks | ⚪ |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** ✅ Strategy docs served as scope+plan; reasonable for a focused feature.

---

### F6. `/bq-now`, mistake memory wiring (alpha.5)

| Step | Status |
|---|---|
| 1-6 | ❌ shortcut to impl |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** 🟡 process shortcut; outcome solid; small-scope additions.

---

### F7. Installer template carry (alpha.6)

| Step | Status |
|---|---|
| 1-6 | ❌ direct impl |
| 7. Implement | ✅ |
| 8-14 | ⚪ partial — focused on installer + extending older commands with standardized fields |
| 15. Verify | ✅ Bash verification of template presence post-commit |

**Verdict:** 🟡 maintenance task; appropriate to shortcut.

---

### F8. `/bq-spec`, `/bq-explain` (alpha.7)

| Step | Status |
|---|---|
| 1-3 | ❌ direct from user prompt |
| 4. Scope | ⚪ embedded in user prompt |
| 5. Plan | ⚪ |
| 6. Tasks | ❌ |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** 🟡 process shortcut.

---

### F9. `/bq-suggest`, `/bq-job-finder`, `/bq-make-money`, worldwide_hidden, deep intel (alpha.8 + alpha.10)

| Step | Status |
|---|---|
| 1. Request | ✅ explicit user prompts; full feature scope provided |
| 2. Discovery | ⚪ implicit |
| 3. Research | ❌ no formal `/bq-research` run (no `RESEARCH_REPORT.md` for these features) |
| 4. Scope | ⚪ embedded in user prompts |
| 5. Plan | ❌ no `IMPLEMENTATION_PLAN.md` |
| 6. Tasks | ❌ no `TASK_LIST.md` |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** 🟠 Significant process drift. Features WORK, but the discipline was skipped because the user provided the spec inline.

---

### F10. `/bq-update` + memory-first behavior (alpha.10)

| Step | Status |
|---|---|
| 1-3 | ❌ direct from user prompt |
| 4. Scope | ⚪ embedded in user prompt |
| 5-6 | ❌ |
| 7. Implement | ✅ |
| 8-14 | ✅ |
| 15. Verify | ⚪ |

**Verdict:** 🟠 Similar process gap.

---

### F11. Installer hotfix (alpha.11)

| Step | Status |
|---|---|
| 1-6 | ❌ direct fix |
| 7. Implement | ✅ |
| 8-14 | ⚪ partial |
| 15. Verify | ✅ |

**Verdict:** ✅ Hotfix appropriate to shortcut.

---

### F12. 4 operating modes (Deep / Fast / Token Saver / Delegate) (alpha.12)

| Step | Status |
|---|---|
| 1. Request | ✅ explicit user prompt |
| 2. Discovery | ⚪ |
| 3. Research | ❌ no formal research on existing mode systems |
| 4. Scope | ⚪ embedded in prompt |
| 5. Plan | ❌ no `IMPLEMENTATION_PLAN.md` for the mode system |
| 6. Tasks | ❌ |
| 7. Implement | ✅ |
| 8-14 | ✅ comprehensive — touched 19 files |
| 15. Verify | ⚪ no formal verify |

**Verdict:** 🟠 Process gap.

---

### F13. Presentation Builder (alpha.13) — **the audit trigger**

| Step | Status | Evidence |
|---|---|---|
| 1. Request to memory | ⚪ embedded in user prompt; not separately filed | — |
| 2. Discovery (`/bq-discover` for presentation domain) | ❌ | No discovery report for "presentation tools landscape" |
| 3. Research (`/bq-research` 11-dim) | ❌ | No `RESEARCH_REPORT.md` for PPTX libraries, HTML frameworks, motion approaches |
| 4. Scope (`SCOPE.md`) | ❌ | No formal scope lock |
| 5. Plan (`IMPLEMENTATION_PLAN.md`) | ❌ | No formal plan |
| 6. Tasks (`TASK_LIST.md`) | ❌ | No task breakdown |
| 7. Implement | ✅ | Command file + skill + 9 templates created |
| 8. Update README | ✅ | New Creative + Content section |
| 9. Update commands.md | ✅ | Full entry |
| 10. Update `/bequite` menu | ✅ | New section |
| 11. Update `/bq-help` | ✅ | alpha.13 surface line added |
| 12. Update command catalog | ✅ | Full entry + tallies bumped |
| 13. Update agent log | ✅ | alpha.13 entry |
| 14. Update changelog | ✅ | alpha.13 released entry |
| 15. Verify command + skill consistency | ❌ | No formal verify; no `VERIFY_REPORT.md` |

**Verdict:** 🟠 **HIGH PROCESS GAP — confirmed.** This is exactly what the user observed. The IMPLEMENTATION half of the workflow was done correctly (steps 7-14 all green). The DISCOVERY + RESEARCH + SCOPE + PLAN + TASKS half was skipped entirely.

**Why it happened:** The user's prompt was extremely detailed (specified PPTX, HTML, variants, strict/creative, morph-like motion, brand extraction, etc.). The agent treated the prompt as a finished spec and went straight to implementation. **The agent did not pause to say "let me first research presentation tools / write a scope / break this into tasks."**

**What should have happened in alpha.13:**

- `/bq-research deep "presentation generation tools and patterns"` → write `.bequite/research/PRESENTATION_DOMAIN_RESEARCH.md` covering PPTX libraries (python-pptx, pptxgenjs, Aspose, Spire), HTML slide frameworks (reveal.js, Slidev, Marp, Spectacle, Impress.js, Eagle), motion approaches (Microsoft Morph, GSAP, Motion One, CSS keyframes, Apple Keynote Magic Move), and brand-extraction tools.
- `/bq-scope "presentation builder feature"` → lock IN: PPTX + HTML + variants + strict/creative + brand extraction. Lock OUT: actual rendering (deferred to per-invocation); auto-install of tools.
- `/bq-plan` → `IMPLEMENTATION_PLAN.md` for: command file + skill file + 9 memory templates + docs updates + installer updates.
- `/bq-assign` → `TASK_LIST.md` enumerating 27 atomic file changes.
- Then `/bq-implement` per task.
- `/bq-verify` post-implementation.

**Repair for alpha.14:**

- ✅ Recognize the gap; write this audit
- ✅ Apply the global feature-addition rule going forward (alpha.15+ must follow the workflow)
- ⚪ Do NOT retroactively redo alpha.13 work — the output is solid; lessons learned are recorded
- ✅ Add `BEQUITE_SYSTEM_RESEARCH_REPORT.md` with the presentation-domain research that should have been done
- ✅ Add the workflow-rule to CLAUDE.md, WORKFLOW_GATES.md, COMMAND_CATALOG, USING_BEQUITE_COMMANDS

---

### F14. Mistake memory wiring (alpha.5)

| Step | Status |
|---|---|
| 1-6 | ❌ direct |
| 7. Implement | ✅ |
| 8-14 | ✅ |

**Verdict:** ✅ Small-scope; appropriate.

---

### F15. Roadmap features (future)

- Bot Maker — roadmap only
- Automation — roadmap only
- Scraping — partial (skill exists; activates on demand)
- Marketing/content/data/report — roadmap only

**Verdict:** ✅ Properly kept as roadmap entries in `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`. No premature implementation. No command clutter.

---

## 3. Aggregate finding

**12 of 15 features had process drift in the discover→research→scope→plan→tasks phase.**

The pattern: when the user provides a detailed spec inline, the agent treats the spec as the equivalent of the scope+plan and shortcuts to implementation. This:

- ✅ Produces working features quickly
- ✅ Honors the user's stated intent
- ❌ Skips independent research that might surface better approaches
- ❌ Skips formal scope lock (so SCOPE.md doesn't reflect every feature)
- ❌ Skips task breakdown (so atomicity isn't enforced)
- ❌ Skips formal verify (so VERIFY_REPORT only exists for the lifecycle MVP)

---

## 4. The global feature-addition rule (alpha.14 codification)

Going forward, **every new BeQuite feature MUST go through this workflow**. The rule applies even when the user provides a detailed spec — the agent must still:

1. **Confirm with the user that the spec is the scope** (or open `/bq-clarify` if any ambiguity)
2. **Run targeted research** if the feature involves a domain BeQuite hasn't researched before (presentations, scraping, automation, jobs, etc.). Even 30 minutes of research often surfaces a better library / approach / pattern.
3. **Write a SCOPE.md** (even a one-pager) so future audits can verify the feature's scope was deliberate
4. **Write a PLAN.md** (even brief) listing the files that will be created/modified
5. **Break into TASKS** when the change touches > 5 files
6. **Implement** the command / skill / docs / memory
7. **Update docs** consistently (the alpha.13 docs work was done well; preserve this discipline)
8. **Run `/bq-verify`** post-implementation. Output a `VERIFY_REPORT.md`.

**Exemptions (still need 7-8):**
- Hotfixes (e.g. alpha.11 installer fix) can skip 2-6
- Doc-only changes can skip 2-6
- Adding a skill that activates only via existing command can skip 2-6 (but should still scope what the skill does)

**Documented in (alpha.14 repair):**
- `CLAUDE.md` — core operating rules section, item 13
- `docs/architecture/WORKFLOW_GATES.md` — new section "Feature-addition workflow"
- `docs/specs/COMMAND_CATALOG.md` — top-of-file note
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` — new section
- Each command file's "Failure behavior" — reference

---

## 5. Per-feature repair check

### Presentation Builder — verify post-alpha.13 state

| Required | Present? |
|---|---|
| `/bq-presentation` command | ✅ |
| `bequite-presentation-builder` skill | ✅ |
| `.bequite/presentations/` memory folder | ✅ |
| PPTX vs HTML decision logic | ✅ in command + skill |
| Strict vs creative mode | ✅ |
| Variants 1-10 | ✅ |
| Source / reference handling | ✅ |
| Design strategy | ✅ via `DESIGN_BRIEF.md` template |
| Motion / morph-like planning | ✅ via `MOTION_PLAN.md` template |
| Speaker notes | ✅ via `SPEAKER_NOTES.md` template |
| README mention | ✅ Creative + Content Workflows section |
| commands.md mention | ✅ full entry |
| `/bequite` menu mention | ✅ Creative + Content Workflows block |
| `/bq-help` mention | ✅ alpha.13 line |
| `/bq-suggest` recommendation | ✅ keyword triggers added |
| Logs / changelog | ✅ |
| **Memory preflight + writeback in `/bq-presentation`** | ✅ `## Files to read`, `## Memory updates` |
| **Quality gate in `bequite-presentation-builder` skill** | ❌ — alpha.14 must add |
| **`When NOT to use` in skill** | ❌ — alpha.14 must add |

**Repair:** add `## Quality gate` and `## When NOT to use` sections to `bequite-presentation-builder` SKILL.md.

### Job Finder + Make Money — verify

| Required | Present? |
|---|---|
| `/bq-job-finder` | ✅ |
| `/bq-make-money` | ✅ |
| Worldwide hidden search | ✅ |
| Community-discovered opportunities | ✅ (alpha.10) |
| AI-assisted work | ✅ |
| Non-English search | ✅ |
| Hidden gems | ✅ |
| Trust checks | ✅ |
| Repeated update behavior | ✅ (compare-runs feature) |
| Memory folders | ✅ `.bequite/jobs/`, `.bequite/money/` |
| README mention | ✅ |
| commands.md mention | ✅ |
| `/bequite` menu mention | ✅ |
| `/bq-help` mention | ✅ |
| `/bq-suggest` recommendation | ✅ |
| **Memory preflight + writeback** | ✅ |
| **Quality gate in skills** | ❌ — alpha.14 must add |
| **`When NOT to use`** | ❌ — alpha.14 must add |

### Modes (Deep / Fast / Token Saver / Delegate) — verify

| Required | Present? |
|---|---|
| Visible near top of README | ✅ "Operating Modes" section is 4th visible section |
| commands.md explains them | ✅ full section |
| `/bequite` shows them | ✅ Operating modes block |
| `/bq-help` explains them | ✅ modes table + composition |
| `/bq-auto` supports via natural language + flags | ✅ |
| `token-free` wording removed | ✅ all 8 occurrences are NEGATIONS ("NOT token-free"); not errors |

✅ All 4 modes consistent.

---

## 6. Acceptance for alpha.14

- [ ] Global feature-addition rule codified in 4+ docs
- [ ] All commands' "Failure behavior" sections reference the rule
- [ ] `bq-add-feature.md` marked as deprecated alias
- [ ] Presentation Builder skill gets `Quality gate` + `When NOT to use`
- [ ] Job Finder + Make Money skills get the same
- [ ] Per-feature audit verified post-repair
