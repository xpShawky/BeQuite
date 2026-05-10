# bequite — BeQuite Layer 1 Harness CLI

> **Build it right the first time. No chatter. No debug spirals.**

The Python CLI for [BeQuite](https://github.com/xpShawky/BeQuite) — a host-portable harness that turns Claude (and any peer coding agent — GPT-5, Codex, Cursor, Cline, Roo, Kilo) into a senior tech-lead capable of shipping software projects from research to handoff **without producing the broken half-builds that dominate today's "vibe coding" output.**

By **xpShawky** ([Ahmed Shawky](https://github.com/xpShawky)). MIT licensed.

This package installs two console scripts (`bequite` and `bq`) and exposes the BeQuite Skill + Memory Bank + Hooks + Doctrines + Templates to any project that opts in via `bequite init`.

## Install

### From PyPI (post-publish; Ahmed-gated)

```bash
uvx bequite --version
# or
pipx install bequite
# or
pip install bequite
```

### From a local clone (works today)

```bash
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -e ./cli
bequite --version
```

## Quickstart

```bash
# Initialize a new project
bequite init my-app --doctrine default-web-saas --scale small_saas
cd my-app

# Run the full 7-phase workflow with safety rails
bequite auto --feature "booking flow" --max-cost-usd 10
```

`bequite auto` runs **P0 Research → P7 Handoff** sequentially with phase-by-phase commits, Skeptic gates at every boundary, hard cost ceiling, hard wall-clock ceiling, and a 3-failure-threshold pause-for-human. Auto-mode never bypasses hooks, never auto-runs one-way-door operations, and never skips Phase 0.

## Command surface (19+ subcommands)

| Command | What it does |
|---|---|
| `init` | Scaffold a new BeQuite project (`.bequite/`, AGENTS.md, CLAUDE.md, per-host adapters) |
| `research` | P0 — find prior art, cited findings |
| `stack` | P1 — educational stack ADR + freshness probe + scale dialog |
| `plan` | P2 — spec + plan + data-model + contracts |
| `phases` | P3 — decompose plan into atomic phase artifacts |
| `tasks` | P4 — atomic task lists (≤5 min each, dependency-ordered) |
| `implement` | P5 — TDD discipline + per-task commit + receipt |
| `verify` | P6 — Playwright walks + smoke + secret-scan + axe-core |
| `review` | Senior code review (13 categories) |
| `handoff` | P7 — engineer + non-engineer HANDOFF.md + screencast checklist |
| `audit` | Constitution + Doctrine drift detector |
| `freshness` | Knowledge probe — verify packages aren't deprecated, EOL'd, replaced |
| `auto` | One-click P0→P7 with 8 safety rails |
| `doctor` | Environment + scaffolding diagnostic |
| `resume` | Reload Memory Bank + state + last green phase |
| `receipts` | List / show / validate-chain / roll-up signed reproducibility receipts |
| `verify-receipts` | Validate ed25519 chain integrity |
| `keygen` | Generate per-project ed25519 keypair |
| `route` | Multi-model routing config (show / list / providers) |
| `pricing` | Refresh / show / list vendor pricing (24h cache + fallback) |
| `ledger` | Token + dollar cost roll-up |
| `auth` | Local-identity login / logout / status / refresh |
| `multi-model` | Multi-model planning (scaffold / compare / merge) |
| `skill install` | Install BeQuite into a host (Claude Code, Cursor, Codex, Cline, Kilo, Continue, Aider, Windsurf, Gemini) |
| `export` | Export project as spec-kit-zip or claude-code-skill bundle |

Run `bequite --help` or `bequite <command> --help` for full details.

## What BeQuite prevents

Current AI coding tools routinely:
- Build a frontend without a working backend
- Hallucinate libraries (PhantomRaven campaign — Koi Security 2025)
- Generate UIs with AI-slop tells (Inter default, purple-blue gradients, gray-on-color)
- Leak secrets to client code (Veracode 2025: ~45% of generated code has OWASP Top-10 issues)
- Hand off "I built X, please test" without booting the app
- Lose all context between sessions

BeQuite prevents these errors with **deterministic gates** instead of fixing them after the fact:
- Versioned Constitution (Iron Laws + forkable Doctrines)
- Six-file Memory Bank (Cline pattern)
- PreToolUse hooks that block destructive operations, secret writes, hallucinated package imports
- Skeptic-as-adversary at every phase boundary
- ed25519-signed reproducibility receipts
- Knowledge-freshness probes before stack picks
- Verification gate (Playwright admin + user walks, smoke tests, axe-core, secret scan)
- Banned weasel-words (`should`, `probably`, `seems to`) trigger exit-code-2 violations

## Doctrines (13 shipped)

`default-web-saas`, `cli-tool`, `ml-pipeline`, `desktop-tauri`, `library-package`, `fintech-pci`, `healthcare-hipaa`, `gov-fedramp`, `ai-automation`, `vibe-defense`, `mena-pdpl`, `eu-gdpr`, `mena-bilingual`.

## Hosts (9)

Claude Code, Cursor, Codex CLI, Gemini CLI, Windsurf, Cline, Kilo Code, Continue.dev, Aider. Per-host install: `bequite skill install`.

## Related

- **Layer 2 Studio Edition** — `studio/marketing/` (cinematic landing) + `studio/dashboard/` (Next.js operations console with xterm.js terminal) + `studio/api/` (Hono on Bun). See [`v2.0.0-alpha.1` release notes](../docs/RELEASES/v2.0.0-alpha.1.md).
- **Constitution** — [`.bequite/memory/constitution.md`](../.bequite/memory/constitution.md) — Iron Laws + Doctrine references.
- **Repo** — https://github.com/xpShawky/BeQuite
- **Issues** — https://github.com/xpShawky/BeQuite/issues

## License

MIT. See [LICENSE](../LICENSE).
