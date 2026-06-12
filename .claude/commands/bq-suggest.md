---
description: BeQuite workflow advisor. Reads your situation + current state, then suggests the best commands, skills, gates, and mode (fast / deep / scoped auto / phase) for what you want to do. Does NOT implement — only recommends the route.
---

# /bq-suggest — workflow advisor

## Purpose

You have 52 active commands and 29 skills. You may not know which to run. `/bq-suggest` is the BeQuite workflow expert that listens to your situation and **recommends a route**: which commands, in what order, with what skills, with which gates, and whether to use fast / deep / scoped auto / phase mode.

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
- `/bq-suggest "Build a PowerPoint about infection control for doctors"`
- `/bq-suggest "Turn this Word file into a lecture"`
- `/bq-suggest "Cinematic keynote deck from a topic"`

### Writing keyword triggers (alpha.19)

If the user mentions any of: **write in my style / my voice / brand voice / sound human / not generic / rewrite this / academic writing / discussion section / methodology / blog post / YouTube script / email copy / product copy / lecture notes / writing profile** — recommend `/bq-writing-dna`.

Guidance to surface: samples → real profile (3+ samples) vs provisional; `strict=true` for academic/source-bound work (zero invented citations); the profile is reusable across pieces. Never frame as AI-detector evasion — if asked for that, explain the ethical line and offer quality/voice/fidelity help instead.

### Confidence + rigor triggers (alpha.21)

"How likely is this to work / what are the risks / how confident are you" → point at the Confidence Forecast in `/bq-plan`/`/bq-assign` output. "Maximum rigor / professional-grade / regulated review" → recommend the `expert` composition (`/bq-auto expert "..."` = deep + strict evidence + safety scope + domain checklist — an alias, not a 5th mode). "Make a cheaper model do this safely" → delegate mode; the task pack embeds the frontier 10-rule card automatically.

### Skill-maintenance trigger (alpha.19)

"Skills feel stale / a skill misfired / clean up the pack" → `/bq-skill-audit` (report-only first).

### Presentation keyword triggers (alpha.13)

If the user mentions any of: **slides, presentation, lecture, PowerPoint, PPTX, keynote, course lesson, screen recording, explain this topic visually, make a deck, convert PDF to slides, make lecture from Word file** — recommend `/bq-presentation`.

Format-pick guidance to surface:
- **PPTX** — editable in PowerPoint / lecture / institutional / offline / speaker recording / Office users
- **HTML** — cinematic motion / responsive / browser delivery / product demo / interactive
- **Both** — same content, two rendering strengths

Strict-vs-creative:
- **strict=true** — Word / PDF / scientific / institutional material → preserve source; no unsupported claims
- **creative=true** — topic-only / keynote / marketing deck → may add hooks + structure (assumptions marked)

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
| "Frontend is inconsistent / middle sections look weak / design drifted / hero good but body generic" | lock `DESIGN_DNA.md` → `/bq-audit` (full continuity sweep) → `/bq-fix`/`/bq-live-edit` per finding → `/bq-verify` (continuity + visual QA). Skill: `bequite-frontend-design-system`. (alpha.17) |
| "Build a frontend that stays consistent top-to-bottom" | `/bq-auto frontend "..."` (deep) — runs Design DNA → section-by-section loop → continuity gate → visual QA |
| "Make the agent more reliable / stop it skipping safety rules / set up guardrails" | review + enable the opt-in hooks (`.claude/settings*.json.example`); lock `PROJECT_DNA.md`; lean on `bequite-context-engineer` + `bequite-anti-hallucination`. Docs: `CLAUDE_CODE_HOOKS_STRATEGY.md`. (alpha.18) |
| "Agent keeps forgetting / repeating mistakes / losing the plan" | `bequite-context-engineer` (PROJECT_DNA + WORKING_NOTES + compact/clear/externalize); read `docs/architecture/CONTEXT_ENGINEERING.md`. (alpha.18) |
| "Multi-domain X + Y" | scoped auto: `/bq-auto "X + Y audit and fix"` or sequential `/bq-audit` → focused fixes |
| "Spec Kit / one-page spec" | `/bq-spec "..."` |
| "Understand inherited code" | `/bq-explain "..."` |
| "Find work / job" | `/bq-job-finder` |
| "Find income opportunity" | `/bq-make-money` |
| "Create a presentation / slides / lecture / deck / keynote" | `/bq-presentation` |
| "Turn this PDF / Word into slides" | `/bq-presentation strict=true source=<file>` |
| "PowerPoint about X" | `/bq-presentation format=pptx` |
| "Cinematic browser slides" | `/bq-presentation format=html` |
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

---

## Automatic skill routing (alpha.20)

This command runs the Skill Router BEFORE acting (execution-contract steps 2–4):

