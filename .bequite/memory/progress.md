# Progress: BeQuite

> The evolution log. What works, what's left, what changed and why.

---

## Current state

- **Sub-version:** v0.7.0 just tagged. **17 sub-versions tagged: v0.1.0 / v0.1.1 / v0.1.2 / v0.2.0 / v0.2.1 / v0.3.0 / v0.4.0 / v0.4.1 / v0.4.2 / v0.4.3 / v0.5.0 / v0.5.1 / v0.5.2 / v0.5.3 / v0.6.0 / v0.6.1 / v0.7.0.** Counts (git-verified post-v0.7.0, pre-commit): ~22 commits, ~170+ tracked files, ~29k lines added net. (Earlier "30,000+/22,000+/13,000+" estimates were inflated; corrected per Article VI honest reporting.)
- **Constitution version:** `1.2.0`. Amendment trail: v1.0.0 (v0.1.0 ratification) → v1.0.1 (v0.1.2 master-merge, ADR-008) → v1.1.0 (v0.5.1 Article VIII Scraping, ADR-009) → v1.2.0 (v0.5.2 Article IX Cybersecurity, ADR-010). All additive; no Iron Law removed or relaxed.
- **Active doctrines (BeQuite-itself):** `library-package`, `cli-tool`, `mena-bilingual`. 12 Doctrines shipped for downstream projects (`default-web-saas`, `cli-tool`, `ml-pipeline`, `desktop-tauri`, `library-package`, `fintech-pci`, `healthcare-hipaa`, `gov-fedramp`, `ai-automation`, `vibe-defense`, `mena-pdpl`, `eu-gdpr`).
- **Active mode:** Safe Mode (master §4, adopted v1.0.1).
- **Phases shipped:** v0.1.0 → v0.7.0 inclusive (17 tags). Target: v1.0.0 (full Layer 1 release). Layer 2 Studio: v2.0.0+ (per ADR-008).
- **Open features:** 1 (the BeQuite v1.0.0 build; 9 sub-versions remain to v1.0.0 — v0.7.1 next).
- **Receipt chain integrity:** N/A on BeQuite-itself (no receipts emitted yet on this project; first phase-transition receipt emits when v0.10.0 wires auto-mode or any user manually invokes `bequite receipts emit`).
- **Receipt schema:** v1 (lands v0.7.0). ed25519 signing lands v0.7.1.
- **Remote:** configured `origin = https://github.com/xpShawky/BeQuite.git` in v0.5.3. NOT pushed — push awaits explicit owner authorization (one-way door per plan §11/12).

## What works (verified, with file-presence evidence)

Receipt-emitting infrastructure ships in v0.7.0; until then, "what works" is verified by smoke-test and module-import evidence:

- **`cli/bequite/audit.py`** — runs `python -m bequite.audit --help` from `cli/`; rule packs for Article IV secrets/env-reads, default-web-saas Rules 2 & 4, library-package Rule 7, ai-automation Rules 1 & 4. Tagged in v0.4.2.
- **`cli/bequite/freshness.py`** — runs `python -m bequite.freshness --help`; per-ecosystem probes (npm/PyPI/crates.io/GitHub), 24h cache, supply-chain incident table. Tagged in v0.4.3.
- **`cli/bequite/verify.py`** — runs `python -m bequite.verify --help`; 17-gate matrix orchestrator, per-stack command detection, GateResult dataclass with exit_code + duration + stdout_hash + stderr_tail. Tagged in v0.6.0.
- **Skill files** — `skill/SKILL.md` + 17 personas + 12 Doctrines + 19 commands + 14 hooks loadable into any Anthropic-Skills-compatible host.
- **Walkthrough fixtures** — `skill/templates/tests/walkthroughs/{admin,user}-walk.md.tpl` + `seed.spec.ts.tpl` + `playwright.config.ts.tpl` + `scripts/{self-walk,smoke}.sh.tpl`.
- **References** — `skill/references/scraping-and-automation.md`, `skill/references/security-and-pentest.md`, `skill/references/playwright-walks.md`.

