# Active Context: BeQuite

> The most-edited file in `.bequite/memory/`. Updated at the end of every task. Phase-snapshotted at the end of every phase. Per Iron Law III — read this on session start; this is what tells the next agent where to resume.

---

## Now (last edited: 2026-05-10, end of v0.7.1)

- **Active feature:** `BeQuite v1.0.0` (the build of BeQuite itself).
- **Active phase:** `phase-3` per `state/project.yaml::build_phases` — Reproducibility + economics (v0.7.0 + v0.7.1 done; v0.8.x next).
- **Active sub-version:** v0.7.1 just tagged. Next: **v0.8.0** — Multi-model routing live (AiProvider adapters: Anthropic + OpenAI + Google + DeepSeek + Ollama; cost ceiling enforcement via stop-cost-budget hook; receipts emit with each model invocation).
- **Last green sub-version:** `v0.7.1` (Signed receipts — ed25519 keypair on init + sign-at-emission + `bequite verify-receipts` validator + 9-test integration suite all passing; total receipts+signing tests: 19/19 green on Python 3.14).
- **18 tags total** at this snapshot: `v0.1.0` `v0.1.1` `v0.1.2` `v0.2.0` `v0.2.1` `v0.3.0` `v0.4.0` `v0.4.1` `v0.4.2` `v0.4.3` `v0.5.0` `v0.5.1` `v0.5.2` `v0.5.3` `v0.6.0` `v0.6.1` `v0.7.0` `v0.7.1`. Real git counts (post-v0.7.1): ~23 commits, ~173+ tracked files, ~30k lines added net.
- **Constitution version:** `v1.2.0`. Amendment trail: v1.0.0 (v0.1.0 ratification) → v1.0.1 (v0.1.2 master-merge, ADR-008) → v1.1.0 (v0.5.1 Article VIII Scraping, ADR-009) → v1.2.0 (v0.5.2 Article IX Cybersecurity, ADR-010). All additive; no Iron Law removed or relaxed. **9 Iron Laws** (I-VII universal + VIII Scraping + IX Cybersecurity).
- **Active mode:** `auto` (Ahmed authorised autonomous execution; safety rails per `state/project.yaml::safety_rails`).
- **Project mode (BeQuite-itself):** Safe Mode.
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0).
- **Skeptic gate state:** `cleared` for v0.6.0 phase exit — verify.py imports green via `python -m bequite.verify --help`.
- **Cost-ceiling status:** session-default ($20 USD); not tracked yet (receipts ship v0.7.0).
- **Wall-clock-ceiling status:** session-default (6 h); not tracked yet.
- **Remote:** `origin = https://github.com/xpShawky/BeQuite.git` configured. **NOT pushed.** Push remains a one-way door per Iron Law IV; awaits explicit owner authorization (`git push origin main && git push origin --tags`).

## Nine operational modules now in place

1. **Skill orchestrator** (v0.2.0) — SKILL.md + 17 personas + routing.json + config TOML.
2. **AI automation module** (v0.2.1) — n8n / Make / Zapier / Temporal / Inngest expert + automation-architect persona + ai-automation Doctrine.
3. **Hooks system** (v0.3.0) — 14 deterministic gates total (10 base + scraping-respect + 3 cyber).
4. **Scraping module** (v0.5.1, Article VIII) — Crawlee / Trafilatura / Firecrawl / Scrapling triad + watch-and-trigger pattern + scraping-engineer persona + polite-mode preset + watch-budget.
5. **Cybersecurity module** (v0.5.2, Article IX) — Trivy / Semgrep / OSV / Strix + scan-and-trigger pattern + 4 personas (security-auditor + pentest-engineer + cve-watcher + disclosure-timer) + RoE template + 3 new Doctrines (vibe-defense / mena-pdpl / eu-gdpr).
6. **Verification gates** (v0.6.0) — walkthrough templates (admin/user) + seed.spec.ts + playwright.config.ts + self-walk + smoke + verify.py orchestrator (17-gate per-Mode matrix).
7. **Frontend Quality Module** (v0.6.1) — vendored Impeccable bundle (23 commands + principles + anti-patterns + aesthetic targets) + tokens.css.tpl (deliberate font choice + light/dark/RTL/reduced-motion) + frontend-stack reference (verified May-2026 libs with license flags) + frontend-mcps reference (shadcn registry / 21st.dev Magic / context7 / tweakcn) + axe-core gate (workflow tpl + Playwright a11y specs + axe-projects in playwright.config.ts.tpl) + default-web-saas Doctrine v1.0.0 → v1.1.0.
8. **Reproducibility receipts** (v0.7.0) — `cli/bequite/receipts.py` (schema v1: version, session_id, phase, timestamp, model, input{prompt+memory hashes}, output{diff+files}, tools_invoked, tests, cost, doctrine, constitution_version, parent_receipt chain) + `ReceiptStore` at `.bequite/receipts/<sha>-<phase>.json` + chain validation (missing-parent, causality, cycle) + `replay_check` (tampered-prompt detection) + `roll_up_by_session/phase/day` + 10-test integration suite (all passing) + `bequite cost` local-first (offline-friendly per Article III) + `bequite receipts {list,show,validate-chain,roll-up}` Click group.
9. **Signed receipts** (v0.7.1) — `cli/bequite/receipts_signing.py` (ed25519 keypair via `cryptography` library; PEM-encoded; private at `.bequite/.keys/private.pem` mode 0600 gitignored, public at `.bequite/keys/public.pem` mode 0644 committed); `Receipt` schema additive `signature` field; `ReceiptStore.write(sign_with=key)` opt-in signing at write-time; `bequite verify-receipts [--strict]` Click command (signature + chain validation; strict rejects unsigned); `bequite keygen [--overwrite]`; `bequite init` auto-generates keypair + appends gitignore patterns; 9-test integration suite covering keygen lifecycle + sign-verify roundtrip + tampered-body rejection + strict-vs-lenient + cross-paste-signature mismatch detection (all passing).

