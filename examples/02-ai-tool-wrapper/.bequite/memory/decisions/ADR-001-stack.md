---
adr: 001
title: Stack decision for example-02-ai-tool-wrapper (mdsum)
status: accepted
date: 2026-05-10
deciders: BeQuite v0.9.0 author
supersedes: null
---

# ADR-001 — Stack for `mdsum` CLI

## Context

A minimal CLI that takes a Markdown file and returns a Claude-generated bulleted summary. Doctrine is `cli-tool`. Must be:
- Distributable via `uvx`/`pipx`/PyPI.
- Single-file installable (no DB, no web server).
- Cheap to invoke (< $0.001 per call at default model).

## Decision

| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| Build | hatchling |
| CLI | click |
| Output | rich |
| HTTP | httpx |
| LLM (primary) | anthropic SDK |
| LLM (alt) | openai SDK (extra) |
| Tests | pytest |
| Lint | ruff |
| Type-check | mypy |

## Rationale

**Python 3.11+.** Matches BeQuite's own stack. `tomllib` in stdlib (no `tomli` dep needed). f-strings + match-case + structural pattern matching handy for argument parsing.

**hatchling.** Modern PEP 517 builder. `pyproject.toml`-driven. Generates wheels + sdists cleanly.

**click.** Most mature Python CLI framework. Better than argparse for nested subcommands; better than typer for stability (typer wraps click anyway). Native bash/zsh/fish completions via `_MDSUM_COMPLETE` env var.

**rich.** For pretty terminal output. Tables, colored text, markdown rendering. Avoids hand-rolling ANSI codes.

**httpx.** Sync + async. Preferred over `requests` (which doesn't expose async). Used here only for the LLM call.

**anthropic SDK (primary).** First-class Claude support. Already in BeQuite's deps.

**openai SDK (alt).** Available via `pip install mdsum[openai]`. For users who prefer GPT-5 or who run on OpenAI-compatible endpoints (Together, Fireworks).

**pytest + ruff + mypy.** Standard Python QA stack.

## Reuses BeQuite

This example **reuses** BeQuite's provider adapters via:

```python
from bequite.providers import get_provider
from bequite.pricing import pricing_for
```

That is: `mdsum` is *also* a consumer of the BeQuite library, demonstrating that the Layer 1 Harness's Python modules are reusable.

## Alternatives considered

- **typer instead of click.** Wraps click; adds type-hint inference. Rejected: extra dependency for marginal benefit.
- **rye/poetry/pdm instead of hatchling.** Rejected: hatchling is the BeQuite default; consistency wins.
- **prompt-toolkit for interactive mode.** Rejected: out of scope for v1; this CLI is fire-and-forget.

## Consequences

- Single-file install via `uvx mdsum`.
- Reusable as a Python library (`from mdsum import summarise`).
- One-line bash completion install.
- Versioned + semver-enforced via hatchling.

## Doctrine compliance (`cli-tool`)

- ✅ Semver discipline: hatchling + tagged releases.
- ✅ Man page: `click-man` generates from click decorators.
- ✅ Bash/zsh/fish completions: built into click.
- ✅ No telemetry without opt-in: this CLI sends only the file content + the LLM prompt — no usage tracking.
- ✅ Public API freezing: any function added with a leading underscore is private; module-level helpers are public + versioned.

## Status: accepted (2026-05-10)
