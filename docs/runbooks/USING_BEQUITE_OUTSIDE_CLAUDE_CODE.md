# Using BeQuite Outside Claude Code

BeQuite's commands are markdown playbooks and its memory is plain files — so you can use it with Codex/ChatGPT-style agents, Cursor, Antigravity-class IDE agents, autonomous agent harnesses, or any LLM with file access. This runbook is the practical how-to; the reasoning lives in `docs/architecture/CROSS_AGENT_COMPATIBILITY_STRATEGY.md`; per-agent details in `docs/specs/AGENT_COMPATIBILITY_MATRIX.md`.

## The universal recipe (works with any capable agent)

1. **Install BeQuite normally** into the project (the installer just copies markdown — no Claude dependency).
2. **Orient the agent.** First instruction every session:
   > Read `CLAUDE.md` (core rules), then `.bequite/state/PROJECT_STATE.md`, `CURRENT_MODE.md`, `CURRENT_PHASE.md`, `WORKFLOW_GATES.md`, `LAST_RUN.md`, and the last 5 entries of `.bequite/logs/AGENT_LOG.md`. Do not act before reading these.
3. **Run a "command" by playbook.** Instead of `/bq-fix login breaks on mobile`:
   > Open `.claude/commands/bq-fix.md` and follow that procedure exactly for this task: "login breaks on mobile". Where it says $ARGUMENTS, use my task description. Honor every gate and refusal rule in it.
4. **Pick skills manually** (no auto-attach outside Claude Code). Choose from `.bequite/skills/SKILL_ROUTER.md`'s domain map:
   > Also read `.claude/skills/bequite-problem-solver/SKILL.md` and apply its procedure.
5. **Navigate with the routers.** Ask: *"Per `.bequite/commands/COMMAND_ROUTER.md`, what should happen next?"* — or open `COMMAND_ID_MAP.md` yourself; IDs (W0.1…C10) work as a shared vocabulary with any agent.
6. **Write back.** End every working session with:
   > Append what you did to `.bequite/logs/AGENT_LOG.md`, update `LAST_RUN.md`, and tick any gates in `WORKFLOW_GATES.md`. Use concrete evidence; the banned-weasel-word rule applies.

## Agent-specific notes

- **Codex / ChatGPT coding agents:** put step 2's orientation into the repo's agent-instructions file (AGENTS.md-class) so it loads automatically; reference playbooks by path in tasks.
- **Cursor:** add a rules file that says "BeQuite rules: see CLAUDE.md; BeQuite procedures: see .claude/commands/". Pin `commands.md` + `COMMAND_ID_MAP.md` as docs context. Paste playbook sections into Composer for multi-file work.
- **Antigravity-class IDE agents:** same as Cursor — repo instructions + playbooks-as-context; `.bequite/` is the persistent store the agent reads first and writes last.
- **Hermes / OpenClaw-style harnesses:** map P0–P5 phases onto the agent's task loop; use `COMMAND_ROUTER.md` spine routes as the task graph; convert the 17 hard human gates into the harness's approval checkpoints — never let an autonomous loop pass them silently.
- **Plain chat LLM (no file access):** paste the playbook + the relevant state files into the prompt; paste results back into your repo manually. Slowest path, still correct.

## What you lose outside Claude Code (plan around it)

| Lost | Mitigation |
|---|---|
| Skill auto-attach | name SKILL.md files explicitly (router map tells you which) |
| Opt-in hooks (machine-blocked destructive ops / secrets / weasel words) | the rules still exist as text — instruct the agent with them and review more carefully |
| `$ARGUMENTS` parsing | pass arguments in prose |
| Automatic CLAUDE.md load | load it explicitly in step 2 |

## What stays fully intact

Memory contract (`.bequite/`) · workflow gates · phases · catalog IDs · execution contract · evidence discipline · confidence forecast format · all specs, docs, audits — they are agent-agnostic markdown. The FRONTIER_REASONING_SUMMARY 10-rule card (`.bequite/state/`) was built precisely to make ANY model follow BeQuite discipline — give it to the agent verbatim.
