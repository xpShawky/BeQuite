---
description: Inspect the repo before planning. Writes .bequite/audits/DISCOVERY_REPORT.md (stack, apps, entry points, commands, ports, docs, tests, CI, risks, missing information) and the project's conventions to .bequite/state/PROJECT_DNA.md.
---

# /bq-discover: know what this is before planning

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Read-only. Discovery exists to make later context smaller: later commands read its report instead of walking the tree again. Skills: `bequite-context-engineer`, `bequite-project-architect` (stack signals), `bequite-security-reviewer` when auth or secrets appear.

## Gates

Needs `BEQUITE_INITIALIZED`. Sets `DISCOVERY_COMPLETE`. An empty folder has nothing to discover: use `/bq-new`.

## Steps

1. **Scan** with Read, Glob and Grep only (no shell commands, no code changes):
   - manifests, lockfiles and package managers, with exact versions ("Next.js 15.5.18", not "a React app");
   - code structure: apps, packages, entry points, routes, layers;
   - infrastructure: Docker, CI workflows, deploy config, migrations;
   - configuration: env files by name only. Never read `.env*` or any file named like a secret or key; note that it exists.
   - documentation: README, docs folders, ADRs, how current they look.
2. **Runtime and commands:** the run, build, test and lint commands as the manifest defines them; the ports and URLs the code names.
3. **Tests:** frameworks, where tests live, roughly what they cover.
4. **Risk surface:** missing or stale README; `.env` referenced with no example file; no tests or CI; many TODO or FIXME marks (count them); pre-1.0 dependencies; committed `node_modules`; secret-looking strings in source (never print the value); a missing lockfile or more than one.
5. **Conventions into `.bequite/state/PROJECT_DNA.md`:** how this codebase names things, handles errors, layers code and which way dependencies point, how tests are written, and exemplar files ("when adding X, follow `<file>`"). New code is judged against it later.
6. **Write `.bequite/audits/DISCOVERY_REPORT.md`:** project shape, apps detected, package managers, commands, ports, documentation, tests, CI, infrastructure, risks, missing information (questions for `/bq-clarify`), an architecture guess labelled as a guess, and a ranked "read these first" list (files the work will touch, their callers, covering tests, exemplars).
7. **Stamp it:** the commit hash and date at the top of both files. A stale map is worse than none; refresh after large changes.

## Output

```
Discovery: <project shape in one line>    stack: <versions>
Risks: <n>   Missing information: <n>
Report: .bequite/audits/DISCOVERY_REPORT.md   Conventions: .bequite/state/PROJECT_DNA.md
Next: /bq-doctor
```

## Quality gate

Every report section is filled or says "unknown"; versions are exact; nothing was read from a secret file; a file that could not be read is noted and skipped, not fatal. If the domain needs expertise BeQuite has no skill for, the report says so.

## Next Command Recommendations (typical)

`/bq-doctor` · `/bq-clarify` when questions remain · `/bq-audit` when discovery flagged risks.