## What's left (in priority order)

The 15-sub-version roadmap from the approved plan:

| Sub-version | Goal | Status |
|---|---|---|
| v0.1.0 | Foundation & Constitution v1.0.0 | ✅ tagged 2026-05-10 |
| v0.1.1 | Doctrines pack (8 default Doctrines) | ✅ tagged 2026-05-10 |
| v0.1.2 | Master-file merge (state/, prompts/, evidence/, CLAUDE.md, AGENTS.md, ADR-008, Constitution v1.0.1) | ✅ tagged 2026-05-10 |
| v0.2.0 | Skill orchestrator (SKILL.md + 11 personas + routing.json + bequite.config.toml.tpl) | ✅ tagged 2026-05-10 |
| v0.2.1 | AI automation skill module (ai-automation Doctrine + automation-architect persona + bundled skills) | ✅ tagged 2026-05-10 |
| v0.3.0 | Hooks (10 deterministic-gate shell scripts + template/.claude/settings.json) | ✅ tagged 2026-05-10 |
| v0.4.0 | Slash commands wave 1 (12 master-aligned: discover, research, decide-stack, plan, implement, review, validate, recover, design-audit, impeccable-craft, evidence, release) | ✅ tagged 2026-05-10 |
| v0.4.1 | Slash commands wave 2 (7 BeQuite-unique: audit, freshness, auto, memory, snapshot, cost, skill-install) | ✅ tagged 2026-05-10 |
| v0.4.2 | `bequite audit` rule engine (`cli/bequite/audit.py`, ~430 lines, 7 rule packs) | ✅ tagged 2026-05-10 |
| v0.4.3 | `bequite freshness` knowledge probe (`cli/bequite/freshness.py`, ~470 lines, supply-chain table) | ✅ tagged 2026-05-10 |
| v0.5.0 | CLI thin wrapper (Click, 19 subcommands, skill_loader, hooks dispatch, ADR-001-python-cli) | ✅ tagged 2026-05-10 |
| v0.5.1 | Article VIII — Scraping & Automation Module (4 personas + 4 Doctrines + 4 hooks + scraping reference) | ✅ tagged 2026-05-10 |
| v0.5.2 | Article IX — Cybersecurity & Authorized-Testing Module (3 personas + 4 Doctrines + 4 hooks + security reference + ROE templates) | ✅ tagged 2026-05-10 |
| v0.5.3 | Repo URL correction + remote configuration + count honesty backfill | ✅ tagged 2026-05-10 |
| v0.6.0 | Verification gates (`cli/bequite/verify.py` 17-gate orchestrator + Playwright walks + walkthrough fixtures + smoke scripts + references/playwright-walks.md) | ✅ tagged 2026-05-10 |
| v0.6.1 | Frontend Quality Module (vendored Impeccable + tokens.css.tpl + frontend-stack + frontend-mcps + axe-core gate + default-web-saas v1.1.0) | ✅ tagged 2026-05-10 |
| v0.7.0 | Reproducibility receipts (`cli/bequite/receipts.py` chain-hashed schema + emitter + store + chain validation + replay-check + roll-ups + 10-test integration suite + `bequite cost` local-first + `bequite receipts {list,show,validate-chain,roll-up}` Click group) | ✅ tagged 2026-05-10 |
| v0.7.1 | Signed receipts (ed25519 keypair on init, sign at emission, `bequite verify-receipts`) | **next** |
| v0.8.0 | Multi-model routing (cost-aware; AiProvider adapters; cost ceiling enforcement via stop hook) | pending |
| v0.8.1 | Live pricing fetch (best-effort; 24h cache; offline fallback) | pending |
| v0.9.0 | Three example projects (bookings-saas + ai-tool-wrapper + tauri-note-app) | pending |
| v0.9.1 | E2E test harness (seven-phase-walk + auto-mode + doctrine-loading) | pending |
| v0.10.0 | Auto-mode state machine (one-click run-to-completion + safety rails + heartbeat) | pending |
| v0.10.1 | Auto-mode resilience (resume / parallel-task / idempotent reruns / state persistence) | pending |
| v0.11.0 | MENA bilingual module (Arabic Researcher, RTL tokens, Egyptian dialect, RTL Playwright walks) | pending |
| v0.12.0 | Universal entry (AGENTS.md tpl + per-host adapters: Cursor, Codex, Gemini, Windsurf, Cline, Kilo, Continue, Aider) | pending |
| v0.13.0 | Vibe-to-handoff exporters (spec-kit-zip + claude-code-skill bundles + JSON-schema validation) | pending |
| v0.14.0 | Documentation (8 docs: README, QUICKSTART, HOW-IT-WORKS, DOCTRINE-AUTHORING, HOSTS, AUTONOMOUS-MODE, SECURITY, MAINTAINER) | pending |
| v0.15.0 | Release engineering (CI workflows + release.yml + osv-scanner + license-checker) | pending |
| **v1.0.0** | **Full release** (final e2e + audit + freshness sweep + tag + announcement) | pending |

