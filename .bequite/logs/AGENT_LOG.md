# Agent log

Append-only chronicle of every BeQuite command run. Newest at top.

## 2026-05-12 — alpha.10 ship: deep opportunity intelligence + /bq-update + memory-first behavior

**Action:** User invoked `/bq-auto` with 4 upgrades. Per /bq-auto discipline, no hard gates tripped — continued autonomously.

**Upgrade 1 — Deep Opportunity Intelligence:**

Updated `/bq-job-finder` + `/bq-make-money` commands with a "Deep Intelligence" section adding:
- **Community + conversation sources:** Reddit (r/forhire, r/WorkOnline, r/beermoney, country subs), Indie Hackers, Hacker News, Product Hunt, X/Twitter, public LinkedIn/Facebook, Discord/Slack, YouTube creator communities, app reviews
- **Trending + short-window opportunities:** new AI task platforms, data labeling campaigns, app testing, research panels, browser panels, regional rotating tasks
- **AI-assisted work paths:** explicit catalog of work types where AI stack is a multiplier (image / video / agent building / automation / data / content / research / lead research / social / scripts / product / landing / ad / website / spreadsheet / AI tool reviewer)
- **Hidden Gems** logic: dedicated section with full per-gem fields (name / country / language / source / why hidden / evidence / payout / eligibility / AI tools / difficulty / time to first payout / risk / trust score / first action / why it fits user)
- **11 new tracks:** worldwide_hidden, trending_now, community_discovered, AI_assisted, no_calls, fast_first_payout, highest_payout, beginner_friendly, skilled_remote, local_country, non_english_platforms — can stack
- **Multi-language search:** English + Arabic + Spanish + Portuguese + German + French + Italian + Turkish + Polish + Lithuanian + Romanian + Indonesian + Hindi (and user-listed languages)
- **Per-opportunity required fields:** legitimacy / payout method / country eligibility / required docs / account requirements / skill requirements / scam signals / payout complaints / risk level / confidence level

New memory files (6):
- `.bequite/jobs/HIDDEN_GEMS.md`
- `.bequite/jobs/COMMUNITY_SIGNALS.md`
- `.bequite/jobs/AI_ASSISTED_WORK.md`
- `.bequite/money/HIDDEN_GEMS.md`
- `.bequite/money/COMMUNITY_SIGNALS.md`
- `.bequite/money/AI_ASSISTED_PATHS.md`

**Upgrade 2 — `/bq-update` command:**

- New `.claude/commands/bq-update.md` — full spec with 5 modes (check / safe / force / source=local / source=github), backup strategy, never-overwrite list, conflict handling (`.bequite-update.md` sibling files), rollback path
- New `.claude/skills/bequite-updater/SKILL.md` — full update discipline (version detection / source resolution / diff via SHA-256 / merge per file class / conflict surface / logging / rollback / test after update)
- New state files: `.bequite/state/BEQUITE_VERSION.md` (seed at alpha.10), `.bequite/state/UPDATE_SOURCE.md` (configured to GitHub xpShawky/BeQuite main)
- New log: `.bequite/logs/UPDATE_LOG.md` (template)
- New directory: `.bequite/backups/` (with .gitkeep)
- Hard rule: never overwrite `.bequite/state/{PROJECT_STATE,DECISIONS,MISTAKE_MEMORY,jobs/,money/,research/,...}` — always back up `.claude/commands/` + `.claude/skills/` before changes

**Upgrade 3 — Memory-First Behavior:**

- New `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` — establishes the principle universally for all commands
- Core memory list: PROJECT_STATE / CURRENT_MODE / CURRENT_PHASE / WORKFLOW_GATES / LAST_RUN / DECISIONS / OPEN_QUESTIONS / MISTAKE_MEMORY (~5-15 KB total)
- Optional memory list: per-command files (DISCOVERY / RESEARCH / IMPLEMENTATION_PLAN / TASK_LIST / SECTION_MAP / etc.)
- Per-command read/write matrix for all 43 commands
- Token-saving memory strategy: read only what's needed; summarize older logs; cache research; use focused skills; avoid re-reading all docs every session
- Auto-mode memory strategy: read core once, pass forward via AUTO_STATE_<session>.json, update gates per phase (not per task)
- Mistake memory strategy: read always; write only when pattern is recurring / lesson is forward-applicable
- Standardized memory preflight + memory writeback templates

**Upgrade 4 — Command Catalog Update:**

- `.claude/commands/bequite.md` — added "Maintenance" section with `/bq-update`
- `.claude/commands/bq-help.md` — added `/bq-update` + alpha.10 deep intelligence note
- `README.md` — version bump to alpha.10; 43-command badge; new "Opportunity and Workflows" + "Maintenance" sections in command map
- `CLAUDE.md` — version bump; new commands + memory-first doc referenced; new memory file paths
- `docs/specs/COMMAND_CATALOG.md` — added /bq-update entry; added deep intelligence flags table; tallies bumped to 43/19
- `commands.md` — added Maintenance section with full /bq-update entry

**Tally after alpha.10:**

- Commands: 42 → 43 (+1: /bq-update)
- Skills: 18 → 19 (+1: bequite-updater)
- Memory files: +6 (3 jobs + 3 money) + 3 state/log/version files = +9
- Memory directories: +1 (backups/)
- Architecture docs: +1 (MEMORY_FIRST_BEHAVIOR.md)
- New tracks for opportunity commands: +11

**Cumulative version state:**

- v3.0.0-alpha.1 → alpha.4: foundation (36 cmds, 15 skills)
- v3.0.0-alpha.5: studio cleanup + /bq-now + mistake memory + commands.md
- v3.0.0-alpha.6: installer auto-copies + 19 commands extended
- v3.0.0-alpha.7: /bq-spec + /bq-explain
- v3.0.0-alpha.8: /bq-suggest + /bq-job-finder + /bq-make-money + worldwide_hidden
- v3.0.0-alpha.9: installer copies alpha.8 templates
- v3.0.0-alpha.10 (this commit): deep opportunity intelligence + /bq-update + memory-first behavior

**Acceptance criteria check:**
- ✅ /bq-update exists (substantive — 5 modes, full conflict handling, backup discipline)
- ✅ bequite-updater skill exists
- ✅ BeQuite version file exists at .bequite/state/BEQUITE_VERSION.md
- ✅ UPDATE_LOG.md exists
- ✅ Backup strategy documented in skill + command
- ✅ MEMORY_FIRST_BEHAVIOR.md exists with full per-command matrix
- ✅ Job Finder includes community + hidden opportunity research
- ✅ Make Money Finder includes community + hidden opportunity research
- ✅ AI-assisted work paths documented (AI_ASSISTED_WORK.md + AI_ASSISTED_PATHS.md)
- ✅ Hidden Gems files exist (jobs + money)
- ✅ Command catalog updated with /bq-update + new flags
- ✅ /bequite root menu updated (Maintenance section)
- ✅ /bq-help updated
- ✅ README updated
- ✅ AGENT_LOG (this entry) + CHANGELOG updated

