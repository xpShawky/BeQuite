# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-2` — Verification + design module (covers v0.6.0 + v0.6.1, both COMPLETE).
- **Sub-version:** Just tagged `v0.6.1`. Next: **`v0.7.0`** (Reproducibility receipts).
- **Last green sub-version:** `v0.6.1` (Frontend Quality Module — vendored Impeccable + tokens.css.tpl + frontend-stack reference + frontend-mcps reference + axe-core gate; default-web-saas Doctrine v1.0.0 → v1.1.0).
- **Mode:** Safe Mode (master §4)
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0)
- **Constitution version:** `v1.2.0` (9 Iron Laws; Modes; 12 Doctrines; Definition-of-done)

## What this sub-version (just tagged) shipped

`v0.6.1` is the **Frontend Quality Module**. Wires the design discipline the brief demanded.

Completed:
- ✅ `skill/skills-bundled/impeccable/` — vendored snapshot of pbakaus/impeccable (MIT, attributed). `.pinned-commit` + `ATTRIBUTION.md` + `README.md` + `SKILL.md` + `references/{principles,anti-patterns,aesthetic-targets}.md` + `commands/CATALOG.md` + `commands/{craft,audit,harden,polish}.md` (4 marquee dispatch contracts; remaining 19 catalogued in CATALOG.md).
- ✅ `skill/templates/tokens.css.tpl` — design tokens with deliberate font-choice comment (Doctrine Rule 2 enforced at the template level), 3-color system (primary + neutral + accent + system-state), strict 4/8/12/16/24/32/48/64/96/128 spacing scale, restrained radius/shadow tokens, ease-out motion (NEVER bounce/elastic; Doctrine Rule 6), light + dark theme overrides, `[dir="rtl"]` overrides for `mena-bilingual` (Tajawal/Cairo/Readex Pro), `prefers-reduced-motion` handling.
- ✅ `skill/references/frontend-stack.md` — verified May-2026 library list with license flags (Sentry BSL/FSL post-2023; AGPL components flagged for closed-source distribution).
- ✅ `skill/references/frontend-mcps.md` — wiring guide: shadcn registry MCP (built into shadcn CLI v3+; no separate install), 21st.dev Magic MCP (`@21st-dev/magic`; API key required), context7 MCP (Upstash; free), tweakcn (visual theme editor; not an MCP).
- ✅ axe-core gate: `skill/templates/.github/workflows/axe.yml.tpl` (workflow template; PR + nightly + manual; HTML+JSON evidence retained 30d) + `skill/templates/tests/a11y/{admin,user}/axe-{admin,user}.spec.ts.tpl` (per-route axe analysis with WCAG 2.0+2.1 A+AA tags) + `skill/templates/playwright.config.ts.tpl` extended with `axeProjects` (axe-admin + axe-user).
- ✅ `skill/doctrines/default-web-saas.md` bumped 1.0.0 → 1.1.0 (additive only — Rules 1–14 unchanged in behavior; new section 5 cross-references all v0.6.1 artifacts; sections 6/7/8 renumbered).
- ✅ `cli/bequite/__init__.py::__version__` → `0.6.1`. `cli/pyproject.toml::version` → `0.6.1`.
- ✅ `CHANGELOG.md` — v0.6.1 entry added with full artifact + bump details.

## Next sub-version

After `v0.6.1`: **`v0.7.0` — Reproducibility receipts (JSON)**.

Tasks for v0.7.0:
1. `cli/bequite/receipts.py` — Pydantic-modeled receipt emitter.
2. Schema: version + session_id + phase + timestamp_utc + model{name, reasoning_effort, fallback_model} + input{prompt_hash, memory_snapshot_hash} + output{diff_hash, files_touched} + tools_invoked[] + tests + cost{input_tokens, output_tokens, usd} + doctrine[] + constitution_version + parent_receipt (chain hash).
3. Storage at `.bequite/receipts/<sha>-<phase>.json`.
4. `bequite cost` walks receipts and rolls up.
5. Receipt-replay test reconstructs prompt + memory state.
6. Updates: `cli/bequite/__init__.py` + `cli/pyproject.toml` → `0.7.0`; CHANGELOG entry; activeContext + progress + recovery; commit + tag.

After v0.7.0: v0.7.1 (ed25519 signing), v0.8.0 (multi-model live), v0.8.1 (live pricing), v0.9.0 (3 examples), v0.9.1 (e2e harness), v0.10.0 (auto-mode), v0.10.1 (auto-mode hardening), v0.11.0 (MENA bilingual), v0.12.0 (host adapters), v0.13.0 (vibe-handoff exporters), v0.14.0 (docs), v0.15.0 (release-eng), **v1.0.0** (final).

## Open questions (none blocking)

- E1 — GitHub org / repo: `xpShawky/BeQuite` confirmed (Ahmed created; remote configured `origin = https://github.com/xpShawky/BeQuite.git`; NOT pushed).
- E2 — PyPI package name + ownership — blocks v0.5.0 PyPI release / v1.0.0 final.
- E3 — Studio (v2.0.0+) timing — after v1.0.0 ships.
- E4 — Telemetry policy — off entirely; pending ADR-002 in v0.7.0.
- E5 — Doctrine distribution model (community fork org) — pending in v0.12.0.
- E6 — MENA bilingual Researcher seeds — Ahmed seeds list at v0.11.0.
- E7 — Codex 5.5 review-mode role — review-only default; pending v0.8.0.

None of these block v0.7.0+ progress.

## Cost / wall-clock telemetry (this session)

Receipts ship in v0.7.0; until then, telemetry is best-effort.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
