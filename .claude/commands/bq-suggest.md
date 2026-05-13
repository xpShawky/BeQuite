---
description: BeQuite workflow advisor. Reads your situation + current state, then suggests the best commands, skills, gates, and mode (fast / deep / scoped auto / phase) for what you want to do. Does NOT implement — only recommends the route.
---

# /bq-suggest — workflow advisor

## Purpose

You have 39 commands and 15 skills. You may not know which to run. `/bq-suggest` is the BeQuite workflow expert that listens to your situation and **recommends a route**: which commands, in what order, with what skills, with which gates, and whether to use fast / deep / scoped auto / phase mode.

**Read-only. Never implements.** It tells you what to do; you decide whether to run it.

## When to use it

- Lost in the command catalog — "I don't know which to run"
- Multi-domain task — "I need UX + security + testing"
- Starting fresh and want a roadmap, not a single command
- Re-orienting mid-project: "what should I do now?"
- Comparing mode choices — "fast or deep or auto?"

## When NOT to use it

- Single obvious task (just run the command — e.g. `/bq-fix "..."` for a bug)
- You already know the workflow (just run it)
- Live status check — use `/bq-now`
- Gate-aware menu — use `/bequite`

## Syntax

```
/bq-suggest "<your situation, goals, or question>"
```

Examples:
- `/bq-suggest "I want to improve UI/UX and security"`
- `/bq-suggest "I have a broken frontend and API"`
- `/bq-suggest "I want to build a scraper and deploy it on VPS"`
- `/bq-suggest "I want to add a feature without restarting the whole workflow"`
- `/bq-suggest "I have a project idea and want to know where to start"`
- `/bq-suggest "I want fast mode only"`
- `/bq-suggest "I want deep mode with research and red-team"`
- `/bq-suggest "I need UX + backend + testing"`

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md` (if exists)
- `.bequite/audits/DISCOVERY_REPORT.md` (if exists)

**Note:** `/bq-suggest` does NOT do web research. It only reads BeQuite memory + the user's situation. If a recommendation requires web research, it points at `/bq-research` (the command that does live web research with WebFetch / Chrome MCP / Computer Use MCP per availability).

## Files to write

- `.bequite/state/LAST_RUN.md` (records suggestion)
- `.bequite/logs/AGENT_LOG.md` (entry)

## Steps

### 1. Read context + parse the user's situation

Load state files. Identify:
- Current phase (`P0`..`P5` or "not started")
- Current mode (one of 6 or "not selected")
- Last command run + outcome
- Pending gates
- Open questions

Parse the user's `"<situation>"` for:
- **Domains** mentioned (frontend, backend, database, auth, security, devops, scraping, UX, testing, deploy, etc.)
- **Task shape** (new project, fix, feature, audit, redesign, release, recover)
- **Mode preference** (fast / deep / scoped auto / phase / no preference)
- **Multi-domain signals** ("X + Y", "I need…and…")
- **Scope qualifier** ("the whole project", "just the dashboard", "one page", "the API")

### 2. Match to BeQuite surface (workflow advisor skill knowledge)

Use `bequite-workflow-advisor` skill to map user situation → recommended workflow.

Decision tree (high-level):

| Situation pattern | Recommendation |
|---|---|
| "Project idea, where to start?" | `/bq-new` or `/bq-auto new "..."` (full P0→P5) |
| "Existing project, what's broken?" | `/bq-existing` → `/bq-audit` → fix list |
| "I have a bug" | `/bq-fix "..."` (scoped) or `/bq-auto fix "..."` |
| "Add feature" | `/bq-feature "..."` or `/bq-auto feature "..."` |
| "Redesign UI" | `/bq-uiux-variants N` → user pick → `/bq-live-edit` for refinement |
| "UX issue in section X" | `/bq-live-edit "..."` direct |
| "Multi-domain X + Y" | scoped auto: `/bq-auto "X + Y audit and fix"` or sequential `/bq-audit` → focused fixes |
| "Spec Kit / one-page spec" | `/bq-spec "..."` |
| "Understand inherited code" | `/bq-explain "..."` |
| "Find work / job" | `/bq-job-finder` |
| "Find income opportunity" | `/bq-make-money` |
| "Pre-release verify" | `/bq-verify` → `/bq-release` |
| "Returning after break" | `/bq-recover` first; then `/bq-now` to confirm |
| "Where do I stand right now" | `/bq-now` (faster than `/bequite`) |
| "What should I do next" | `/bequite` for full menu |

### 3. Identify gate state

Check `WORKFLOW_GATES.md` for which gates are met (`✅`) and which are pending (`❌`).

If user wants something whose required gates are pending → surface that:

> "You want to run `/bq-implement`, but `PLAN_APPROVED` is pending. Run `/bq-plan` first."

### 4. Choose mode

Based on situation + gate state:

| Signal | Recommended mode |
|---|---|
| Small fix, trivial scope | `--mode fast` |
| Regulated / production / high-stakes | `--mode deep` |
| Long session / cost-sensitive | `--mode token-saver` |
| Multi-domain audit + fix | scoped auto (`/bq-auto "..."`) |
| Single phase end-to-end | phase orchestrator (`/bq-p0`..`/bq-p5`) |
| Full lifecycle new build | `/bq-auto new "..." --mode deep` |
| Just orientation | `/bq-now` or `/bequite` (no mode) |

### 5. Identify missing information

If the user's situation is too vague to suggest a route:

> "I need one more piece of info: is this an **existing project** (then start with `/bq-existing`) or a **new project** (then start with `/bq-new`)?"

Limit to **one** clarifying question. After answer → continue.

### 6. Produce the recommendation

Output format:

```
## Suggested route for: <user's situation, condensed>

