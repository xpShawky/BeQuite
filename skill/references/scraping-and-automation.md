# Scraping & Automation reference

> Canonical reference for Article VIII (Constitution v1.1.0). Loaded by the **scraping-engineer** subagent in P1 (stack ADR), P2 (plan), P5 (implement). Cross-references the existing `ai-automation` Doctrine (v0.2.1).
>
> **Do not invent libraries.** Every entry below is verified by URL + star count + last commit (May 2026). Adding a new library requires an ADR + freshness probe pass (`bequite freshness --package <name>`).

## 1. The canonical library list (verified May 2026)

### A. Default scraping triad — pick one based on intent

| Library | Stars | Lang | URL | Pick when |
|---|---|---|---|---|
| **Crawlee** | 22.4k | TS | https://github.com/apify/crawlee | **General default for Node/TS stacks.** Native queues + retries + proxy rotation; wraps Cheerio / Playwright / JSDOM / HTTP. Battle-tested at scale. |
| **Crawlee for Python** | 8.6k | Py | https://github.com/apify/crawlee-python | **General default for Python stacks.** Wraps Parsel / BeautifulSoup4 / Playwright / HTTP. Same queue+retry+proxy ergonomics as Node sibling. |
| **Trafilatura** | 5.5k | Py | https://github.com/adbar/trafilatura | **Default for text-only / RAG / news-article extraction.** Faster + cheaper than Firecrawl when goal is clean readable text. CSV / JSON / HTML / MD / TXT / XML output. Apache-2.0. |
| **Firecrawl** | 117.7k | TS | https://github.com/firecrawl/firecrawl | **Hosted-no-infra easy button** (verified May 2026 — last release v2.9.0 2026-04-10; AGPL-3.0). LLM-ready markdown / structured-data extraction. **Note: AGPL-3.0** — using the self-host inside a closed-source SaaS that *includes* Firecrawl code triggers AGPL network-copyleft. Use the hosted API (paid) or quarantine self-host behind a remote-procedure boundary if you ship closed-source. Use when "I just want clean markdown now" matters more than infra ownership. |
| **Crawl4AI** | 65.3k | Py | https://github.com/unclecode/crawl4ai | **OSS LLM-friendly alternative to Firecrawl** (verified May 2026 — last release v0.8.5 2026-03-18; **Apache-2.0**). LLM-friendly OSS web crawler that emits clean Markdown ready for RAG, with browser pooling and adaptive crawling. Use when AGPL-3.0 of Firecrawl is a license-blocker for your commercial product. |
| **Scrapling** | 30.4k | Py | https://github.com/D4Vinci/Scrapling | **Stealth + selector-resilience specialist.** Single-request → full-crawl. Built-in Playwright integration. MCP server. Auto-adapts when sites change selectors. **Stealth modes require ADR** with `legitimate-basis` field per Article VIII. |

**Decision rule (the triad → single):**

1. Is the stack Node/TS? → **Crawlee**.
2. Is the stack Python? → **Crawlee for Python** (general) OR **Trafilatura** (text-only).
3. Is the goal "give me clean markdown for an LLM" + we don't want to operate infra? → **Firecrawl** (with budget alarm; see §4).
4. Selectors keep breaking? → **Scrapling** (stealth modes ADR-gated).

### B. Specialist scrapers (pick when task fits)

| Library | Stars | Lang | URL | Pick when |
|---|---|---|---|---|
| **Scrapy** | 60.8k | Py | https://github.com/scrapy/scrapy | Mature Python framework. Default for **large multi-page crawls** with pipelines, middlewares, items/loaders, distributed crawling (`scrapy-redis`). |
| **Colly** | 25.2k | Go | https://github.com/gocolly/colly | High-perf Go scraping. Default for **raw speed / low memory in Go stack**. |
| **WebMagic** | 11.7k | Java | https://github.com/code4craft/webmagic | Scalable Java crawler. Default for **JVM stack**. |
| **Ferret** | 5.9k | Go | https://github.com/MontFerret/ferret | Declarative scraping with FQL query language. Default for **SQL-like declarative scraping in Go**. |
| **ScrapeGraphAI** | 23k | Py | https://github.com/ScrapeGraphAI/Scrapegraph-ai | LLM-driven — describe scrape in natural language. Default for **one-off / exploratory scrapes**. |
| **AutoScraper** | 7.1k | Py | https://github.com/alirezamika/autoscraper | Smart auto-scraper — give it a sample, it learns selectors. Default for **fast prototypes**. |
| **Pydoll** | 6.7k | Py | https://github.com/autoscrape-labs/pydoll | Chromium automation without WebDriver (CDP-direct). Anti-detection, captcha-aware. Default when **WebDriver fingerprints are getting flagged**. |
| **Tabula** | 7.4k | Java | https://github.com/tabulapdf/tabula | PDF table extraction. Default for **PDF-bound sources** (regulators, gov docs). Pair with `pdfplumber` for text. |

