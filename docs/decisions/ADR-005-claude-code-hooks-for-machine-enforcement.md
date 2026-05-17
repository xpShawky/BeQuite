# ADR-005 — Claude Code hooks for machine-enforcement of safety rules

**Status:** Proposed (drafted in alpha.16; implementation deferred to alpha.17+)
**Date:** 2026-05-17
**Decision drivers:** BeQuite v3.0.0-alpha.14 audit (`FULL_SYSTEM_ALIGNMENT_AUDIT.md`); alpha.15 audit-implementation pass.
**Author:** xpShawky + agent (auto-mode)
**Supersedes:** none
**Superseded by:** none

---

## Context

BeQuite's safety rules are **convention-enforced**, not machine-enforced:

- Banned weasel words (`should`, `probably`, `seems to`, `appears to`, etc.) — documented in CLAUDE.md, listed in `/bq-auto` failure behavior. **The agent is expected to check itself.**
- Secret scan — `bequite-security-reviewer` skill documents the discipline. **The agent is expected to grep before commit.**
- Destructive op block (`rm -rf`, `git push --force`, `git reset --hard`, `terraform destroy`, `DROP DATABASE`) — listed in `/bq-auto` hard human gates. **The agent is expected to recognize + pause.**
- Workflow-gate refusal — documented in WORKFLOW_GATES.md. **The agent is expected to read `WORKFLOW_GATES.md` and refuse if a required gate is `❌`.**

