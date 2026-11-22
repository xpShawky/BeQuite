---
name: bequite-orchestrator
description: Use at the start of any BeQuite command that has to choose a route (/bequite, /bq-suggest, /bq-auto, /bq-plan, /bq-discover, /bq-implement, /bq-review, /bq-verify, /bq-skill-audit), whenever two commands or skills both seem right, when the next step is unclear, when the user asks "which command" or "where do I start", or when nothing in the pack fits the task. Holds the map, the routing rules, the operating card every model follows, and the rule for when a subagent is worth its cost. Replaces the former workflow-advisor and frontier-reasoning-coach skills.
last_verified: 2026-11-21
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://www.anthropic.com/engineering/multi-agent-research-system
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/costs
---

# bequite-orchestrator: the map, the routes, the card

One skill that knows what BeQuite can do, so every route is chosen from the map and not from habit, and a gap is admitted instead of stretched over. It reads the catalogs at run time (`.bequite/state/ORCHESTRATION_MAP.md`, `templates/bequite/commands/COMMAND_ID_MAP.md` as installed in `.bequite/commands/`, `.bequite/skills/SKILL_REGISTRY.md`, the gates files) and never repeats their counts.

## When to use / when not

Use: at a decision point (which command, which skill, which mode, does a subagent pay, is this new work), on any conflict between commands, skills or routers, and when the request matches nothing.
Not: inside a step whose route is already fixed, or for read-only commands with fixed behaviour (`/bq-help`, `/bq-explain`). Do not re-derive the map on every message.

## The operating card (every model, strong or cheap)

1. Recover before acting: read the active work and what the session-start block points to; restate the goal and what "done" means.
2. Audit before adding: look for a command, skill or file that already does it; extend it instead of making a second source of truth.
3. Decompose into artifact-shaped tasks, about five files at most each, in dependency order.
4. Label claims verified, inferred or assumed; write `UNVERIFIED:` for gaps.
5. At real uncertainty ask one question with a default, or run a small spike; never promise through it.
6. At review, re-run the evidence yourself and look for drift: invented paths, stale counts, flat confidence, banned words.
7. If a rule would be broken, stop and fix before going on.

## Procedure

1. **Resolve the work.** `.bequite/ACTIVE.md`: does the request belong to the active work, or is it new work (`/bq-work new`)? Say which in one line.
2. **Route the situation** (one to five commands, never the full lifecycle for a small job):

| Situation | Route |
|---|---|
| a new idea or empty folder | `/bq-mode new` or `/bq-auto new` |
| an existing project | `/bq-discover`, then `/bq-doctor`, then `/bq-audit` |
| something is broken | `/bq-fix` |
| a feature | `/bq-feature` |
| a redesign / one section looks wrong | `/bq-uiux-variants` then `/bq-live-edit` / `/bq-live-edit` |
| back after a break | `/bq-recover` |
| ready to ship | `/bq-verify` then `/bq-release` |
| slides | `/bq-presentation` |
| a film, ad or reel | `/bq-motion`; website motion goes to `bequite-frontend-design-system` |
| content to post | `/bq-content`; a standing team: `/bq-team` |
| a video to understand | `/bq-watch`; a niche's winning format: `/bq-dna` |
| income / jobs / turning work into a product | `/bq-make-money` / `/bq-job-finder` / `/bq-productize` |

3. **Pick the mode.** Trivial or a spike: fast. Production, regulated, security or a new build: deep. Long or cost-sensitive: token-saver. A large feature with a clear shape: delegate (`bequite-delegation`). Conflicts: fast with deep asks one question and defaults to deep for new, security, release and deploy work; delegate on a tiny task is refused in favour of fast; delegate with no research composes with deep.
4. **Respect the gates.** Never recommend a command whose gate is open; name the prerequisite (`/bq-implement` needs `PLAN_APPROVED`, `/bq-release` needs `VERIFY_PASSED`). If the user insists, state the consequence.
5. **Prefer the lighter route.** Avoid the full lifecycle for a small fix, multi-plan for low stakes, red-team for a trivial change, deep mode for a prototype. Offer the heavier route as "if this is higher stakes than I assume".
6. **Resolve conflicts by boundary, not preference**: audit is not review; scope is not spec is not plan; verify is not release readiness; `/bq-content` makes a piece, `/bq-team` runs a standing team. Still ambiguous: one question.
7. **Admit a missing capability.** When nothing fits, write:

```
Missing capability: <what is needed>
Why existing commands/skills are not enough: <one line>
Workaround now: <safe or none>
Proposal: <skill / command / spec>, build now or park
```

Log it to `.bequite/state/OPEN_QUESTIONS.md`; go on only with a safe workaround. Never stretch a wrong command to fake coverage.

## When a subagent pays

- Allowed when the reading is wider than five sources, when a check must be independent of the builder, or when the output would flood the main context. Otherwise work inline.
- Effort scaling: one fact is inline (3 to 10 tool calls); a comparison of two to four options gets two to four readers; never more readers than distinct questions. Sweeps run on the fast model.
- The shipped subagents: `bq-researcher` (wide reading with cited findings), `bq-verifier` (re-runs the evidence), `bq-red-team` (attacks a plan or a diff), `bq-scout` (fast sweeps of trends and sources).

## Output of a recommendation

The route (commands in order), the skills each loads, the mode, the gates it needs, at most one missing piece of information, the next command, and one line on why not each main alternative.

## Worked example (2026-11-21, this repo)

Request: "check that BeQuite is the latest before every task, and set up my agent folder." Routed as two works: a pack change (installers + command contract, deep mode because it runs code from GitHub on users' machines; plan stated, then built and tested in a sandbox) and a workspace setup outside the repo (no command fits "set up a folder for my team" end to end: `/bq-team init` covers the team, the rest was done inline and logged). The team's first heartbeat was not run: the owner's gate.

## Quality gate

A route names the row, boundary or rule it used. "I picked X" with no cited rule is redone. "Done" means exercised the way a user would (the browser for UI, the real command for a CLI) with the evidence pasted.

## Boundaries

Writes nothing of its own except `OPEN_QUESTIONS.md` entries for missing capabilities and the routing line in the work log. Hard human gates (`CLAUDE.md`) are never routed around.