**Article VI honest reporting:**
- /bq-update is structurally in place. Runtime behavior depends on git availability + source reachability. Backup logic + conflict surfacing + never-overwrite list are documented; the agent enforces them per the skill.
- Deep intelligence is now documented as the methodology Claude follows when running /bq-job-finder + /bq-make-money. Actual runtime depends on which research tools are loaded (WebFetch / Chrome MCP / Computer Use MCP per alpha.8 hotfix).
- Memory-first behavior is a doctrine + matrix. Not enforced by harness hooks; agent honors it per command spec.
- Installer scripts NOT yet updated to copy the 6 new memory files (HIDDEN_GEMS / COMMUNITY_SIGNALS / AI_ASSISTED_*) — alpha.11 work.
- v3.0.0-alpha.10 NOT git-tagged (user-gated).

---

## 2026-05-12 — alpha.9 ship: installer copies alpha.8 jobs + money templates

**Action:** Installer scripts updated to carry the alpha.8 memory templates into target projects on `/bq-init`. Without this, new BeQuite installs were missing the 10 opportunity-template files even though the commands referenced them.

**Updates to `scripts/install-bequite.ps1` + `scripts/install-bequite.sh`:**

- Bumped `BEQUITE_VERSION` messaging: `v3.0.0-alpha.5` → `v3.0.0-alpha.8`
- Banner counts: "37 slash commands" → "42"; "15 specialist skills" → "18"
- Added directory scaffold: `.bequite/jobs/`, `.bequite/money/`
- Added 10 new `copy_template` calls (5 jobs + 5 money templates)
- CLAUDE.md template additions: surface `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` + the `worldwide_hidden=true` flag
- Final install banner now shows "Opportunity and Workflows (alpha.8)" section with the 3 new commands

**Templates now installed automatically into target projects:**

| Category | File |
|---|---|
| alpha.3 | `.bequite/principles/TOOL_NEUTRALITY.md` |
| alpha.5 | `.bequite/state/MISTAKE_MEMORY.md`, `ASSUMPTIONS.md` |
| alpha.4 | `.bequite/uiux/SECTION_MAP.md`, `LIVE_EDIT_LOG.md`, `UIUX_VARIANTS_REPORT.md`, `selected-variant.md` |
| alpha.5 | `commands.md` at project root |
| **alpha.8 — jobs** | `.bequite/jobs/JOB_PROFILE.md`, `JOB_SEARCH_LOG.md`, `OPPORTUNITIES.md`, `APPLICATION_TRACKER.md`, `PITCH_TEMPLATES.md` |
| **alpha.8 — money** | `.bequite/money/MONEY_PROFILE.md`, `MONEY_SEARCH_LOG.md`, `OPPORTUNITIES.md`, `TRUST_CHECKS.md`, `ACTION_PLAN.md` |

All `copy_template` calls preserve existing files (don't overwrite — the user's intake/log/results stay intact across re-installs).

**Effect:** new BeQuite installs now match alpha.8 functionality immediately — no manual file copying required.

**Article VI honest reporting:**
- Installer logic verified by code inspection. Not yet end-to-end tested by running `irm | iex` from a fresh repo. The first user install on alpha.9+ will be the real verification.
- Version string is `v3.0.0-alpha.8` in messaging (templates ARE alpha.8; the installer code itself can be thought of as alpha.9 since it adds the new copy operations).

**Pending (alpha.10):**
- Live verification of `/bequite` against fresh real-world projects (user action — installer is now feature-complete)
- `/bq-help` extended with full standardized fields (currently has alignment notice + brief block)
- Architecture docs expanded from concise summaries to full reference depth

---

## 2026-05-12 — alpha.8 hotfix: clarify Claude-side search + add "How to use" section to README

**Action:** User clarified that:
1. The 3 new opportunity commands run **Claude-side searches** — not user-side. The user invokes; Claude searches.
2. Claude should use Computer Use MCP or Chrome MCP if WebFetch/WebSearch can't reach a site.
3. README needs a clear "How to use" section for the 3 new features, especially `/bq-make-money` + worldwide_hidden mode.

**Updates:**

- `/bq-job-finder` — added "Step 3 — Research (Claude searches for you)" with 3-tier tool table (WebFetch → Chrome MCP → Computer Use MCP) + failure handling (rate limits / captcha / login walls / ToS / suspicious links)
- `/bq-make-money` — same 3-tier tool table + failure paths added to "Step 3 — Live research"
- `/bq-suggest` — added clarifying note that it doesn't do web research itself; only reads BeQuite memory + situation
- `bequite-job-finder` skill — full "Research methodology — Claude does the search work" section with per-tier failure handling table
- `bequite-make-money` skill — same Research methodology section added
- `README.md` — added "How to use the 3 new opportunity commands" section near the top of the body:
  - Clarifies Claude-side searching with tier fallbacks
  - Per-command usage block (suggest / job-finder / make-money)
  - Detailed `/bq-make-money` section with track table + 10 ranked output sections + Hidden Gems explanation + 7-day action plan note + strict safety rules
  - Specific examples including all worldwide_hidden=true variants

**Article VI honest reporting:**
- The commands and skills now explicitly document Claude-side discovery via WebFetch / Chrome MCP / Computer Use MCP.
- Actual runtime behavior depends on which MCP servers are loaded in the user's Claude host. The agent detects tools at runtime; the documentation is the playbook.
- README now has a dedicated section that a new user can read in under 5 minutes to understand how to invoke the 3 new commands.

---

## 2026-05-12 — alpha.8 ship: /bq-suggest + /bq-job-finder + /bq-make-money + worldwide_hidden mode

**Action:** User invoked `/bq-auto` with a feature-shaped task (3 new capabilities). Per /bq-auto discipline, no hard gates tripped — continued autonomously through the full task.

**New commands (3):**

### /bq-suggest "<situation>"

BeQuite workflow advisor. Reads user's situation + state, recommends best commands / skills / mode / required gates / one next command. Read-only. Activates `bequite-workflow-advisor` skill (knows all 42 commands + 18 skills + 23 gates + 17 hard human gates + mode flags).

