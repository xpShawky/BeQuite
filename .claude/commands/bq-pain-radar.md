---
description: Pain Radar (C6). Mine PUBLIC pain in a niche/industry/market and turn it into buildable opportunities — MVP, service, automation, bot, and course ideas with source + opportunity confidence. Differs from /bq-make-money (earning tracks): pain-radar finds problems worth building for. Never scrapes behind login, never bypasses auth, never violates platform terms.
---

# /bq-pain-radar — public pain → buildable opportunities (C6)

Full spec: `docs/specs/PAIN_RADAR.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block.

## Syntax

```
/bq-pain-radar "<niche / industry>" [country=<market>] [language=<lang>]
/bq-pain-radar from-exports "<path to user-provided exports/screenshots>"
```

## Ethics (refusal-grade — checked before any source access)

**No scraping behind login without permission. No authentication bypass. No platform-terms violations.** Auth-gated platform ⇒ offer in order: (1) official API, (2) user-provided exports/screenshots, (3) authorized browser session only if allowed, (4) public sources only. Every source logged with access method + confidence.

## Steps (after contract steps 1–7)

1. **Source sweep** (public/authorized only): Reddit, HN, GitHub issues, forums, public X/LinkedIn/Facebook where accessible, official APIs, user exports → `SOURCE_LOG.md`.
2. **Pain mapping** — cluster complaints into named pains with frequency, intensity, who-pays signals → `PAIN_MAP.md`. Every pain cites sources (anti-hallucination: citation-or-strike).
3. **Opportunity shaping** — per strong pain: `OPPORTUNITY_BRIEFS.md` + categorized idea files (MVP / SERVICE / COURSE / AUTOMATION) with monetization angle each.
4. **Confidence** — `CONFIDENCE_REPORT.md`: source confidence × opportunity confidence per the alpha.21 bands; weak-evidence ideas marked clearly, not hidden.

## Writes

`.bequite/pain-radar/{PAIN_MAP,SOURCE_LOG,OPPORTUNITY_BRIEFS,MVP_IDEAS,SERVICE_IDEAS,COURSE_IDEAS,AUTOMATION_IDEAS,CONFIDENCE_REPORT}.md` + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

researcher · make-money (verification discipline) · scraping-automation (polite-mode, public targets only, only if live scraping is actually warranted) · anti-hallucination.

## Next Command Recommendations (typical — the "monetize a niche" journey)

Required next: **C10 `/bq-make-money`** (match pains to earning tracks) — can auto-run: yes. Set: C8 `/bq-proposal` (pitch a chosen opportunity) · C5 `/bq-course` (if an education product is viable) · W4.2 `release proof` (once something ships). Do not run yet: C8 proposal before an opportunity is chosen — pitching without a validated pain is the overpromise path.
