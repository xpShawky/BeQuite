---
description: Review CURRENT changes (uncommitted diff or recent commits). Per-file commentary. Verdict: Approved / Approved-with-comments / Blocked.
---

# /bq-review — review changes

You are a senior code reviewer. Look at the **current changes** (uncommitted diff + recent commits) and produce a structured review.

## Step 1 — Get the diff scope

By default, review:
- All uncommitted changes (`git status` + `git diff`)
- Plus the last 1-3 commits (if user didn't say otherwise)

If user passed an argument (`/bq-review HEAD~3..HEAD` or `/bq-review feature-branch`), use that.

## Step 2 — Read context

- `.bequite/plans/IMPLEMENTATION_PLAN.md` (what we're supposed to be building)
- `.bequite/tasks/TASK_LIST.md` (which task this is)
- `.bequite/state/DECISIONS.md` (what's locked)

## Step 3 — Review each file

For each changed file, comment on:

1. **Correctness** — does the code do what the commit message / task says?
2. **Tests** — are there tests for the change? If not, why not?
3. **Edge cases** — null/undefined handling, async errors, off-by-ones, race conditions
4. **Security** — secrets, validation, auth checks, SQL injection, XSS
5. **Style** — does it match the existing project conventions? (Don't bike-shed; only note real divergence.)
6. **Naming** — are names clear? Specific? Self-documenting?
7. **Comments** — does the code need a comment? Are existing comments accurate?
8. **DRY** — is this duplicating logic that lives elsewhere?
9. **Performance** — any obvious O(n²) loops or unnecessary network calls?
10. **Reversibility** — is this easy to roll back if something goes wrong?

## Step 4 — Write REVIEW report

`.bequite/audits/REVIEW-<YYYYMMDD-HHMMSS>.md`:

```markdown
# Review

**Generated:** <ISO 8601 UTC>
**Scope:** <git ref>
**Files changed:** <count>

## Verdict

**<Approved | Approved-with-comments | Blocked>**

(One sentence explaining why.)

## Per-file commentary

### `<path/to/file.ts>` — <NEW | MODIFIED | DELETED>

- **Correctness:** <comment>
- **Tests:** <comment>
- **Issues:**
  - [BLOCKER] <issue> at L<line>
  - [HIGH] <issue> at L<line>
  - [NIT] <issue>
- **Praise:** <one positive note if warranted>

(repeat per file)

## Cross-cutting concerns

- (anything that's not file-specific — e.g. "the new auth flow doesn't log out the user on session expiry")

## Action items before merge

1. <e.g. add test for csv export error path>
2. <e.g. rename `processData` to `parseBookingCSV`>

## Action items after merge (track separately)

1. <e.g. consider extracting csv helper to lib/ once we have a second use>
```

## Step 5 — Assign verdict

- **Approved** — no issues found, or only NITs. Safe to merge.
- **Approved-with-comments** — addressable issues that don't block. User can merge then follow up.
- **Blocked** — at least one BLOCKER or HIGH issue. Don't merge until fixed.

## Step 6 — Update state + log

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Step 7 — Report back

```
<Approved | Approved-with-comments | Blocked>

Files reviewed: <count>
Blockers:       <count>
High:           <count>
Nits:           <count>

Report: .bequite/audits/REVIEW-<timestamp>.md

Next: /bq-fix <first-blocker>  (if Blocked)
      /bq-red-team             (if you want adversarial follow-up)
      /bq-verify               (if Approved)
```

## Rules

- **Be specific.** Quote the line, name the file. Vague "could be better" is useless.
- **Don't bike-shed.** If the project's existing code uses a convention, don't fight it.
- **Cite tests as evidence.** "There's no test for this branch" is a real finding.
- **Praise when warranted.** A short positive note builds trust + reduces friction.
- **No drive-by suggestions.** If you spot something unrelated to this diff, log it to OPEN_QUESTIONS.md or AGENT_LOG.md, don't add it to this review.

## Standardized command fields (alpha.6)

**Phase:** P3 — Quality and Review
**When NOT to use:** no uncommitted changes + no recent commits (nothing to review); whole-project audit needed (use `/bq-audit`).
**Preconditions:** `BEQUITE_INITIALIZED`; git repo with diff or recent commits
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:**
- `REVIEW-<timestamp>.md` written
- Per-file commentary with correctness / tests / security / style fields
- Verdict explicit: Approved / Approved-with-comments / Blocked
- Mistake-memory entries appended for repeat-pattern findings
- Marks `REVIEW_DONE ✅`
**Failure behavior:**
- No diff to review → exit with hint to run `/bq-implement` first
- New dep added in the diff without a decision section → BLOCKER (tool neutrality)
- Banned weasel word in commit message → flag as finding; don't auto-edit history
**Memory updates:** Sets `REVIEW_DONE ✅`. Appends repeat-pattern entries to `MISTAKE_MEMORY.md`.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- The current diff (via `git diff`, `git log`)
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/tasks/TASK_LIST.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `.bequite/audits/REVIEW-<timestamp>.md` (new)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- Approved → `/bq-verify`
- Approved-with-comments → fix nits then `/bq-verify`
- Blocked → `/bq-fix <issue-id>`
- Need a second opinion → `/bq-red-team`

---

## Mistake memory update

When a review surfaces a finding that's a **repeat of a previous fix** (same pattern, different file), append a MISTAKE_MEMORY entry:

- Note that this is the **second occurrence** of a pattern
- Update the existing entry's "How to detect next time" with the new detection signal (since the previous one missed this instance)
- Strengthen the prevention rule

If the review uncovers a **new** pattern worth remembering, add a fresh entry. Skip for one-off issues confined to a single file.

See `.bequite/state/MISTAKE_MEMORY.md` template.

---

## Tool neutrality (global rule)

⚠ **Reviews must flag any "use X" claim in the diff that lacks a decision section.**

When reviewing a diff that adds a new dependency, library, framework, or tool, check:

1. Is there a decision section in the plan, feature mini-spec, or PR description?
2. Does it answer the 10 decision questions?
3. Does it justify this tool over named alternatives?
4. Does it include a test plan + rollback plan?

If any answer is no → mark **Blocked** with a finding: "New dep `<name>` added without a decision section. Required: Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan."

The 10 decision questions every new tool must answer:
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

**Tool neutrality findings are a real BLOCKER category.** Treat them as such.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
