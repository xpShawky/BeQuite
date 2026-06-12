# Scraping / Web Automation Context Audit (alpha.22 stabilization)

**Run:** 2026-06-12 · Claude Fable 5 · repo-reality evidence. Question: did the scraping/web-automation capability layer survive alpha.22, and is it properly documented?

## Verdict up front: **PRESENT, FIRST-CLASS, NOT WEAKENED.** Nothing was lost in alpha.22 (git diff `bffbd67..5ab5c45` deletes no capability files). One routing gap found and fixed (Command Router had no scraping signal row).

## Question-by-question, with evidence

| Question | Answer | Evidence |
|---|---|---|
| Still present? | **Yes** — 232-line skill | `.claude/skills/bequite-scraping-automation/SKILL.md` |
| Shape? | **Skill** (activates when a target project needs it) + `/bq-auto scraping` and `/bq-auto automation` intents; no command — correct per anti-bloat | bq-auto.md:54-55: "`scraping` \| Scraping workflow \| scraping-automation" |
| First-class when needed? | Yes — auto intents + registry row + router domain + pain-radar companion | SKILL_REGISTRY + SKILL_ROUTER rows verified |
| API-first default? | Yes — decision tree halts at captcha with "Consider whether the target's API would be a legitimate path"; pain-radar rules order official-API first | SKILL.md §Decision tree; bq-pain-radar.md §Ethics |
| Static scraping / crawling / browser / managed-browser documented? | Yes — tool catalog sections: General-purpose (Python) · JS/TS · Specialized · Compiled/Go · **MCP servers (Claude Code / Cursor)** · Workflow automation | SKILL.md §"Verified 2026 tool catalog" headings |
| Change monitoring + triggers? | Yes | SKILL.md §"Watch-and-trigger pattern (canonical scaffold)" + Article VIII #4 "Watch-budget per target. `max_fires_per_week`" |
| Logs/retry/failure-visible? | Yes | SKILL.md §"Output discipline" + polite-mode preset |
| Legal/robots/ToS? | Yes — Article VIII: "robots.txt + ToS respect… No captcha-solving services (CFAA-class concern)… No stealth without legitimate-basis ADR… No PII extraction without consent log" | SKILL.md §Article VIII (quoted) |
| Auto-selected when relevant? | Yes — registry triggers + router map + auto intents; **was missing from COMMAND_ROUTER signals → FIXED this pass** (row added §2) | COMMAND_ROUTER.md §2 (new row) |
| Buried by alpha.22? | No — alpha.22 added pain-radar which *references* the skill ("scraping-automation (polite-mode, public targets only)") | bq-pain-radar.md §Skill routing |
| Skill-only or future `/bq-automation`? | **Skill-only now**; `/bq-automation` remains the strongest parked V2 candidate (spec-first), per the Older-V1 review #7 | APPROVED_CAPABILITY_SHAPE_DECISIONS §V1 #7 |

## The two named docs — honest finding

`docs/architecture/WEB_AUTOMATION_AND_SCRAPING_STRATEGY.md` and `docs/specs/WEB_AUTOMATION_REQUIREMENTS_TEMPLATE.md` **do not exist and never existed in the v3 lineage** (repo-wide search). The v2-era heritage lives at `.bequite/memory/decisions/ADR-009-article-viii-scraping.md` (internal memory) and the retired `skill/` heavy-direction tree (agents/scraping-engineer.md, hooks/pretooluse-scraping-respect.sh). **The v3 canonical carrier is the skill itself**, which contains the strategy (Article VIII + decision tree) AND the requirements discipline (output discipline + quality gate). Ruling: do NOT create duplicate strategy docs — that would be a second source of truth; the skill stays canonical, and the catalog/router now point at it.

## Tool catalog check (user's candidate list vs the skill)

Already in the skill's verified catalog: Scrapy · Crawlee (+ Crawlee Python) · Playwright · Puppeteer · Browserless · Apify · Firecrawl · **Scrapling** · ScrapeGraphAI · AutoScraper · Trafilatura · Colly · browser-use · Playwright MCP · workflow automation (n8n-class). Selenium: correctly positioned as compatibility-only. **"Scrapling" name verified live 2026-06-12** (WebFetch github.com/D4Vinci/Scrapling → "An adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl", v0.4.9 June 2026, actively maintained, ships an MCP server) — the user's earlier "scrappinging" reference = **Scrapling**, already correctly named in the skill. No catalog rot detected; the skill's own rule "always re-verify freshness via WebFetch before installing" stands. **Nothing installed by default** — unchanged.
