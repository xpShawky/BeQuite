---
description: Environment health check - Node / Python / Docker / package managers / ports / scripts / env files / CI / hooks - and the capability inventory of this machine (.bequite/state/CAPABILITIES.md). Reports blockers and the next recommended command.
---

# /bq-doctor: can this machine build and run it, and what does it have

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Read-only probes. It never installs a tool and never opens `.env`. Safe to run at any time.

## Gates

Needs `BEQUITE_INITIALIZED`. Sets `DOCTOR_COMPLETE` (also when blockers were found: the report is the result).

## Steps

1. **Read** `.bequite/audits/DISCOVERY_REPORT.md` for the stack (run `/bq-discover` first if it is missing and the folder has code).
2. **Probe the tools the stack needs** with `command -v <tool>` (`where.exe` on Windows) and note each version: Node and its package manager, Python and pip, Rust, Go, Bun, Docker with a reachable daemon, Playwright when it is a dependency. Warn when a version is below what the project documents.
3. **Ports:** which ports the project uses and whether something already listens there.
4. **Env clarity:** which variables the code reads, whether an example file documents them. Names only.
5. **Scripts and README:** do the run, build and test scripts exist, and could a new person start the project from the README alone.
6. **CI:** which workflows exist and what they run.
7. **BeQuite hooks:** present (`.claude/hooks/`) and active (a `hooks` block in `.claude/settings.json` or `settings.local.json`, or the plugin). Not active: say "run `/bq-hooks status`". Never enable them here.
8. **Capability inventory** into `.bequite/state/CAPABILITIES.md`, so every plan's options board offers routes that can run on this machine:
   - **Detect, do not ask:** programs on PATH or in their usual folders (git, Python, Node, ffmpeg, yt-dlp, Whisper; After Effects, Premiere, Blender, DaVinci Resolve, Photoshop, Illustrator), browsers, the browser and computer-use tools this session has, the MCP servers connected. Each with its version or "found, version unknown".
   - **Ask once, then never again:** paid tools and subscriptions the user already has, accounts the work may use, and anything they do not want used. Names only: never a password, key or token.
   - Refresh it when the user says something changed, or a plan needs a capability the file does not list. In a public repository, ask before committing it.
9. **Write `.bequite/audits/DOCTOR_REPORT.md`:** each probe with a status (ok, warning, missing) and an install hint, then blockers, recommendations, and the next command.

## Output

```
Doctor: <n> ok, <n> warnings, <n> missing    blockers: <list or none>
Capabilities: .bequite/state/CAPABILITIES.md (<n> programs, <n> tools)
Report: .bequite/audits/DOCTOR_REPORT.md
Next: /bq-clarify
```

## Quality gate

Every probe has an explicit status; a probe that fails marks that one tool and the rest continue; nothing was installed; no secret was read or written.

## Next Command Recommendations (typical)

Blockers: fix the environment, then re-run. Clean: `/bq-clarify` or `/bq-plan`.
