# Feature Expansion Roadmap

**Status:** roadmap only — NOT implementation plan
**Adopted:** 2026-05-12
**Reference:** ADR-001 (lightweight skill pack first), TOOL_NEUTRALITY.md

---

## The principle

BeQuite must stay **lightweight**. Adding 40 new slash commands would create command clutter and dilute discipline.

Instead, group future capabilities into **feature families**. Each family is a combination of:

- One (sometimes zero) new slash command
- Existing skills extended with family-specific procedures
- Templates in `.bequite/`
- Roadmap-only items that don't ship as commands

**Acceptance for any future feature:**
- Does it earn a slash command, or live as a skill / template?
- Does it conflict with tool neutrality (per ADR-003)?
- Does it work with existing gates (per ADR-002)?
- Does it fit lightweight discipline (per ADR-001)?
- Can it be off-label'd (used in domains beyond the obvious one)?

---

## Feature families (proposed)

### Family 1 — Bot & automation builders

| Idea | Type | Notes |
|---|---|---|
| Bot Maker | Roadmap → command (`/bq-build-bot`) | General bot scaffolder; intent: Telegram, Discord, Slack, WhatsApp |
| Booking Automation Builder | Template | n8n/Make/Zapier candidates per tool neutrality; not auto-installed |
| Website Change Monitor | Roadmap → command (`/bq-monitor`) | Watches URLs, triggers actions on diff; pairs with scraping skill |
| Auto Refresh Trigger | Skill extension | Part of scraping-automation skill |
| Notification Bot Builder | Template | Per platform (Telegram / Slack / Email) |
| Sales Agent Builder | Template + skill | Personality + sales workflow; CRM-agnostic |
| Support Bot Builder | Template + skill | FAQ + escalation patterns |

**Proposed command (1):** `/bq-build-bot "platform + purpose"` — scaffolds a bot with safety gates, env-var template, deployment hint.

### Family 2 — Scraping & data extraction

| Idea | Type | Notes |
|---|---|---|
| Scraping Product Builder | Skill extension | Already in `bequite-scraping-automation` |
| Price Tracker Builder | Template | Pairs with Website Change Monitor |
| Stock Availability Tracker | Template | Same pattern |
| Lead Finder | Template + ADR | Requires explicit ToS / GDPR / PDPL review |
| Competitor Intelligence Bot | Roadmap | Heavy ToS risk; needs ADR per target |

**No new command.** All scraping flows route through `bequite-scraping-automation`.

### Family 3 — Marketing & content

| Idea | Type | Notes |
|---|---|---|
| Marketing Campaign Builder | Roadmap → command (`/bq-marketing`) | Persona + JTBD + channel pick |
| Media Buying Analyzer | Skill extension | Analyzes Facebook / Google ads data |
| Ad Creative Generator | Template | Brand-voice tool integration (off-label) |
| Content Writer Skill Factory | Template + skill | Per niche (SaaS / healthcare / finance) |
| Human Academic Writer | Skill extension | Research-heavy; uses `bequite-researcher` |
| Lecture Builder | Template + skill | Off-label use of plan + research workflow |
| Course Builder | Template | Pairs with Lecture Builder |
| Tender/Proposal Writer | Template | Off-label; uses plan + research workflow |

**Proposed command (1):** `/bq-content "type + topic + audience"` — single command that routes by `type` (campaign / academic / lecture / proposal / blog).

### Family 4 — Research & intelligence

| Idea | Type | Notes |
|---|---|---|
| Research Assistant Builder | Skill extension | Already covered by `bequite-researcher` |
| SaaS Idea Validator | Roadmap → command (`/bq-validate`) | Runs `bequite-product-strategist` + `bequite-researcher` |
| Competitor Intelligence Bot | Template | Off-label of research workflow |
| Decision Support Tool | Template | Uses multi-model planning |

**Proposed command (1):** `/bq-validate "idea description"` — runs scoped research + JTBD + persona + differentiation tests; produces VALIDATION_REPORT.md.

### Family 5 — Product builders

| Idea | Type | Notes |
|---|---|---|
| Landing Page Generator | Skill extension | Uses `bequite-ux-ui-designer` + variants |
| Dashboard Generator | Skill extension | Same |
| Internal Tool Builder | Roadmap → command (`/bq-saas`) | Lightweight admin tool scaffolder |
| Micro-SaaS Factory | Roadmap | Full lifecycle / template; off-label of new project mode |
| Agent Marketplace Template | Roadmap | Template for shipping BeQuite skills as commercial products |