### Recommended workflow (in order)

1. /bq-X     — <why this first>
2. /bq-Y     — <why this next>
3. /bq-Z     — <why this last>

### Skills that will be activated
- `bequite-<skill>` — <how it helps>
- `bequite-<skill>` — <how it helps>

### Mode recommendation
**<fast | deep | token-saver | (default)>** — <reasoning>

### Auto vs. scoped auto vs. phase vs. individual commands
- **Best fit:** <scoped-auto | individual commands | phase orchestrator | full auto>
- **Suggested single command:** `/bq-auto <intent> "..."` (if applicable)

### Required gates (must be ✅ first)
- <gate 1> — <how to satisfy>
- <gate 2> — <how to satisfy>

### Optional gates (skippable if you accept the trade-off)
- <gate> — <trade-off>

### Missing information (if any)
- <one question OR "none — ready to run">

### One recommended next command (start here)
`/bq-X "..."`

### Why NOT each alternative
- Why not `/bq-Y`? <one-line>
- Why not `/bq-auto`? <one-line>
```

### 7. Update state + log

- `LAST_RUN.md` ← "Suggested route for: <situation>"
- `AGENT_LOG.md` ← entry

## Output format

The structured recommendation above. Concise. Actionable.

## Quality gate

- Recommendation respects gate state (no recommending out-of-order commands)
- At least one specific command suggested
- Mode recommendation matches situation (fast for trivial; deep for high-stakes)
- "Why NOT each alternative" present (helps user understand the choice)
- No banned weasel words
- No more than one clarifying question

## Failure behavior

- User situation too vague → ask ONE clarifying question; then continue
- Multiple plausible workflows tie → present top 2 ranked; let user pick
- No commands match (extremely unusual goal) → say so; suggest `/bq-clarify` to surface what BeQuite actually offers

## Memory updates

- `LAST_RUN.md` ← suggestion summary
- (no other state changes — `/bq-suggest` is advisory)

## Log updates

- `AGENT_LOG.md` — entry

## Tool neutrality (global rule)

`/bq-suggest` recommends BeQuite commands and skills. The commands themselves respect tool neutrality (every named tool is a candidate). `/bq-suggest` shouldn't recommend external tools — only BeQuite's own surface.

If user asks about non-BeQuite workflows (e.g. "should I use Spec Kit or BeQuite?") — answer honestly: BeQuite has `/bq-spec` for Spec Kit-compatible specs; both can coexist; neither is mandatory.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Standardized command fields (alpha.8)

**Phase:** Any (advisory; read-only)
**When NOT to use:** single obvious task; gate-aware menu (use `/bequite`); one-line status (use `/bq-now`)
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:** recommendation cites specific commands; respects gate state; matches mode to situation; no banned weasel words
**Failure behavior:** vague situation → 1 clarifying question; tie → top 2 ranked
**Memory updates:** `LAST_RUN.md` (advisory note); no state mutation
**Log updates:** `AGENT_LOG.md`

## Usual next command

The command in the "One recommended next command" line of the output.