## What's uncertain

- **Freshness probe brittleness.** Vendor pricing pages and registry APIs change. Mitigation: 24h cache + offline fallback + best-effort tag + ongoing v1.x tuning.
- **Skill format constraints.** Anthropic API skills cannot install packages. Mitigation: two skill modes (`claude-code-full` and `api-portable`) documented in `docs/HOSTS.md` (lands v0.14.0).
- **Anthropic beta header lifetime.** `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14` are beta. Mitigation: receipts log header version (v0.7.0); `bequite doctor` surfaces deprecations.
- **MENA module verifiability.** Arabic NLP / RTL Playwright walks need Arabic-native QA. Mitigation: v0.11.0 ships pause-for-Ahmed-review on first MENA-locale walks.
- **Remote-push one-way door.** Repo `xpShawky/BeQuite` exists but is empty; first push transmits the entire 19-commit history publicly. Awaits explicit owner authorization.

## Evolution log (newest first)

```
2026-05-10  v0.7.0 tagged — Reproducibility receipts. cli/bequite/receipts.py (~510 lines) introduces dataclass-based Receipt schema v1: version, session_id (UUID), phase (P0..P7), timestamp_utc, model{name, reasoning_effort, fallback_model}, input{prompt_hash sha256, memory_snapshot_hash sha256}, output{diff_hash sha256, files_touched}, tools_invoked[{name, args_hash, exit}], tests{command, exit, stdout_hash}, cost{input_tokens, output_tokens, usd}, doctrine[], constitution_version, parent_receipt (sha256 chain pointer). make_receipt() computes hashes (sha256 of prompt; sha256-of-files-and-paths for memory snapshot dir; git diff for output). Receipt.content_hash() canonicalizes JSON (sorted keys, no whitespace, None-stripped) and sha256s the result. ReceiptStore writes/reads .bequite/receipts/<sha>-<phase>.json. validate_chain detects missing parents + causality violations + cycles. replay_check verifies recorded prompt + memory hashes against re-derived hashes (used by tests + future v0.7.1 verify-receipts). roll_up_by_session/phase/day for cost analytics. CLI: `python -m bequite.receipts {emit,list,show,validate-chain,roll-up}`. Click integration: `bequite cost` reads local receipts first (offline-first per Article III) with skill-dispatch fallback; new `bequite receipts {list,show,validate-chain,roll-up}` group. tests/integration/receipts/ with 10-test smoke suite (emit + list + chain validation valid/missing-parent + replay pass/tamper-rejection + roll-ups by session/phase/day + content-hash determinism + round-trip preservation) — all 10 pass on Python 3.14. cli/bequite/__init__.py + cli/pyproject.toml bumped to 0.7.0.

2026-05-10  v0.6.1 tagged — Frontend Quality Module. skill/skills-bundled/impeccable/ vendored: .pinned-commit + ATTRIBUTION.md + README.md + SKILL.md + references/{principles,anti-patterns,aesthetic-targets}.md + commands/CATALOG.md + commands/{craft,audit,harden,polish}.md (4 marquee command dispatch contracts; remaining 19 catalogued in CATALOG.md). skill/templates/tokens.css.tpl with deliberate font-choice comment + 3-color system + 4/8/12/16 spacing scale + restrained radius/shadow + ease-out motion (NEVER bounce/elastic) + light/dark/RTL overrides + reduced-motion handling. skill/references/frontend-stack.md (verified May-2026 library list with license flags: Sentry BSL/FSL post-2023 flagged; AGPL components flagged for commercial closed-source distribution). skill/references/frontend-mcps.md (shadcn registry MCP via shadcn CLI v3+ built-in; 21st.dev Magic with TWENTY_FIRST_API_KEY env requirement; context7 free; tweakcn visual-only). axe-core gate: skill/templates/.github/workflows/axe.yml.tpl (PR + nightly + workflow-dispatch; HTML+JSON evidence retained 30d) + skill/templates/tests/a11y/{admin,user}/axe-{admin,user}.spec.ts.tpl (per-route axe analysis with WCAG 2.0+2.1 A+AA tags). skill/templates/playwright.config.ts.tpl extended with axeProjects (axe-admin + axe-user). skill/doctrines/default-web-saas.md bumped 1.0.0 → 1.1.0 with new section 5 (Frontend Quality Module subsections 5.1-5.5 cross-referencing all v0.6.1 artifacts; rules unchanged). cli/bequite/__init__.py + cli/pyproject.toml bumped to 0.6.1. CHANGELOG entry added.

2026-05-10  v0.6.0 tagged — Verification gates. cli/bequite/verify.py (17-gate orchestrator: lint/typecheck/test/build/secret-scan/audit/freshness/playwright-admin-walk/playwright-user-walk/smoke/axe/visual-diff/console-errors/network-errors/HAR-capture/screenshot/coverage; per-stack command detection; GateResult dataclass with exit_code+duration+stdout_hash+stderr_tail; per-Mode rigour Fast/Safe/Enterprise). skill/templates/tests/walkthroughs/{README,admin-walk,user-walk}.md.tpl (natural-language flows + accessibility-first locator hints). skill/templates/tests/seed.spec.ts.tpl (Playwright-based DB seed). skill/templates/playwright.config.ts.tpl (projects per role × viewport × locale; trace+video+screenshot on failure). skill/templates/scripts/{self-walk,smoke}.sh.tpl (cheap-curl complement to heavier suite). skill/references/playwright-walks.md (canonical 4-step planner→spec-writer→generator→healer pattern). qa-engineer persona refreshed with the pattern. cli/pyproject.toml bumped to 0.6.0; cli/bequite/__init__.py to "0.6.0".

2026-05-10  v0.5.3 tagged — Repo URL casing correction (xpshawky→xpShawky across 10 writable files; preserved BEQUITE_BOOTSTRAP_BRIEF.md and prompts/v1/* as immutable history). git remote configured (origin = https://github.com/xpShawky/BeQuite.git; NOT pushed). Inflated line-count claims corrected ("30,000+"/"22,000+" → 24,132 git-verified). README Quickstart reframed as today (local checkout) vs after-first-push (uvx --from git+...) vs v1.0.0 (PyPI). CHANGELOG backfilled.

2026-05-10  v0.5.2 tagged — Article IX Cybersecurity & Authorized-Testing Module. Constitution v1.1.0 → v1.2.0 (Article IX added with 4 amendments: internal red-team carve-out under 8 hard guardrails, cryptojackers added to malware list, defensive-validation clause, plural disclosure-frameworks). 3 personas: security-auditor, pentest-engineer, cve-watcher (+ disclosure-timer). 4 Doctrines: vibe-defense (Veracode 45% OWASP-Top-10 backstop), default-web-saas-hardened (additive), eu-gdpr (right-to-erasure, breach-72h, DPA), gov-fedramp-controls (NIST SP 800-53 Rev 5 mapping). 4 hooks: pretooluse-scraping-respect (already shipped v0.5.1), pretooluse-pentest-authorization (RoE+scope check), pretooluse-no-malware (hard block + internal-RT carve-out), pretooluse-cve-poc-context (PoC writes require ACTIVE_PENTEST). skill/references/security-and-pentest.md (25+ tools verified May-2026, lite vs full scanner stack, scan-and-trigger / harden-on-deploy / incident-response patterns). skill/templates/projects/scan-and-trigger.md. skill/templates/roe-template.md (4 variants: ROE / RoE-RT / RoE-self / RoE-CTF; 8-guardrail RT additions). ADR-010-article-ix-cybersecurity. License flags called out: AGPL Pentagi/THC-Hydra/Shannon (commercial blockers); Apache-2.0 Strix/Trivy/OSV-Scanner/Nuclei (clean).

2026-05-10  v0.5.1 tagged — Article VIII Scraping & Automation Module. Constitution v1.0.1 → v1.1.0 (Article VIII added with 4 amendments: rate-limit 1 req/3 sec default, stealth requires legitimate-basis enum, captcha clause, watch-budget). 4 personas: research-analyst (refreshed for scraping intel), scraping-engineer, automation-architect (refreshed), data-extraction-engineer. 4 Doctrines: ai-automation refreshed; mena-pdpl (jurisdictional branching: Egypt PDPL Law 151/2020, Saudi PDPL SDAIA enforceable 2024-09-14, UAE Federal Decree-Law 45/2021 + DIFC DPL 5/2020 + ADGM Data Protection Regs 2021); eu-gdpr scaffold; library-package refreshed. 4 hooks: pretooluse-scraping-respect (robots.txt + ToS check + rate-limit ≥3sec), pretooluse-block-destructive (refreshed), pretooluse-verify-package (refreshed), stop-verify-before-done (refreshed for VIII compliance). skill/references/scraping-and-automation.md (verified May-2026 library list with license flags: Crawlee/Crawlee-Python clean, Trafilatura clean, Firecrawl AGPL-3.0 commercial-blocker flag, Crawl4AI Apache-2.0, Scrapling clean, Shannon AGPL flagged; decision tree, polite-mode preset, watch-and-trigger pattern, MCP servers). skill/templates/projects/watch-and-trigger.md (with n8n in docker-compose by default). ADR-009-article-viii-scraping.

2026-05-10  v0.5.0 tagged — CLI thin wrapper. cli/pyproject.toml (hatchling, version 0.5.0, bequite + bq console scripts, deps: click + rich + httpx + pydantic + anthropic + cryptography + tomli). cli/bequite/{__init__,__main__,commands,skill_loader,config,hooks}.py. Click app with 19 subcommands. skill_loader.py reads skill/SKILL.md + linked agents into Claude API requests with the right beta headers. config.py Pydantic model for bequite.config.toml. hooks.py shells out to skill/hooks/*.sh from non-Claude hosts. ADR-001-python-cli accepted. README + CHANGELOG updated.

2026-05-10  v0.4.3 tagged — `bequite freshness` knowledge probe. cli/bequite/freshness.py (~470 lines): per-ecosystem probes (npm view, pip index versions, cargo search, GitHub repo last-commit, OSV-Scanner CVE check, context7 indexed-version probe), 24h cache keyed package@version, supply-chain incident table (PhantomRaven Aug-Oct 2025 by Koi Security, Shai-Hulud broader 2025 pattern), pricing-tier mismatch detection. Wires into `bequite stack` to block stale candidates from ADR sign-off. skill/references/package-allowlist.md seeded.

2026-05-10  v0.4.2 tagged — `bequite audit` Constitution drift detector. cli/bequite/audit.py (~430 lines): rule-based scan engine, 7 rule packs (Article I spec-id-in-commit, Article III activeContext-after-code, Article IV secrets + env-reads, Article V destructive-without-ADR, Article V scale-honesty, Article VII imports-not-in-lockfile, Doctrine web-saas Rules 2+4 hardcoded-Inter+gray-on-color, Doctrine library-package Rule 7, Doctrine ai-automation Rules 1+4). Reports finding with file:line + suggested fix. .github/workflows/audit.yml CI. skill/hooks/posttooluse-audit.sh runs lightweight subset on Edit/Write.

2026-05-10  v0.4.1 tagged — Slash commands wave 2 (7 BeQuite-unique). audit, freshness, auto, memory, snapshot, cost, skill-install. Each Markdown file with persona prompt + tool-list. /memory ops (read/show/snapshot), /snapshot (versioned prompts/v<N>/ creation), /cost (receipt rollup), /skill-install (install BeQuite into a host: detects Claude Code / Cursor / Codex / Gemini / Windsurf / Cline / Kilo / Continue / Aider).

2026-05-10  v0.4.0 tagged — Slash commands wave 1 (12 master-aligned). discover, research, decide-stack, plan, implement, review, validate, recover, design-audit, impeccable-craft, evidence, release. Each ~80-120 lines: persona prompt, tool list, Mode rigour matrix, evidence requirements, exit criteria.

2026-05-10  v0.3.0 tagged — 10 deterministic-gate shell scripts. pretooluse-secret-scan (regex API/secret/password/token/jwt + AWS access pattern, exit 2), pretooluse-block-destructive (rm-rf outside /tmp + terraform destroy + DROP DATABASE + git push -f to main + force-with-lease to main, exit 2), pretooluse-verify-package (PhantomRaven defense: diff package.json/pyproject.toml/Cargo.toml; npm view / pip index versions / cargo search; cross-check references/package-allowlist.md, exit 2), posttooluse-format (biome/prettier/black/ruff/clippy by language detection), posttooluse-lint (warn-only), stop-verify-before-done (banned weasel words + task-incomplete check, exit 2), sessionstart-load-memory (preloads Memory Bank + active ADRs + state/recovery.md), sessionstart-cost-budget. Wired into template/.claude/settings.json. tests/integration/hooks/ scaffolding.

2026-05-10  v0.2.1 committing — AI automation skill module per Ahmed's request to "add AI automation features and be expert in n8n and Make." skill/doctrines/ai-automation.md (12 binding rules); skill/agents/automation-architect.md (12th persona); skill/skills-bundled/ai-automation/ with README + 6 references (n8n + Make deep, Zapier/Temporal/Inngest brief, patterns cross-platform). SKILL.md + routing.json + bequite.config.toml.tpl updated for the 12th persona and the bundled skill loading rules.

2026-05-10  v0.2.0 tagged — Skill orchestrator. skill/SKILL.md (Anthropic Skills frontmatter, 7-phase router, Fast/Safe/Enterprise mode selector, 19-command surface). 11 personas (master's 10 + Skeptic): product-owner, research-analyst, software-architect, frontend-designer (Impeccable-loaded), backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist, skeptic. skill/routing.json (provider abstraction, AkitaOnRails 2026 split-only-when-parallel rule, Aider architect-mode review pattern). bequite.config.toml.tpl. template/.claude/skills/bequite/README.md.

2026-05-10  v0.1.2 tagged — master-file merge: docs/merge/MASTER_MD_MERGE_AUDIT.md (Buckets A/B/C/D/E classification), root CLAUDE.md + AGENTS.md, state/{project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json}, prompts/{master, discovery, research, stack_decision, implementation, review, recovery}, evidence/README.md, ADR-008-master-merge, Constitution v1.0.0 → v1.0.1 patch (additive: Modes, command-safety three-tier, prompt-injection rule, three-level def-of-done, state/ refs). README + CHANGELOG updated. Two-layer architecture decided: Harness (current) + Studio (v2.0.0+). Commit 64c6a74.

2026-05-10  v0.1.1 tagged — 8 default Doctrines: default-web-saas, cli-tool, ml-pipeline, desktop-tauri, library-package, fintech-pci, healthcare-hipaa, gov-fedramp. Each ~150 lines with rules, stack guidance, verification gates, forking guidance. mena-bilingual deferred to v0.11.0. Commit 50ebfe6.

2026-05-10  v0.1.0 tagged — repo skeleton, Iron Laws Constitution v1.0.0, 6 Memory Bank templates, ADR template, Doctrine schema authored. Plan snapshotted. Ahmed authorised autonomous execution through v1.0.0. Commit 22330e7.

2026-05-10  ExitPlanMode accepted. Build plan at .bequite/memory/prompts/v1/2026-05-10_initial-plan.md.

2026-05-10  4 forks resolved by Ahmed: engineer-first (with vibe-handoff seeded) / skill-first / layered Constitution / full-power v1.

2026-05-10  Brief verification complete. 10 surgical updates baked into Constitution + templates (Aider direction, Stronghold deprecation, EV cert obsolescence, Spec-Kit command count, Roo Code shutdown, shadcn MCP move, Clerk MAU, Vercel timeout, Supavisor, PhantomRaven naming).

2026-05-10  Initial brief (BEQUITE_BOOTSTRAP_BRIEF.md) read in full. Three parallel research agents dispatched: spec-driven tools, AI coding tool landscape, security/quality fact-check.
```