**Proposed command (1):** `/bq-saas "domain + audience"` — full-lifecycle scaffolder; runs P0→P5 with SaaS-specific templates.

### Family 6 — Data & reports

| Idea | Type | Notes |
|---|---|---|
| Data Cleaner | Roadmap → command (`/bq-data`) | Pandas/SQL cleaning playbooks |
| Report Generator | Roadmap → command (`/bq-report`) | Markdown / PDF / dashboard outputs |
| QA Bot | Skill extension | Uses `bequite-testing-gate` + `bequite-frontend-quality` |
| Style Cloner | Template + skill | Brand-voice + variants |
| Persona Simulator | Template | Multi-model planning + persona |

**Proposed commands (2):** `/bq-data "task"` and `/bq-report "subject + audience"`.

### Family 7 — Local business / vertical packs

| Idea | Type | Notes |
|---|---|---|
| Local Business Automation Pack | Template family | Per industry (clinic, gym, restaurant, retail) |
| Medical/Pharmacy Assistant Builder | Template + doctrine | Healthcare HIPAA doctrine + safety gates |
| UI Remix Generator | Skill extension | Uses variants + live-edit |
| Auto Documentation Builder | Skill extension | Uses writing discipline + research |

**No new commands.** All route through existing `/bq-feature` or `/bq-auto` with templates.

---

## Roadmap commands summary

| Possible command | Family | Replaces | Priority |
|---|---|---|---|
| `/bq-build-bot` | Bot & automation | None | v2 |
| `/bq-monitor` | Scraping & monitoring | None | v2 |
| `/bq-marketing` | Marketing & content | None | v2 |
| `/bq-content` | Marketing & content | None | v2 |
| `/bq-validate` | Research & intelligence | None | v2 |
| `/bq-saas` | Product builders | None | v2 |
| `/bq-data` | Data & reports | None | v2 |
| `/bq-report` | Data & reports | None | v2 |

**Total proposed new commands: 8 (vs. ~40 if each idea got its own).**

Names are placeholders. Research + user feedback would refine them.

---

## Cross-cutting features (apply to all families)

### Fast Mode / Deep Mode / Token Saver Mode

Proposed flags on `/bq-auto`:

```
/bq-auto fix "..." --mode fast       # shorter workflow, minimal research
/bq-auto new "..." --mode deep       # full research + multi-plan + red-team
/bq-auto fix "..." --mode token-saver  # summarize old context, focused skills only
```

**Fast Mode:**
- Skip 11-dim research (use 3 dims: stack, scalability, security)
- Skip multi-model planning
- Skip red-team
- Run verify

**Deep Mode:**
- Full 11-dim research
- Multi-model planning prompted
- Red-team mandatory
- Full verify + audit

**Token Saver Mode:**
- Read only memory files needed for this task
- Avoid loading all docs every session
- Summarize older log entries to recent ~5
- Use focused skills (not all 15)
- Cache research results

**Status:** roadmap. To ship: add `--mode` flag parsing to `/bq-auto`; each mode modifies the scope per intent.

### Mistake Memory (alpha.5)

Already specified at `.bequite/state/MISTAKE_MEMORY.md`. Commands need wiring (alpha.5 work).

### Next Best Command

Already implemented via `/bequite` gate-aware menu. Future: improve recommendation quality based on `MISTAKE_MEMORY` + `ASSUMPTIONS`.

### Browser inspection tiers

Already specified in `bequite-live-edit` skill (3 tiers). Future: extend to `/bq-uiux-variants` and `/bq-audit`.

### Section mapping

Already in `.bequite/uiux/SECTION_MAP.md`. Future: expand to backend section mapping (API route → handler → tests).

---

## Feature roadmap detail (per family)

### Family 1 — Bot & automation: `/bq-build-bot`

- **Use cases:** Telegram bot for bookings, Slack bot for status reports, WhatsApp bot for customer support, Discord bot for community FAQ.
- **Skill:** new `bequite-bot-builder` SKILL.md
- **Command needed:** Yes (`/bq-build-bot "platform + purpose"`)
- **Templates:** per-platform starter code
- **Scraping?** Maybe (for monitoring bots)
- **VPS/cloud?** Yes (deployment gate)
- **Safety gates:** PII handling, paid API activation, secret/key
- **MVP / V1 / V2:** V2
- **Complexity:** medium
- **Why it helps:** common request; lightweight if templates are well-designed

