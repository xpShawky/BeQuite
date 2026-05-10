---
adr_id: ADR-009-article-viii-scraping
title: Article VIII added — scraping & automation discipline; Constitution v1.0.1 → v1.1.0
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
superseded_by: null
constitution_version: 1.0.1   # decided UNDER 1.0.1; output is 1.1.0
related_articles: [VIII]
related_doctrines: [default-web-saas, ai-automation, library-package]
---

# ADR-009: Article VIII added — scraping & automation discipline

> Status: **accepted** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

A huge class of real BeQuite-managed projects is "watch X, when it changes, trigger Y" — the watch-and-trigger pattern. Current AI coding agents are bad at it: they hallucinate scraping libraries that don't exist, ignore `robots.txt`, get blocked by Cloudflare on day 2, scrape personal data without consent (GDPR / CCPA / Egyptian PDPL violations), and roll custom integrations when n8n / Zapier / Make already solve the problem.

The existing `ai-automation` Doctrine (v0.2.1) governs *workflow* automations (n8n, Make, Zapier, Temporal, Inngest). It does not govern the *scraping inputs* that feed those workflows — and scraping is exactly where AI agents most often produce malpractice.

Without a Constitution-level rule, agents will keep producing scrapers that violate ToS, ignore rate limits, harvest PII, and trip stealth measures without legitimate basis. The lessons from the `ai-automation` Doctrine (v0.2.1) — workflows-as-source / idempotency / retry+DLQ / secrets-via-connector / observability — apply equally to scraping inputs, and need their own canonical placement.

## Decision

Add **Article VIII — Scraping & automation discipline** to the Constitution as an Iron Law. Bump Constitution `1.0.1 → 1.1.0` (minor; additive only — no Iron Law removed or relaxed).

The article is renumbered from the brief's "Article XI" to fit BeQuite's existing 7-Iron-Law structure (we trimmed from the original 10 articles to 7 in v0.1.0). The substantive text is otherwise verbatim from the addendum, with four amendments based on senior-architect review:

1. **Default rate limit changed from `1 req/sec/domain` → `1 req/3 sec/domain`** — polite-scraper-aligned (Googlebot, Bingbot, Common Crawl average 1 req every 2-10s/domain). Faster requires explicit ADR.
2. **Stealth requires `legitimate-basis ∈ { own-site, bug-bounty-allows, ToS-explicitly-allows, security-research-with-coordinated-disclosure }`** — not just "an ADR exists." The hook greps the ADR for the specific field value.
3. **Captcha-solving clause added** — solving captchas is in many jurisdictions equivalent to bypassing access controls (CFAA-class). Forbidden by default; allowed only with ADR + same legitimate-basis enumeration.
4. **Watch-budget added** — every watch-and-trigger flow declares `max_fires_per_week`; 3× exceeded → pause and ask. Catches noisy-diff cascades.

## Rationale

- **Pairs with `ai-automation` Doctrine (v0.2.1):** that Doctrine governs the workflow-execution side; this Article governs the scraping-input side. Together: full watch-and-trigger.
- **Catches the most common AI-vibe-coding scraping failures:** hallucinated libraries (cross-references existing Article VII + `pretooluse-verify-package.sh`), robots.txt ignored, ToS unread, PII aggregated without consent, custom integration where n8n exists.
- **MENA-aware compliance:** explicit reference to Egyptian PDPL (Law No. 151 of 2020), Saudi PDPL, UAE PDPL alongside GDPR/CCPA. Aligns with `mena-bilingual` Doctrine (v0.11.0).
- **Anti-PII-aggregation hook addition (improvement I1.3 from session):** previous Articles forbade PII aggregation in *prose*; the new hook makes it *enforceable* (greps for `phone`/`ssn`/`email`/`address` field assignments from scraped HTML without consent-log path).
- **Watch-budget addition (improvement I1.4):** the cost-economist persona handles LLM-call cost; scraping cost (Firecrawl credits + proxy cost + bandwidth) is a separate budget worth its own discipline.

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| Keep "Article XI" numbering | Verbatim with addendum | Creates gap (Constitution has VII, then jumps to XI) | Renumbering to VIII keeps structure consistent |
| Add as a Doctrine, not an Iron Law | Lighter; Doctrines fork easily | Robots.txt / consent / rate limit are universal, not project-type-specific | These rules apply to every project that scrapes; Iron Law is the right home |
| Default rate-limit 1 req/sec | Faster for owned sites | Trips rate limits on smaller sites; not polite-scraper-aligned | 1 req/3 sec polite default; ADR for faster |
| No captcha clause | Lighter rule surface | Captcha-bypass is a real legal exposure; silence implies permission | Add clause |

## Consequences

### Positive

- AI-vibe-coded scrapers can no longer produce GDPR / PDPL violations silently.
- The watch-and-trigger pattern has canonical scaffold; users stop reinventing.
- Hooks make discipline enforceable, not documentary.
- MENA compliance gets first-class mention (no other AI coding harness does this).

### Negative

- One more Iron Law (eight total). Cognitive surface grows.
- The hook needs maintenance (regex-based detection has false-positive surface).
- Rate-limit default of 1 req/3 sec is slower than what some users will want — they need to write an ADR for a sane reason. Some friction.

### Constitutional impact

- Patch bump → Minor bump. v1.0.1 → v1.1.0. No Iron Law removed or relaxed; purely additive.

### Refactoring path

- If we ever want to make Article VIII conditional (only when scraping is in the spec), the path is a future minor bump that turns it into a Doctrine. Unlikely; the rules are universal enough for Iron Law.

## Verification

- ✅ Constitution v1.1.0 amendment applied to `.bequite/memory/constitution.md`.
- ✅ `skill/templates/constitution.md.tpl` to be updated in v0.5.2 (after Article IX is also added; reduce template churn).
- ✅ `skill/references/scraping-and-automation.md` exists with the verified library list + decision logic + watch-and-trigger pattern + polite-mode + carve-outs.
- ✅ `skill/agents/scraping-engineer.md` exists; subagent invoked in P1/P2/P5 when scraping/automation is in the spec.
- ✅ `skill/hooks/pretooluse-scraping-respect.sh` blocks unsafe scraper commits (robots.txt missing / rate-limit missing / stealth without ADR / captcha without ADR / PII-aggregation without consent log).
- ✅ `skill/templates/projects/watch-and-trigger.md` ships canonical scaffold with n8n in `docker-compose.yml` (opt-out via `--no-n8n`), polite-mode default ON, watch-budget declared.
- ✅ `bequite audit` rule pack adds Article VIII checks (in v0.6.0+).

## References

- Related ADRs: ADR-008-master-merge (last Constitution amendment).
- External docs:
  - GDPR Art. 6 (lawful basis for processing) — https://gdpr-info.eu/art-6-gdpr/
  - Egyptian PDPL (Law No. 151 of 2020) — https://www.dpc.gov.eg/
  - Saudi PDPL (SDAIA) — https://sdaia.gov.sa/
  - UAE PDPL — https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws
  - Robots Exclusion Standard (RFC 9309) — https://www.rfc-editor.org/rfc/rfc9309
  - PhantomRaven incident (Koi Security, Aug-Oct 2025).
- Memory Bank entries: `.bequite/memory/systemPatterns.md::ADR index`, `.bequite/memory/progress.md::Decisions made`.

## Amendments

```
2026-05-10 — initial draft + accepted in same session per Ahmed's "make it fully loaded" delegation.
```
