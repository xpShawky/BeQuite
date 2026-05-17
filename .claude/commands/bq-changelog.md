---
description: Update CHANGELOG.md with a new entry. Reads recent commits + open feature specs. Categorizes Added / Changed / Fixed / Deprecated / Removed / Security.
---

# /bq-changelog — update CHANGELOG.md

You are keeping the project's CHANGELOG sharp. Format: Keep a Changelog v1.1.0 + Semantic Versioning.

## Step 1 — Detect the existing CHANGELOG

Look for (in order):
1. `CHANGELOG.md` at repo root
2. `.bequite/logs/CHANGELOG.md` (BeQuite's project changelog)
3. `docs/CHANGELOG.md`

If none exists, create one at repo root with the standard header:

```markdown
# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is [Semantic Versioning](https://semver.org/).

## [Unreleased]

(no entries yet)
```

## Step 2 — Get the new entries

The user may have invoked this directly OR as part of `/bq-release`. Either way:

- Read all unreleased changes: `git log <last-tag>..HEAD --oneline`
- Read recently-added feature specs: `.bequite/plans/feature-*.md`
- Read `ERROR_LOG.md` (recent fixes)
- Read `DECISIONS.md` (recent decisions affecting users)

## Step 3 — Categorize each entry

| Category | Use for |
|---|---|
| **Added** | New features, new commands, new endpoints |
| **Changed** | Behavior changes that aren't breaking |
| **Deprecated** | Features still working but marked for removal |
| **Removed** | Features that no longer exist |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability patches (CVE if applicable) |

For each entry, write **one line** describing what changed from the user's perspective. Not from the developer's. "Renamed lib/x.ts → lib/y.ts" is not a changelog entry; "Renamed CLI command `--old` to `--new`" is.

## Step 4 — Write or update the entry

If called standalone (not from `/bq-release`): append to `## [Unreleased]` section.

If called from `/bq-release`: move `[Unreleased]` content under a new `## [<version>] — <date>` heading + recreate empty `[Unreleased]`.

Template:

```markdown
## [Unreleased]

(or)

## [1.3.0] — 2026-05-15

### Added
- New `/bq-multi-plan` slash command (manual-paste multi-model planning, ToS-clean).
- Studio dashboard now shows real recent receipts in the AgentPanel.

### Changed
- `/bq-doctor` now also probes Node, Bun, Docker, and ports 3000-3002.
- `bequite-frontend-quality` skill expanded with the 15 AI-slop patterns from Impeccable.

### Fixed
- Marketing site Hero star particles no longer sit static (the `@keyframes glint` was missing).
- Dashboard `BEQUITE_DASHBOARD_MODE` env var is now read on every request (was cached at build time).

### Security
- (none this release)

### Deprecated
- (none)

### Removed
- (none)
```

## Step 5 — Verify the entry

Read the entry. Does each line:
- Describe the change from the USER'S perspective?
- Use past tense? ("Added support for X" not "Adding support")
- Not contain banned weasel words? (no "should", "probably", "seems to")
- Cite a spec file or PR if applicable?

If yes, you're done. If no, rewrite.

## Step 6 — Update state + log

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Step 7 — Report back

```
✓ CHANGELOG updated

Entries added: <count>
Section:       <Unreleased | <version>>

CHANGELOG: <path>

Next: /bq-release  (if you were prepping a release)
      back to /bq-implement (if you were mid-development)
```

## Rules

- **User-facing language.** "Bumped `eslint` from 9.13 to 9.14" is rarely a CHANGELOG entry. "Updated lint rules" is, IF the user sees the difference.
- **Keep a Changelog v1.1.0 categories** — Added / Changed / Deprecated / Removed / Fixed / Security. Don't invent new ones.
- **Date in ISO 8601** (`YYYY-MM-DD`).
- **Version in semver** (`MAJOR.MINOR.PATCH`).
- **Link compare URLs at the bottom** (`[1.3.0]: https://github.com/.../compare/v1.2.0...v1.3.0`) if the project uses GitHub.

## Standardized command fields (alpha.6)

**Phase:** P4 — Release
**When NOT to use:** no commits since last CHANGELOG entry; cosmetic-only commits (typos, comment fixes) with no user impact.
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:**
- Commits since last tag categorized per Keep a Changelog v1.1
- Sections: Added / Changed / Deprecated / Removed / Fixed / Security (each present if applicable)
- Entries are user-visible (no "Refactored lib/csv.ts" — that's internal)
- No banned weasel words in entries
- Marks `CHANGELOG_READY ✅`
**Failure behavior:**
- Commits have weak messages → suggest user re-message via `git commit --amend` (don't auto-edit)
- Breaking change detected but not in CHANGELOG under `### Removed` / `### Changed` → flag as quality issue
**Memory updates:** Sets `CHANGELOG_READY ✅`. Updates `CHANGELOG.md`.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- `CHANGELOG.md` (or wherever it lives)
- `git log <last-tag>..HEAD`
- `.bequite/plans/feature-*.md`
- `.bequite/logs/ERROR_LOG.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `CHANGELOG.md` (or wherever it lives — updated)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- `/bq-release` (if you were prepping a release)
- `/bq-implement` (if you were mid-development and just wanted to keep CHANGELOG current)

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