Output structure:
- Recommended workflow (1-5 commands in order)
- Skills activated
- Mode recommendation (fast / deep / token-saver / default)
- Auto vs. scoped vs. phase vs. individual
- Required gates + optional gates
- Missing information (one question max)
- One recommended next command
- Why NOT each alternative

### /bq-job-finder

Real work opportunity discovery. Intake form → JOB_PROFILE.md → live research at runtime → trust check per platform → ranked classification → pitches.

Supports `worldwide_hidden=true` mode — searches beyond country/English platforms across multilingual sources (Portuguese / Spanish / German / French / Italian / Turkish / Polish / Romanian / Indonesian / Hindi / Arabic + English) and country-specific platforms.

Categories: Best fit / Easy start / High pay / Fast application / Needs portfolio / Needs learning / Risky / Not recommended / Hidden Gems.

Strict safety: no scams / fake reviews / VPN misrepresentation / upfront-fee / identity misuse / CAPTCHA farms.

### /bq-make-money

Earning opportunity discovery with 10 tracks (highest-payout / easiest-start / fastest-first-dollar / long-term-stable / ai-assisted / no-calls / remote-global / local-only / beginner / skilled).

Supports `worldwide_hidden=true` for Hidden Gems section. 7-day action plan output. Repeat-search behavior compares with previous run + marks 🆕 / ✅ / ❌ / ⚠ / ⬆ / 🔍.

Strict safety: no fraud / fake accounts / platform abuse / spam / VPN / upfront-fee / unrealistic claims.

**New skills (3):**

- `bequite-workflow-advisor` — recommendation engine; knows entire BeQuite surface
- `bequite-job-finder` — platform knowledge + trust check criteria + safety rules + worldwide hidden methodology
- `bequite-make-money` — track-based knowledge + 10-track filtering + Hidden Gems methodology

**New memory folders:**

- `.bequite/jobs/` — 5 templates: JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES
- `.bequite/money/` — 5 templates: MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN

**Updated:**

- `/bequite` root menu — added "Opportunity and Workflows" section with /bq-suggest, /bq-job-finder, /bq-make-money
- `/bq-help` — added Opportunity & Workflows commands to the alpha.2+ commands list
- `README.md` — version bump to alpha.8; 42-command badge; new commands in command map + roadmap + Worldwide Hidden Opportunity Search section
- `CLAUDE.md` — version bump; new commands referenced; new memory paths
- `docs/specs/COMMAND_CATALOG.md` — added full entries for 3 new commands + bumped tallies
- `commands.md` — added Opportunity and Workflows section with full entries + Worldwide Hidden Opportunity Search explanation

**Tally after alpha.8:**

- Commands: 39 → 42 (+3)
- Skills: 15 → 18 (+3)
- Memory folders: +2 (`.bequite/jobs/`, `.bequite/money/`)
- Memory templates: +10
- Hard human gates: 17 (unchanged)
- Workflow gates: 23 (unchanged)

**Cumulative version state:**

- v3.0.0-alpha.1: lightweight skill pack MVP (24 commands, 7 skills)
- v3.0.0-alpha.2: mandatory workflow gates + 6 modes + 7 specialist skills
- v3.0.0-alpha.3: tool neutrality principle
- v3.0.0-alpha.4: scoped /bq-auto + variants + live edit (36 commands, 15 skills)
- v3.0.0-alpha.5: studio cleanup + /bq-now + mistake memory + --mode + commands.md (37/15)
- v3.0.0-alpha.6: installer auto-copies + 19 commands extended (37/15)
- v3.0.0-alpha.7: /bq-spec + /bq-explain + bq-help alignment (39/15)
- v3.0.0-alpha.8 (this commit): /bq-suggest + /bq-job-finder + /bq-make-money + worldwide_hidden (42/18)

**Constraints honored:**

- ✅ No heavy app added
- ✅ No dashboard added
- ✅ No big CLI added
- ✅ No heavy dependencies added by default
- ✅ Commands + skills + docs + memory updates only
- ✅ No actual scraping runtime / job API / browser automation in commands (research happens via available WebFetch/WebSearch at runtime per command)
- ✅ Tool neutrality enforced (platforms named are candidates, not endorsements)
- ✅ Safety rules documented exhaustively for opportunity commands

**Pending (alpha.9):**

- Live verification of `/bequite` against fresh real-world projects (user action)
- Installer updated to copy `.bequite/jobs/` + `.bequite/money/` templates into target projects
- Architecture docs expanded from concise summaries to full reference depth
- `/bq-help` extended with full standardized fields (only has alignment notice + brief block currently)

**Article VI honest reporting:**

- All 3 new commands + 3 new skills + 10 memory templates are STRUCTURALLY in place. The agent's runtime behavior (the actual intake conversation, the live web research, the trust checks) is per-command documented in Steps + Output format sections.
- No actual job APIs or browser automation runtime added (per user constraint). Live web research happens at runtime via available WebFetch/WebSearch when the user invokes the command — the command files document the sources and methodology.
- v3.0.0-alpha.8 is NOT git-tagged yet (user-gated per release discipline).
- Installer scripts NOT yet updated to copy `.bequite/jobs/` + `.bequite/money/` templates to target projects — listed as alpha.9 work.

---

## 2026-05-12 — alpha.7 ship: /bq-spec + /bq-explain + bq-help alignment

**Action:** User said "continue" — picking up the remaining alpha.7 work after alpha.6 (installer + 19 commands extension) landed.

**New commands (2):**

### /bq-spec "<feature>"

Spec Kit-compatible one-page spec writer. Bridges BeQuite to the GitHub Spec Kit ecosystem. Writes `specs/<slug>/spec.md` with structured fields:
- What / Why / Who
- What changes for the user (before/after)
- Acceptance criteria (testable, observable)
- Out of scope (explicit non-goals)
- Constraints (privacy / compliance / performance / budget)
- Open questions
- Success metric (one number)
- How (high-level, optional)

Phase P1/P2. Activates `bequite-product-strategist` for JTBD discipline. Tool neutrality: Spec Kit is an interop target, not a dependency — `/bq-spec` produces markdown that works in BeQuite + Spec Kit + Notion + any wiki.

### /bq-explain "<target>"

Plain-English explainer for files / functions / decisions / concepts / BeQuite artifacts. 4-section output:
- What it is
- What it does
- Why it matters
- Things to be careful of

Read-only. Use cases: onboarding new engineers, vibe-handoff prep, understanding AI-generated code, learning what `/bq-auto` did. Optional save to `.bequite/handoff/explain-<slug>.md` for `/bq-handoff` bundling.

