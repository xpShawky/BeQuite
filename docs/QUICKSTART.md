# Quickstart

> Get from zero to a BeQuite-managed project in 5 minutes.

## Prerequisites

- Python ≥ 3.11
- git
- (Optional) `uvx` or `pipx` for the easiest install

## Install

### Today (post-first-push, pre-PyPI)

```bash
git clone https://github.com/xpShawky/BeQuite ~/BeQuite
cd ~/BeQuite/cli
pip install -e .
bequite --version
```

### After v1.0.0 (PyPI)

```bash
uvx bequite init demo --doctrine default-web-saas
# or
pipx install bequite
bequite init demo --doctrine default-web-saas
```

## First project

```bash
# 1. Scaffold
bequite init my-app \
  --doctrine default-web-saas \
  --mode safe \
  --scale small_saas \
  --audience engineer
cd my-app/

# 2. Probe environment
bequite doctor                # checks Python + git + locales + active doctrines

# 3. Plan with multi-model (manual-paste mode; works with your Claude + ChatGPT subscriptions)
bequite plan --multi-model "Build a bookings flow"
# → scaffolds docs/planning_runs/RUN-<datetime>/prompts/
# → paste each prompt into Claude / ChatGPT
# → save responses; bequite models compare && bequite models merge --judge claude

# 4. Single-model planning (or after multi-model finalizes)
bequite discover              # P0 product discovery
bequite decide-stack          # P1 stack ADR (uses bequite freshness probe)
bequite plan                  # P2 plan + contracts
bequite phases                # P3 decompose into phases
bequite tasks                 # P4 atomic tasks (≤5 min each)

# 5. Implement + verify (per task)
bequite implement <task-id>   # P5
bequite review                # P5 cross-cutting review
bequite verify                # P6 — Playwright walks + axe + smoke + audit + freshness
bequite handoff               # P7 — generate HANDOFF.md
```

## Run BeQuite on its own work (eat your own food)

```bash
bequite audit --repo .        # Constitution + Doctrine drift detector
bequite freshness             # registry + license + CVE freshness probe
bequite verify                # full validation mesh
```

## Authentication (Phase-2 stub; Phase-3 in v0.11.x+)

```bash
bequite auth login            # local-identity stub for now
bequite auth whoami
bequite auth status
```

CI mode:

```bash
BEQUITE_CI_MODE=true BEQUITE_API_KEY=sk-... bequite ...
```

## Auto-mode (one-click run-to-completion)

```bash
bequite auto run \
  --feature "add-health-endpoint" \
  --max-cost-usd 5 \
  --max-wall-clock-hours 2 \
  --mode auto
```

Auto-mode walks P0 → P7 with safety rails (cost ceiling, wall-clock ceiling, banned-word check, hook-block respect). Pauses at one-way doors (PyPI publish, npm publish, git push to main, etc.).

## Per-host install

```bash
bequite skill install         # detects existing host configs + extends each
bequite skill install --host cursor   # specific host
```

Supports: claude-code / cursor / codex / cline / kilo / continue / aider / windsurf / gemini.

## Cross-references

- `docs/HOW-IT-WORKS.md` — architecture deep-dive
- `docs/HOSTS.md` — per-host install + behavior notes
- `docs/AUTONOMOUS-MODE.md` — auto-mode safety rails + recovery
- `docs/DOCTRINE-AUTHORING.md` — fork or write your own Doctrine
- `docs/SECURITY.md` — threat model + Article IV + Article IX
- `.bequite/memory/constitution.md` — the Iron Laws

## Troubleshooting

| Symptom | Try |
|---|---|
| `bequite: command not found` | `pip install -e cli/` from BeQuite source root |
| Hook fails on commit | Read the hook's stderr; it tells you exactly what's blocked + why |
| `bequite verify` red | Read evidence/<phase>/; fix the failing gate; rerun. Do not bypass. |
| Multi-model paste workflow unclear | See `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md` §4 |
| Auth says "not signed in" | Phase-3 device-code flow lands v0.11.x+; Phase-2 ships local-identity stub |