### Family 2 — Scraping: skill extension only

- **Use cases:** Price tracker, stock availability, lead finder, change monitor
- **Skill:** `bequite-scraping-automation` (existing) — add new procedures
- **Command:** No (route through `/bq-feature scraping` or `/bq-auto scraping`)
- **Templates:** per-target patterns
- **Safety gates:** robots.txt, polite-rate, no captcha, no PII without consent
- **MVP / V1 / V2:** V1
- **Why it helps:** discipline already exists; just adds patterns

### Family 3 — Content: `/bq-content`

- **Use cases:** Marketing campaign, academic writer, lecture builder, proposal writer
- **Skill:** new `bequite-content-writer` SKILL.md
- **Command needed:** Yes (`/bq-content "type + topic + audience"`)
- **Templates:** per content type
- **Safety gates:** Brand voice, citation accuracy, no plagiarism
- **MVP / V1 / V2:** V2
- **Why it helps:** off-label uses are huge; consolidates a lot of demand

### Family 4 — Validation: `/bq-validate`

- **Use cases:** SaaS idea validation, market fit check, competitor analysis
- **Skill:** `bequite-product-strategist` + `bequite-researcher` (existing)
- **Command needed:** Yes (`/bq-validate "idea"`)
- **Templates:** validation report template
- **Safety gates:** None (research-only)
- **MVP / V1 / V2:** V2
- **Why it helps:** common pre-build question; single command saves a flow

### Family 5 — SaaS factory: `/bq-saas`

- **Use cases:** Internal admin tool, micro-SaaS, dashboard
- **Skill:** existing 15 + new `bequite-saas-scaffolder` SKILL.md
- **Command needed:** Yes (`/bq-saas "domain + audience"`)
- **Templates:** SaaS starters per scale tier
- **Scraping?** No
- **VPS/cloud?** Yes
- **Safety gates:** All existing gates
- **MVP / V1 / V2:** V2
- **Why it helps:** "new project" is too generic; SaaS-specific scaffold is high-value

### Family 6 — Data & reports: `/bq-data`, `/bq-report`

- **Use cases:** ETL playbook, KPI dashboard, executive report
- **Skill:** new `bequite-data-engineer` + `bequite-report-writer`
- **Commands:** 2 (`/bq-data`, `/bq-report`)
- **Templates:** per output format
- **MVP / V1 / V2:** V2
- **Why it helps:** business / ops users have specific needs

### Family 7 — Vertical packs

- **Use cases:** Clinic management, gym booking, restaurant ordering, retail inventory
- **Skill:** existing 15 + new doctrine packs (healthcare, hospitality, etc.)
- **Command:** No (route through `/bq-feature` with doctrine-specific templates)
- **Templates:** Per industry
- **Safety gates:** Doctrine-specific (HIPAA, PCI, PDPL, etc.)
- **MVP / V1 / V2:** V2
- **Why it helps:** templates compound; vertical fit is huge for B2B

---

## What we REJECT

- ❌ Building a Studio dashboard (per ADR-001)
- ❌ Building a heavy Python CLI / TUI (per ADR-001, ADR-004)
- ❌ Auto-installing dependencies (per ADR-003)
- ❌ 40 separate slash commands (command clutter)
- ❌ Removing tool neutrality for "easier" defaults
- ❌ Skipping gates for "fast mode" (fast mode adjusts scope, not safety)
- ❌ Generic "AI agent marketplace" features (we ship a skill pack; users build their own)

---

## What we'd consider with hesitation

- ❓ A `studio-lite/` browser-based memory inspector (zero deps, vanilla HTML) — only if user pull is strong
- ❓ A Python helper for `bequite skill install` from a registry — only after multi-host support exists
- ❓ Self-hosted MCP server for BeQuite — only when Claude Code MCP ecosystem stabilizes

---

## Final positioning

**BeQuite is a thinking layer, not a product builder.** Future commands extend the thinking layer to new domains; they don't make BeQuite an "app".

The slogan stays: **research → plan → build → verify → log**. Every new family follows that arc.

When you can't decide whether a feature is BeQuite-shaped, ask: does it strengthen the agent's thinking, or replace it? Strengthen → yes. Replace → no.
