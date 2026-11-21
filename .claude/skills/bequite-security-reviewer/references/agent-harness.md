# Agent harness review: permissions, hooks, MCP, sandbox, logs (verified 2026-11-21)

Use for any project where an AI agent writes code, runs commands, browses or calls tools, including the development agent itself.

## 1. Permissions (Claude Code as the example harness)

Source: https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/security

- Rules are evaluated deny, then ask, then allow; the first match decides. A broad deny beats a narrower allow.
- A command rule matches the command text. `Bash(curl *)` does not stop `/usr/bin/curl` or a Python one-liner that opens a socket. Treat rules as intent, not a wall. Filesystem and network limits need the sandbox (`/sandbox` in Claude Code).
- Modes run from `default` (ask) through `acceptEdits`, `plan`, `auto`, `dontAsk` to `bypassPermissions`. Review: which mode does the project recommend, and which commands are pre-allowed in the checked-in settings? A checked-in allow rule is granted to everyone who clones.
- Check for: `Bash(*)`-style blanket allows; allows on `git push`, package publish, `curl`, `ssh`, cloud CLIs; no deny on credential paths.

Example settings block to propose (the user merges it):

```json
{ "permissions": {
    "deny":  ["Read(./.env*)", "Read(~/.ssh/**)", "Bash(git push *)", "Bash(npm publish *)"],
    "ask":   ["Bash(curl *)", "Bash(rm *)"],
    "allow": ["Bash(npm run test *)", "Bash(python scripts/bq_check.py *)"] } }
```

## 2. Hooks

- Hooks are shell commands that run with the user's rights on every matching event. Review them as code; a hook from a third-party plugin is a supply-chain item (ASI04).
- PreToolUse exit code 2 blocks the call; exit 1 does not. Test each hook with crafted JSON on stdin and record exit codes.
- Pattern hooks are bypassable (BeQuite's own destructive-op hook allows `find -delete`, measured 2026-11-21). Say so in the report; do not present a hook as enforcement.
- Check the matcher: a secret scan wired to `Write|Edit` misses secrets written through `Bash`.

## 3. MCP servers

Source: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices

For each server in `.mcp.json`, user settings or a plugin:

| Check | Pass |
|---|---|
| Origin | Repo or registry page read this session; maintainer, licence, last release recorded. |
| Install command | The exact command was shown to the user before first run (local server compromise). |
| Transport | Local servers prefer stdio; an HTTP server on localhost requires a token. |
| Tokens | The server accepts only tokens issued for it (audience check) and never passes the user's token on to another API (token passthrough is forbidden). |
| Scopes | Minimal scopes at start; extra scopes requested when needed. |
| SSRF | Servers that fetch URLs block private and link-local ranges (169.254.0.0/16) and follow redirects safely. |
| Proxies | A proxy server with one static client ID keeps per-client consent (confused deputy). |
| Data reach | Lethal-trifecta test across all enabled servers together, not one at a time. |

Anthropic does not audit MCP servers; trust is the user's decision, recorded in the report.

## 4. Browser and computer-use agents

Sources: https://claude.com/blog/claude-for-chrome, https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

- Web pages and screenshots can carry instructions. The vendor's own test measured 23.6% attack success without mitigations and 11.2% with them; neither is zero.
- Run computer use in a dedicated VM or container with minimal rights; keep credentials out of reach; allow-list domains; a human confirms consequential actions.
- Signed-in browsers belong to the user: act only on the pages the task needs; never type passwords, card numbers or API keys.

## 5. Secrets in agent output and logs

Places secrets leak in agent workflows: transcripts, `AGENT_LOG.md`, `evidence.md` (pasted command output), CI logs (the tj-actions incident printed secrets into logs, CVE-2025-30066), error trackers, GIF recordings and screenshots, model prompts.

- Before pasting command output into evidence, scan it with the same patterns as the secret hook.
- `env`, `printenv`, `cat .env`, `docker inspect` and verbose HTTP clients (`curl -v` with auth headers) are never pasted whole.
- Quote at most the first four characters of a secret in any report.
- If a secret reached a log or a commit: rotate it first, then purge. History rewrites need the owner's yes.

Common patterns (starting set; extend per project): `AKIA[0-9A-Z]{16}` · `gh[pousr]_[A-Za-z0-9_]{36,}` · `github_pat_[A-Za-z0-9_]{60,}` · `xox[baprs]-[A-Za-z0-9-]+` · `sk_(test|live)_[A-Za-z0-9]{24,}` · `-----BEGIN [A-Z ]*PRIVATE KEY-----`.
