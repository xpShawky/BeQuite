# Agent Compatibility Matrix

How BeQuite works across coding agents. **Capability columns reflect general tool patterns as of 2026-06 — verify against each tool's current docs before relying on a cell**; this matrix is re-verified when a listed agent changes materially. How-to: `docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md`.

| Agent / tool | Slash commands? | Project memory (reads/writes `.bequite/`)? | Reads markdown playbooks? | Hooks? | Recommended BeQuite usage | Limitations | Suggested adapter later |
|---|---|---|---|---|---|---|---|
| **Claude Code** (CLI/desktop/IDE) | ✅ native (`.claude/commands/`) | ✅ automatic | ✅ + skills auto-attach | ✅ opt-in BeQuite hooks | full native experience — reference platform | — | — (is the reference) |
| **OpenAI Codex / ChatGPT coding agents** | ❌ | ✅ (file access in repo) | ✅ | ❌ (own sandbox policies instead) | AGENTS.md carries the orientation block; tasks reference playbooks by path; manual skill naming | no auto-attach; no BeQuite hooks; rules must be loaded explicitly | AGENTS.md generator (`/bq-handoff agents` argument, roadmap) |
| **Cursor** | ❌ (has its own commands concept) | ✅ | ✅ (docs context + rules files) | ❌ (BeQuite hooks won't run) | rules file → CLAUDE.md; pin commands.md + COMMAND_ID_MAP as context; playbook sections in Composer | context limits on big playbooks; no gate machine-enforcement | rules-file template in repo (roadmap) |
| **Antigravity-class IDE agents** | ❌ | ✅ | ✅ | varies | same pattern as Cursor: repo instructions + playbooks + memory-first orientation | mechanism names vary per tool — verify | same rules-file template |
| **Hermes / OpenClaw-style autonomous harnesses** | ❌ | ✅ (if given file tools) | ✅ | harness-specific | map P0–P5 onto the task loop; COMMAND_ROUTER routes = task graph; 17 hard gates = harness approval checkpoints | autonomous loops must NOT bypass hard gates — wire approvals explicitly | phase-map adapter doc (roadmap) |
| **Local CLI agents / scripts (any model)** | ❌ | ✅ (plain files) | ✅ (pipe/paste) | ❌ | wrapper assembles playbook + state snapshot into the prompt; append results to AGENT_LOG | manual writeback discipline | thin `bq` prompt-assembly script (strategy §4, NOT built) |
| **Plain chat LLM, no file access** | ❌ | ⚠ manual copy | ⚠ paste-in | ❌ | paste playbook + state files; copy results back by hand | slow; human is the file system | — |

**AGENTS.md note (verified 2026-06-12):** AGENTS.md is now a Linux Foundation standard with native support across most rows (Codex, Cursor, Gemini CLI, Copilot, Zed, Warp, Windsurf, Aider, Devin, Junie) - the single bridge file in INSTALL_FOR_OTHER_AGENTS.md section 2 is the default setup for any non-Claude agent; per-tool rules files are optional refinements.

**Reading the matrix:** every row works *today* with documentation alone — the rightmost column is roadmap, not requirement. The portable core (memory contract, gates, playbooks, IDs, evidence rules) is identical in all rows; what varies is invocation sugar and machine-enforcement.
