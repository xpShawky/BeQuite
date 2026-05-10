---
name: cli-tool
version: 1.0.0
applies_to: [cli, terminal-tool]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: cli-tool v1.0.0

> Doctrine for terminal-only CLI tools. No frontend, no UI design rules; instead: argument-parsing discipline, semver, completions, distribution. Loaded by `.bequite/bequite.config.toml::doctrines = ["cli-tool"]`.

## 1. Scope

Tools that ship as a single binary or a single Python entry-point invoked via `cmd args...`. Examples: `bequite` itself, `gh`, `pip`, `kubectl`. Covers argument design, output format, distribution channel, and the testing surface.

**Does NOT cover:** TUI applications with a full-screen interface (those need their own Doctrine — `tui-tool`, future). Web apps (use `default-web-saas`).

## 2. Rules

### Rule 1 — Semver-strict
**Kind:** `block`
**Statement:** Public flag/subcommand surface follows semantic versioning. Removing or renaming a flag is a major bump. Adding a flag is minor. Bug fix is patch.
**Check:** `bequite audit` diffs `--help` output between commits; flags non-additive changes without a major bump.
**Why:** scripts depend on flag names.

### Rule 2 — `--help` and `--version` always
**Kind:** `block`
**Statement:** Every subcommand supports `--help` (no args, prints usage) and `--version` (returns the version + commit SHA).
**Check:** `bequite audit` runs the binary with `--help` and `--version`; expects exit 0 and non-empty output.
**Why:** Unix CLI convention; users will try them.