### C. Browser automation

| Library | URL | When |
|---|---|---|
| **Playwright** | https://github.com/microsoft/playwright | **Default browser automation across the stack.** Cross-browser (Chromium / Firefox / WebKit), cross-language (TS / Py / Java / .NET). Also our verifier in P6. |
| **Puppeteer** | https://github.com/puppeteer/puppeteer | Chrome-only, simpler than Playwright. |
| **Selenium** | https://github.com/SeleniumHQ/selenium | Legacy; only when WebDriver protocol is explicitly required. |

### D. Stealth / anti-detection — **ADR REQUIRED** per Article VIII

> **Stealth is gated.** ADR must enumerate `legitimate-basis ∈ { own-site, bug-bounty-allows, ToS-explicitly-allows, security-research-with-coordinated-disclosure }`. The hook (`pretooluse-scraping-respect.sh`) refuses imports without the ADR's specific field value set.

| Library | Stars | URL | When |
|---|---|---|---|
| **undetected-chromedriver** | 12.5k | https://github.com/ultrafunkamsterdam/undetected-chromedriver | Selenium that bypasses Cloudflare / Distil / Imperva / Datadome. |
| **Camoufox** | 6.2k | https://github.com/daijro/camoufox | Anti-detect Firefox + Playwright. C++/Py. |
| **Scrapling** (stealth mode) | 30.4k | https://github.com/D4Vinci/Scrapling | Default scraper triad option; stealth mode gated separately. |

### E. OSINT / username enumeration — **RoE REQUIRED** per Article IX

| Library | Stars | URL | When |
|---|---|---|---|
| **Sherlock** | 73.6k | https://github.com/sherlock-project/sherlock | Username-OSINT across social media. RoE (`legitimate-basis = security-research-with-coordinated-disclosure` minimum) required for non-self targets. |
| **Maigret** | 19.2k | https://github.com/soxoj/maigret | Dossier-builder by username. Same RoE gate. |
| **Osintgram** | 12.5k | https://github.com/Datalux/Osintgram | Instagram-specific. Heavy ToS implications. RoE + ADR confirming Instagram ToS-allows or bug-bounty path. |
| **SpiderFoot** | 16.9k | https://github.com/smicallef/spiderfoot | Automated OSINT — 200+ modules. Default for **attack-surface mapping of your own assets**. |

### F. Removed from canonical list (do NOT use)

| Library | Why removed | Replacement |
|---|---|---|
| `requests-html` | Last commit Apr 2024; maintainer (Kenneth Reitz) stepped back from OSS. | `httpx` + `selectolax` OR `httpx` + `BeautifulSoup4`. |
| `headless-chrome-crawler` | Last commit Apr 2023; >2 years dead. | `Crawlee` + `Playwright`. |
| `tfsec` | Officially retired into Trivy per the repo description. Last release v1.28.14 2025-05. | `Trivy` (covers IaC scanning). |

These are listed for reference. The hook flags imports of either as warn-level (suggests replacement).

### G. Reference / meta (not deps)

| Resource | URL | Use when |
|---|---|---|
| `awesome-web-scraping` | https://github.com/lorien/awesome-web-scraping | Curated meta-list. **Reference only**, never a dep. |

---

## 2. The decision tree — which library for which scenario

```
START
 │
 ├── Is the goal LLM-ready content for RAG / AI agent?
 │   ├── Want hosted, no infra? ─────▶ Firecrawl
 │   ├── Text-only / news / articles? ─▶ Trafilatura (+ pdfplumber for PDFs)
 │   └── Want NL-driven exploration? ──▶ ScrapeGraphAI
 │
 ├── Is the stack already Node/TS? ────▶ Crawlee
 ├── Is the stack already Python? ─────▶ Crawlee-Python (general) | Scrapy (large pipelines)
 ├── Is the stack already Go? ─────────▶ Colly (general) | Ferret (declarative SQL-like)
 ├── Is the stack already Java/JVM? ───▶ WebMagic
 │
 ├── Site is JS-heavy / SPA / behind login?
 │   ├── Default ─────────────────────▶ Playwright (wrapped by Crawlee or Crawlee-Python)
 │   ├── WebDriver fingerprints flagged? ─▶ Pydoll (CDP-direct)
 │   └── Stealth needed? ──────────────▶ Scrapling stealth mode  *(ADR-gated)*
 │
 ├── Site actively bot-detected (Cloudflare, Distil, Datadome)?
 │   └── ────────────────────────────▶ undetected-chromedriver | Camoufox  *(ADR-gated)*
 │
 ├── Quick prototype / one-off?
 │   ├── Sample-based learning ───────▶ AutoScraper
 │   └── NL-driven ───────────────────▶ ScrapeGraphAI
 │
 ├── Source is PDF? ────────────────────▶ Tabula (tables) + Trafilatura/pdfplumber (text)
 │
 ├── Goal is change-detection + trigger (watch-and-trigger pattern)?
 │   └── ────────────────────────────▶ Scraper (per stack above) + cron/Trigger.dev scheduler + hash-diff detector + webhook → n8n / Zapier / Make / Trigger.dev
 │
 └── Goal is OSINT (username dossier, Instagram-specific, etc.)?
     └── ────────────────────────────▶ Sherlock | Maigret | Osintgram  *(RoE + Article IX gate)*
```