## Five working Python modules (runnable today from local checkout)

```bash
python -m cli.bequite.audit              # Constitution + Doctrine drift detector (v0.4.2)
python -m cli.bequite.freshness --all    # Knowledge probe (v0.4.3)
python -m cli.bequite.verify             # Phase 6 validation mesh (v0.6.0)
python -m cli.bequite.receipts list      # Reproducibility receipts (v0.7.0)
python -m cli.bequite.receipts_signing keygen   # ed25519 keypair (v0.7.1)
```

All three smoke-tested via `python -m`; help output prints correctly. CLI thin wrapper at `cli/bequite/__main__.py` (v0.5.0) wires all three under the `bequite` console script alongside `discover` / `research` / `decide-stack` / `plan` / `implement` / `review` / `validate` / `recover` / `evidence` / `release` / `auto` / `cost` / `memory show|validate` / `skill install` / `design audit|craft` (skill-dispatch stubs; live API call lands v0.6.1+).

## What I'm doing right now (after this commit)

v0.7.1 just shipped. Continuing to **v0.8.0 — Multi-model routing (cost-aware)** per the main plan:

1. Refresh `skill/routing.json` schema to be cost-aware: `{ phase, persona, model, reasoning_effort, fallback_model, max_input_tokens, max_output_tokens }`.
2. Implement AiProvider adapters in `cli/bequite/providers/`:
   - `anthropic.py` (primary)
   - `openai.py` (planner alt)
   - `google.py` (free-tier doc-gen via Gemini)
   - `deepseek.py` (cheap implementer)
   - `ollama.py` (offline mode)
3. `skill_loader.py` reads routing → picks model per call.
4. Wire `stop-cost-budget.sh` hook to enforce `bequite.config.toml::cost.session_max_usd` ceiling. On hit: pause + ask before continuing.
5. Provider auth via env vars + Doppler/Infisical reference docs.
6. Receipts emit with each model invocation (the v0.7.0+v0.7.1 chain + signing already operational; v0.8.0 just needs the model-call hook).
7. Routing-test fixture forces Sonnet for implementer + Opus for reviewer; receipts confirm.
8. Cost-ceiling test stops correctly when threshold reached.

After v0.8.0: v0.8.1 (live pricing fetch + 24h cache + offline fallback) → v0.9.0 (3 example projects) → v0.9.1 (e2e harness) → v0.10.0 (auto-mode state machine + safety rails + heartbeat) → v0.10.1 (auto-mode hardening) → v0.11.0 (MENA bilingual) → v0.12.0 (host adapters) → v0.13.0 (vibe-handoff exporters) → v0.14.0 (docs) → v0.15.0 (release-eng) → **v1.0.0**.

## Open questions (none blocking)

- [ ] E1 — GitHub org / repo name: `xpShawky/BeQuite` confirmed (Ahmed created the repo). Push when authorized.
- [ ] E2 — PyPI package name + ownership — blocks v0.5.0 PyPI release / v1.0.0 final.
- [ ] E3 — Studio (v2.0.0+) timing (after v1.0.0).
- [ ] E4 — Telemetry policy (off entirely; pending ADR-002 in v0.7.0).
- [ ] E5 — Doctrine distribution model (separate org for community; pending v0.12.0).
- [ ] E6 — MENA bilingual Researcher seeds (Ahmed seeds list at v0.11.0).
- [ ] E7 — Codex 5.5 review-mode role (pending v0.8.0).

## Blockers

| Blocker | Why it blocks | Owner | Mitigation |
|---|---|---|---|
| (none) | | | |

## Next 5 things I'll do (after this v0.7.1 commit)

1. v0.8.0 — Multi-model routing live (AiProvider adapters: Anthropic + OpenAI + Google + DeepSeek + Ollama). routing.json cost-aware schema. stop-cost-budget hook. Receipts emit per model call. Commit + tag.
2. v0.8.1 — Live pricing fetch (24h cache, offline fallback). Vendor-pricing-changed warnings. Commit + tag.
3. v0.9.0 — Three example projects (bookings-saas Next/Hono/Supabase + ai-tool-wrapper CLI + tauri-note-app desktop) with full seven-phase walks executed. Commit + tag.
4. v0.9.1 — E2E test harness (seven-phase walk + auto-mode + doctrine-loading) + `examples-e2e.yml` CI workflow. Commit + tag.
5. v0.10.0 — Auto-mode state machine + safety rails (cost ceiling, wall-clock ceiling, 3-failure threshold, banned-word check, hook-block respect, one-way-door pauses) + heartbeat (`activeContext.md` every 5 min). Commit + tag.

