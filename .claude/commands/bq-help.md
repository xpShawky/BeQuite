---
description: Full BeQuite command reference. Explains every command — when to use it, what it reads, what it writes, what comes next. Grouped by workflow phase, not alphabetically. For the deep reference, see commands.md at repo root.
---

# /bq-help — full command reference

You are showing the user the complete BeQuite command reference. Order by workflow phase. For each command, give:

- **When to use it**
- **What it reads** (memory files + project files)
- **What it writes**
- **What output to expect**
- **Usual next command**

Print this in the chat. Do not run any other action — `/bq-help` is read-only documentation.

> **Note (alpha.5+):** For the canonical reference with full per-command detail (Preconditions / Required gates / Quality gate / Failure behavior / etc.), see [`commands.md`](../../commands.md) at the project root. This `/bq-help` output is the in-Claude-Code summary; `commands.md` is the deep reference.
>
> For one-line orientation: `/bq-now`. For the gate-aware menu: `/bequite`.

---

## Phase 0 — Setup and Understanding

### /bequite (the root menu)
- **When:** anytime — quick orientation, recommended next steps
- **Reads:** all `.bequite/state/*.md`
- **Writes:** nothing
- **Output:** status box + recommended 3 commands + full map
- **Next:** whatever was recommended

### /bq-help (you are here)
- **When:** when you want the full command reference
- **Reads:** nothing
- **Writes:** nothing
- **Next:** `/bq-init` if BeQuite is fresh

### /bq-init
- **When:** first time installing BeQuite into a repo. Also `/bq-init new` for a brand-new empty folder.
- **Reads:** detects package.json / pyproject.toml / Cargo.toml etc.; existing CLAUDE.md if any
- **Writes:** creates `.bequite/state/PROJECT_STATE.md`, `CURRENT_PHASE.md`, `LAST_RUN.md`; appends a BeQuite section to CLAUDE.md if missing
- **Output:** "BeQuite initialized. Run /bq-discover next."
- **Next:** `/bq-discover` (existing repo) or `/bq-clarify` (new project)

### /bq-discover
- **When:** after init, before planning. Inspect the repo to understand what's there.
- **Reads:** package manifests, README, tests, docker-compose, .github/workflows, etc.
- **Writes:** `.bequite/audits/DISCOVERY_REPORT.md`
- **Output:** Detected stack, apps, entry points, ports, docs, tests, risks, missing info
- **Next:** `/bq-doctor`

