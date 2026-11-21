# The operator: text your own computer (design and threat model)

Sources read 2026-11-21: Telegram Bot API 10.4 (core.telegram.org/bots/api, /faq), Claude Code docs (headless, remote-control, channels), NanoClaw security page. Code: `scripts/operator_bridge.py`; offline test: `scripts/test_operator_bridge.py`.

## Options board (show it to the user before building anything)

| Route | What the phone gets | Build | Needs | Where it falls short |
|---|---|---|---|---|
| **Remote Control** (`claude remote-control`) | the full session in the Claude app: chat, files, approvals with push | none | a claude.ai plan sign-in; machine on; a session process running | not Telegram; transcript stored on Anthropic servers while connected; no BeQuite approvals view |
| **Official Telegram channel** (`telegram@claude-plugins-official`, research preview) | messages pushed into a running session; replies back; tool-approval relay | install the plugin, BotFather token, pair | Bun, a session left open, plan sign-in | every allow-listed sender can approve tool use; preview flags may change; one long-lived session |
| **BeQuite bridge** (`operator_bridge.py`) | one headless run per message; read-only answers; proposals with Approve/Decline; `/shot`; `/team`, `/approve`, `/decline` for the command center; audit log | this script (standard library) | Python, a signed-in CLI, a bot the owner creates | needs `claude auth login` on the CLI; no streaming; one message at a time |

Recommend Remote Control when the user only wants to drive a session. Recommend the bridge when the user wants Telegram, the command-center approvals, and an audit on disk. Build nothing the user did not choose.

## How the bridge behaves

1. Long polling with `getUpdates` (no webhook, so no inbound port and no tunnel). `deleteWebhook` at start, because getUpdates does not work while a webhook is set. Offset = last `update_id` + 1.
2. **Allow-list.** Only private chats whose ID is in `BQ_TG_ALLOWED_CHATS`. Anyone else gets silence (no reply confirms the bot exists) and an audit line. An empty list refuses to start.
3. **Read-only first.** Each message runs `claude -p` with `Read,Glob,Grep,WebSearch,WebFetch`, `--permission-prompts none` and a JSON schema (`answer`, `needs_approval`, `proposed_action`, `send_file`). A run that would change anything must propose instead.
4. **Approval.** A proposal is sent with inline buttons; `callback_data` is `ok:<8 hex>` (under the 64-byte limit). The press must come from an allow-listed user in the same chat, within one hour, once. Approved: one run, resumed on the same session, with write tools and `acceptEdits`, told to do exactly the approved action. Declined: nothing runs.
5. **Screenshots.** `/shot` captures the primary screen (PowerShell + System.Drawing on Windows, `screencapture` on macOS, `import` on Linux) and uploads it with `sendPhoto` (10 MB limit). A run can return `send_file` (sent with `sendDocument`, 50 MB limit).
6. **Audit.** Append-only JSONL (`~/.bequite/operator-audit.jsonl`): refusals, messages, runs (exit, seconds, cost estimate), proposals, decisions, files sent, errors. The token is replaced by `<token>` in every line.
7. **Pace.** At most one message per second per chat (FAQ); long answers split at 4,000 characters (limit 4,096).

## Threat model

| Threat | Control |
|---|---|
| Someone finds the bot | allow-list by numeric chat ID; private chats only; silence to strangers |
| A stolen phone or a hijacked Telegram account | the attacker can read through the agent: keep `BQ_OP_WORKDIR` narrow (never the home folder); changes still need a button press, which the attacker can also press, so keep the bridge off when travelling; Telegram two-step verification on the owner's account (owner's action) |
| Prompt injection from a web page or a file the agent reads | read-only first run; a change must be proposed in words the owner reads before pressing Approve; the approved run is told to do only that action |
| The token leaks | the token lives only in the env file outside any repo; child processes get an environment without `*TOKEN*`, `*SECRET*`, `*API_KEY*`, `BQ_TG_*`; the audit log redacts it; if it leaks, revoke it in BotFather (`/revoke`) |
| A runaway run | `--max-turns 25`, optional `--max-budget-usd`, 30-minute timeout |
| Replay of an old button | each proposal is single-use, bound to one chat, and expires after one hour; a bridge restart forgets all pending proposals |

## Setup the owner does (the agent never does these)

1. In Telegram, message @BotFather: `/newbot`, a name, a username ending in `bot`. BotFather returns the token.
2. Create `~/.bequite/operator.env` (outside every repo) with `BQ_TG_TOKEN=...`, `BQ_TG_ALLOWED_CHATS=<your numeric id>`, `BQ_OP_WORKDIR=<one project folder>`, optionally `BQ_OP_TEAM=<team folder>`. Your numeric ID: send any message to the bot, then open the audit log: the first `refused` line shows your chat ID; add it and restart.
3. `claude auth login` once, so headless runs can authenticate.
4. `python operator_bridge.py --check` (calls getMe), then run it in a terminal you keep open.