## Heartbeat (auto-mode)

- Last heartbeat: 2026-05-10 (v0.7.1 close).
- Receipts emit + verify operational; first auto-mode receipt lands when v0.10.0 wires phase transitions.
- Last commit (pending): `feat(v0.7.1): Signed receipts — ed25519 keypair + sign-at-emission + bequite verify-receipts + 9-test signing suite`.

## Recent decisions (last 12)

```
2026-05-10  v0.7.1 Signed receipts: ed25519 via cryptography library (already in deps); per-project keypair (private gitignored, public committed). Strict-mode opt-in for v0.7.1 to allow gradual adoption; flip-to-default decision deferred to v0.10.0 when auto-mode wires emit-with-signing as the only path. ReceiptStore.write(sign_with=) keeps filenames deterministic from inputs (allowing key rotation without breaking chain pointers). Integration suite proves: keygen lifecycle (creates / refuses-overwrite / explicit-overwrite); sign-verify roundtrip; tamper rejection; cross-paste-signature rejection; strict-vs-lenient.

2026-05-10  v0.7.0 Reproducibility receipts: schema v1 dataclass-based (stdlib-only runtime; no pydantic dependency at receipt-time) — keeps receipts emittable from any environment that has python ≥ 3.11. ReceiptStore is filesystem-only (no DB) for offline-friendliness per Article III. Chain-hashing uses sha256 over canonical-JSON (sorted keys, no whitespace, None-stripped) — deterministic across OSes. validate_chain checks missing-parent + causality (parent.ts ≤ child.ts, allowing equality for same-second emissions) + cycle. Cost rollups across session/phase/day. CLI: `bequite cost` walks .bequite/receipts/ first (offline-first), falls through to skill-dispatch only when no receipts. New `bequite receipts {list,show,validate-chain,roll-up}` Click group. 10-test integration suite (tests/integration/receipts/test_receipts_smoke.py) all passing on Python 3.14.

2026-05-10  v0.6.1 Frontend Quality Module: vendored Impeccable (MIT, attributed, pinned) + tokens.css.tpl with deliberate font choice (Doctrine Rule 2 enforcement at the template level) + frontend-stack reference with license flags (Sentry BSL/FSL flagged; AGPL components flagged for closed-source distribution) + frontend-mcps reference (shadcn registry as built-in MCP since CLI v3+; 21st.dev Magic with API-key requirement; context7 free; tweakcn as visual-only) + axe gate as Playwright projects (axe-admin / axe-user) + workflow template + per-route JSON evidence. default-web-saas Doctrine bumped 1.0.0 → 1.1.0 (additive only).
2026-05-10  v0.6.0 verify.py: 17-gate matrix per Constitution v1.0.1 §4. Per-stack command detection. Stops on first required-gate failure (Article II + master §3.7).
2026-05-10  v0.5.3: URL casing → xpShawky/BeQuite; line counts corrected to git-verified numbers; uvx commands reframed as post-first-push (honest reporting per Article VI).
2026-05-10  Remote configured at https://github.com/xpShawky/BeQuite.git. NOT pushed; awaits owner authorization.
2026-05-10  ADR-010 accepted: Article IX Cybersecurity. Four senior amendments: internal RT carve-out (8 guardrails), cryptojackers added, defensive-validation clause, plural disclosure frameworks.
2026-05-10  ADR-009 accepted: Article VIII Scraping. Four senior amendments: rate-limit 1 req/3 sec, stealth requires legitimate-basis enum, captcha clause added, watch-budget added.
2026-05-10  Three new Doctrines (v0.5.2): vibe-defense (DEFAULT for audience: vibe-handoff; 15 strict rules per Veracode 2025 45% finding), mena-pdpl (jurisdiction-branched Egypt/KSA/UAE), eu-gdpr (12 rules).
2026-05-10  Two new personas (v0.5.2): security-auditor (defensive) + pentest-engineer (RoE-gated offensive). Plus support: cve-watcher + disclosure-timer = 4 new in v0.5.2.
2026-05-10  ADR-008 accepted (v0.1.2): two-layer architecture; Constitution v1.0.0 → v1.0.1.
2026-05-10  DEC-007 personas merge: master's 10 + Skeptic + automation-architect = 12, then v0.5.1/v0.5.2 added scraping-engineer + 4 cyber = 17 personas total.
2026-05-10  DEC-008 slash commands: 12 master + 7 unique = 19 commands.
2026-05-10  DEC-002 Skill-first distribution; CLI is thin Python wrapper.
2026-05-10  DEC-004 Full v1 power from day 1; autonomous execution authorised.
```