### /bq-doctor
- **When:** verify the environment is ready to build
- **Reads:** project manifests + PATH tools (node, python, docker, bun, etc.)
- **Writes:** updates `.bequite/state/PROJECT_STATE.md` with the environment snapshot
- **Output:** Tabular health report — stack, package manager, versions, env files, ports, CI, blockers
- **Next:** `/bq-clarify` (if questions remain) or `/bq-audit` (if doctor surfaced issues) or `/bq-plan` (if everything's clean)

---

## Phase 1 — Problem Framing

### /bq-clarify
- **When:** before planning. Ask the user 3-5 high-value clarifying questions only.
- **Reads:** DISCOVERY_REPORT.md, PROJECT_STATE.md
- **Writes:** `.bequite/state/OPEN_QUESTIONS.md` (with the user's answers folded in)
- **Output:** Numbered questions. Recommended defaults if user says "skip".
- **Next:** `/bq-research` (if any answer needs evidence) or `/bq-plan`

### /bq-research
- **When:** before stack decisions or library picks — verify freshness, deprecation, CVEs.
- **Reads:** OPEN_QUESTIONS.md
- **Writes:** `.bequite/audits/RESEARCH_REPORT.md`
- **Output:** Cited findings, library candidates, freshness verdicts.
- **Next:** `/bq-scope` (if the research expanded the question set) or `/bq-plan`

### /bq-scope
- **When:** when the problem is sprawling. Lock what's IN, what's OUT, what's a non-goal.
- **Reads:** OPEN_QUESTIONS.md, RESEARCH_REPORT.md
- **Writes:** `.bequite/plans/SCOPE.md`
- **Output:** In / Out / Non-goals lists.
- **Next:** `/bq-plan`

### /bq-plan
- **When:** the main planning command. Writes a complete implementation plan WITHOUT writing code.
- **Reads:** all of Phase 0–1 outputs
- **Writes:** `.bequite/plans/IMPLEMENTATION_PLAN.md`
- **Output:** Vision, context, non-goals, architecture, stack decision, file plan, phase plan, task list, test plan, risks, acceptance criteria, rollback plan
- **Next:** `/bq-assign` (most common) or `/bq-multi-plan` (if planning quality is critical and you want a second opinion)

### /bq-multi-plan
- **When:** for high-stakes plans where independent thinking from two models matters.
- **Reads:** all Phase 0–1 outputs
- **Writes:** `.bequite/prompts/generated_prompts/PROMPT_CLAUDE.md`, `PROMPT_CHATGPT.md`. Waits for user to paste back two outputs. Then merges into `.bequite/plans/IMPLEMENTATION_PLAN.md` with a comparison report.
- **Output:** Prompts to paste; wait for paste-back; merged final plan.
- **Next:** `/bq-assign`

---

## Phase 2 — Build

### /bq-assign
- **When:** plan is approved, time to break it into atomic tasks.
- **Reads:** IMPLEMENTATION_PLAN.md
- **Writes:** `.bequite/tasks/TASK_LIST.md` with task IDs, priorities, dependencies, owners
- **Output:** Numbered task list (T-1.1, T-1.2, etc.) with acceptance criteria each
- **Next:** `/bq-implement`

### /bq-implement
- **When:** the workhorse. Implement ONE approved task at a time.
- **Reads:** TASK_LIST.md, IMPLEMENTATION_PLAN.md
- **Writes:** source code; updates `.bequite/state/CURRENT_PHASE.md`, `LAST_RUN.md`; appends `.bequite/logs/AGENT_LOG.md`
- **Output:** Files changed, tests run, exit codes
- **Rules:** inspect files first, make minimal safe changes, run relevant tests, stop on blocker
- **Next:** `/bq-test` (verify what you just built) → `/bq-implement` (next task) → repeat

### /bq-add-feature
- **When:** safer wrapper for adding a new feature (spec → plan → impl → test atomic).
- **Reads:** PROJECT_STATE.md
- **Writes:** spec at `.bequite/plans/feature-<slug>.md`, then code changes, then tests
- **Output:** Spec preview + impl plan + diff summary + test results
- **Next:** `/bq-test` then `/bq-review`

### /bq-fix
- **When:** something is broken. Reproduce → root-cause → smallest safe patch.
- **Reads:** ERROR_LOG.md + the failing output
- **Writes:** code change + new/updated test + appends ERROR_LOG.md with the root cause
- **Output:** Reproduction steps, root cause, fix diff, verification result
- **Next:** `/bq-test` to confirm the fix held; `/bq-changelog` to record it

---

## Phase 3 — Quality

### /bq-test
- **When:** after any implementation. Run tests AND write missing ones.
- **Reads:** package manifests to find the test command (`npm test`, `pytest`, `cargo test`, etc.)
- **Writes:** new test files when coverage gaps surface
- **Output:** Test count, pass/fail breakdown, any new tests added
- **Next:** `/bq-review` or `/bq-implement` (if green)

### /bq-audit
- **When:** comprehensive project review. Catches what `/bq-doctor` + `/bq-test` miss.
- **Reads:** entire repo
- **Writes:** `.bequite/audits/FULL_PROJECT_AUDIT.md`
- **Output:** Findings table by severity (blocker / warning / nit) with file:line and suggested fixes
- **Next:** `/bq-fix` for each blocker, then `/bq-verify`

### /bq-review
- **When:** before merging / shipping a chunk of work. Reviews CURRENT changes (git diff style).
- **Reads:** uncommitted changes + recent commits
- **Writes:** `.bequite/audits/REVIEW-<timestamp>.md`
- **Output:** Per-file commentary. Verdict: Approved / Approved-with-comments / Blocked.
- **Next:** `/bq-red-team` (if review is too friendly) or `/bq-verify` (if clean)

### /bq-red-team
- **When:** adversarial review. Try to find what's actually broken.
- **Reads:** current changes + plan
- **Writes:** `.bequite/audits/RED_TEAM-<timestamp>.md`
- **Output:** 8 attack angles (security / arch / testing / deployment / scale / UX / token-waste / hidden-assumptions). Severity-tagged findings.
- **Next:** `/bq-fix` for each finding

---

## Phase 4 — Ship

### /bq-verify
- **When:** before claiming the project is clean. Runs the full local verification matrix.
- **Reads:** package manifests
- **Writes:** `.bequite/audits/VERIFY_REPORT.md`
- **Output:** Each gate (install / lint / typecheck / unit / integration / build / smoke / frontend / api / cli) with status
- **Next:** `/bq-release` if all green; otherwise `/bq-fix`

### /bq-release
- **When:** verify passed. Confirm ship-ready.
- **Reads:** VERIFY_REPORT.md
- **Writes:** updates `CHANGELOG.md` + tags a release (if user approves) + writes `.bequite/state/LAST_RUN.md` "released"
- **Output:** Release summary, tag suggestion, push-to-remote command
- **Next:** `/bq-changelog` (if you want to make sure CHANGELOG is detailed) or `/bq-handoff` (if handing off)

### /bq-changelog
- **When:** keep the project's CHANGELOG.md sharp.
- **Reads:** recent commits + any feature specs
- **Writes:** prepends a new entry to `CHANGELOG.md` (or creates it)
- **Output:** Diff of the new entry. Asks user to confirm before committing.
- **Next:** `/bq-release` if you're shipping right now

---

## Phase 5 — Continue Later

### /bq-memory
- **When:** read or write BeQuite memory snapshots.
- **Reads:** `.bequite/state/*` + recent logs
- **Writes:** `.bequite/state/SNAPSHOT-<timestamp>.md`
- **Output:** Summary of what's in memory + what to do with it
- **Next:** `/bq-recover` (if loading) or back to the workflow command you were running

### /bq-recover
- **When:** new session after a break. Reload context and continue from last green state.
- **Reads:** all `.bequite/state/*` + last few logs
- **Writes:** updates `.bequite/state/LAST_RUN.md` "resumed"
- **Output:** Summary: last task, last commit, last error, next safe step
- **Next:** whatever was in progress (`/bq-implement` usually) — see the recovery output

### /bq-handoff
- **When:** handing the project to another engineer.
- **Reads:** full repo + all `.bequite/` artifacts
- **Writes:** `HANDOFF.md` at repo root (engineer-friendly) + a vibe-handoff section (non-engineer-friendly)
- **Output:** Path to HANDOFF.md + a checklist of what the receiver should verify
- **Next:** (none — handoff is the final action)

---

## When in doubt

Run `/bequite` for the menu. It reads your current state and tells you the next 3 best commands.

---

## Standardized command fields (alpha.6+)

**Phase:** Any (meta — read-only reference)
**When NOT to use:** quick orientation (use `/bq-now`); gate-aware menu (use `/bequite`); full deep reference (open [`commands.md`](../../commands.md) — has Preconditions / Required gates / Quality gate / Failure behavior fields per command).
**Preconditions:** none
**Required previous gates:** none
**Quality gate:** output covers all 37 commands grouped by phase; no out-of-date phase names; surfaces alpha.5+ additions (`/bq-now`, `/bq-spec`, `/bq-explain`, `/bq-uiux-variants`, `/bq-live-edit`)
**Failure behavior:** if the user wants more depth than this command provides, point them at `commands.md` (the full reference) or `/bequite` (the menu)
**Memory updates:** none (read-only)
**Log updates:** none (read-only navigation aid)

## Notes on the alpha.5+ surface

This help output has the original Phase 0-5 names that pre-date alpha.2. The current canonical names are:
- **Phase 0 — Setup and Discovery** (was "Setup and Understanding")
- **Phase 1 — Product Framing and Research** (was "Problem Framing")
- **Phase 2 — Planning and Build** (was "Build")
- **Phase 3 — Quality and Review** (was "Quality")
- **Phase 4 — Release** (was "Ship")
- **Phase 5 — Memory and Handoff** (was "Continue Later")

Additional commands not listed above (alpha.2+):
- `/bq-mode`, `/bq-new`, `/bq-existing` (P0)
- `/bq-feature` (P2 — supersedes `/bq-add-feature`)
- `/bq-auto`, `/bq-p0`..`p5` (orchestrators)
- `/bq-uiux-variants`, `/bq-live-edit` (UI workflow — alpha.4)
- `/bq-now` (one-line orientation — alpha.5)
- `/bq-spec`, `/bq-explain` (alpha.7)
- `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` (Opportunity and Workflows — alpha.8)
- `/bq-update` (Maintenance — alpha.10; safe BeQuite self-update with backup + conflict surfacing)
- `/bq-presentation` (Creative and Content Workflows — alpha.13; premium PPTX / HTML presentations with variants, strict-vs-creative modes, morph-like motion planning)

### Alpha.10 deep intelligence for opportunity commands

`/bq-job-finder` and `/bq-make-money` now search **community signals** (Reddit / IH / HN / Product Hunt / X / forums) + **trending short-window** opportunities + **AI-assisted paths** in addition to standard platforms. New tracks: `worldwide_hidden`, `trending_now`, `community_discovered`, `AI_assisted`, `no_calls`, `fast_first_payout`, `highest_payout`, `beginner_friendly`, `skilled_remote`, `local_country`, `non_english_platforms`. New memory files: `HIDDEN_GEMS.md`, `COMMUNITY_SIGNALS.md`, `AI_ASSISTED_WORK.md` / `AI_ASSISTED_PATHS.md`.

---

## Operating Modes (alpha.12 — 4 composable modes)

4 modes that adjust how BeQuite executes — without ever skipping safety. All 17 hard human gates apply regardless. Set on any command as a positional flag.

| Mode | Best for | Research | Tests | Output | Cost |
|---|---|---|---|---|---|
| **deep** | Quality-critical · production · regulated · big new builds | Full 11-dim + community + competitors + failure stories | Full + red-team | Long, detailed | Higher (worth it) |
| **fast** | Small scoped fix · trivial feature · prototype | 3 dims (stack / security / scale) + memory-first | Run tests for changed surface | Compact | Lower |
| **token-saver** *(alias `lean`)* | Long sessions · cost-sensitive · cached research reuse | Reuse prior + targeted reads + summaries | Scoped | Compact | Lowest — NOT token-free |
| **delegate** | Strong model designs, cheap model implements, strong model reviews | Strong model does research in Phase 1 | Cheap model runs task-pack tests; strong model verifies | Variable | Cheaper than `deep` alone |

### Mode examples

```
/bq-auto deep "Build a SaaS dashboard for clinic booking"
/bq-research deep "Research best architecture and product gaps"

/bq-auto fast "Fix dashboard text contrast"
/bq-fix fast "Fix install error"

/bq-auto token-saver "Add a small settings toggle"
/bq-auto lean "Quick scoped task"                      # alias

/bq-auto delegate "Build this feature"
/bq-plan delegate "Create implementation tasks for a cheaper model"
/bq-review delegate "Review implementation made by cheaper model"
```

### Composition (modes stack)

```
/bq-auto deep delegate "Research deeply, then produce delegated tasks"
/bq-auto fast token-saver "Quick small fix with low context use"
/bq-auto uiux variants=5 deep "Create high-quality design directions"
/bq-auto security deep "Full security review"
```

### Conflict resolution

| Conflict | Resolution |
|---|---|
| `fast` + `deep` | Ask one question; default `deep` for quality-critical intents (new / security / release / deploy); `fast` for trivial scoped fixes |
| `delegate` + tiny task | Refuse delegate; recommend `fast` (handoff overhead not worth it) |
| `delegate` + no prior research | Auto-compose with `deep` (delegate needs research to write a good task pack) |
| Any mode + hard human gate | Mode never bypasses safety; gate fires regardless |

**Important:** Modes adjust **depth + cost + speed**, NOT safety. Token Saver is **token-lean**, not "token-free". Fast mode still runs tests and verification.

- Active mode for current run: `.bequite/state/CURRENT_MODE.md`
- Mode history + outcomes + cost: `.bequite/state/MODE_HISTORY.md`
- Full strategy: `docs/architecture/AUTO_MODE_STRATEGY.md` §11
- Delegate task pack: `.bequite/tasks/DELEGATE_*.md` + `.bequite/audits/DELEGATE_REVIEW_REPORT.md`

For the complete picture: [`commands.md`](../../commands.md).