## Decisions made (newest first)

```
2026-05-10  ADR-010 accepted: Article IX Cybersecurity & Authorized-Testing Module. 4 senior-architect amendments (internal red-team carve-out under 8 hard guardrails: dual sign-off, corporate-IP-only, callback-URL compile-time-assertion, engagement-id+expiry, private-repo, sandboxed-build, post-engagement cryptographic-shred, no-reuse; cryptojackers added to malware list; defensive-validation clause; plural disclosure frameworks). Constitution v1.1.0 → v1.2.0.

2026-05-10  ADR-009 accepted: Article VIII Scraping & Automation Module. 4 senior-architect amendments (rate-limit 1 req/3 sec default; stealth requires legitimate-basis enum; captcha clause; watch-budget). Constitution v1.0.1 → v1.1.0.

2026-05-10  ADR-008 accepted: two-layer architecture (Harness v0.1.0 → v1.0.0, Studio v2.0.0+); Constitution v1.0.0 → v1.0.1 patch amendment (additive only: Modes, command-safety three-tier, prompt-injection rule, three-level def-of-done, state/ refs).

2026-05-10  ADR-001 accepted: Python 3.11+ CLI via hatchling/click/anthropic/rich/httpx/pydantic/cryptography (v0.5.0). Reasoning: matches Spec-Kit's proven pattern (uvx/pipx); Python's ML/data ecosystem; offline-friendly tomllib in stdlib.

2026-05-10  Personas merge (DEC-007): 17 total personas across all modules. Original 10 (product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist) + Skeptic = 11 in v0.2.0; +automation-architect in v0.2.1 = 12; +scraping-engineer + data-extraction-engineer in v0.5.1 = 14; +security-auditor, pentest-engineer, cve-watcher (+ disclosure-timer) in v0.5.2 = 17.

2026-05-10  Slash commands merge (DEC-008): master's 12 (/discover, /research, /decide-stack, /plan, /implement, /review, /validate, /recover, /design-audit, /impeccable-craft, /evidence, /release) + BeQuite's 7 unique (/audit, /freshness, /auto, /memory, /snapshot, /cost, /skill-install) = 19 commands. Authored across v0.4.0 → v0.4.3.

2026-05-10  Master file scope deferred (DEC-005): TypeScript monorepo + Postgres + Next.js dashboard + NestJS API + Worker → Studio Layer 2 (v2.0.0+). Layer 1 Harness (current) preserved. Captured in ADR-008.

2026-05-10  (DEC-002) Skill-first distribution: SKILL.md is source of truth, CLI is thin Python wrapper, host adapters generated.

2026-05-10  (DEC-001) Engineer-first v1, with vibe-handoff seeded into artifact discipline.

2026-05-10  (DEC-003) Layered Constitution: Iron Laws + forkable Doctrines. Impeccable bundled as default-loaded Doctrine for frontend projects (vendor lands in v0.6.1).

2026-05-10  (DEC-004) Full v1 power from day 1; autonomous execution authorised by Ahmed; 15 sub-versions to v1.0.0.

2026-05-10  Iron Laws structure (v1.0.0 ratification): 7 articles (Spec, Verify, Memory, Security, Scale, Honest, Hallucination). Stack discipline (was Article IV in brief), UI distinctiveness (was VII), and Research-first (was VIII) are NOT Iron Laws — they're Doctrines or implicit in the seven phases. Reasoning: a CLI tool / library / ML pipeline doesn't need Article-VII UI rules; layered Constitution is more honest. Subsequently extended to 9 articles via ADR-009 (Article VIII Scraping) and ADR-010 (Article IX Cybersecurity); Iron Laws remain additive-only.
```

