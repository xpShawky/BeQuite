---
description: Generate a handoff package so a second engineer or a non-technical owner can pick the project up cold. Writes HANDOFF.md at the repo root with an engineer section, a plain-language section and a receiver's checklist. Arguments - client (a client-facing bundle), workflow-export (a secret-safe playbook of the workflow).
---

# /bq-handoff: someone else can run this tomorrow

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Built only from what is written down: `.bequite/` memory, the work folders, the repo. A fact that lives only in someone's head is asked for and recorded before the handoff is written. Skills: `bequite-context-engineer`, `bequite-security-reviewer` (the secret scan).

## Syntax

```
/bq-handoff [client | workflow-export]
```

- `client`: a bundle for a client: runbooks, a credential checklist with names, where each lives and who rotates it (never a value), a maintenance calendar, the warranty and support terms, and "what you own now" in plain language.
- `workflow-export`: the workflow as a reusable playbook and prompt pack in `.bequite/exports/` (spec: `.claude/bequite/docs/specs/WORKFLOW_EXPORT.md`).

A solo project with nobody to hand to: `/bq-memory snapshot` gives the same information with less ceremony.

## Gates

Needs `BEQUITE_INITIALIZED`. Sets `HANDOFF_GENERATED`. Any secret value in the draft is a hard stop: remove it, tell the user, and have them review before anything is shared.

## Steps

1. **Read everything recorded:** `PROJECT_STATE.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `MISTAKE_MEMORY.md`, the discovery and doctor reports, the active and archived work folders (`plan.md`, `verify.md`, `log.md`), the README and the changelog. If discovery is missing, run `/bq-discover` first; no partial handoff.
2. **Write `HANDOFF.md` at the repo root:**
   - **For engineers:** a five-line summary, quickstart (the exact commands), stack with versions, architecture, repository layout, key decisions and why, what is done, what is open, known issues, common operations, the release runbook, troubleshooting, who to ask.
   - **For non-engineers:** what the product does, who uses it, what works today, what comes next, what it costs to run, who to call when something breaks.
   - **Receiver's checklist:** yes-or-no items the receiver confirms (it installs, it runs, the tests pass, the env variables are documented, access was granted).
   - Each fact names where it came from ("Stack: Next.js 15, from the discovery report").
3. **Secret and privacy scan** over the draft and any export: keys, tokens, env values, personal or client data, internal paths. Env variables appear by name only.
4. **Report**, with the items the receiver must still get from the owner in person (credentials, access).

## Output

```
Handoff: HANDOFF.md (<n> sections, checklist of <n>)    secret scan: clean | <n> removed
Still needed from the owner: <list or none>
```

## Quality gate

Both audiences are served; the checklist is concrete; nothing is stated that memory or the repo does not support; no secret value anywhere.

## Next Command Recommendations (typical)

The receiver starts with `/bq-recover` or `/bequite`. Before a release handoff: `/bq-verify`.
