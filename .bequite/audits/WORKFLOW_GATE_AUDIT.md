# Workflow Gate Audit (alpha.14)

**Run date:** 2026-05-17
**Reference:** `docs/architecture/WORKFLOW_GATES.md` + `.bequite/state/WORKFLOW_GATES.md` (template for installed projects)

---

## 1. The gate model — what's documented vs. what's enforced

BeQuite's gate model is **convention-enforced, not machine-enforced**. The gates are:

1. Documented in `docs/architecture/WORKFLOW_GATES.md`
2. Tracked in `.bequite/state/WORKFLOW_GATES.md` (ledger of which gates are `✅` / `❌` / `⚪`)
3. Listed in each command's "Required previous gates" section
4. **Expected** to be respected by the agent reading the command file

There is no hook, no daemon, no script that REFUSES to run a command when its gates aren't met. The discipline is **enforced by the agent honoring the contract**.

**This is acceptable** for a markdown-driven skill pack — but the discipline must be:
- Clearly documented (so users + agent both know)
- Explicit in every command's behavior section (so the agent refuses out-of-order invocations)
- Backed by the gate ledger in `.bequite/state/WORKFLOW_GATES.md` (so state is checkable)

---

## 2. Per-command gate refusal behavior

For each command, does the file include explicit instruction to **refuse if gates aren't met + recommend prerequisite**?

| Command | Required gates listed | "Refuse if gates unmet" instruction | Recommends prerequisite | Severity |
|---|---|---|---|---|
| `bequite.md` (menu) | ⚪ (read-only; n/a) | ✅ ("never recommend a command whose required gates aren't met") | ✅ | ✅ |
| `bq-init` | ⚪ (none — always runs) | ⚪ | ⚪ | ✅ |
| `bq-mode` | `BEQUITE_INITIALIZED` | ⚪ implicit | ⚪ | 🟡 |
| `bq-new` | `BEQUITE_INITIALIZED` + mode | ⚪ implicit | ⚪ | 🟡 |
| `bq-existing` | `BEQUITE_INITIALIZED` + mode | ✅ explicit step 1 ("If not 'Existing Project Audit', refuse + suggest `/bq-mode`") | ✅ | ✅ |
| `bq-discover` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | 🟡 |
| `bq-doctor` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | 🟡 |
| `bq-clarify` | `DISCOVERY_COMPLETE` | ⚪ | ⚪ | 🟡 |
| `bq-research` | `DISCOVERY_COMPLETE` | ⚪ | ⚪ | 🟡 |
| `bq-scope` | `RESEARCH_COMPLETE` | ⚪ | ⚪ | 🟡 |
| `bq-plan` | `SCOPE_LOCKED` | ⚪ | ⚪ | 🟡 |
| `bq-multi-plan` | `PLAN_APPROVED` | ⚪ | ⚪ | 🟡 |
| `bq-spec` | `BEQUITE_INITIALIZED` + `MODE_SELECTED` (recommended) | ⚪ | ⚪ | 🟡 |
| `bq-assign` | `PLAN_APPROVED` | ⚪ | ⚪ | 🟡 |
| `bq-implement` | `TASKS_ASSIGNED` | ⚪ | ⚪ | 🟡 |
| `bq-feature` | `BEQUITE_INITIALIZED` (self-contained) | ⚪ | ⚪ | ✅ |
| `bq-fix` | `BEQUITE_INITIALIZED` (self-contained) | ⚪ | ⚪ | ✅ |
| `bq-add-feature` (legacy) | n/a (alias) | ⚪ | ⚪ | 🟡 (mark deprecated) |
| `bq-test` | `IMPLEMENTATION_STARTED` | ❌ none stated; no refusal logic | ❌ | 🟠 high |
| `bq-audit` | `IMPLEMENTATION_DONE` (or audit-only mode) | ⚪ | ⚪ | 🟡 |
| `bq-review` | `IMPLEMENTATION_DONE` | ⚪ | ⚪ | 🟡 |
| `bq-red-team` | `IMPLEMENTATION_DONE` | ⚪ | ⚪ | 🟡 |
| `bq-verify` | `TESTS_PASS` + `REVIEW_APPROVED` | ⚪ | ⚪ | 🟡 |
| `bq-release` | `VERIFY_PASSED` | ⚪ | ⚪ | 🟡 |
| `bq-changelog` | none | ⚪ | ⚪ | ✅ |
| `bq-memory` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ |
| `bq-recover` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ |
| `bq-handoff` | `VERIFY_PASSED` | ⚪ | ⚪ | 🟡 |
| `bq-auto` | `BEQUITE_INITIALIZED` + `MODE_SELECTED` | ✅ explicit | ✅ | ✅ |
| `bq-p0..p5` | per phase | ⚪ implicit | ⚪ | 🟡 |
| `bq-uiux-variants` | `BEQUITE_INITIALIZED` + frontend exists | ⚪ | ⚪ | 🟡 |
| `bq-live-edit` | `BEQUITE_INITIALIZED` + frontend exists | ✅ | ✅ | ✅ |
| `bq-suggest` | `BEQUITE_INITIALIZED` | ✅ implicit (read-only advisor) | ✅ | ✅ |
| `bq-job-finder` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ (orthogonal to dev workflow) |
| `bq-make-money` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ (orthogonal) |
| `bq-update` | `BEQUITE_INITIALIZED` + git on PATH | ✅ | ✅ | ✅ |
| `bq-presentation` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ (orthogonal; creative workflow) |
| `bq-now` | none | ⚪ | ⚪ | ✅ |
| `bq-explain` | `BEQUITE_INITIALIZED` | ⚪ | ⚪ | ✅ |

