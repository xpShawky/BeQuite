---
description: Find real work opportunities — full-time / part-time / remote / freelance / tasks / AI-assisted gigs — based on country, skills, languages, AI tools, payment methods, and availability. Supports worldwide_hidden mode for overlooked opportunities. Live research at runtime; safety-first; no scams.
---

# /bq-job-finder: real openings, checked before you see them

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A business-pack command. It searches live in the user's languages, checks every listing for scams and for whether the user's country is admitted, and writes short pitches from the user's real proof. The procedure, where to look and the worked example are in `bequite-job-finder`; payout paths for freelance platforms come from `bequite-make-money`.

## Syntax

```
/bq-job-finder ["<situation or filter>"] [worldwide_hidden=true]
```

`worldwide_hidden=true` also searches regional boards and non-English sites in the user's languages; each find gets the full check and a line on why it is overlooked.

Not for earning routes without an employer or client (`/bq-make-money`). It never invents experience: a CV or pitch uses only the user's facts.

## Gates

Needs `BEQUITE_INITIALIZED`. BeQuite never applies, messages a recruiter, fills a form or accepts terms. Reading a professional network in the user's own browser needs their OK each time, and stays read-only.

## Steps

1. **Profile:** read `.bequite/jobs/JOB_PROFILE.md` (if under 30 days old), or ask once and save it: country and city, languages and level, role and seniority, skills with one proof each (a link, a repo, a portfolio), the kind of work, remote or on-site, minimum pay and currency, payout methods, time zone.
2. **Search strings** from the profile in each language: role synonyms, seniority, the variants of "remote".
3. **Collect** 15 to 30 raw listings with URL, company, date posted, location rule, and pay if stated.
4. **Check each** and record it in `.bequite/jobs/TRUST_CHECKS.md`: the company exists outside the post; the post is on its own careers page or a reputable board; no fee to apply, train or be placed, no cheque to forward, no reshipping; the location rule admits the user's country; contractor or employee and how they pay; posted within 30 days.
5. **Classify:** best fit, easy start, high pay, fast apply, needs a portfolio first, needs learning first, risky or unclear, not recommended (with the failed check), hidden gem.
6. **Write** `OPPORTUNITIES.md` (the top 10 to 15 with their check rows) and `PITCH_TEMPLATES.md` (one per kind of opening, under 200 words: the deliverable first, then the proof link, then availability). `APPLICATION_TRACKER.md` is the user's to maintain.
7. **Repeat runs:** mark new, still open, expired, risk increased, and append the changes to `JOB_SEARCH_LOG.md`.

## Output

```
Listings checked: <n>    shown: <n>    not recommended: <n> (reasons in TRUST_CHECKS.md)
Best fit: 1. <role, company, location rule, posted <date>>  2. ...  3. ...
Pitches: .bequite/jobs/PITCH_TEMPLATES.md
```

## Quality gate

Every listing shown has its URL, date posted, location rule and check row; anything that asks the candidate for money appears only as a warning; pitches contain only the user's real facts; results are in the user's languages, not English only; at least five verified openings or an honest smaller number.

## Next Command Recommendations (typical)

Pick two or three and apply yourself · `/bq-make-money` for income alongside the search · re-run weekly.
