---
description: Find legitimate ways to make money based on user's country, skills, AI tools, time, devices, payment methods, and risk tolerance. Supports tracks (highest-payout / easiest-start / fastest-first-dollar / etc.) and worldwide_hidden mode for overlooked opportunities. Safety-first; no fraud.
---

# /bq-make-money: earning routes that pay out in your country

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A business-pack command. It finds legitimate routes, checks each one on the platform's own pages for the user's country, and turns the best two or three into a seven-day plan. The procedure, the route families, the worked example and the safety rules are in `bequite-make-money`; the source ladder is `bequite-researcher`.

## Syntax

```
/bq-make-money ["<situation>"] [track=<name>] [country=<...>] [skills='<...>'] [worldwide_hidden=true]
```

Tracks: `highest-payout`, `easiest-start`, `fastest-first-payout`, `long-term-stable`, `ai-assisted`, `no-calls`, `remote-global`, `local-only`, `beginner`, `skilled`. No track given: pick one from the profile and say why. `worldwide_hidden=true` also searches beyond the user's region and beyond the famous English-language platforms, in the user's languages; each find gets the same full check.

Not for a job with an employer (`/bq-job-finder`), packaging one offer (`/bq-offer`), or turning finished work into a product (`/bq-productize`). Requests for illegal or unrealistic income are refused with the reason.

## Gates

Needs `BEQUITE_INITIALIZED`. BeQuite never signs up, accepts terms, applies or moves money for the user.

## Steps

1. **Profile:** read `.bequite/money/MONEY_PROFILE.md`, or ask once and save it: country, languages, skills and tools (including AI tools already paid for), hours per week, devices, payout methods already held, risk tolerance.
2. **Shortlist** six to ten candidates for the track from the route families in the skill.
3. **Verify each for this country, live:** residents accepted, a payout path that ends in money the user can use (method, minimum, fee, days), the platform's commission, documents required, location rules, payout complaints and their dates, a realistic first payout date. One row per platform in `.bequite/money/TRUST_CHECKS.md`, every cell with its URL and the date read, or `UNVERIFIED:`.
4. **Exclude** anything that breaks a safety rule or has no verified payout path, and log why.
5. **Rank** for the track and write `OPPORTUNITIES.md` (each route with its check row; hidden finds say why they are overlooked).
6. **Plan:** `ACTION_PLAN.md` for seven days: at most three sign-ups, one concrete deliverable per day, an acceptance test per day, a first-payout target.
7. **Repeat runs:** compare with the last list (new, still active, expired, risk increased, better alternative) and append the changes to `MONEY_SEARCH_LOG.md`.

## Safety rules

No fraud, fake accounts, fake reviews or bought engagement; no CAPTCHA farms; no VPN or false location to pass eligibility; no rented accounts or someone else's identity; no upfront fee to get work; no MLM, pump-and-dump or guaranteed-income schemes; no mass unsolicited outreach; nothing against a platform's terms. No income promise is ever made: pay figures come from the platform's own pages or are marked `UNVERIFIED:`. Tax and legal questions go to an accountant.

## Output

```
Track: <name> (<why>)    verified routes: <n>    excluded: <n> (reasons in TRUST_CHECKS.md)
Top: 1. <route> (first payout ~<date>, via <method>)  2. ...  3. ...
Plan: .bequite/money/ACTION_PLAN.md    Unverified items: <n>
```

## Quality gate

Every recommended route has a payout path verified for the user's country, with URL and date; at least five verified routes or an honest smaller number; no more than three sign-ups in the plan; excluded routes are listed with reasons.

## Next Command Recommendations (typical)

Day 1 of `ACTION_PLAN.md` · `/bq-offer` to package a service · `/bq-job-finder` for a main job · re-run in two to four weeks (country facts older than 30 days are re-checked).
