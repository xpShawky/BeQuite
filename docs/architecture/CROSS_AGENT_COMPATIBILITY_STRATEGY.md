# Cross-Agent Compatibility Strategy

BeQuite is built Claude-Code-first, but most of it is **plain markdown + a file-based memory contract** — which means most of it ports. This strategy defines what is Claude-specific, what is portable, and how other coding agents use BeQuite today without any adapter. Companion docs: `docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md` (how-to) · `docs/specs/AGENT_COMPATIBILITY_MATRIX.md` (per-agent) · `.bequite/audits/CROSS_AGENT_COMPATIBILITY_AUDIT.md` (current-state findings).

## 1. The portability split

| Layer | Claude-specific? | Portability |
|---|---|---|
| **Slash command invocation** (`/bq-*`) | YES — Claude Code derives commands from `.claude/commands/` filenames | other agents can't *invoke* them — but every command file is a readable **markdown playbook**; paste-as-prompt works everywhere |
| **Skills** (`.claude/skills/*/SKILL.md` auto-activation) | YES — auto-attach is a Claude Code mechanism | the skill *content* is plain markdown expertise; any agent told to read a SKILL.md gets the same procedure |
| **`.bequite/` memory** | NO — plain files | fully portable; any agent that reads/writes files can honor the memory contract |
| **Workflow gates / phases / contract / routers** | NO — markdown rules + state files | portable wherever the agent follows instructions in context |
| **Hooks** (`.claude/hooks/`, opt-in) | YES — Claude Code hook runtime | not portable; other agents rely on the convention layer only |
| **CLAUDE.md** | partially — Claude Code reads it automatically | Cursor reads `.cursorrules`/AGENTS.md-class files; Codex-class agents read AGENTS.md; content is reusable, the auto-load path differs |
| **Catalog IDs / docs / specs / audits** | NO | pure markdown |

**Core insight: a BeQuite command file IS a prompt.** `/bq-fix` in Claude Code = "paste bq-fix.md + your bug description" anywhere else. The slash is sugar; the playbook is the product.

## 2. Per-agent usage patterns (today, no adapter)

- **Claude Code** — native: slash commands, skills auto-attach, hooks optional, memory automatic. Reference experience.
- **OpenAI Codex / ChatGPT-style coding agents** — point the agent at the repo; instruct it (in AGENTS.md or the task prompt) to: read `CLAUDE.md` § rules + `.bequite/state/*` before acting, then follow the relevant `.claude/commands/bq-*.md` playbook verbatim, then write back to `.bequite/logs/AGENT_LOG.md` + state files. Treat each playbook as a procedure spec.
- **Cursor** — add a rules file pointing at `CLAUDE.md` and the command playbooks; use Cursor's docs-context to keep `commands.md` + `COMMAND_ID_MAP.md` in scope; paste playbook sections into composer for big tasks. Cursor reads the repo, so `.bequite/` memory works as shared state.
- **Antigravity-class IDE agents** — same pattern as Cursor: repo-level instructions file + playbooks-as-context + `.bequite/` as the persistent store the agent is told to read first and write last.
- **Hermes / OpenClaw-style autonomous agents** — map BeQuite phases onto the agent's task loop: P0 discover → P1 frame → P2 build → P3 quality → P4 release → P5 memory. The agent's planner consumes `COMMAND_ROUTER.md` routes as its task graph; hard human gates become approval checkpoints in whatever approval mechanism the harness has.
- **Local CLI agents / scripts** — `.bequite/` is greppable plain text; a wrapper can inject any playbook + state into any model prompt. (A thin `bq` shell wrapper is a plausible FUTURE adapter — see §4. Not built.)

## 3. What NOT to rely on outside Claude Code

1. Skill **auto-attach** — name the SKILL.md files explicitly in the prompt instead (use `SKILL_ROUTER.md` to pick).
2. **Hooks** machine-enforcement — outside Claude Code only the convention layer exists; treat banned-weasel-words/destructive-op rules as instructions, and review more.
3. **Slash invocation + $ARGUMENTS parsing** — pass arguments in prose.
4. **Automatic CLAUDE.md loading** — feed the rules explicitly (or via the agent's own rules-file mechanism).
5. Model-specific behavior notes (Fable/Opus guidance) — irrelevant on other models; the FRONTIER_REASONING_SUMMARY 10-rule card is designed exactly for this: give it to ANY model.

## 4. Future adapter sketch (NOT built — roadmap only)

A lightweight `bq` wrapper (single script, no runtime deps) could: list playbooks by catalog ID → assemble playbook + state-snapshot into a prompt → copy to clipboard / pipe to any CLI model → append the result to AGENT_LOG. Also plausible: an AGENTS.md generator (`/bq-handoff agents` argument) emitting a cross-agent briefing. Both deferred until cross-agent demand is real; no heavy universal app, no provider APIs, per the lightweight charter.

## 5. Maintainer rules

Every new command must remain **playbook-readable** (self-contained procedure; no Claude-only references in the steps themselves). Claude-specific mechanics (skills auto-attach, hooks) are always labeled as such in docs. The compatibility matrix is re-verified when a listed agent changes materially.