This is acceptable for a markdown-driven skill pack. But it relies on the agent honoring the contract every single time. **When the agent is fresh / loaded with too much context / pressured for speed, discipline drift is real** (alpha.13's Presentation Builder was the recent precedent).

Claude Code supports **hooks** that fire on agent lifecycle events. Hooks are shell scripts run by the Claude Code harness; they can block or modify agent behavior. The relevant hook types:

- **PreToolUse** — fires before any tool call. Can block the tool call (exit code 2 → tool refused).
- **PostToolUse** — fires after a tool call. Can run validators / formatters / linters.
- **Stop** — fires before the agent finalizes a response. Can rewrite the response or block it.
- **SessionStart** — fires at session start. Can preload context.

The question: **should BeQuite ship hooks for machine-enforcement?**

---

## Decision

**Tentatively yes, but cautiously.** Implement in alpha.17+ as an **opt-in** layer (`.claude/settings.json` with hooks pointing to `.claude/hooks/*.sh`). Default off; users with the corresponding shell environment opt in by installing the hooks.

Specifically, ship 3 hooks (with conservative blocking + clear failure messages):

### Hook 1 — `pretooluse-block-destructive.sh`

Fires before Bash / Write / Edit / Delete tool calls.

Blocks (exit 2) if the proposed command matches:
- `rm -rf` outside `/tmp` or `node_modules`
- `git push --force` / `git push -f` to protected branches (main, master, prod, release/*)
- `git reset --hard` without explicit user-go-ahead in recent history
- `terraform destroy`
- `DROP TABLE` / `DROP DATABASE` (case-insensitive SQL scan)
- `rm -rf .bequite/` / `rm -rf .claude/` (preserve project memory)

Message: "Hook blocked destructive op `<command>`. Hard human gate per `/bq-auto`. Re-run with explicit user confirmation, or use a safer alternative."

### Hook 2 — `pretooluse-secret-scan.sh`

Fires before any file Write / Edit.

Scans the new content for patterns:
- `[A-Z0-9_]*(API|SECRET|PASSWORD|TOKEN|JWT)[-_]?(KEY|TOKEN)?\s*=\s*['"]?[A-Za-z0-9+/]{20,}`
- AWS access key pattern: `AKIA[0-9A-Z]{16}`
- GitHub token pattern: `gh[pousr]_[A-Za-z0-9_]{36,}`
- Anthropic API key: `sk-ant-[A-Za-z0-9_-]+`
- OpenAI key: `sk-[A-Za-z0-9]{48,}`
- Private SSH key header: `-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----`

Blocks (exit 2) on match. Message: "Hook blocked secret-shaped string in `<file>`. Move to `.env` / OS keychain / secret manager. Add the file path to `.gitignore` if needed."

### Hook 3 — `stop-banned-weasel-words.sh`

Fires before agent finalizes a response (Stop hook).

Scans the response for banned weasel words in completion-claim contexts:
- "should work" / "should be fixed" / "should pass"
- "probably works" / "probably correct"
- "seems to work" / "appears to work"
- "I think it works" / "I believe it works"
- "might fix" / "hopefully fixed"
- "in theory" / "in principle"

If found in a sentence claiming the work is done → exit 2; ask the agent to rewrite with concrete verification or honest report.

---

## What this ADR does NOT propose

- Hooks for `bq-research` content gating (research is generative; hooks would over-constrain)
- Hooks for `/bq-presentation` output review (creative work; hooks would over-constrain)
- Mandatory hooks on every install (opt-in, per the lightweight direction in ADR-001)
- Server-side or daemon-based enforcement (preserved ADR-004 retirement of heavy direction)
- Hooks that talk to external services (no telemetry; no phone-home)

---

## Rationale

**For:**
- Machine-enforced safety beats convention-enforced safety. Especially when an agent is fresh or under context pressure.
- The 3 proposed hooks address the 3 most common discipline-drift modes: destructive ops, secret leakage, banned weasel words.
- The hooks are local-only, opt-in, well-scoped, and honor tool neutrality (no external tool installed; just shell scripts that BeQuite ships).
- Compatible with the lightweight direction — no daemons, no localhost, no Docker.

**Against:**
- Hooks add complexity to the install (`.claude/settings.json` + `.claude/hooks/*.sh`).
- Cross-platform shell shocks (bash vs PowerShell vs cmd). The install will need both `.sh` and `.ps1` variants.
- False positives in pattern matching (a real secret-shaped string might be a base64-encoded test fixture, not a credential).
- Hooks can be bypassed (`--no-verify` flags exist for some tools).
- Hooks may interfere with users who have their own preferred safety tooling.

**Trade-off:** ship opt-in by default; provide clear opt-out per `.claude/settings.json` toggles; provide both shell + PowerShell variants. Hooks should fail SOFT when they can't determine — i.e. log a warning but don't block.

---

## Implementation plan (alpha.17+)

1. **alpha.17 — Prototype + safety-rail validation**
   - Author `.claude/hooks/pretooluse-block-destructive.{sh,ps1}` + `pretooluse-secret-scan.{sh,ps1}` + `stop-banned-weasel-words.{sh,ps1}`
   - Test against fixtures with planted violations
   - Document in `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`

2. **alpha.18 — Settings integration**
   - Provide `.claude/settings.json.example` template
   - Document how to enable in `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md`
   - Add `/bq-doctor` check for hooks presence + version

3. **alpha.19 — Documentation + opt-in default**
   - Add hook documentation to CLAUDE.md
   - Installer prompts user to opt in
   - Add hooks to `bequite-updater` skill so `/bq-update` can refresh them

4. **v3.0.0-stable — Production-ready**
   - Hooks tested across Windows + macOS + Linux
   - Cross-platform parity verified
   - Documented as part of the recommended install path

---

## Consequences

- **Positive:** Discipline drift is harder. Destructive ops require explicit confirmation. Secrets can't slip into commits accidentally. Banned weasel words are caught before delivery.
- **Negative:** Install gets more complex (shell scripts to deploy + maintain). False positives on first-time users may frustrate. Cross-platform parity is real work.
- **Neutral:** No effect on existing workflows that don't use hooks (opt-in).

---

## Open questions

- Should the destructive-op hook block on **all** branches, or only on the configured "protected" set? (Lean: only on configured protected set; respects local-experiment freedom.)
- Should the secret-scan hook scan files BEFORE the edit goes through, or AFTER (PostToolUse on commit)? (Lean: PreToolUse — catch before write.)
- Should the banned-weasel-word hook block the response, or just warn? (Lean: warn for the first 3 occurrences in a session; then block.)

---

## References

- `docs/decisions/ADR-001-lightweight-skill-pack-first.md` — direction reset to lightweight
- `docs/decisions/ADR-004-no-heavy-studio-or-cli.md` — no Studio / daemons / dashboard
- `.bequite/audits/FULL_SYSTEM_ALIGNMENT_AUDIT.md` — alpha.14 audit that surfaced this need
- `.bequite/audits/WORKFLOW_GATE_AUDIT.md` — gate-refusal logic gaps (alpha.15 added explicit refusal sections to 16 commands; this ADR proposes machine enforcement for the safety subset)
- `.bequite/research/BEQUITE_SYSTEM_RESEARCH_REPORT.md` § 7 "Workflow improvements" — risk #2 "convention-enforced gates can be ignored"
- `CLAUDE.md` core operating rules 6 (banned weasel words) + 8 (PhantomRaven defense)
- Claude Code official hooks docs (verify in alpha.17 against current release)
