---
description: BeQuite workflow advisor. Reads your situation + current state, then suggests the best commands, skills, gates, and mode (fast / deep / scoped auto / phase) for what you want to do. Does NOT implement — only recommends the route.
---

# /bq-suggest: which command, which mode, in what order

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Advisory and read-only: it recommends a route and changes nothing. The routing knowledge lives in `bequite-orchestrator` (the map, the routing table, the rule for when a subagent pays); the routes and IDs are in `.bequite/commands/COMMAND_ROUTER.md` and `COMMAND_ID_MAP.md`.

## Syntax

```
/bq-suggest "<your situation, goal or question>"
```

Examples: "I have a broken frontend and API" · "add a feature without restarting the whole workflow" · "I have a project idea, where do I start" · "a PowerPoint about infection control for doctors" · "a reel about my product" · "how can I earn from this skill".

For a single obvious task just run its command; for the gate-aware menu use `/bequite`.

## Gates

Needs `BEQUITE_INITIALIZED`.

## Steps

1. **Read the state:** `PROJECT_STATE.md`, `CURRENT_MODE.md`, `CURRENT_PHASE.md`, `WORKFLOW_GATES.md`, `ACTIVE.md` and the active work's `gates.md`, `LAST_RUN.md`, `.bequite/state/PACKS.md` (which packs are installed), `CAPABILITIES.md`.
2. **Parse the situation** into domains and outputs (code, a page, a film, a deck, a post, an offer, research only) and match it to routes with the orchestrator's table. Signals worth knowing:
   - writing in someone's voice, academic or brand writing: `/bq-writing-dna` (never framed as evading AI detectors);
   - a film, reel, promo or kinetic type: `/bq-motion`; slides: `/bq-presentation`; a post from trend to package: `/bq-content`; understanding a video: `/bq-watch` (studio pack);
   - earning, jobs, offers, proposals: `/bq-make-money`, `/bq-job-finder`, `/bq-offer` (business pack);
   - "what are the risks", "how confident": the plan's confidence and risk check, or `/bq-red-team`.
   A route that needs a pack that is not installed says which pack to add.
3. **Check the gates** the route needs. Never recommend a command whose required gate is open; recommend the command that closes it first.
4. **Choose the mode** and say why: `fast` for small, trusted, reversible work; `deep` for new builds, regulated or high-stakes work; `token-saver` for long sessions with cached research; `delegate` for a large feature with a clear shape; and whether `/bq-auto` fits or the phase commands by hand are better.
5. **Ask at most one question**, only if the answer changes the route.
6. **Recommend:**

```
Suggested route for: <the situation, condensed>
Required next:   <command> <args>    (<reason>; skills: <...>)
Then:            <2 to 6 commands in order, each with its reason>
Mode:            <fast | balanced | deep | token-saver | delegate>, because <...>
Auto or manual:  <the exact /bq-auto line, or why by hand>
Gates:           <open gates that block, and what closes each>
Do not run yet:  <command> (<why>)
Why not the alternatives: <one line each>
```

7. **No route fits:** never force a fit. Say so in this shape and log it to `OPEN_QUESTIONS.md`:

```
Missing capability: <what is needed>
Why the existing commands and skills are not enough: <...>
Workaround for now: <...>
Worth building (`/bq-forge`) or parking: <...>
```

## Quality gate

Every recommendation respects the gates; at least one specific command with its arguments; the mode fits the stakes; the alternatives are explained; no weasel words.

## Next Command Recommendations (typical)

The "Required next" line of the route. The choice is appended to `.bequite/commands/NEXT_COMMAND_LOG.md`.