### Findings

1. **`/bq-test` is the worst offender** — no gate refusal logic. Should refuse if `IMPLEMENTATION_STARTED ❌`.
2. **Phase orchestrators `/bq-p1`..`/bq-p5`** rely on "implicit" refusal — they call subcommands that themselves refuse. Acceptable, but each orchestrator should add an explicit check at the top.
3. **P1 commands (`clarify`, `research`, `scope`, `plan`)** all list their gate but lack explicit refusal logic. The gate is documented but not actively enforced by the command body.

---

## 3. Gate ledger consistency

`.bequite/state/WORKFLOW_GATES.md` defines gate names. Some command files use different spellings:

| Canonical (in WORKFLOW_GATES.md) | Variant found in command files |
|---|---|
| `DISCOVERY_COMPLETE` | `DISCOVERY_DONE` (in COMMAND_CATALOG.md, several command bodies) |
| `RESEARCH_COMPLETE` | `RESEARCH_DONE` (in COMMAND_CATALOG, some commands) |
| `IMPLEMENTATION_DONE` | `IMPLEMENT_DONE` (in COMMAND_CATALOG) |
| `SCOPE_LOCKED` | ✅ consistent |
| `PLAN_APPROVED` | ✅ consistent |
| `TASKS_ASSIGNED` | `ASSIGN_DONE` (in COMMAND_CATALOG) |
| `TESTS_PASS` | `TEST_DONE` (in COMMAND_CATALOG) |
| `AUDIT_COMPLETE` | `AUDIT_DONE` (in COMMAND_CATALOG) |
| `REVIEW_APPROVED` | `REVIEW_DONE` (in COMMAND_CATALOG) |
| `VERIFY_PASSED` | `VERIFY_PASS` (in COMMAND_CATALOG) |
| `RELEASE_PREPPED` | `RELEASE_READY` (in COMMAND_CATALOG) |

**Repair decision:** Adopt the `_DONE` naming as canonical (shorter, parallel form across all gates). Update `WORKFLOW_GATES.md` to match `COMMAND_CATALOG.md`.

Alternative: keep both forms documented as aliases. Lower repair cost; clearer for users. **Pick this option in alpha.14 — document both in WORKFLOW_GATES.md "Aliases" section.**

---

## 4. Mode-specific gate behavior

The gate model has mode-specific skips defined in `WORKFLOW_GATES.md` (§ "Mode-specific gate overrides"):

| Mode | Skipped gates | Required additional gates |
|---|---|---|
| Fix Problem | `MODE_SELECTED`, `RESEARCH_COMPLETE`, `SCOPE_LOCKED`, `PLAN_APPROVED` | `BUG_REPRODUCED`, `ROOT_CAUSE_IDENTIFIED`, `FIX_APPLIED`, `FIX_VERIFIED` |
| Add Feature | `MODE_SELECTED = New Project / Existing Audit` | `FEATURE_TYPE_IDENTIFIED`, `FEATURE_SPEC_APPROVED`, `FEATURE_IMPLEMENTED`, `FEATURE_TESTED` |
| Research Only | (stops at `RESEARCH_COMPLETE`) | — |
| Release Readiness | requires `IMPLEMENTATION_DONE` | runs only P3 + P4 |

**Finding:** These mode-specific gates are documented but not implemented as separate ledger entries in `.bequite/state/WORKFLOW_GATES.md`. The mode overrides are honored only by the agent reading the doc. This is acceptable for a convention-driven system but should be made explicit in alpha.14.

---

## 5. Per-mode workflow alignment

For each of the 6 explicit modes + alpha.13 workflow categories, does the system have a clean path through the gates?

