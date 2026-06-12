# Pain Radar — `/bq-pain-radar` (C6) — alpha.22

Mine **public** pain and turn it into buildable opportunities: MVPs, services, automations, bots, course ideas. Distinct from C10 `/bq-make-money` (which finds earning tracks); pain-radar finds *problems worth building for* — they chain naturally (pain → opportunity → proposal/course).

## Inputs

niche keyword · industry · country/market · language · complaint corpus (user/business) · sources: Reddit, HN, GitHub issues, forums, public X/LinkedIn/Facebook **only when accessible**, user-provided exports/screenshots for auth-gated platforms, official APIs when available, manual collection templates when sources are closed.

## Ethics (hard rules — refusal-grade)

**Do not scrape behind login without permission. Do not bypass authentication. Do not violate platform terms.** If a platform requires login: (1) use its official API if available, (2) ask the user to provide exports/screenshots, (3) use an authorized browser session only if allowed, (4) otherwise public sources only. Every source row in SOURCE_LOG carries access-method + source confidence.

## Outputs — `.bequite/pain-radar/`

PAIN_MAP · SOURCE_LOG · OPPORTUNITY_BRIEFS · MVP_IDEAS · SERVICE_IDEAS · COURSE_IDEAS · AUTOMATION_IDEAS · CONFIDENCE_REPORT (per opportunity: source confidence × opportunity confidence × monetization angle).

## Routing

Skills: researcher + make-money (opportunity verification discipline) + scraping-automation (polite-mode, only when scraping public sources is actually needed) + anti-hallucination (every pain claim cites a source or is struck). Next: C10 make-money → C8 proposal → C5 course (see COMMAND_ROUTER "monetize a niche" journey).
