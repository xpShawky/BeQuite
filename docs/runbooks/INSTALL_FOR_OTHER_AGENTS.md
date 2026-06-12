# Installing BeQuite for Other AI Agents (per-agent setup)

BeQuite installs the same files everywhere — what differs per agent is **where that agent looks for instructions**. This runbook gives spec-kit-style setup for each supported agent, on Windows / macOS / Linux, in both **per-project** and **global** layouts. Usage after setup: `USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md` · capability detail: `docs/specs/AGENT_COMPATIBILITY_MATRIX.md`.

> **Honesty note:** third-party agents change their instruction-file mechanisms often. The bridge-file pattern below is mechanism-independent (plain markdown the agent is pointed at); where an agent-specific path is named, verify it against that tool's current docs before relying on it.

## 1. The two layouts

**Per-project (recommended):** run the normal installer inside each project — every agent then finds `.claude/commands/` (playbooks), `.claude/skills/` (expertise), `.bequite/` (memory) in the repo it's working on.

```powershell
# Windows (inside the project)
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```
```bash
# macOS / Linux (inside the project)
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

**Global (one source, many projects):** clone BeQuite once, then install per project from the local clone (faster, offline-capable, version-pinned):

```powershell
# Windows — global clone + per-project install from it
git clone https://github.com/xpShawky/BeQuite.git "$env:USERPROFILE\.bequite-src"
cd <your-project>
& "$env:USERPROFILE\.bequite-src\scripts\install-bequite.ps1" -FromLocal "$env:USERPROFILE\.bequite-src"
```
```bash
# macOS / Linux
git clone https://github.com/xpShawky/BeQuite.git ~/.bequite-src
cd <your-project>
~/.bequite-src/scripts/install-bequite.sh --from-local ~/.bequite-src
```

Agents that can read arbitrary paths can also use the global clone's playbooks directly (read-only) while keeping per-project `.bequite/` memory — but per-project install is simpler and is the default recommendation. Update the global clone with `git -C ~/.bequite-src pull` then re-run the per-project install with `--force` (memory is preserved).

## 2. The universal bridge file - AGENTS.md (now an industry standard)

**Verified 2026-06-12 (https://agents.md):** AGENTS.md is a Linux Foundation (Agentic AI Foundation) standard used by 60,000+ projects and supported natively by OpenAI Codex, Cursor, Gemini CLI, GitHub Copilot, Zed, Warp, Windsurf, Aider, goose, Devin, JetBrains Junie, Google Jules, and VS Code - one bridge file covers nearly every non-Claude agent in the table below. Create it once per project at the repo root; for the few agents that read nothing automatically, paste the same block as the first session message:

```markdown
# BeQuite bridge — instructions for any AI coding agent

This project uses BeQuite (workflow + skills + memory in markdown).
Before acting, ALWAYS:
1. Read `CLAUDE.md` (core operating rules — they apply to you regardless of model).
2. Read `.bequite/state/PROJECT_STATE.md`, `CURRENT_MODE.md`, `CURRENT_PHASE.md`,
   `WORKFLOW_GATES.md`, `LAST_RUN.md`, `CONTEXT_SUMMARY.md` (if present),
   and the last 5 entries of `.bequite/logs/AGENT_LOG.md`.
3. To run a BeQuite command, open `.claude/commands/bq-<name>.md` and follow it
   as an exact procedure ($ARGUMENTS = my task description).
4. Pick expert procedures from `.bequite/skills/SKILL_ROUTER.md` and read the
   chosen `.claude/skills/bequite-*/SKILL.md` files.
5. When unsure what's next: `.bequite/state/ORCHESTRATION_MAP.md` is the source of truth.
6. Before claiming done: evidence (command + exit code + output). Never the words
   "should work / probably / seems to". Unverified ⇒ say UNVERIFIED.
7. After working: append to `.bequite/logs/AGENT_LOG.md`, update `LAST_RUN.md`, tick gates.
8. Follow `.bequite/state/FRONTIER_REASONING_SUMMARY.md` (10 rules) at all times.
NEVER: delete tracked code, touch secrets/auth/payments/migrations, push releases,
or bypass `.bequite/state/WORKFLOW_GATES.md` without explicit human approval.
```

## 3. Per-agent setup

| Agent | Where the bridge goes | Notes (Win/mac/Linux identical unless stated) |
|---|---|---|
| **Claude Code** | none needed | native: slash commands + skills auto-attach + CLAUDE.md auto-load + optional hooks |
| **Antigravity (Google)** | repo `AGENTS.md` (+ paste-block fallback); add BeQuite docs to its workspace context | IDE-agent pattern; verify its current rules-file name in product docs |
| **Gemini CLI** | `GEMINI.md` at repo root with the same bridge content | Gemini CLI reads GEMINI.md project context; global: also `~/.gemini/GEMINI.md` pointing to the clone |
| **Cursor** | `AGENTS.md` + a rule in `.cursor/rules/` (e.g. `bequite.mdc`) containing the bridge | pin `commands.md` + `COMMAND_ID_MAP.md` as docs context; Composer for multi-file playbook runs |
| **Codex — CLI** | `AGENTS.md` at repo root | Codex-style agents read AGENTS.md natively; one playbook task per run works best |
| **Codex — app/web (ChatGPT)** | `AGENTS.md` in the connected repo; for chat-only sessions paste the bridge + the playbook | one task per session; demand evidence per step |
| **Kimi (Moonshot) agents** | paste-block as the session's first message (or its project-instructions field if available) | treat as Tier B per `LOW_COST_MODEL_RULES.md` unless proven otherwise |
| **MiniMax agents** | same paste-block pattern | same tiering rule |
| **DeepSeek (chat/coder)** | same paste-block pattern; for repo-connected modes use `AGENTS.md` | strong coder models still get Guard Pass on output |
| **Ollama / local models** | paste-block prepended to every prompt by your wrapper script; ONE task per prompt | Tier C: drafts/boilerplate/demo-data only; follow `USING_BEQUITE_WITH_SMALLER_MODELS.md` |
| **OpenClaw-style agents** | bridge in the agent's workspace instructions; map P0–P5 onto its task loop | hard gates MUST become explicit approval checkpoints |
| **Hermes agents** | same as OpenClaw pattern | autonomous loops: Guard Pass before any auto-merge |

## 4. Multi-agent projects (several agents, one repo)

Safe by design: `.bequite/` is the shared memory — every agent reads it first and writes back, so agents see each other's work via `AGENT_LOG.md`/`LAST_RUN.md`. Rules: one agent works at a time per task (no concurrent edits to the same surface) · every agent obeys the same gates · disagreements between agents resolve via `ORCHESTRATION_MAP.md`, then the human.

## 5. Roadmap (not built)

`/bq-handoff agents` argument auto-generating AGENTS.md/GEMINI.md bridges + a Cursor rules template + the `bq` prompt-assembly wrapper — parked in `REMAINING_ROADMAP_TASKS.md` §E until cross-agent demand is real. Today's setup is copy-paste and takes ~2 minutes per project.
