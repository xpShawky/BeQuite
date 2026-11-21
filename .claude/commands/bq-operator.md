---
description: Text your own computer from Telegram. Sets up and runs a local bridge - an allow-listed bot that turns each message into a read-only headless Claude run, sends changes back as Approve/Decline proposals, returns screenshots, decides command-center approvals, and keeps an audit log. Modes - options, setup, check, start, audit.
---

# /bq-operator: your computer, from your phone

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` (hourly; it updates BeQuite when a newer version is published, backs up first, never touches `.bequite/` memory, never blocks) and say its one line.
> 2. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 3. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 4. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 5. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 6. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 7. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 8. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

Skill: `bequite-agent-team` (`references/operator.md` holds the design and threat model). Bridge: `<skill>/scripts/operator_bridge.py`, Python standard library only, no package to install.

## Modes (`$ARGUMENTS`)

| Mode | Does |
|---|---|
| `options` (default) | shows the options board from `references/operator.md`: Remote Control, the official Telegram channel plugin, the BeQuite bridge; what each needs on this machine (checks `claude auth status`, `bun --version`, `python --version`); recommends one with a reason |
| `setup` | walks the user through the steps only they can do (below), then writes the env file template with every value except the token, outside any repo |
| `check` | `python operator_bridge.py --env <file> --check`: validates the config, calls `getMe`, prints the bot name and the allow-list size. Never prints the token |
| `start` | prints the command to run the bridge in a terminal the user keeps open (the agent does not keep a background process alive between sessions) |
| `audit [n]` | shows the last n lines of the audit log (default 20): refusals, runs, proposals, decisions |

## What only the user does (stop and ask; never do these for them)

1. Create the bot: Telegram -> @BotFather -> `/newbot` -> name -> username ending in `bot`. BotFather returns the token.
2. Paste the token into the env file themselves (`BQ_TG_TOKEN=`). The token never goes in chat, in git, in a command line, or in a log.
3. Sign in the CLI once: `claude auth login`. Headless runs fail without it (measured: "OAuth session expired" while `loggedIn: false`).
4. Find their numeric chat ID: message the bot once with the bridge running; the audit log's first `refused` line shows it. Add it to `BQ_TG_ALLOWED_CHATS`, restart.
5. Turn on Telegram two-step verification for their own account (recommended).

## Env file (`~/.bequite/operator.env`, outside every repo)

```
BQ_TG_TOKEN=            # the user pastes it; never the agent
BQ_TG_ALLOWED_CHATS=    # numeric chat IDs, comma-separated
BQ_OP_WORKDIR=          # ONE project folder, never the home folder
BQ_OP_TEAM=             # optional: the /bq-team folder, for /team, /approve, /decline
BQ_OP_MAX_BUDGET_USD=   # optional cap per run
```

## Rules the bridge enforces

- Allow-listed private chats only; silence and an audit line for anyone else; an empty allow-list refuses to start.
- Every message runs read-only. Anything that changes the machine or the outside world comes back as a proposal with Approve / Decline; an approved proposal runs once, within an hour, from the same chat.
- Child processes never receive token-like environment variables; the audit log redacts the token.
- Publishing from the command center still goes through `approvals/` and the publish step; the bridge only lets the owner press the button from the phone.

## Gates

Hard human gates (CLAUDE.md): secret handling (the token is the user's), creating accounts or bots (the user's), and any outward action the bridge proposes. In auto mode the agent stops at `setup` step 1 and waits.

## Evidence

`check` output and one round trip (a question, a proposal approved from the phone, a `/shot`) go to the work's `evidence.md` with the audit lines that prove them. The offline test (`python -I .claude/skills/bequite-agent-team/scripts/test_operator_bridge.py`, a mock Bot API on 127.0.0.1) is the check before any change to the bridge.