---

## 3. The watch-and-trigger pattern (canonical scaffold)

```
┌─────────────────────────────────────────────────────────┐
│  scheduler (cron / Trigger.dev / GitHub Actions cron /  │
│             Inngest cron / Wazuh rule)                  │
└─────────────────────────────┬───────────────────────────┘
                              ▼
                ┌─────────────────────────┐
                │ scraper (Crawlee /      │  ← respects robots.txt
                │ Trafilatura / Firecrawl │     + rate-limits 1/3sec
                │ / Scrapling)            │     + 24h sqlite cache
                └─────────────┬───────────┘     + ToS reviewed
                              ▼
                ┌─────────────────────────┐
                │ change detector         │
                │ (hash diff / JSON-Patch │
                │ / structural diff /     │
                │ "watch-budget" gate)    │
                └─────────────┬───────────┘
                              ▼
                ┌─────────────────────────┐
                │ trigger (webhook →      │
                │ n8n / Zapier / Make /   │
                │ Activepieces /          │
                │ Trigger.dev / Inngest / │
                │ Slack / email / DB)     │
                └─────────────────────────┘
```

**Context-aware questions when a user describes this pattern (NOT five generic ones):**

1. **"How fresh do you need it?"** (every 1 min / hourly / daily) → picks scheduler tier.
2. **"Public site or behind login?"** → picks scraper. Public + LLM-ready → Firecrawl. Login-required → Crawlee + Playwright. Stealth needed → Scrapling (with ADR).
3. **"How big is the change you care about?"** (any pixel change / specific field / structural) → picks diff strategy.
4. **"What should happen on change?"** (email / Slack / webhook / DB write / kick off workflow) → picks trigger destination + automation tool per the `ai-automation` Doctrine guidance.
5. **"What's the legal basis?"** (Article VIII gate — public data / ToS allows / you own the site / consent on file).
6. **"What's the expected fire frequency?"** (`max_fires_per_week`) → declares the watch-budget; >3× exceeded triggers pause-and-ask.

---

## 4. Polite-mode preset (default ON)

Every BeQuite project that has scraping in its spec gets `polite_mode = true` in `bequite.config.toml::scraping.polite_mode` by default. This one flag enables:

| Setting | Polite-mode value |
|---|---|
| `respect_robots_txt` | `true` |
| `rate_limit_per_domain` | `1 req / 3 sec` |
| `cache_ttl_hours` | `24` (sqlite or redis) |
| `cache_bust_requires_adr` | `true` |
| `stealth_libraries_blocked` | `true` (lifted only by ADR with `legitimate-basis`) |
| `captcha_solving_blocked` | `true` (lifted only by ADR with `legitimate-basis`) |
| `pii_aggregation_requires_consent_log` | `true` |
| `user_agent` | `BeQuite-Scraper/<version> (+contact-from-bequite.config.toml::project.maintainer)` |
| `watch_budget_max_fires_per_week` | `5` (pause-and-ask at 3× = 15 fires) |
| `cost_alarm_warn_usd` | `10` per crawl run |
| `cost_alarm_block_usd` | `100` per crawl run (without ADR) |

To disable: explicit ADR documenting which polite-mode rules are relaxed and why.

---

## 5. Anti-bot / stealth posture

**Default = honest scraping.** Real User-Agent identifying you, robots.txt respected, rate limits enforced, ToS reviewed.

The harness **REFUSES** to silently enable stealth without an ADR. Article VIII non-negotiable.