### Rule 3 — Exit-code discipline
**Kind:** `block`
**Statement:** Exit codes follow:
- `0` — success
- `1` — runtime error (the user's input was valid, the operation failed)
- `2` — usage error (the user's input was invalid; show usage)
- `>2` — domain-specific (documented in `--help`)
**Check:** integration tests assert exit codes per scenario.
**Why:** scripting interoperability.

### Rule 4 — Stdout for output, stderr for diagnostics
**Kind:** `block`
**Statement:** Successful output goes to stdout (pipe-able). All status / progress / log messages go to stderr. Exception: `--quiet` suppresses stderr below errors.
**Check:** integration tests pipe output through `grep` / `jq` to verify clean stdout.
**Why:** pipe interoperability.

### Rule 5 — Plain-text + machine-readable output
**Kind:** `recommend`
**Statement:** Default output is plain text for human reading. Add `--json` (or `--format=json`) for machine-readable output in any subcommand a script might call.
**Check:** advisory; reviewed in design.
**Why:** humans + scripts both consume CLIs.

### Rule 6 — `--no-color` and `NO_COLOR=1`
**Kind:** `block`
**Statement:** Respect the [NO_COLOR](https://no-color.org/) standard and a `--no-color` flag. Default to colour when stdout is a TTY; default to no colour otherwise.
**Check:** integration test pipes output to `cat`; expects no ANSI escapes.
**Why:** logs, CI, accessibility.

### Rule 7 — Bash + zsh + fish completions
**Kind:** `recommend`
**Statement:** Ship completions for bash, zsh, and fish. Document `<tool> completion <shell> > /path/to/completion` in the README.
**Check:** advisory; reviewed in `bequite handoff`.
**Why:** discoverability.

### Rule 8 — Man page from `--help`
**Kind:** `recommend`
**Statement:** Generate a man page from the help output via `help2man` (or equivalent). Ship it in the package; install it on `pip install` / `brew install`.
**Check:** advisory.
**Why:** the Unix way; integrates with `man <tool>`.

### Rule 9 — Distribution: uvx / pipx for Python; npm / brew / apt for binaries
**Kind:** `recommend`
**Statement:** Python CLIs: distribute via PyPI; document `uvx --from <pkg> <cmd>` and `pipx install <pkg>` in the README. Compiled CLIs: distribute via package manager appropriate to OS (homebrew taps for macOS/Linux, scoop or winget for Windows, .deb/.rpm).
**Check:** advisory.
**Why:** users have a package manager; meet them there.

### Rule 10 — No persistent global state without explicit consent
**Kind:** `block`
**Statement:** Don't write to `~/.config`, `~/.cache`, the registry, or any system-wide location without an explicit prompt or `--yes`. Document every file the tool writes in `--help` or the man page.
**Check:** integration test runs the tool in a sandbox; asserts no writes outside CWD.
**Why:** users who run tools in CI / containers / Docker get angry when state leaks.

### Rule 11 — Idempotent operations
**Kind:** `recommend`
**Statement:** Operations that change state SHOULD be idempotent — running them twice has the same effect as running them once. Use `--force` to override safety checks.
**Check:** integration test calls each mutation twice; expects identical end state.
**Why:** scripting reliability.

### Rule 12 — No interactive prompts in a non-TTY
**Kind:** `block`
**Statement:** When stdin / stdout is not a TTY, the tool MUST NOT prompt interactively. Either fail with exit 2 (usage error: "interactive prompt required; use --yes") or accept the operation via flags.
**Check:** integration test pipes input/output; expects no prompt.
**Why:** prompts hang CI.

### Rule 13 — No telemetry without opt-in
**Kind:** `block`
**Statement:** Telemetry is **opt-in only**, never opt-out. Document what's collected. The user controls collection via env var or flag (`--telemetry on/off` or `<TOOL>_TELEMETRY=off`).
**Check:** `bequite audit` greps for telemetry endpoints; expects to find them only behind a config gate.
**Why:** privacy + trust.

## 3. Stack guidance

For Python CLIs (default for BeQuite-itself):
- **Build**: `hatchling` via `pyproject.toml`. Distributable through `uvx --from .` or `pipx install -e .`.
- **Argparse**: `click` (preferred) or `typer` (when type-hint-first). Avoid `argparse` for non-trivial trees.
- **Pretty output**: `rich` (default colour, tables, progress, syntax highlighting).
- **Testing**: `pytest` + `click.testing.CliRunner`.
- **Lint/format**: `ruff` (lint) + `black` or `ruff format` (format).

For compiled CLIs:
- **Rust**: `clap` for argparsing, `anyhow`/`thiserror` for errors, `indicatif` for progress.
- **Go**: `cobra` for commands, `viper` for config.

## 4. Verification

`bequite verify` runs additional gates for CLI projects:

1. **`--help` exits 0 and prints non-empty usage** for every subcommand.
2. **`--version` exits 0 and prints `<name> <version>`**.
3. **Exit-code matrix** — runs each subcommand with bad / good / missing args; asserts exit codes per Rule 3.
4. **Stdout cleanliness** — pipes output through `cat`; asserts no ANSI when `NO_COLOR=1`.
5. **No interactive prompts in non-TTY** — runs with stdin/stdout redirected; asserts no prompt.
6. **Idempotency** — for state-changing subcommands, runs twice; asserts same end state.

## 5. Examples and references

- click: https://click.palletsprojects.com/
- typer: https://typer.tiangolo.com/
- rich: https://rich.readthedocs.io/
- clap: https://docs.rs/clap
- cobra: https://cobra.dev/
- NO_COLOR standard: https://no-color.org/
- help2man: https://www.gnu.org/software/help2man/

Reference CLIs that exemplify this Doctrine: `gh`, `kubectl`, `cargo`, `git`, `ripgrep`.

## 6. Forking guidance

Common forks:
- **`tui-tool`** — adds full-screen TUI rules (textual / ratatui / blessed-contrib).
- **`devops-tool`** — adds destructive-op safety, `--dry-run` flag mandatory, `--yes` required to execute.
- **`oneshot-tool`** — pure stateless transformer (no global config, no caches).

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: cli-tool@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–13 ratified.
```