## Failures and learnings

```
2026-05-10  Edit-state mismatches across multi-file batches. When chaining many Edits across files separated by Bash calls, Anthropic harness reset Edit-state for some files, requiring an explicit Read-before-Edit. Fixed throughout via paired Read-Edit pairs and several backfill chore commits (13bdfe0 chore(v0.4.1), 3c1ab39 chore(state) v0.4.2/v0.4.3/v0.5.0, 646a6e2 chore: backfill v0.5.2). Learning for v0.6.1+: read-before-edit any file modified earlier in a session.

2026-05-10  Inflated count claims ("30,000+", "22,000+", "13,000+") corrected. Real numbers came from `git log --pretty=tformat: --numstat | awk '{a+=$1; s+=$2} END {print a, s}'`: 24,132 added net across 19 commits as of v0.6.0. Article VI honest reporting violation; corrected in v0.5.3 + propagated through all Memory Bank files in v0.6.0 housekeeping.

2026-05-10  Repo URL casing wrong (xpshawky/bequite lowercase) — fixed to xpShawky/BeQuite via sed sweep across 10 writable files in v0.5.3; preserved BEQUITE_BOOTSTRAP_BRIEF.md and prompts/v1/* (immutable history).

2026-05-10  Aspirational `uvx --from git+...` install commands in README implied they worked — they didn't (repo was empty). Fix: reframed as "post-first-push + v1.0.0 PyPI publish" with today's path being `python -m cli.bequite.audit` from local checkout. v0.5.3.

2026-05-10  Initial Constitution numbering conflict: addenda used "Article XI" / "XII" but BeQuite Constitution had only 7 Iron Laws. Fix: renumbered to Article VIII / Article IX; kept addendum text otherwise verbatim with 4 senior-architect amendments per article.

2026-05-10  Library list errors caught by parallel research agent: Crawl4AI URL was crawl4ai/crawl4ai (404) → corrected to unclecode/crawl4ai. n8n MCP n8n-io/n8n-mcp 404 → corrected to community czlonkowski/n8n-mcp (marked community, not official). mendableai/firecrawl* redirected → updated to canonical firecrawl/*. tfsec retired into Trivy (last release May 2025) — removed from canonical list. requests-html and headless-chrome-crawler dead (>2yr) — removed.

2026-05-10  License-flag misses corrected: Firecrawl is AGPL-3.0 (commercial closed-source-blocker), not "MIT"; Shannon AGPL-3.0; BunkerWeb AGPL-3.0. Strix is Apache-2.0 (clean). Wazuh GPL-2.0; SafeLine GPL-3.0. Added prominent license-flag callouts in references.
```