1. Load `.bequite/skills/SKILL_REGISTRY.md` (the token-cheap routing index — NOT the skill files)
2. Classify the task into domains per `.bequite/skills/SKILL_ROUTER.md` (user text → command → files present → mode/phase → memory → risk tier → output type)
3. Auto-select skills: domain primaries + cross-cutting auto-attach (anti-hallucination on claims · testing-gate on code · context-engineer on >5 files or >1 session · security-reviewer on R3 paths · frontend-design-system on >1 UI section) + mode sizing (fast = smallest safe set · deep = broader · token-saver = lazy-load · delegate = skills named in task pack)
4. Emit the selection block in the output, then load ONLY the selected SKILL.md files:

```
Skill Selection:
- Selected: bequite-<skill> — <one-line reason tied to this task>
- Not selected: bequite-<skill> — <why considered and skipped>
```

**The user never has to name skills** — describe the goal; the router picks the disciplines. An explicit user skill choice overrides routing (log the override). At writeback, append the selection + outcome to `.bequite/skills/SKILL_USAGE_LOG.md`.

Strategy: `docs/architecture/AUTO_SKILL_ROUTING_STRATEGY.md`.

## Main navigation assistant (alpha.22 — Command Router front-end)

`/bq-suggest` is the interactive front-end of the Workflow Command Router (`docs/architecture/WORKFLOW_COMMAND_ROUTER.md`; routes in `.bequite/commands/COMMAND_ROUTER.md`; IDs in `COMMAND_ID_MAP.md`). Every answer now includes ALL of:

1. **Next workflow command** (catalog ID + reason)
2. **Relevant capability commands** (C# — only when task signals justify them)
3. **Selected skills** (via the Skill Router — commands answer *what next*, skills answer *how well*; never confuse the two)
4. **Confidence forecast** for the recommended route
5. **Manual vs auto advice** (and the exact `/bq-auto` invocation if auto fits)
6. **Gate status** — anything blocking, and the prerequisite command that unblocks it

Output uses the multi-command format: Required next · Recommended command set (2–6, each with args + reason + skills + can-auto-run) · Optional accelerators · Do not run yet (+ why). Decisions append to `.bequite/commands/NEXT_COMMAND_LOG.md`.

### Worked journey routes

**"I want to create a course"** → 1. C5 `/bq-course` (validation + curriculum first) · 2. C4 `/bq-knowledge build` if source docs exist · 3. C1 `/bq-presentation` when slides needed · 4. C2 `/bq-writing-dna` for scripts/narration · 5. localization-rtl skill if Arabic/MENA. Skills: researcher, writing-dna, presentation-builder (+anti-hallucination if academic).

**"I want to make money from a niche"** → 1. C6 `/bq-pain-radar` (verified pain first) · 2. C10 `/bq-make-money` (match to earning tracks) · 3. **C11 `/bq-offer`** (package the standing product) · 4. C8 `/bq-proposal` (pitch it per-client) · 5. C5 `/bq-course` only if an education product is viable · 6. W4.2 `/bq-release proof` once something ships. Explain the order: evidence → opportunity → offer → pitch → proof.

**"I want this app to integrate with an API"** → 1. C7 `/bq-integrate` (blueprint) · 2. W1.4 `/bq-plan` · 3. W2.3 `/bq-feature` · 4. W3.1 `/bq-test from-spec` · 5. W4.1 `/bq-verify`. Skills: backend-architect, security-reviewer, testing-gate.

**"I like this website style"** → 1. C3 `/bq-reference screenshot|url` (extraction + originality guardrails) · 2. W2.5 `/bq-uiux-variants` if multiple directions · 3. W2.3 `/bq-feature` once approved · 4. W4.1 `/bq-verify` (visual QA) · 5. W4.2 `/bq-release proof` for a case study. Skills: frontend-design-system, ux-ui-designer, frontend-quality.

## Orchestrator + missing-capability detection (alpha.22 orchestration update)

`/bq-suggest` consults the global brain first: `bequite-orchestrator` skill + `.bequite/state/ORCHESTRATION_MAP.md` (source of truth on conflict/confusion/duplication). When NO existing command/skill/workflow fits the request, never force a fit — emit:

```
Missing Capability Detected:
- Needed capability:
- Why existing commands/skills are not enough:
- Temporary workaround:
- Recommended new skill/command/spec:
- Should this be built now or parked?
- Confidence:
```

…and log it to OPEN_QUESTIONS / FEATURE_EXPANSION_ROADMAP (feature-workflow step 1).

## Remaining-work queries (canonical source rule)

When the user asks any form of: *what remains? / what is left? / what should we do next? / what version is next? / what is parked? / what is alpha.23? / what is V2? / what is built but untested?* — READ `.bequite/tasks/REMAINING_WORK_MASTER.md` (sections A–G) and answer from it. Do not answer from memory alone; if the file is missing, say so and offer to rebuild it from the trackers.