When the legitimate case is documented (`legitimate-basis ∈ { own-site, bug-bounty-allows, ToS-explicitly-allows, security-research-with-coordinated-disclosure }`), surface (don't recommend) these vendor options. Vendor-naming gated on the RoE-positive context — agents do NOT proactively suggest these absent the ADR.

| Category | Vendors (gated; RoE-positive only) |
|---|---|
| **Residential/mobile proxy rotation** | Bright Data · Oxylabs · Smartproxy · NetNut · Soax |
| **Captcha solver fallback** | 2Captcha · CapSolver · AntiCaptcha · DeathByCaptcha |
| **Fingerprint randomization** | Camoufox built-ins · Scrapling defaults · Multilogin (commercial) |
| **Distributed scheduling** | Crawlee's queue · Scrapy-Redis · Apache Airflow |

---

## 6. MCP servers auto-installed when scraping is detected in the spec

Recommended (the `bequite skill install` command wires these on `--with-scraping`):

- **`firecrawl-mcp-server`** — official Firecrawl MCP at `github.com/firecrawl/firecrawl-mcp-server` (v3.2.1, MIT). Crawl/scrape directly from Claude Code / Cursor / Codex / Gemini. (Note: the underlying Firecrawl service is AGPL-3.0 / paid hosted — see §1A library table.)
- **`scrapling-mcp`** — Scrapling's built-in MCP server.
- **`n8n-mcp` (community)** — at `github.com/czlonkowski/n8n-mcp` (v2.51.1, MIT, ~20.5k stars, **community-maintained, not official n8n-io**). Exposes n8n's 525+ nodes to agents; lets an LLM author + validate n8n workflows.
- **`playwright-mcp`** — already required by Phase 6 verifier; doubles as scraping browser.
- **`context7`** — already required; live up-to-date library docs (resists hallucination of scraping API surfaces).

---

## 7. Compliance map (regulatory frameworks that govern scraping)

| Framework | Scope | Article VIII alignment |
|---|---|---|
| **GDPR (EU)** Art. 6 (lawful basis) + Art. 9 (special-category data) | Personal data of EU residents | PII clause: consent or other lawful basis required; document in spec. |
| **CCPA / CPRA (California)** | Personal info of CA residents | Same as GDPR; "Do Not Sell" + opt-out flows respected. |
| **Egyptian PDPL** (Law No. 151 of 2020) | Personal data in Egypt | Pair with `mena-bilingual` + `mena-pdpl` Doctrines (v0.5.2 / v0.11.0). |
| **Saudi PDPL** (SDAIA) | Personal data in Saudi Arabia | Same. |
| **UAE PDPL** | Personal data in UAE | Same. |
| **CFAA (US)** | Unauthorized access | Stealth + captcha-bypass clauses align. |
| **Computer Misuse Act (UK)** | Unauthorized access | Same. |
| **Robots Exclusion Standard (RFC 9309)** | robots.txt | Always honor `Disallow`. |
| **Site Terms of Service** | Per-site | Skeptic explicitly probes "what does the ToS say" at every scraping phase boundary. |

---

## 8. Examples — golden-path projects

The `template/projects/watch-and-trigger/` template is the canonical scaffold. See also:

- **News-article RAG ingest** — Trafilatura + cron + ChromaDB → answer questions over news.
- **Competitor price watcher** — Crawlee + cron + hash-diff + n8n → Slack on price change.
- **Government regulation tracker** — Tabula + Trafilatura (PDF) + cron + structural diff → email + Linear ticket.
- **Bug-bounty recon** — Crawlee + own-scope-only filter + Nuclei → findings to Linear (paired with Article IX `pentest-engineer` subagent + RoE).

---

## 9. Forking guidance

To fork this reference for a downstream project (e.g. a vertical-specific scraping setup):

1. Copy `skill/references/scraping-and-automation.md` → `.bequite/references/scraping-and-automation-<your-name>.md`.
2. Add or remove libraries with explicit ADRs.
3. Update `decision-tree` for your vertical's specifics.
4. Document compliance overlays (e.g. PCI for payment scraping, HIPAA for medical).
5. The `scraping-engineer` subagent reads from `.bequite/references/` first, falling back to `skill/references/` for unforked entries.

---

## Verification footer

Every library URL + star count + last-release date in this document was verified via GitHub REST API (`api.github.com/repos/{owner}/{repo}` and `/releases/latest`) on **2026-05-10**. Entries also re-verified by `bequite freshness --all` quarterly via CI (planned v0.6.0+).

**License flags worth knowing for commercial use:**
- **Firecrawl, Shannon, BunkerWeb** = AGPL-3.0 — network-copyleft; cannot be embedded in closed-source SaaS. Use the hosted API or quarantine behind a remote-procedure boundary.
- **SafeLine** = GPL-3.0 — strong copyleft; same caveat, slightly less restrictive scope.
- **Strix, Crawl4AI, Crawlee, Crawlee-Python, Trafilatura, Trivy, OSV-Scanner, Nuclei** = Apache-2.0 — clean for closed-source SaaS use.
- **Scrapling** = BSD-3-Clause — clean.
- **Most MCP servers** = MIT — clean.

When in doubt: run `bequite freshness --package <name>` and read the `license` field; cross-reference your own legal-counsel review.
