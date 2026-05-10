# Example 02 — AI tool wrapper (`mdsum`)

> A Python CLI that summarises a Markdown file using Claude. Demonstrates BeQuite's `cli-tool` Doctrine end-to-end: minimal scaffold, semver discipline, no UI, man-page generation, bash completions.

## What it does

```bash
mdsum README.md                          # prints a 5-bullet summary to stdout
mdsum docs/HOW-IT-WORKS.md --bullets 10  # configurable depth
mdsum --version                          # prints version
mdsum --help                             # prints help
```

## Stack (decided in P1)

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | matches BeQuite itself; tomllib in stdlib |
| Build | hatchling | Doctrine-recommended; standard PEP 517 |
| CLI framework | click | Mature, well-documented, BeQuite's choice |
| Output formatting | rich | Pretty terminal output without bloat |
| HTTP | httpx | Sync + async; preferred over requests |
| LLM provider | anthropic SDK (primary) + openai SDK (alt via `bequite[openai]` extra) | Reuse BeQuite providers/ adapters where possible |
| Distribution | uvx + pipx + PyPI | Same as BeQuite |
| Tests | pytest | |

## Phases

### P0 — Discovery
"What's the minimum useful summariser?" Answer: take a markdown file, return N bullets, configurable model + bullets count.

### P1 — Stack ADR
See `.bequite/memory/decisions/ADR-001-stack.md`.

### P2 — Plan + Contracts
- Single command: `mdsum <file> [--bullets N] [--model M] [--reasoning-effort low|default|high]`
- Reads file, sends prompt to Claude, returns formatted bullets via rich.
- Errors: file not found → exit 2 + clear message; API error → exit 1 + redacted error; truncation → warn.

### P3 — Phases
- phase-1: scaffold + `--help` works
- phase-2: API call + summarise + format
- phase-3: tests + man-page + completions

### P4 — Tasks
Atomic per-phase; see `specs/markdown-summariser/tasks.md` (placeholder).

### P5 — Implementation
Single file `mdsum/__main__.py` (~80 lines). Single responsibility — file → summary.

### P6 — Verify
- pytest covering: missing file (exit 2), too-large file (>1MB warn), happy path (mocked Anthropic response).
- `mdsum --help` man-page-able output.
- Smoke: `mdsum README.md` runs in < 5s for a 5KB file.

### P7 — Handoff
README + `--help` + man page. No screencast needed (CLI tool).

## Doctrine compliance

`cli-tool` Doctrine: no UI doctrine; man-page generation; semver discipline; bash completions. PASS:
- Man page via click's `--help` rendered with `click-man`.
- Semver enforced by hatchling + tagged releases.
- Bash completion via `_MDSUM_COMPLETE=bash_source mdsum > /etc/bash_completion.d/mdsum`.

## Cost (per invocation)

At default `claude-haiku-4-5`:
- 1KB markdown ≈ 250 input tokens.
- 5-bullet summary ≈ 100 output tokens.
- Cost: $0.0002 + $0.0004 = ~$0.0006 per invocation.
- 1000 invocations/day = ~$0.60/day = ~$18/mo.

## Cross-references

- Doctrine: `../../skill/doctrines/cli-tool.md`
- ADR: `.bequite/memory/decisions/ADR-001-stack.md`
- Provider adapters reused: `../../cli/bequite/providers/anthropic.py` (v0.8.0)
- Pricing: `../../cli/bequite/pricing.py` (v0.8.1)