| Mode / workflow | Entry command | Gate path | Status |
|---|---|---|---|
| New Project | `/bq-new` → `/bq-p0` → `/bq-p1` → ... → `/bq-p5` | full P0→P5 gate sequence | ✅ |
| Existing Project Audit | `/bq-existing` → `/bq-discover` → `/bq-doctor` → `/bq-audit` | P0 + audit gate path | ✅ |
| Add Feature | `/bq-feature "..."` | mini-spec → impl → test (feature-specific gates) | ✅ |
| Fix Problem | `/bq-fix "..."` | reproduce → root → patch → test → verify (fix-specific gates) | ✅ |
| Research Only | `/bq-mode research-only` → `/bq-clarify` → `/bq-research` → stop | P0 + P1 partial | ✅ |
| Release Readiness | `/bq-mode release` → `/bq-verify` → `/bq-release` | P3 + P4 only | ✅ |
| **Presentation Builder (alpha.13)** | `/bq-presentation` | creative workflow; orthogonal to P0–P5 | ⚪ NOT formally a "mode"; just a command |
| **Job Finder (alpha.8)** | `/bq-job-finder` | orthogonal lifestyle workflow | ⚪ NOT formally a mode |
| **Make Money (alpha.8)** | `/bq-make-money` | orthogonal lifestyle workflow | ⚪ NOT formally a mode |
| **UI/UX Variants (alpha.4)** | `/bq-uiux-variants N "..."` | variants → user picks → merge | ⚪ feature-mode, no separate gate set |
| **Live Edit (alpha.4)** | `/bq-live-edit "..."` | section-map → edit → verify | ⚪ feature-mode, no separate gate set |

**Finding:** The 6 documented modes (`New / Existing / Add Feature / Fix / Research / Release`) are well-defined. **Newer workflows (alpha.4+ UI variants, alpha.8 Opportunity, alpha.13 Presentation) operate as commands without formal mode declarations.** This is acceptable — they're either:
- Feature-modes that operate INSIDE Add Feature mode (UI variants, live edit)
- Orthogonal lifestyle/creative workflows that don't need a mode (Job/Money/Presentation)

**Repair for alpha.14:** Document this clearly in `WORKFLOW_GATES.md` and `CURRENT_MODE.md` template — modes are for **dev lifecycle**; orthogonal workflows don't change the mode.

---

## 6. Verification: hard human gates from `/bq-auto`

The 17 hard human gates documented in `/bq-auto`:

1. Destructive file deletion
2. DB migration on shared/prod
3. Production server change
4. VPS/Nginx/SSL
5. Paid service activation
6. Secret/key handling
7. Auth/security model change
8. Project architecture change
9. Deleting old implementation
10. Scope contradiction
11. User explicit manual-approval
12. Cost ceiling reached
13. Wall-clock ceiling reached
14. Banned weasel words
15. 3 consecutive failures
16. UI variant winner selection
17. Release git push / tag

**These are not "workflow gates" in the WORKFLOW_GATES.md sense** — they're runtime human-confirmation requirements during autonomous mode. They're documented in `/bq-auto.md`, `CLAUDE.md`, `commands.md`, README.md. ✅ Consistent across docs.

---

## 7. Repair plan for alpha.14

### Priority 1 — Add explicit refusal logic to commands

For each command lacking explicit "refuse if gates unmet" logic, add a "Step 0 — Gate check" or expand "Failure behavior":

```markdown
## Gate check (alpha.14)

Before doing any work, verify required gates from `.bequite/state/WORKFLOW_GATES.md`:

If `<required-gate>` is ❌:
> "You're trying to run `/bq-X`, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

Refuse + recommend prerequisite. Don't proceed.
```

Apply to: `bq-test`, `bq-audit`, `bq-review`, `bq-red-team`, `bq-verify`, `bq-release`, `bq-handoff`, `bq-multi-plan`, `bq-assign`, `bq-implement`, `bq-clarify`, `bq-research`, `bq-scope`, `bq-plan`.

### Priority 2 — Gate name aliasing

Add an "Aliases" section to `docs/architecture/WORKFLOW_GATES.md`:

```markdown
## Gate name aliases

Both spellings are valid; commands may use either:

| Canonical | Short alias |
|---|---|
| `DISCOVERY_COMPLETE` | `DISCOVERY_DONE` |
| `RESEARCH_COMPLETE` | `RESEARCH_DONE` |
| `IMPLEMENTATION_DONE` | `IMPLEMENT_DONE` |
| `TASKS_ASSIGNED` | `ASSIGN_DONE` |
| `TESTS_PASS` | `TEST_DONE` |
| `AUDIT_COMPLETE` | `AUDIT_DONE` |
| `REVIEW_APPROVED` | `REVIEW_DONE` |
| `VERIFY_PASSED` | `VERIFY_PASS` |
| `RELEASE_PREPPED` | `RELEASE_READY` |
```

### Priority 3 — Orthogonal workflow clarification

Add a section to `WORKFLOW_GATES.md`:

```markdown
## Orthogonal workflows (don't change mode)

These commands operate independently of the 6 dev lifecycle modes:
- `/bq-presentation` — creative + content
- `/bq-job-finder` — opportunity discovery
- `/bq-make-money` — earning discovery
- `/bq-suggest` — workflow advisor (read-only)
- `/bq-now` — orientation (read-only)
- `/bq-explain` — explainer (read-only)
- `/bq-help` — reference (read-only)
- `/bq-update` — BeQuite self-maintenance

They don't advance phase or set mode. They don't require any phase-gate beyond `BEQUITE_INITIALIZED`.
```

---

## 8. Acceptance

- [ ] Explicit refusal logic added to 14 commands lacking it
- [ ] Gate name aliases documented
- [ ] Orthogonal workflow section added
- [ ] Mode-specific gate overrides made explicit