**bq-help.md aligned:**
- Added standardized command fields block at the end
- Added alpha.5+ alignment notice at top pointing to `commands.md` for the canonical reference
- Added "Notes on the alpha.5+ surface" section documenting:
  - Updated phase names (Setup and Discovery / Product Framing and Research / Planning and Build / Quality and Review / Release / Memory and Handoff)
  - Commands added in alpha.2+ that weren't in the original phase 0-5 listing (`/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-feature`, `/bq-auto`, `/bq-p0..p5`, `/bq-uiux-variants`, `/bq-live-edit`, `/bq-now`, `/bq-spec`, `/bq-explain`)

**Updated:**
- `README.md` — version bump to alpha.7; badge shows 39 commands; `/bq-spec` added to P1 command map; `/bq-explain` added to root; alpha.7 entries added to "MVP now" + alpha.8 pending list
- `CLAUDE.md` — version bump to alpha.7; 39 commands; new commands referenced
- `docs/specs/COMMAND_CATALOG.md` — bumped to alpha.7; added `/bq-spec` + `/bq-explain` entries with skills + path conventions
- `commands.md` — added `/bq-spec` + `/bq-explain` full entries; updated version + tally; added `/bq-explain` to Quick orientation table

**Tally after alpha.7:**
- Commands: 37 → 39 (+2: `/bq-spec`, `/bq-explain`)
- Skills: 15 (unchanged)
- Commands with standardized template: 38 of 39 (only `/bq-help` has a notes-style block at the end vs. the inline labeled fields; close enough — that command is itself a reference)

**Cumulative version state:**
- v3.0.0-alpha.1: lightweight skill pack MVP (24 commands, 7 skills)
- v3.0.0-alpha.2: mandatory workflow gates + 6 modes + 7 specialist skills (34 commands, 14 skills)
- v3.0.0-alpha.3: tool neutrality principle (no command count change)
- v3.0.0-alpha.4: scoped /bq-auto + variants + live edit (36 commands, 15 skills)
- v3.0.0-alpha.5: studio cleanup + /bq-now + mistake memory wiring + --mode flag + commands.md (37 commands, 15 skills)
- v3.0.0-alpha.6: installer auto-copies alpha.5 templates + 19 commands extended (37 commands, 15 skills)
- v3.0.0-alpha.7 (this commit): /bq-spec + /bq-explain + bq-help alignment (39 commands, 15 skills)

**Pending (alpha.8 — minimal remaining):**
- Live verification of `/bequite` inside Claude Code against a fresh real-world project (user action — installer is ready for this)
- Architecture docs expanded from concise summaries to full reference depth (4 docs; current versions are 60-100 lines, full ref would be 200-300 each)
- `/bq-undo` and `/bq-cost` commands (lower priority; defer unless user pull is strong)

