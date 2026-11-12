<!-- BEQUITE -->

## BeQuite {{VERSION}}

This project uses **BeQuite**, a lightweight Claude Code workflow pack (slash commands + skills + `.bequite/` memory + gates).

- `/bequite`: menu with project state and the next recommended commands. `/bq-help`: full reference (also `commands.md`).
- `/bq-auto [intent] "task"`: autonomous runner; it stops only at hard human gates.
- `/bq-suggest "<situation>"`: tells you which command and mode fit the goal.
- Memory lives in `.bequite/`; commands in `.claude/commands/`; skills in `.claude/skills/bequite-*/`.

### Core rules

1. **Plan first:** for non-trivial work, research (the web when no reference is given) → plan → wait for approval → then produce.
2. **Skills first:** before acting on any command, select and announce the suitable skills (the `Skill Selection:` block).
3. **Evidence over claims:** never say "done" without the command + exit code + output; otherwise write `UNVERIFIED:`. Banned in completion reports: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
4. **Verify each phase** with tests/QA before starting the next; failures go to `/bq-fix`.
5. **Write back:** after real actions, update `.bequite/logs/AGENT_LOG.md`, `.bequite/state/LAST_RUN.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson was learned.
6. **Tool neutrality:** named tools are examples; pick per project with reasons (`.bequite/principles/TOOL_NEUTRALITY.md`).
7. **Gates:** refuse out-of-order commands; hard human gates (destructive ops, production, secrets, paid services, releases) always wait for a yes.

<!-- /BEQUITE -->
