# BeQuite hooks (OPT-IN, machine-enforced safety)

These shell/PowerShell scripts turn three of BeQuite's *advisory* rules into *deterministic* guardrails Claude Code cannot skip — per ADR-005 and Anthropic's guidance ("hooks are deterministic and guarantee the action happens"; CLAUDE.md is only advisory).

> ⚠️ **SECURITY — read before enabling.** Hooks run arbitrary code on your machine on agent lifecycle events. Committed-in-repo hooks have been an RCE vector (CVE-2025-59536 / CVE-2026-21852). **Review every script yourself, then enable manually.** BeQuite ships these as `.example` config that is **NOT active by default** — nothing runs until *you* merge the hooks block into your own `.claude/settings.json`.

## The three hooks

| Script | Event | What it does |
|---|---|---|
| `pretooluse-block-destructive.{sh,ps1}` | PreToolUse (Bash) | blocks `rm -rf` on tracked code, force-push to protected branches, `git reset --hard`, `terraform destroy`, SQL `DROP`, and deletion of `.bequite/`/`.claude/` |
| `pretooluse-secret-scan.{sh,ps1}` | PreToolUse (Write\|Edit) | blocks writing AWS/GitHub/Anthropic/OpenAI/Slack keys + private-key blocks |
| `stop-banned-weasel-words.{sh,ps1}` | Stop | blocks a turn that claims completion with a banned weasel word instead of evidence (most experimental; fails soft) |

All use **exit 2 = block** (exit 1 does NOT block). They **fail soft**: if they can't parse the input, they allow the action rather than wedging your session.

## Enable (after reviewing the scripts)

1. macOS/Linux/WSL: open `.claude/settings.json.example`. Windows: open `.claude/settings.windows.json.example`.
2. **Merge** its `hooks` block into your real `.claude/settings.json` (or `settings.local.json`) — don't overwrite an existing settings file.
3. (unix) `chmod +x .claude/hooks/*.sh`. (Windows) you may need `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
4. Hooks load when Claude Code reads settings (often immediately in current builds; reload the window if `/hooks` doesn't list them). Test with a harmless trigger before relying on them.

## Known gotcha (verified live 2026-06-13)

The destructive-block + secret-scan hooks scan the **entire command/content string** - including echo text, labels, comments, and example text. So do NOT write `rm -rf`, `DROP TABLE`, or a secret-shaped string literally even as documentation inside a command you run, or the whole tool call is blocked (exit 2). Refer to dangerous patterns by description, or split the literal. The destructive matcher covers both the **Bash and PowerShell** tools on Windows (widened from the original Bash-only example).

Full protocol + tuning + disable instructions: `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`.
