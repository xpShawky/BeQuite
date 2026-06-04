# Claude Code Hooks Strategy

**Status:** active (v3.0.0-alpha.18) — implements ADR-005
**Scope:** opt-in, machine-enforced safety. The single highest-leverage harness upgrade available to a markdown skill-pack.
**Sources:** verified against the official [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) + [Hooks guide](https://code.claude.com/docs/en/hooks-guide).

---

## 1. Why hooks (the advisory → deterministic gap)

BeQuite's safety so far is **convention-enforced**: CLAUDE.md prose + the 17 hard gates ask the *model* to check itself. Anthropic is blunt that this isn't enough: *"Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."* When the agent is fresh, context-pressured, or rushing, advisory rules drift.

Hooks are *"user-defined shell commands that execute at specific points in Claude Code's lifecycle… ensuring certain actions always happen rather than relying on the LLM to choose to run them."* They are pure config + scripts — no deps, no server, no daemon. That keeps them inside ADR-001 (lightweight), ADR-003 (tool-neutral), and ADR-004 (no heavy direction).

**A `PreToolUse` deny fires before any permission-mode check — it blocks even under `--dangerously-skip-permissions` / `bypassPermissions`.** Hooks can *tighten* safety but never *loosen* it. That is exactly the property BeQuite's hard gates want.

---

## 2. ⚠ Security model (non-negotiable — why these are OPT-IN)

Hooks run **arbitrary code on your machine** on lifecycle events. Hooks committed in project files have been a remote-code-execution vector (CVE-2025-59536, CVE-2026-21852: a malicious repo ships a hook that runs when you open it). Therefore BeQuite:

- ships hooks as **`.example` config that is NOT active by default** — nothing runs until *you* merge the `hooks` block into your own `.claude/settings.json`;
- ships the scripts so you can **read every line before enabling**;
- never auto-enables hooks in the installer or `/bq-update`;
- keeps every hook **fail-soft**: if it can't parse the input it **allows** the action (never wedges your session).

**Rule:** review → enable manually → test with a harmless trigger → only then rely on them. Treat any hook you didn't write as untrusted until reviewed.

---

## 3. Protocol reference (verified)

**Input:** every hook gets JSON on **stdin** — `session_id`, `cwd`, `hook_event_name`, `transcript_path`, plus event-specific fields (`tool_name` + `tool_input` for tool events; `prompt` for UserPromptSubmit; `stop_hook_active` for Stop).

**Output — exit codes (what BeQuite uses):**
- `exit 0` — allow. For `SessionStart`/`UserPromptSubmit`, **stdout is injected into Claude's context** (cap ~10,000 chars).
- `exit 2` — **BLOCK**. stdout is ignored; **stderr is fed to Claude as the reason**. Blocks on PreToolUse, UserPromptSubmit, Stop, SubagentStop, PreCompact.
- any other code — non-blocking error; the action proceeds; first stderr line shown as a hook error.
- **Gotcha: `exit 1` does NOT block — only `exit 2` does.**

**Output — structured JSON (alternative to exit codes; don't mix with exit 2):**
- PreToolUse: `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny|allow|ask","permissionDecisionReason":"…"}}` (+ `updatedInput` to rewrite args).
- PostToolUse / Stop / UserPromptSubmit: top-level `{"decision":"block","reason":"…"}`.
- Context injection without blocking: `additionalContext`.

**Stop-hook loop safety (critical):** a Stop hook MUST `exit 0` when `stop_hook_active` is true, or it loops forever. Claude Code force-overrides after **8** consecutive blocks.

**Config:** `hooks` → event → `[{ "matcher": "<tool pattern>", "hooks": [{ "type":"command", "command":"…", "timeout":N }] }]`. Matcher: `""`/omitted = all; `Edit|Write` = exact/OR; anything else = JS regex; case-sensitive. `$CLAUDE_PROJECT_DIR` resolves to the project root. Toggle everything with `"disableAllHooks": true`. Inspect with `/hooks`.

**Locations:** `~/.claude/settings.json` (all projects) · `.claude/settings.json` (project, committed) · `.claude/settings.local.json` (project, gitignored).

---

## 4. The three BeQuite hooks (this release)

| Script | Event · matcher | Blocks |
|---|---|---|
| `pretooluse-block-destructive.{sh,ps1}` | PreToolUse · `Bash` | `rm -rf` on tracked code (allows `/tmp`, `node_modules`), force-push to `main`/`master`/`prod`/`release`, `git reset --hard`, `terraform destroy`, SQL `DROP`, deletion of `.bequite/`/`.claude/` |
| `pretooluse-secret-scan.{sh,ps1}` | PreToolUse · `Write\|Edit` | AWS `AKIA…`, GitHub `gh*_…`, Anthropic `sk-ant-…`, OpenAI `sk-…`, Slack `xox*-…`, `-----BEGIN … PRIVATE KEY-----`. (Generic `KEY=<value>` left commented to avoid false positives.) |
| `stop-banned-weasel-words.{sh,ps1}` | Stop | a completion claim using `should work / probably / seems to / appears to / i think it works / might fix / hopefully / in theory` instead of evidence. **Most experimental; fails soft; respects `stop_hook_active`.** |

These map 1:1 to CLAUDE.md core rules 6 (banned weasel words) + 8 (don't leak/destroy) and hard human gates #1 (destructive deletion) + #6 (secrets). They make the *safety subset* of the gates machine-enforced; the rest stay convention-enforced (research is generative — over-constraining it with hooks is wrong, per ADR-005).

---

## 5. Enable / tune / disable

**Enable:** review the scripts → merge the `hooks` block from `.claude/settings.json.example` (unix) or `.claude/settings.windows.json.example` (Windows) into your real settings file → `chmod +x .claude/hooks/*.sh` (unix) or allow PowerShell execution (Windows) → restart / `/hooks` to confirm → test.

**Tune:** edit the regexes in the scripts (e.g. add your own protected branches, enable the optional generic-secret pattern, add `terraform apply -auto-approve`). Keep them fail-soft.

**Disable:** remove the `hooks` block, or set `"disableAllHooks": true`, or just don't merge the example. `/bq-doctor` reports whether hooks are present + active.

**Updates:** `/bq-update` refreshes the hook *scripts* and the `.example` files but **never** edits your live `settings.json` (it can't silently change what executes on your machine).

---

## 6. Honest test boundary (verify-before-claim)

The scripts are written to the **documented protocol** (exit codes, stdin JSON shape, `stop_hook_active`, matchers) and verified by logic review. They were **not fired through a live Claude Code hook runtime in the session that authored them** — there was no hook runtime available. That's also why the security model *requires* you to review + test before enabling. Treat them as a reviewed reference implementation: enable, trigger each one with a harmless test (e.g. ask the agent to run `rm -rf ./scratch-test` in a throwaway dir), confirm the block, then rely on them. Report any environment-specific fix back so the scripts can harden.

---

## 7. Relationship to the gates + the self-verify pattern

- These hooks **enforce** a subset of the 17 hard human gates; they don't replace the gate ledger. The gates remain the source of truth; hooks are the deterministic backstop for the most dangerous ones.
- For teams that want a **`Stop`-hook self-verify loop** ("don't end the turn until build + tests pass"), see the recipe in `docs/runbooks/USING_BEQUITE_COMMANDS.md` — it's the same protocol (`Stop` + `stop_hook_active` guard) pointed at the project's own test command. Shipped as a documented opt-in, not a default (BeQuite can't know your test command).

See also: ADR-005 (the decision), `docs/architecture/WORKFLOW_GATES.md` (the gates), `bequite-security-reviewer` (secret-handling discipline).
