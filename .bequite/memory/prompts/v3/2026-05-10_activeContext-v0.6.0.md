# Active Context: BeQuite

> The most-edited file in `.bequite/memory/`. Updated at the end of every task. Phase-snapshotted at the end of every phase. Per Iron Law III — read this on session start; this is what tells the next agent where to resume.

---

## Now (last edited: 2026-05-10, end of v0.6.0 + memory snapshot)

- **Active feature:** `BeQuite v1.0.0` (the build of BeQuite itself).
- **Active phase:** `phase-2` per `state/project.yaml::build_phases` — Verification + design module (covers v0.6.0 + v0.6.1).
- **Active sub-version:** v0.6.0 just tagged. Next: **v0.6.1** — Frontend Quality Module (Impeccable bundle + shadcn / 21st.dev Magic / context7 MCP wiring + tokens.css.tpl + axe-core gate config).
- **Last green sub-version:** `v0.6.0` (Verification gates — Playwright walks + verify.py orchestrator).
- **15 tags total** at this snapshot: `v0.1.0` `v0.1.1` `v0.1.2` `v0.2.0` `v0.2.1` `v0.3.0` `v0.4.0` `v0.4.1` `v0.4.2` `v0.4.3` `v0.5.0` `v0.5.1` `v0.5.2` `v0.5.3` `v0.6.0`. Real git counts: 19 commits, 153 tracked files, ~25k lines added net.
- **Constitution version:** `v1.2.0`. Amendment trail: v1.0.0 (v0.1.0 ratification) → v1.0.1 (v0.1.2 master-merge, ADR-008) → v1.1.0 (v0.5.1 Article VIII Scraping, ADR-009) → v1.2.0 (v0.5.2 Article IX Cybersecurity, ADR-010). All additive; no Iron Law removed or relaxed. **9 Iron Laws** (I-VII universal + VIII Scraping + IX Cybersecurity).
- **Active mode:** `auto` (Ahmed authorised autonomous execution; safety rails per `state/project.yaml::safety_rails`).
- **Project mode (BeQuite-itself):** Safe Mode.
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual` (full content lands v0.11.0).
- **Skeptic gate state:** `cleared` for v0.6.0 phase exit — verify.py imports green via `python -m bequite.verify --help`.
- **Cost-ceiling status:** session-default ($20 USD); not tracked yet (receipts ship v0.7.0).
- **Wall-clock-ceiling status:** session-default (6 h); not tracked yet.
- **Remote:** `origin = https://github.com/xpShawky/BeQuite.git` configured. **NOT pushed.** Push remains a one-way door per Iron Law IV; awaits explicit owner authorization (`git push origin main && git push origin --tags`).

## Six operational modules now in place

1. **Skill orchestrator** (v0.2.0) — SKILL.md + 17 personas + routing.json + config TOML.
2. **AI automation module** (v0.2.1) — n8n / Make / Zapier / Temporal / Inngest expert + automation-architect persona + ai-automation Doctrine.
3. **Hooks system** (v0.3.0) — 14 deterministic gates total (10 base + scraping-respect + 3 cyber).
4. **Scraping module** (v0.5.1, Article VIII) — Crawlee / Trafilatura / Firecrawl / Scrapling triad + watch-and-trigger pattern + scraping-engineer persona + polite-mode preset + watch-budget.
5. **Cybersecurity module** (v0.5.2, Article IX) — Trivy / Semgrep / OSV / Strix + scan-and-trigger pattern + 4 personas (security-auditor + pentest-engineer + cve-watcher + disclosure-timer) + RoE template + 3 new Doctrines (vibe-defense / mena-pdpl / eu-gdpr).
6. **Verification gates** (v0.6.0) — walkthrough templates (admin/user) + seed.spec.ts + playwright.config.ts + self-walk + smoke + verify.py orchestrator (17-gate per-Mode matrix).

## Three working Python modules (runnable today from local checkout)

```bash
python -m cli.bequite.audit              # Constitution + Doctrine drift detector (v0.4.2)
python -m cli.bequite.freshness --all    # Knowledge probe (v0.4.3)
python -m cli.bequite.verify             # Phase 6 validation mesh (v0.6.0)
```

All three smoke-tested via `python -m`; help output prints correctly. CLI thin wrapper at `cli/bequite/__main__.py` (v0.5.0) wires all three under the `bequite` console script alongside `discover` / `research` / `decide-stack` / `plan` / `implement` / `review` / `validate` / `recover` / `evidence` / `release` / `auto` / `cost` / `memory show|validate` / `skill install` / `design audit|craft` (skill-dispatch stubs; live API call lands v0.6.1+).

## What I'm doing right now (after this snapshot)

Continuing to **v0.6.1 — Frontend Quality Module**. Per the build plan:

1. Vendor `pbakaus/impeccable` at a pinned commit at `skill/skills-bundled/impeccable/`. Attribute Paul Bakaus in `ATTRIBUTION.md` (MIT-license-respecting). Note: Impeccable verified as `~26.6k stars, 23 commands` per session research.
2. Wire 23 Impeccable commands as `bequite design <command>` aliases (already structurally in place via v0.4.0 `design-audit` + `impeccable-craft` slash-commands; v0.6.1 wires the 23 specific names).
3. shadcn registry MCP wiring (built into shadcn CLI v3+ per session research; not third-party).
4. 21st.dev Magic MCP wiring (`@21st-dev/magic`); document API-key requirement.
5. context7 MCP wiring (Upstash, version-pinned docs).
6. tweakcn link in stack-matrix; theme JSON template.
7. `templates/tokens.css.tpl` — design tokens with named, deliberate font choice.
8. axe-core gate config in CI workflow.
9. Update `default-web-saas` Doctrine to reference all of the above.

After v0.6.1: v0.7.0 (Receipts JSON) → v0.7.1 (ed25519 signing) → v0.8.0+ per main plan.

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

## Next 5 things I'll do (after this memory snapshot commits)

1. Commit the memory-snapshot chore (this file + progress + recovery + prompts/v3/ snapshot).
2. v0.6.1 — vendor Impeccable + wire Frontend Quality MCPs + tokens.css.tpl + axe-core. Commit + tag.
3. v0.7.0 — Receipts JSON schema + emitter + storage. Commit + tag.
4. v0.7.1 — ed25519 signing + verify-receipts. Commit + tag.
5. v0.8.0+ per main plan (multi-model live, examples, auto-mode, MENA, host adapters, vibe-handoff exporters, docs, release engineering, v1.0.0).

## Heartbeat (auto-mode)

- Last heartbeat: 2026-05-10 (this snapshot).
- Last receipt: none (receipts ship v0.7.0).
- Last commit: `8e088e4 feat(v0.6.0): Verification gates — Playwright walks + verify.py orchestrator`.
- Pending commit: state-snapshot chore.

## Recent decisions (last 12)

```
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