**Article VI honest reporting:**
- `/bq-spec` and `/bq-explain` are structurally in place. Runtime behavior (the agent's actual response when invoked) follows the procedures documented in each file's Steps + Output format sections.
- `bq-help.md` was given a standardized fields block at the end AND an alignment notice at top. The body still uses original phase names but the alignment notice corrects this. Full body rewrite deferred to alpha.8 if needed.
- README's alpha.7 entries are accurate per this commit. v3.0.0-alpha.7 is NOT tagged yet (user-gated).

---

## 2026-05-12 — alpha.6 ship: installer auto-copies alpha.5 templates + 19 alpha.1 commands extended with standardized fields

**Action:** User said "continue" — picking up the deferred alpha.6 work.

**Installer scripts updated (both PowerShell + bash):**
- Bumped version messaging to `v3.0.0-alpha.5`
- Added directory scaffold for `.bequite/principles/`, `.bequite/decisions/`, `.bequite/uiux/screenshots/`, `.bequite/uiux/archive/`
- Copy alpha.5 template files into target project (preserves existing):
  - `.bequite/principles/TOOL_NEUTRALITY.md`
  - `.bequite/state/MISTAKE_MEMORY.md`
  - `.bequite/state/ASSUMPTIONS.md`
  - `.bequite/uiux/SECTION_MAP.md`
  - `.bequite/uiux/LIVE_EDIT_LOG.md`
  - `.bequite/uiux/UIUX_VARIANTS_REPORT.md`
  - `.bequite/uiux/selected-variant.md`
- Copy `commands.md` to target project root
- Updated CLAUDE.md template (created or appended) to reference `/bq-now`, `/bq-auto`, `commands.md`, TOOL_NEUTRALITY.md, gates
- Refreshed end-of-install message to highlight autonomous mode + new commands

**19 alpha.1 commands extended with Standardized fields (alpha.6) section:**
- bq-init, bq-discover, bq-doctor, bq-clarify, bq-scope, bq-assign, bq-implement, bq-test, bq-audit, bq-review, bq-red-team, bq-verify, bq-release, bq-changelog, bq-memory, bq-recover, bq-handoff, bequite (root menu), bq-add-feature (legacy alias)

Each gained:
- **Phase** (P0..P5 or Any)
- **When NOT to use** — specific anti-patterns per command
- **Preconditions** — what must be true to run
- **Required previous gates** — explicit list of WORKFLOW_GATES dependencies
- **Quality gate (success criteria)** — bulleted concrete conditions
- **Failure behavior** — per-failure-mode response
- **Memory updates** — which gates ticked + state files touched
- **Log updates** — AGENT_LOG always; CHANGELOG when user-visible

**Tally after alpha.6:**
- Commands with full template: 36 of 37 (only `/bq-help` lacks the block — it's a meta reference command)
- New skills: 0
- Total commands: 37
- Total skills: 15

**Cumulative version state:**
- v3.0.0-alpha.1: lightweight skill pack MVP (24 commands, 7 skills)
- v3.0.0-alpha.2: mandatory workflow gates + 6 modes + 7 specialist skills (34 commands, 14 skills)
- v3.0.0-alpha.3: tool neutrality principle (no command count change)
- v3.0.0-alpha.4: scoped /bq-auto + variants + live edit (36 commands, 15 skills)
- v3.0.0-alpha.5: studio cleanup + /bq-now + mistake memory wiring + --mode flag + commands.md (37 commands, 15 skills)
- v3.0.0-alpha.6 (this commit): installer auto-copies templates + 19 commands extended with standardized fields

**Pending (alpha.7):**
- Live verification of `/bequite` inside Claude Code against a fresh real-world project (user action — installer is now ready)
- Architecture docs expanded from concise summaries to full reference depth (4 docs)
- Additional trendy commands evaluated (`/bq-spec`, `/bq-explain`, `/bq-undo`, `/bq-cost`) — defer unless user pull is strong
- bq-help.md extended with standardized fields (was excluded; less critical for a meta reference command)

**Article VI honest reporting:**
- Installer scripts: tested logic by inspecting the code paths. NOT yet end-to-end tested by running `irm | iex` from a fresh repo. The first user install on alpha.6+ will be the real verification.
- 19 commands gained a standardized fields block at the bottom (before "## Memory files this command reads"). The original command procedures are unchanged; the new block ADDS the missing labeled sections.
- bq-help.md was excluded from this pass because it's a meta-reference command with a different structure. Listed as alpha.7 pending.

---

## 2026-05-12 — v3.0.0-alpha.5 ship: studio cleanup + /bq-now + mistake memory wiring + --mode flag + commands.md

**Action:** User invoked `/bq-auto` with a focused scope: delete only `studio/` (not other heavy folders), continue with v1 features, add trendy/catchy commands, create `commands.md` linked from README, revise all md files, push final to GitHub.

**Studio cleanup (executed — user authorized):**
- `git rm -r studio/` (Studio Next.js app: marketing + api + dashboard + brand)
- `git rm docker-compose.yml` (Studio compose orchestration)
- `git rm scripts/docker-up.ps1 scripts/docker-up.sh` (Studio dev runner)
- **Kept** (per user instruction "remove studio only and files related to studio"):
  - `cli/`, `tests/`, `template/`, `evidence/`, `examples/`, `prompts/`, `state/`, `skill/`
  - `.dockerignore`, `.env.example`, `Makefile`, `package.json`, `.commitlintrc.json`
  - `scripts/bootstrap.{ps1,sh}`, `scripts/install.{ps1,sh}` (CLI installers; not Studio)
  - `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`, `docs/runbooks/LOCAL_DEV.md`
  - `BeQuite_MASTER_PROJECT.md`, root `CHANGELOG.md` — preserved at root

**New (v1 features delivered):**
- `.claude/commands/bq-now.md` — quick orientation; one-line status + next command
- `commands.md` (repo root) — full human-readable command reference; workflow-ordered; linked from README
- `--mode fast|deep|token-saver` flag added to `/bq-auto` (depth adjustment; does NOT skip safety gates)
- Mistake memory wired into 7 commands:
  - `/bq-fix` — pattern recognition for recurring root causes
  - `/bq-audit` — systemic patterns across the codebase
  - `/bq-review` — repeat patterns from previous fixes
  - `/bq-red-team` — every BLOCKER + most HIGH findings become MISTAKE_MEMORY entries with attack-angle tags
  - `/bq-verify` — patterned failures (CI ≠ local drift, recurring strict-mode silencing)
  - `/bq-auto` — auto-mode appends entries for surfaced patterns
  - `/bq-live-edit` — frontend patterns (design-system slips, responsive misses, token violations)

**Updated:**
- `README.md` — version bump to alpha.5; badge shows 37 commands; explicit `commands.md` link surfaced near the top; command map updated; roadmap moved alpha.4 items to "MVP now" and deferred remaining items to alpha.6
- `CLAUDE.md` — version bump; new file paths; mistake memory + `/bq-now` + `commands.md` referenced
- `docs/specs/COMMAND_CATALOG.md` — added `/bq-now` entry; bumped tallies; pointed at `commands.md`
- `docs/changelogs/CHANGELOG.md` — alpha.5 Unreleased section moved to released; alpha.6 pending

**Tally:**
- Commands: 36 → 37 (+1: `/bq-now`)
- Skills: 15 (unchanged)
- Hard human gates: 17 (unchanged)
- Mistake-memory-wired commands: 0 → 7
- New top-level docs: 1 (`commands.md`)
- Architecture docs: 4 (alpha.4 wrote 4 missing ones — total 7 active)

**Trendy/catchy command research outcome:**
Considered candidates (per user's deep-research ask): `/bq-spec` (Spec Kit interop), `/bq-explain` (plain-English file explainer), `/bq-undo` (rollback last command), `/bq-cost` (session token spend), `/bq-vibe` (vibe-handoff). Added only `/bq-now` (highest daily-driver impact); deferred others to alpha.6+ to keep the slash-command surface lightweight per FEATURE_EXPANSION_ROADMAP discipline.

**Pending (alpha.6 — explicitly deferred):**
- 20 alpha.1 commands retroactively extended with new template sections (Preconditions / Required gates / Quality gate / Failure behavior) — mechanical work; substantial
- Installer auto-copies `.bequite/principles/TOOL_NEUTRALITY.md` + `.bequite/uiux/` templates into target projects on `/bq-init` (script update)
- Live verification of `/bequite` inside Claude Code against a fresh real-world project (user action)
- Architecture docs expanded from concise summaries to full reference depth (WORKFLOW_GATES / RESEARCH_DEPTH_STRATEGY / FEATURE_AND_FIX_WORKFLOWS / DEVOPS_CLOUD_SAFETY)
- Additional trendy commands evaluated above (`/bq-spec`, `/bq-explain`, `/bq-undo`, `/bq-cost`)

**Heavy-app status:**
- alpha.1 → alpha.4: "paused, on disk"
- alpha.5 (this commit): **`studio/` + studio-specific files removed from main branch; preserved in git history**
- Other heavy assets (`cli/`, `tests/`, `template/`, `evidence/`, `examples/`, root state/skill/prompts) **explicitly preserved** per user instruction

**Article VI honest reporting:**
- Studio cleanup executed surgically — only studio/ + 3 closely-related files. Everything else kept per user's "don't remove other than studio" constraint
- `/bq-now`, mistake-memory wiring, and `--mode` flag are STRUCTURALLY in place (text + spec). The agent runtime behavior of reading/writing MISTAKE_MEMORY.md and respecting `--mode` is per-command interpretation; not enforced by harness hooks
- `commands.md` is human-readable; the canonical agent-readable specs remain at `.claude/commands/<name>.md`
- NOT live-tested in Claude Code against a real project this session — same caveat as alpha.2/.3/.4
- Installer scripts NOT yet updated to copy new alpha.5 templates — deferred to alpha.6

---

## 2026-05-12 — GitHub-ready cleanup pass (v3.0.0-alpha.5 prep — Phase A non-destructive)

**Action:** User invoked `/bq-auto` with a major cleanup + README polish task. The old Studio / heavy CLI / TUI direction must be removed from the GitHub-facing project. README rewritten for VIP coders + new-user clarity.

**Phase A files created/updated (non-destructive, this commit):**
- `.bequite/audits/GITHUB_READY_CLEANUP_AUDIT.md` — full repo inventory, what to keep / remove / rewrite / archive
- `README.md` — full rewrite, 12 sections (hero / what is / why / install / quickstart / how-to-use / command-map / architecture / examples / feature-highlights / tool-neutrality / what-it-is-NOT / roadmap / off-label uses / docs / contributing / license / maintainer)
- `CLAUDE.md` — dropped "two-track history" framing; references retired heavy direction as history, not "paused"
- `docs/decisions/ADR-004-no-heavy-studio-or-cli.md` — formalizes the cleanup decision
- `.bequite/state/MISTAKE_MEMORY.md` — new memory file with template + tag system + pruning rules
- `.bequite/state/ASSUMPTIONS.md` — new memory file with template
- `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md` — proposed 8 future commands grouped into 7 feature families (Bot & automation, Scraping, Marketing & content, Research & intelligence, Product builders, Data & reports, Vertical packs). Plus Fast/Deep/Token-saver mode flags
- `docs/architecture/WORKFLOW_GATES.md` — workflow gate strategy (23 gates, 17 hard human gates, mode-specific overrides)
- `docs/architecture/RESEARCH_DEPTH_STRATEGY.md` — 11-dimension research model + per-mode emphasis table
- `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md` — 12-type feature router + 15-type fix router
- `docs/architecture/DEVOPS_CLOUD_SAFETY.md` — production safety gates + monitoring + rollback discipline
- `docs/changelogs/CHANGELOG.md` — slim, Keep-a-Changelog-compliant; covers alpha.1 → alpha.4 + Unreleased

**Phase B (DESTRUCTIVE — pauses for user authorization):**
The following deletion list is proposed. Will NOT execute without explicit user OK (per ADR-002 hard human gate "destructive file deletion" + ADR-004):

Heavy-direction folders (entire tree):
- `studio/`, `cli/`, `tests/`, `template/`, `evidence/`, `examples/`, `prompts/`, `state/`, `skill/`

Heavy-direction files:
- `docker-compose.yml`, `.dockerignore`, `.env.example`, `Makefile`, `package.json`, `.commitlintrc.json`
- `scripts/docker-up.{ps1,sh}`, `scripts/bootstrap.{ps1,sh}`, `scripts/install.{ps1,sh}`
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`
- `docs/runbooks/LOCAL_DEV.md`

Archive (move, not delete):
- `BeQuite_MASTER_PROJECT.md` → `docs/legacy/MASTER_PROJECT.md`
- `CHANGELOG.md` (148KB heavy lineage) → `docs/legacy/CHANGELOG-legacy.md`; replace root `CHANGELOG.md` with slim pointer

Keep with caveat:
- `BEQUITE_BOOTSTRAP_BRIEF.md` — historical brief, stays at root
- `.bequite/memory/` — internal v2.x Memory Bank, stays (not in public docs)
- `.github/` — needs audit to ensure workflows don't reference removed paths

**Phase C — final commit + push (after user OK on Phase B):**
- `git rm -r` the heavy paths
- Move 2 large historical docs to `docs/legacy/`
- Audit + clean `.github/workflows/`
- Commit + push
- Optional tag v3.0.0-alpha.5

**Pending phase A also:**
- Mistake-memory writes need wiring into 7 commands (`/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit`) — deferred to alpha.5
- Fast / Deep / Token-saver mode flags on `/bq-auto` — deferred to alpha.5
- 20 alpha.1 commands extended with new template sections — deferred to alpha.5

**Result:** repo is now GitHub-ready in terms of public-facing docs + README. Cleanup of heavy folders pauses for user authorization (ADR-002 hard human gate).

**Heavy-app status:**
- alpha.1 → alpha.4: "paused, on disk"
- alpha.5 (proposed, this audit): "removed from main branch; preserved in git history"

**Article VI honest reporting:**
- README is rewritten; not yet rendered + reviewed on github.com
- 4 new architecture docs are stubs that summarize existing inline content; can be expanded later
- The destructive Phase B is intentionally NOT executed in this commit; requires user explicit OK
- Mistake memory + assumptions templates exist; the agent does NOT automatically write to them yet (commands need wiring in alpha.5)

---

## 2026-05-12 — workflow upgrades (v3.0.0-alpha.4): scoped auto + UI variants + live edit

**Action:** User requested three workflow upgrades to keep BeQuite lightweight while making it more useful:

1. **Scoped auto mode** — `/bq-auto` parses `$ARGUMENTS` for 17 intent types and runs ONLY the relevant scope. Continues by default; does NOT pause for plan / clarify / scope approval. Pauses only at 17 hard human gates.
2. **UI/UX variant mode** — `/bq-uiux-variants [N]` generates 1-10 isolated design directions; user picks winner; agent merges.
3. **Live edit mode** — `/bq-live-edit` section-by-section frontend edits using SECTION_MAP.md + (optional) browser automation. No heavy Studio. No auto-installed Playwright.

**Files created (this cycle):**
- `docs/architecture/AUTO_MODE_STRATEGY.md` — 11-section strategy (intent router, scope per intent, continue-by-default rules, hard human gates, output discipline, cost/time, failure handling, resume)
- `docs/architecture/UIUX_VARIANTS_STRATEGY.md` — 10-section strategy (count discipline, direction selection, isolation A/B/C, workflow, report template, acceptance criteria, tool neutrality, when not to use, anti-patterns)
- `docs/architecture/LIVE_EDIT_STRATEGY.md` — 13-section strategy (mental model, when to use / not, workflow, SECTION_MAP, LIVE_EDIT_LOG, edit categories, quality rules, tool neutrality, anti-patterns, failure modes, rollback)
- `.claude/commands/bq-uiux-variants.md` — new command (count rules, isolation strategies, full workflow, report template, hard gate at winner selection)
- `.claude/commands/bq-live-edit.md` — new command (stack detection, dev server detection, three-tier browser inspection, section mapping, edit, verify, log)
- `.claude/skills/bequite-live-edit/SKILL.md` — new skill (14 sections covering stack detection, browser inspection tiers, section mapping, source resolution, edit strategy, responsive checks, screenshots, tests, failures, rollback)
- `.bequite/uiux/SECTION_MAP.md` — template
- `.bequite/uiux/LIVE_EDIT_LOG.md` — template (append-only log)
- `.bequite/uiux/UIUX_VARIANTS_REPORT.md` — template
- `.bequite/uiux/selected-variant.md` — template (winner record)
- `.bequite/uiux/screenshots/.gitkeep`
- `.bequite/uiux/archive/.gitkeep`

**Files updated (this cycle):**
- `.claude/commands/bq-auto.md` — full rewrite: 17 intent types, $ARGUMENTS parsing, continue-by-default, 17 hard human gates (replaced the 12 from alpha.2)
- `CLAUDE.md` — v3.0.0-alpha.4 spec, 36 commands, 15 skills, hard gate list expanded, new file paths, new architecture docs, intent types
- `docs/specs/COMMAND_CATALOG.md` — added bq-uiux-variants, bq-live-edit, expanded bq-auto entry with intent types + 17 hard gates
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` — added v3.0.0-alpha.4 section with examples for scoped auto / variants / live edit
- `.claude/skills/bequite-frontend-quality/SKILL.md` — activation list extended (uiux-variants, live-edit, auto intents)
- `.claude/skills/bequite-ux-ui-designer/SKILL.md` — new sections "When activated by /bq-uiux-variants" + "When activated by /bq-live-edit"
- `.claude/skills/bequite-testing-gate/SKILL.md` — new section for variant + live-edit verification
- `.claude/skills/bequite-problem-solver/SKILL.md` — note that scoped auto fix + live-edit fix-shaped tasks both invoke this skill
- `.claude/skills/bequite-project-architect/SKILL.md` — activation list extended (auto new, uiux-variants)

**Tally:**
- Commands: 34 → 36 (+2: bq-uiux-variants, bq-live-edit)
- Skills: 14 → 15 (+1: bequite-live-edit)
- Hard human gates in `/bq-auto`: 12 → 17 (added VPS/Nginx/SSL change, paid service activation, secret/key handling, architecture change, deleting old impl with callers; clarified variant winner selection + release git ops as gates)
- Auto intent types: 0 (unscoped) → 17 (new/existing/feature/fix/uiux/frontend/backend/database/security/testing/devops/scraping/automation/deploy/live-edit/variants/release)
- Architecture docs: 1 → 4 (+3)

**Heavy-app status unchanged.**
- No reintroduction of Studio
- No reintroduction of CLI/TUI
- No local dashboard for BeQuite itself
- No Playwright auto-installed (tier-3 code-inspection fallback documented)
- No frontend libs / Docker / testing frameworks added by default

**Result:** v3.0.0-alpha.4 spec complete on disk. Skills registry detects all 15 skills + 36 commands. Auto-mode now scopes per intent; UI/UX variants + live edit available.

**Pending (user-gated, intentionally not auto-done):**
- Live verification in Claude Code against a fresh project
- Tag `v3.0.0-alpha.4` after live verification
- Installer scripts update to copy `.bequite/uiux/` templates + `.bequite/principles/TOOL_NEUTRALITY.md` (carried over from alpha.3)
- 20 alpha.1 commands still don't have the new template sections (Preconditions / Required gates / etc.) — out-of-scope this cycle

**Article VI honest reporting:**
- Skills + commands are structurally correct (YAML validates, SKILL.md format matches Anthropic spec, gate references consistent)
- Cross-references between commands (e.g. `/bq-auto uiux variants=N` → `/bq-uiux-variants N`) are documented but the dispatch logic is the agent's responsibility at run time, not a hard wired router
- Not live-tested in Claude Code against a real project — same caveat as alpha.2/alpha.3
- Browser-automation tier-1 (Playwright MCP) and tier-2 (project-local Playwright) are described in the live-edit skill; the actual MCP tool detection happens at runtime
- No `.bequite/uiux/` templates yet auto-installed in target projects; needs installer update

---

## 2026-05-11 — global correction (v3.0.0-alpha.3): tool neutrality principle

**Action:** User correction. Every tool, library, repo, framework, design system, workflow, or method named in BeQuite is an EXAMPLE, not a fixed mandatory choice. BeQuite must research the project first, choose tools second, justify every pick.

**Files created:**
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth (the rule, 10 questions, decision section format, do-not-auto-install defaults, research-depth rule)
- `docs/decisions/ADR-003-tool-neutrality.md` — formalizes the decision

**Files updated (11 skills):**
- bequite-researcher
- bequite-project-architect
- bequite-frontend-quality
- bequite-ux-ui-designer
- bequite-backend-architect
- bequite-database-architect
- bequite-security-reviewer
- bequite-testing-gate
- bequite-devops-cloud
- bequite-scraping-automation
- bequite-release-gate

Each gained a "Tool neutrality (global rule)" section at the end with: the rule, the 10 decision questions, the decision section format, and a project-specific reframing (e.g. "Drizzle is one candidate. Compare against Prisma, Kysely, raw SQL...").

**Files updated (8 commands):**
- /bq-research — research enables decisions, not commitments
- /bq-plan — §5 stack picks require decision sections, not bare names
- /bq-feature — new deps need decision sections in the mini-spec
- /bq-fix — fixes should rarely add tools; if they do, decision section required
- /bq-audit — recommendations are diagnostic, not prescriptive
- /bq-review — flag any "use X" claim without justification as BLOCKER
- /bq-red-team — adds 9th attack angle: tool choice
- /bq-verify — flags new deps in build lacking decision sections (warning, not blocker)

**Files updated (1 root):**
- CLAUDE.md — tool neutrality is now Core Operating Rule #1; 10 decision questions enumerated; do-not-auto-install added as Rule #12

**Result:** every BeQuite material now explicitly frames named tools as candidates. Concrete examples remain in body text for learning value; the tool-neutrality block at the end of each file makes the framing explicit. Canonical phrasing standardized: "X is one candidate. Research and compare against other options. Use it only if it fits this project."

**Heavy-app status unchanged.** No deletions. No new dependencies installed. No installer changes.

**Pending (user-gated):**
- Live verification in Claude Code
- Tag v3.0.0-alpha.3 after live verification
- Installer scripts update to copy `.bequite/principles/TOOL_NEUTRALITY.md` template into target projects (currently the rule lives in BeQuite's own repo; needs propagation to target installs)
- Future pass to rewrite inline "use X" language across the body of skills/commands (currently the rule is enforced via the block at the end; body text is unchanged)

**Article VI honest reporting:**
- The tool-neutrality block is appended uniformly to all 11 skills + 8 commands; the existing body text still uses some "default X" phrasing in places. The block at the end overrides, but a future pass should rewrite inline language for full consistency.
- Installer scripts have NOT been updated to copy `.bequite/principles/TOOL_NEUTRALITY.md` into target projects. Follow-up task.

---

## 2026-05-11 — direction reset Cycle 2 (v3.0.0-alpha.2): mandatory workflow gates + modes + orchestrators + specialist skills

**Action:** second major direction reset on top of v3.0.0-alpha.1. The brief required BeQuite to **prevent skipping important steps** and force the AI to think like a senior product engineer, architect, researcher, designer, security reviewer, and DevOps engineer before implementation. The alpha.1 spec was advisory only. This cycle introduces enforcement.

**Files created (this cycle):**
- `.bequite/state/WORKFLOW_GATES.md` — gate ledger (23 gates across P0-P5)
- `.bequite/state/CURRENT_MODE.md` — 6-mode selector
- `.claude/commands/bq-mode.md` — mode selector command
- `.claude/commands/bq-new.md` — New Project workflow entry
- `.claude/commands/bq-existing.md` — Existing Project Audit workflow entry
- `.claude/commands/bq-feature.md` — Add Feature workflow with 12-type router
- `.claude/commands/bq-auto.md` — autonomous full-cycle runner with 12 hard human gates
- `.claude/commands/bq-p0.md` through `.claude/commands/bq-p5.md` — six phase orchestrators
- `.claude/skills/bequite-researcher/SKILL.md` — 11-dimension verified evidence
- `.claude/skills/bequite-product-strategist/SKILL.md` — JTBD + persona + MVP
- `.claude/skills/bequite-ux-ui-designer/SKILL.md` — 10 principles + 15 anti-patterns
- `.claude/skills/bequite-backend-architect/SKILL.md` — API + async + caching
- `.claude/skills/bequite-database-architect/SKILL.md` — schema + migrations + indexing
- `.claude/skills/bequite-security-reviewer/SKILL.md` — OWASP + supply-chain
- `.claude/skills/bequite-devops-cloud/SKILL.md` — CI/CD + deploys + safety
- `docs/decisions/ADR-002-mandatory-workflow-gates.md`
- `docs/specs/COMMAND_CATALOG.md`

**Files rewritten (this cycle):**
- `.bequite/audits/DIRECTION_RESET_AUDIT.md` (Cycle 2 appended)
- `.bequite/state/CURRENT_PHASE.md` (updated to 6 phases with orchestrators)
- `.claude/commands/bequite.md` (now gate-aware; reads WORKFLOW_GATES.md, blocks out-of-order recommendations)
- `.claude/commands/bq-research.md` (11 dimensions vs the alpha.1 single-dimension freshness probe)
- `.claude/commands/bq-plan.md` (15 sections; multi-skill activation; quality gate)
- `.claude/commands/bq-multi-plan.md` (unbiased external prompts — explicit no-mention-of-Claude protocol)
- `.claude/commands/bq-fix.md` (15-type problem router; skill activation per type)
- `CLAUDE.md` (reflects 34 commands, 14 skills, gates, modes, hard human gates)

**Tally:**
- Commands: 24 → 34 (+10)
- Skills: 7 → 14 (+7)
- Workflow gates: 0 → 23
- Hard human gates in /bq-auto: 0 → 12
- Modes: implicit → 6 explicit
- Phase orchestrators: 0 → 7 (`/bq-p0` through `/bq-p5` + `/bq-auto`)
- ADRs added: 1 (ADR-002)

**Heavy-app status unchanged (still paused):**
- `studio/`, `docker-compose.yml`, `tests/e2e/`, `cli/` — all paused per Cycle 1 audit; no deletion

**Result:** v3.0.0-alpha.2 spec complete on disk. Skills registry detects all 14 skills + all 34 commands. Ready for live verification inside Claude Code.

**Pending (user-gated, not auto-tagged):**
- Live verification: paste `/bequite` into Claude Code against a fresh project; confirm gate-aware menu renders + blocks out-of-order commands
- Tag `v3.0.0-alpha.2` after live verification
- Decision: continue extending existing 24 commands with full Preconditions / Required gates / Quality gate / Failure behavior sections, OR defer to alpha.3
- Decision: write remaining architecture docs (WORKFLOW_GATES.md narrative, RESEARCH_DEPTH_STRATEGY.md, FEATURE_AND_FIX_WORKFLOWS.md, DEVOPS_CLOUD_SAFETY.md) — currently they live inline within commands + skills

**Article VI honest reporting:**
- I have NOT live-tested `/bequite` inside Claude Code against the new gate-aware behavior. Skills + commands are structurally correct (YAML frontmatter validates, Anthropic Skills SKILL.md format matches, gate references are consistent across commands), but actual command-dispatch behavior is unverified.
- The 24 alpha.1 commands have NOT been retroactively updated with the new `Preconditions` / `Required previous gates` / `Quality gate` sections — only the 4 rewritten commands (research, plan, multi-plan, fix) and 10 new commands have the full template. The other 20 still work but their gate references are advisory until updated.
- I have NOT verified the installer scripts copy the new 7 skills + 10 commands + state file templates. They likely need an update; that's a follow-up.

---

## 2026-05-11 — direction reset to lightweight skill pack

**Action:** reset BeQuite from "heavy app" direction (Studio dashboard + Docker + multi-app) to lightweight project skill pack.

**Files created:**
- `.bequite/audits/DIRECTION_RESET_AUDIT.md` — full keep/pause/delete-later inventory
- `.claude/commands/bequite.md` + 23 `bq-*.md` files (24 total slash commands)
- `.claude/skills/bequite-project-architect/SKILL.md`
- `.claude/skills/bequite-problem-solver/SKILL.md`
- `.claude/skills/bequite-frontend-quality/SKILL.md`
- `.claude/skills/bequite-testing-gate/SKILL.md`
- `.claude/skills/bequite-release-gate/SKILL.md`
- `.claude/skills/bequite-scraping-automation/SKILL.md`
- `.claude/skills/bequite-multi-model-planning/SKILL.md`
- `.bequite/state/{PROJECT_STATE,CURRENT_PHASE,LAST_RUN,DECISIONS,OPEN_QUESTIONS}.md`
- `.bequite/logs/{AGENT_LOG,CHANGELOG,ERROR_LOG}.md`
- `.bequite/prompts/{user_prompts,generated_prompts,model_outputs}/.gitkeep`
- `.bequite/plans/.gitkeep`
- `.bequite/tasks/.gitkeep`

**Files paused (not deleted, per DIRECTION_RESET_AUDIT):**
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`
- `studio/*/Dockerfile`, `studio/*/.dockerignore`
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`

**Result:** SUCCESS — lightweight skill pack structure complete. Ready for live verification inside Claude Code.

**Commits this cycle:**
- 215ed75 — direction reset audit + 5 Phase-0 commands
- 801b893 — 19 more commands (Phases 1-5)
- (this commit) — skills + memory scaffold + installer + docs + ADR-001

**Next:** user reviews + tests `/bequite` in a fresh Claude Code session against a sample project.

---

## (older entries preserved at `.bequite/memory/progress.md` and `docs/changelogs/AGENT_LOG.md`)

For BeQuite's pre-reset history (Studio v2.0.0-alpha.6 audit cycle), see `docs/changelogs/AGENT_LOG.md`.
