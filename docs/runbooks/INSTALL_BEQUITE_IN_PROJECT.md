# Installing BeQuite into a project

This runbook is for **end users** who want BeQuite inside their existing project (or a brand-new empty folder). For developers working on BeQuite itself, see `docs/runbooks/LOCAL_DEV.md`.

---

## TL;DR

```powershell
# Windows
cd <your-project>
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
# macOS / Linux
cd <your-project>
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

Open Claude Code in `<your-project>`. Type `/bequite`. Follow the menu.

---

## What the installer does

1. Refuses to overwrite an existing `.bequite/` (your memory) without `--force`.
2. Downloads BeQuite from `https://github.com/xpShawky/BeQuite` (shallow clone) — or uses `--from-local` if you already have a clone.
3. Copies into your project:
   - `.claude/commands/` — 24 slash commands (markdown files)
   - `.claude/skills/bequite-*` — 7 skills
4. Scaffolds:
   - `.bequite/state/` (5 markdown files with sensible defaults)
   - `.bequite/logs/` (3 markdown files, empty)
   - `.bequite/prompts/{user_prompts,generated_prompts,model_outputs}/`
   - `.bequite/{audits,plans,tasks}/`
5. Appends a short "BeQuite" section to your `CLAUDE.md` (or creates one if missing).
6. Prints next steps.

**What it does NOT do:**

- Install any package
- Touch your `package.json` / `pyproject.toml` / `Cargo.toml`
- Modify any of your source code
- Start any process
- Open any network connection except the initial download

---

## Prerequisites

- **git** — to clone BeQuite (used by the installer)
- **PowerShell 5.1+** (Windows) or **bash** (macOS / Linux)
- **Claude Code** — to actually use the commands after install

That's it. No Node, no Python, no Docker for BeQuite itself.

---

## After install

Open Claude Code in your project. The slash commands appear in the picker. Start with:

```
/bequite              # the menu
```

You'll see:

```
BeQuite by xpShawky — lightweight project skill pack
Plan it. Build it. Be quiet.

Status:
  Project type:    <detected>
  BeQuite state:   <fresh after install>
  Current phase:   <Phase 0>
  Last run:        none

Recommended next 3 commands:
  1. /bq-init        formally initialize (writes baseline state)
  2. /bq-discover    inspect this repo + write DISCOVERY_REPORT.md
  3. /bq-doctor      environment health check
```

Run them in order. Each writes its output to `.bequite/`. You'll have a project map within ~5 minutes.

---

## Common workflows

### A — existing project, want to improve quality

```
/bequite              menu
/bq-init              initialize
/bq-discover          inspect (writes DISCOVERY_REPORT.md)
/bq-doctor            environment health (writes DOCTOR_REPORT.md)
/bq-audit             full audit (writes FULL_PROJECT_AUDIT.md with prioritized findings)
/bq-fix <blocker>     fix the first blocker
/bq-fix <next>        next
... iterate ...
/bq-verify            confirm clean
```

### B — new project from scratch

```
/bequite              menu
/bq-init new          initialize as new project
/bq-clarify           answer 3-5 high-value questions (recommended defaults available)
/bq-research          verify your library picks aren't deprecated (optional)
/bq-plan              write IMPLEMENTATION_PLAN.md (no code yet)
/bq-assign            break the plan into atomic tasks
/bq-implement         workhorse — one task at a time
/bq-test              after each implement
/bq-verify            before shipping
/bq-release           ship
```

### C — adding a feature to an existing project

```
/bequite              menu
/bq-add-feature "csv export on bookings page"
                      writes mini-spec, asks for approval, implements, tests
/bq-review            review your own changes
/bq-verify            full gate matrix
```

### D — resuming after a break

```
/bq-recover           reads .bequite/ memory, tells you exactly where you left off + what's safe to do next
```

---

## Updating BeQuite

To update an existing install to a newer version:

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex -Force
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash -s -- --force
```

`--Force` / `--force` overwrites `.claude/commands/` and `.claude/skills/` with the latest. **Your `.bequite/` memory is preserved.**

---

## Uninstalling

BeQuite leaves no system traces. To remove:

```powershell
Remove-Item -Recurse -Force .\.claude\commands\bequite.md, .\.claude\commands\bq-*.md
Remove-Item -Recurse -Force .\.claude\skills\bequite-*
Remove-Item -Recurse -Force .\.bequite
```

```bash
rm -rf .claude/commands/{bequite.md,bq-*.md} .claude/skills/bequite-* .bequite/
```

And edit your `CLAUDE.md` to remove the `<!-- BEQUITE -->` section.

---

## Troubleshooting

### `irm ... | iex` says "running scripts is disabled"

PowerShell execution policy. Run once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then re-run the installer.

### `git clone` fails

The installer needs git. Install from https://git-scm.com or `winget install Git.Git`.

If you have a private git proxy / SSH-only setup, use `--from-local`:

```powershell
git clone https://github.com/xpShawky/BeQuite.git C:\dev\BeQuite
cd <your-project>
C:\dev\BeQuite\scripts\install-bequite.ps1 -FromLocal C:\dev\BeQuite
```

### "BeQuite appears to already be installed here"

Expected if you already installed. Re-running won't overwrite your `.bequite/` memory without explicit `--force`. If you really want to start over:

```powershell
Remove-Item -Recurse -Force .\.bequite, .\.claude\commands\bq-*.md, .\.claude\skills\bequite-*
irm ... | iex
```

### Claude Code doesn't show the `/bequite` command

- Make sure you're in the project directory (not a parent).
- Reload Claude Code's window.
- Check that `.claude/commands/bequite.md` exists at the project root.
- Check the file has YAML frontmatter (`description:` line).

### The CLAUDE.md got messed up

The installer is supposed to append a fenced `<!-- BEQUITE --> ... <!-- /BEQUITE -->` section. If it didn't, edit manually + add a section pointing at `.claude/commands/` + `.bequite/`.

---

## Multiple BeQuite versions on one machine

Each project gets its own `.bequite/` + `.claude/` copy. There's no global install. Updating one project's BeQuite doesn't affect others.

If you want all projects on the same version, re-run the installer in each.

---

## What about the Python CLI?

The Python CLI (`bequite` + `bq` commands) is **optional** and **separate** from the skill pack. The skill pack does everything the CLI does, but from inside Claude Code. The CLI is useful for:

- Scripting / CI usage
- Working outside Claude Code (Cursor, plain terminal, etc.)
- Power users who prefer terminal commands

To install the CLI on top of the skill pack:

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash
```

This is a separate `pip install` flow. The CLI lives in a venv; doesn't interact with the skill pack directly.
