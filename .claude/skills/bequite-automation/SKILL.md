---
name: bequite-automation
description: Use when a project needs data from websites, a watch-and-trigger job, a scheduled workflow, a webhook handler or a bot (Telegram, Discord, WhatsApp, web chat), through /bq-knowledge automation, /bq-offer local-business, /bq-knowledge integrate or a plan that includes scraping. Official API first; where there is none, Scrapling is the default engine with polite settings; every automation ships with idempotency, bounded retries, signature checks, logs and a kill switch. Replaces the former scraping-automation and automation-engineer skills.
last_verified: 2026-11-21
sources:
  - https://pypi.org/project/scrapling/
  - https://github.com/D4Vinci/Scrapling
  - https://www.rfc-editor.org/rfc/rfc9309
  - https://core.telegram.org/bots/api
  - https://core.telegram.org/bots/faq
  - https://docs.stripe.com/api/idempotent_requests
  - https://docs.stripe.com/webhooks
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
  - https://github.com/n8n-io/n8n/blob/master/LICENSE.md
  - https://github.com/microsoft/playwright-mcp
---

# bequite-automation

Get the data the cleanest legal way, and make every automated action safe to run twice. Installs nothing until the project needs it and the choice is written down.

## When to use

- A plan or feature needs website data, monitoring, a scheduled job, a webhook, or a bot.
- `/bq-knowledge automation`, `/bq-offer local-business`, `/bq-knowledge integrate`.

Not for: one API call inside app code (`bequite-backend-architect`); research reading for a decision (`bequite-researcher` and the browser).

## Layer 1: the data source ladder

1. **Official API or feed** (REST, GraphQL, RSS, sitemap, export, partner programme). Read its terms and rate limits; use it even if slower to set up.
2. **No API, page allowed:** fetch with Scrapling (owner's default engine; 0.5.1, BSD-3-Clause, PyPI 2026-11-04). `pip install "scrapling[fetchers]"` (plain `scrapling` is the parser only); `scrapling install` only when a browser fetch is needed. HTTP `Fetcher` first; the browser fetcher only for pages that render with JavaScript.
3. **The user's own browser** for one-off reading (Chrome extension or the in-app browser), never for bulk.
4. **Stop:** login walls you are not authorised for, CAPTCHAs, paywalls, personal data without consent. Say so and offer the legitimate route (API, partnership, export, asking the owner).

Candidates to compare when Scrapling does not fit: Scrapy 2.20.0 (very large crawls), Crawlee 3.18.2 (JS/TS), Playwright (app-like pages, tests), Trafilatura 2.3.1 (article text). Firecrawl is AGPL-3.0: flag it.

## Polite preset (always start here)

- robots.txt read before the first request (RFC 9309): 5xx or no answer means disallow all; cache it at most 24 hours; respect the most specific rule.
- One request at a time per host and a delay of about 3 seconds (house default; raise only with a written reason); cache pages and skip unchanged ones.
- Honest identity: `stealthy_headers=False` and a User-Agent with a contact. Scrapling's default adds browser-like headers and a Google referer (seen in a run below): off in BeQuite.
- `StealthyFetcher`, Cloudflare solving and proxy rotation are off. Using them needs a decision record with a legitimate basis: own site, written permission, a bug bounty that allows it, or coordinated security research.
- No personal data collected without a lawful basis recorded.

## Layer 2: workflows and bots

Pick the runner by the ten questions: the project's own cron, queue or worker if it has one; GitHub Actions for repo jobs; a durable engine (Temporal, Inngest, Trigger.dev) for long, stateful, retry-heavy flows; a no-code tool for simple flows a non-developer maintains. n8n is under the Sustainable Use License (internal or non-commercial use only; not OSI open source); Activepieces Community Edition is MIT.

Every automation blueprint has:

- **Idempotency:** a stable key per action; store processed IDs; for payment-style APIs send an `Idempotency-Key` (Stripe keeps keys at least 24 hours).
- **Duplicates and order:** webhooks can arrive twice and out of order: dedupe by event ID, never order by "created".
- **Signatures:** verify on the raw body with a constant-time compare (GitHub `X-Hub-Signature-256`; Stripe `Stripe-Signature` with a 5-minute tolerance; Telegram `X-Telegram-Bot-Api-Secret-Token` from `setWebhook`'s `secret_token`).
- **Retries:** bounded, with backoff; a dead-letter list for what exhausts them; alerts on failure.
- **Secrets:** environment or a secret store; never in code, logs or chat.
- **Gates:** dry-run mode; human approval before money, mass messages, deletes or production changes; a kill switch that disables the job in one step.
- **Logs:** one line per run (input ID, action, result) the owner can read.

Bots also need: an allow-list of users or chat IDs, a command whitelist, rate limits (Telegram: about 1 message per second per chat, 20 per minute per group, about 30 per second overall), a path to a human, and no destructive command without confirmation. WhatsApp only through the official Business API or an approved provider.

## Procedure

1. Write the trigger, the data source per the ladder, the actions, and the failure plan in `work/<id>/plan.md`.
2. Record the tool decision (ten questions) and the robots/terms status of each host.
3. Build with the polite preset; test against a saved fixture and once live.
4. Run the reliability checklist above; paste the dry-run output in `evidence.md`.

## Worked example (real run, 2026-11-21)

```
robots.txt https://pypi.org -> can_fetch("/project/scrapling/") = True
Fetcher.get(...)                         -> 200 in 0.53 s, log: "referer: https://www.google.com/"
Fetcher.get(..., stealthy_headers=False, headers={"User-Agent": "BeQuiteResearch/1.0 (contact)"})
                                         -> 200, log: "referer: None"
parsed: "This work is licensed under the BSD-3-Clause License."
```

The default run proved the engine works and exposed the fake referer; the polite run is the one BeQuite ships. For a version check the PyPI JSON API (rung 1) is still better than scraping the page.

## Quality gate

- The official-API question was answered first, with the link.
- robots.txt and terms status recorded per host; polite preset in the code.
- Idempotency, dedupe, signatures, bounded retries, secrets, gates, kill switch and logs present.
- The library and its version were checked in the registry this session.

## Boundaries

No CAPTCHA solving, no stealth without a recorded legitimate basis, no account farming, fake reviews, scalping or personal-data harvesting. Hooks that enforce scraping respect stay opt-in. Names are candidates except Scrapling, the owner's default.
