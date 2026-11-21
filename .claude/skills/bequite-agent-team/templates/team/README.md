# Team folder (BeQuite command center)

## Niche

<one line: topic, language, audience, platforms. The chief keeps only ideas that fit it.>

## Layout

| Path | What it holds | Who writes it |
|---|---|---|
| `roles/*.md` | one file per role, in subagent format (name, description, tools, model, prompt) | the owner |
| `board.md` | the generated board: tickets, approvals, budget | `heartbeat.py` only |
| `inbox/` | ideas and requests waiting for the chief | owner, analyst, Telegram bridge |
| `tickets/T-xxxx/` | `ticket.md` (state, history), `brief.md`, `draft.md`, `review.md`, `package.md` | roles, one file each |
| `approvals/` | what waits for the owner's yes | producer, `heartbeat.py` |
| `budget.json` | monthly token cap per role, warn at 80%, pause at 100% | `heartbeat.py`; the owner raises caps |
| `log/` | append-only `YYYY-MM-DD.jsonl`, analyses, raw run records | `heartbeat.py` |
| `metrics/`, `voice/`, `outbox/` | numbers from published pieces, the owner's writing DNA, approved packages | owner, analyst |

One heartbeat: `HEARTBEAT.md`. Everything here is local; no server, no database, no secret.
