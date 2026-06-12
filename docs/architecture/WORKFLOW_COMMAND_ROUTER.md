# Workflow Command Router / Next Command Advisor (alpha.22)

**The second routing layer.** The Skill Router (alpha.20) answers *"which expert procedures should BeQuite use?"* The **Command Router** answers *"which command or workflow step should happen next?"* Never confuse the two: commands = what happens next; skills = how it's done well.

Operational map: `.bequite/commands/COMMAND_ROUTER.md` · ID vocabulary: `.bequite/commands/COMMAND_ID_MAP.md` · decisions logged to `.bequite/commands/NEXT_COMMAND_LOG.md`.

---

## 1. Where it runs

Works in **all** contexts: manual + auto mode; deep / fast / token-saver / delegate / `expert` alias; feature, fix, new-project, existing-project, content/presentation/course, monetization, frontend, and release work. Mode changes verbosity, never correctness: fast/token-saver emit Required-next + a 1–3 item set; deep adds accelerators and do-not-run-yet reasoning.

## 2. Routing inputs (in order)

1. `WORKFLOW_GATES.md` — what's unlocked (a blocked command is never recommended as runnable; it appears under "do not run yet" with its missing gate)
2. `CURRENT_MODE.md` + `CURRENT_PHASE.md` — workflow position
3. The just-finished command's outcome (PASS/FAIL changes the route: failed verify → W2.4 fix, not W4.2 release)
4. Task signals (frontend? course? API? monetization? Arabic/RTL?) → capability suggestions
5. `MODE_HISTORY.md` + `NEXT_COMMAND_LOG.md` — user patterns, accepted/ignored advice

## 3. Output contract — Next Command Recommendations

Every **non-trivial** command (trivial = `/bq-now`, `/bq-explain`, `/bq-help` reads) ends with this block (contract step 12):

```
Next Command Recommendations:

Required next:
- <ID> <command> — <reason> — can auto-run: yes/no — <why>

Recommended command set (2–6):
1. <ID> <command> <suggested args>
   Reason: … | Skills likely used: … | Can auto-run: yes/no
2. …

Optional accelerators:
- <command> — <why it may help now>

Do not run yet:
- <command> — <why premature/risky (missing gate, missing artifact, wrong order)>
```

Rules: **Required next** is exactly one (or "none — pause for user" at a hard gate). The set has 2–6 entries ordered by value. Capability commands (C#) appear **only when task signals justify them** — never pad the list. Every entry shows the ID so users learn the catalog passively.

## 4. Auto-mode behavior

Auto mode does **not** literally invoke slash commands — it runs the equivalent internal workflow, then reports the steps in catalog vocabulary:

```
Internal workflow executed:
- W0.3 /bq-discover
- W1.2 /bq-research (3 dims, fast mode)
- W1.4 /bq-plan
- W2.2 /bq-implement (4 tasks)
- W4.1 /bq-verify — PASS
```

At the end, auto mode emits the same Next Command Recommendations block for whatever follows the run. Hard human gates (all 17) interrupt routing exactly as before — the router never bypasses a gate, it routes *around* nothing.

## 5. `/bq-suggest` = the main navigation assistant

`/bq-suggest "<situation>"` is the router's interactive front-end. It must output: next workflow command + relevant capability commands + selected skills (Skill Router) + confidence forecast + manual-vs-auto advice + any blocking gate. Worked journey routes (monetize-a-niche, create-a-course, website-style, API-integration) live in `COMMAND_ROUTER.md` §3.

## 6. Logging + learning

Non-trivial routing decisions append one line to `NEXT_COMMAND_LOG.md` (date · finished command · required-next · set · accepted?). `/bq-skill-audit` and `/bq-verify drift` read it to detect dead recommendations (always ignored → demote) and missing ones (users keep running X after Y → add to map).

## 7. Maintainer rule

New command ⇒ add: ID map row + router routes + "usually next" links from neighbors. Removing ⇒ retire ID, purge routes. Skipping this = drift violation.

## Orchestration linkage (alpha.22 orchestration update)

The Command Router is one layer of the global orchestration model (BEQUITE_ORCHESTRATION_MODEL.md). On conflict, duplication, or unclear next step, routing defers to .bequite/state/ORCHESTRATION_MAP.md (source of truth) via the bequite-orchestrator skill. When no command fits, the router emits the Missing Capability block instead of forcing a nearest-match.
