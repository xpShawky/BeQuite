# Heartbeat drivers: the options board

Read on 2026-11-21 from the Claude Code docs (scheduled-tasks, desktop-scheduled-tasks, routines, headless, agent-teams) and measured on the owner's machine. Pick one per team and write the choice in the team `README.md`.

| Route | Reads the local team folder | Runs with the app closed | Idle cost | Needs | Verdict |
|---|---|---|---|---|---|
| **A. Desktop scheduled task** (`/bq-team schedule`) | yes | no: only while the app is open and the machine awake; a missed run fires once on wake | one short session per tick (the gate answers `NO_WORK`) | the desktop app; the task's permission mode set by the owner in the app | **default**: the only Claude-native scheduler that sees local files |
| **B. OS scheduler + `heartbeat.py run`** (Task Scheduler, cron, launchd) | yes | yes, while the machine is on | zero: the script gate exits before any model call | a signed-in CLI (`claude auth status` -> `loggedIn: true`) | best for frequent ticks once the CLI is signed in |
| **C. `/loop` or the Cron tools in an open session** | yes | no: dies with the session; recurring jobs expire after 7 days | none between ticks, but the session stays open | an open session | for a supervised afternoon, not for a standing team |
| **D. Cloud routine** | no: fresh clone of a repo, no local files | yes | per run | a GitHub repo holding the team folder; 1-hour minimum | only if the team folder lives in a repo and nothing private is in it; step 2 (VPS) is the better answer |
| **E. Agent teams** (experimental) | yes | no: interactive only, not `-p` | the lead and every teammate keep a context | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | a live "war room" for one big piece, not a heartbeat |

## Route A in practice (measured 2026-11-21)

- `create_scheduled_task` with no cron and no fireAt makes a manual-only task, stored at `~/.claude/scheduled-tasks/<id>/SKILL.md`.
- A task created from a session does not inherit that session's permission mode. Its first run waited on the first Bash prompt (started 17:56:53Z, idle after 17:56:59Z). The owner must open the task in the app once, choose its permission mode, and click **Run now** to pre-approve `Bash(python ...heartbeat.py*)`, Write and the web tools. Approvals given during a run are stored on the task.
- The run starts on the app's default model. The dispatcher's own work is tiny (run the script, start a subagent, record); the roles carry their own `model`, so the expensive part follows the role files, not the dispatcher. `UNVERIFIED:` whether a task can be pinned to a cheaper model.
- Cadence: Paperclip's examples run every 4 hours; OpenClaw's default check is every 30 minutes. For a content team, 2 to 3 ticks a day (`0 9,15,21 * * *`) is enough: each tick can carry a ticket through the whole pipeline.

## Route B command

```
python <skill>/scripts/heartbeat.py run --team <team> --max-jobs 8
```

Each job runs `claude -p` with the role's prompt, `--model` from the role file, `--allowedTools` from its `tools`, `--permission-mode acceptEdits`, `--max-turns 30`, `--output-format json`, cwd = the team folder, and an environment with every token-like variable removed. Tokens and `total_cost_usd` (an estimate on a subscription) go to `budget.json` and `log/runs/`.

## Agent-teams hook (option, `UNVERIFIED:` not run with teams enabled)

In a war-room session, a `TaskCompleted` hook can refuse to close a task named `publish:*` unless `approvals/` holds an approved file for it: exit 2 with the reason on stderr keeps the task open (hooks reference, TaskCompleted).
