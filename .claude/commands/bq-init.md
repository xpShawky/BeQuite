---
description: Initialize BeQuite in this project. Makes sure the .bequite/ memory scaffold and the BeQuite section in CLAUDE.md exist (the script installer creates them; a plugin install gets them here), then writes the baseline state files. Use `bq-init new` for a brand-new empty folder.
---

# /bq-init: give the project its memory

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

The first command in a project. It never overwrites anything that exists: every step adds what is missing and leaves the rest alone.

## Syntax

```
/bq-init          an existing repo
/bq-init new      a brand-new, empty folder
```

## Gates

None needed. Sets `BEQUITE_INITIALIZED`.

## Steps

1. **Detect the state** with Read and Glob: manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` ...), `.git/`, `CLAUDE.md`, and whether `.bequite/` exists.
2. **The scaffold.**
   - Script install: `.bequite/` is already there (the installer copied it, baseline state files included), so the project is initialized. Go to step 3 to fill in what is known.
   - Plugin install, or `.bequite/` is missing: copy the scaffold from `${CLAUDE_PLUGIN_ROOT}/templates/bequite/` into `.bequite/`, file by file, skipping every file that already exists and replacing `{{VERSION}}` with the plugin's version (its `VERSION` file). If that folder is not readable either, stop and tell the user to run the installer from the README.
3. **Baseline state files.** The scaffold already carries them; write any that is still missing, and never replace one that exists:
   - `.bequite/state/PROJECT_STATE.md`: the date, the project name (the folder's), one line on what it is ("unknown until `/bq-discover`" for an existing repo), the stack if a manifest shows it.
   - `.bequite/state/CURRENT_MODE.md`: "Not selected" (set by `/bq-mode`).
   - `.bequite/state/CURRENT_PHASE.md`: "P0 Setup".
   - `.bequite/state/LAST_RUN.md`: this run.
   - `.bequite/state/DECISIONS.md`: a first entry, "BeQuite initialized", with the date.
   - `.bequite/state/OPEN_QUESTIONS.md`: empty, with its heading.
   - `.bequite/logs/AGENT_LOG.md`: append the first entry.
4. **`CLAUDE.md`.** If it has no `<!-- BEQUITE -->` block, add the block from `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.bequite.md` (script installs already have it): create the file if it is missing, otherwise append the block after a `---` line. Never rewrite the user's own sections. A plugin install also says in that block that commands are called `/bequite:<name>`.
5. **Git hygiene, ask first:** in a git repository, offer to add `.bequite/backups/` and `.bequite/state/UPDATE_CHECK.md` to `.gitignore`. Do not edit `.gitignore` without a yes.
6. **Mark `BEQUITE_INITIALIZED`** in `.bequite/state/WORKFLOW_GATES.md` and report.

## Output

```
BeQuite initialized (<script | plugin> install, v<version>)
Scaffold: <n> files added, <n> already there    CLAUDE.md: <created | block added | unchanged>
Next: /bq-discover (existing repo) or /bq-clarify (bq-init new)
```

## Quality gate

Nothing that existed was overwritten; every baseline state file exists; the gate is set; a second run changes nothing.

## Next Command Recommendations (typical)

Existing repo: `/bq-mode`, then `/bq-discover` and `/bq-doctor`. New project: `/bq-mode`, then `/bq-clarify`.
