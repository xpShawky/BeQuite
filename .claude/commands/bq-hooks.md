---
description: Manage BeQuite's opt-in Claude Code safety hooks (M3). status / enable / disable / test. Hooks ship DISABLED by default (they run shell scripts = an RCE vector; review before enabling). enable merges the hooks block into .claude/settings.json (never overwrites); test fires each hook script with a crafted input and checks exit codes; a Claude Code reload is required for enable/disable to take effect.
---

# /bq-hooks — manage the opt-in safety hooks (M3)

The 3 BeQuite hooks (destructive-op block · secret scan · banned-weasel-word stop) ship as `.claude/hooks/*.{sh,ps1}` but are **OFF by default** — Claude Code only runs hooks listed in `.claude/settings.json` (or `settings.local.json`), and BeQuite never adds them automatically because hooks execute shell on every tool call (RCE vector; review first). Strategy: `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md` · ADR-005.

## Syntax

```
/bq-hooks status     ← are hooks installed? wired? which platform? reload needed?
/bq-hooks test       ← fire each hook script with crafted input, check exit codes (no Claude reload needed)
/bq-hooks enable      ← MERGE the hooks block into .claude/settings.json (asks first; never overwrites)
/bq-hooks disable     ← remove ONLY the BeQuite hooks block from settings (keeps your other settings)
```

## status

Report: (1) hook scripts present in `.claude/hooks/` (list the 6 .sh/.ps1); (2) is there a `hooks` block in `.claude/settings.json` / `settings.local.json`? (3) detected OS → which example applies (`settings.windows.json.example` for Windows/PowerShell, `settings.json.example` for macOS/Linux bash); (4) verdict: **DISABLED** (no hooks block) / **ENABLED but reload pending** / **ENABLED & active**. Remind: Claude Code reads hooks at session start — after enable/disable you must reload the Claude Code window.

## test (works whether or not hooks are enabled)

Hooks fire on Claude Code tool events, which the agent can't self-trigger mid-session — so `test` validates the SCRIPTS directly (the same logic Claude Code would run). For each hook, pipe a crafted stdin JSON to the script and assert the exit code. Protocol: **exit 2 = BLOCK, exit 0 = allow** (exit 1 does NOT block).

Windows (PowerShell) example the command runs:
```
# destructive -> expect exit 2 (BLOCK)
'{"tool_input":{"command":"rm -rf /data"}}' | <write to a temp .json in the project> 
Get-Content tmp.json -Raw | powershell -NoProfile -ExecutionPolicy Bypass -File .claude\hooks\pretooluse-block-destructive.ps1 ; $LASTEXITCODE  # 2
# safe -> expect exit 0 (ALLOW): {"tool_input":{"command":"ls -la"}}
# secret -> expect exit 2: {"tool_input":{"file_path":"x.env","content":"AWS_SECRET=AKIA...EXAMPLE"}}
# weasel Stop -> expect exit 2: {"response":"the fix is complete and it should work now"}
```
macOS/Linux: `printf '<json>' | bash .claude/hooks/<hook>.sh ; echo $?`. Report PASS/FAIL per hook (matched expected exit code). Use temp JSON files inside the project dir to avoid shell quote/path issues; clean them up. Verified pattern (alpha.24): all 3 PS1 hooks returned the correct codes.

## enable (asks for confirmation first — security-sensitive)

1. **Show the user** which `.ps1`/`.sh` scripts will run and remind them this is an RCE-class change (review the scripts first). Wait for explicit yes.
2. Pick the example by OS: Windows → `.claude/settings.windows.json.example`; macOS/Linux → `.claude/settings.json.example`.
3. **MERGE** the `hooks` block into `.claude/settings.json` (preferred) or `settings.local.json`, preserving any existing `permissions`/other keys — **never overwrite an existing settings file**. If no settings.json exists, create one containing only the hooks block.
4. Windows note: may require `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
5. Tell the user: **reload the Claude Code window** for hooks to load, then run a real check (e.g., ask the agent to attempt `rm -rf` on a throwaway path — it should be blocked).

## disable

Remove ONLY BeQuite's `hooks` block (the destructive/secret/weasel entries) from settings; leave the rest intact. Reload to take effect.

## Files

Reads: `.claude/hooks/*` · `.claude/settings*.json*` · the two `.json.example` files. Writes (enable/disable only, with confirmation): `.claude/settings.json` (merge) + AGENT_LOG + LAST_RUN. **R3 file-risk** (settings/config) — enable/disable is a hard human gate even in auto mode.

## Next Command Recommendations

After enable → reload, then `/bq-hooks test` style real check. Set: `/bq-doctor` (env health incl. hooks presence). Do not run yet: enabling on a repo whose `.claude/hooks/*` scripts you have not personally reviewed.
