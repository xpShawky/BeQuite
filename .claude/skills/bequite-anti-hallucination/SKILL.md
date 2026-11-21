---
name: bequite-anti-hallucination
description: Use before any completion claim, review finding, package install, API call from memory, or factual statement in a report. Forces every claim to carry a source or a run from this session, and an explicit UNVERIFIED label otherwise. The Stop hook enforces the same rule at the end of a turn.
last_verified: 2026-11-21
sources:
  - https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
  - https://code.claude.com/docs/en/hooks
  - https://arxiv.org/abs/2406.10279
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://google.github.io/osv.dev/api/
  - https://docs.pypi.org/api/json/
---

# bequite-anti-hallucination

One rule: **a claim needs a source or a run.** If neither exists in this session, the claim is written `UNVERIFIED:` or "I don't know: <the gap>". A labelled gap is a valid answer; a confident guess is not.

## When to use

- Any "done", "fixed", "passes", "works" (completion reports, `/bq-verify`, `/bq-implement`, `/bq-fix`).
- Any review, audit or red-team finding.
- Before installing or importing a package, or writing a call to an API you did not read this session.
- Any number, price, limit, version or availability claim in a report.

Not for: brainstorming that claims nothing; quoting the user back to themselves.

## The checks

| # | Claim | Required evidence |
|---|---|---|
| 1 | "Done / passes / works" | `$ command` -> `exit N` -> the lines of output that prove it, in `work/<id>/evidence.md` |
| 2 | "It looks right" (UI, page, slide, film) | A screenshot or a browser read taken this session, saved or quoted |
| 3 | A finding in a review | `path:line` and the quoted code. No quote: retract the finding |
| 4 | A package | Registry check this session (exists, latest version, upload date, licence, repo matches); OSV for the pinned version |
| 5 | An API signature | Docs for the pinned version read this session, unless the call is common and stable (over-fetching stale docs adds error) |
| 6 | A fact or number | URL + date read (`bequite-researcher`); else `UNVERIFIED:` |
| 7 | A risky action | Confidence (high / medium / low, with the reason) and the single biggest unknown |

Low confidence on a load-bearing claim goes to a fresh verifier (`bequite-guard-pass`, run by the `bq-verifier` subagent): it sees the diff and the acceptance criteria, not your reasoning.

## Procedure

1. Before writing the report, list every claim it makes.
2. For each, attach the evidence from the table, or rewrite it as `UNVERIFIED:` with what would settle it.
3. Remove the banned words when they stand in for evidence: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
4. Write the evidence entries in `work/<id>/evidence.md` before saying "done". The Stop hook (when enabled) blocks a completion claim that has no evidence entry for this turn; do not fight it, add the evidence.

## Worked example (real runs, 2026-11-21)

Plan draft said: "Add `scrapling-pro-stealth` for hard sites; jinja2 3.1.4 is safe."

```
$ curl -s -o /dev/null -w "%{http_code}" https://pypi.org/pypi/scrapling-pro-stealth/json
404
$ curl -s -X POST https://api.osv.dev/v1/query -d '{"package":{"name":"jinja2","ecosystem":"PyPI"},"version":"3.1.4"}'
6 advisories: GHSA-cpwx-vrp4-4pq7, GHSA-gmj6-6f8f-6699, GHSA-q2x7-8rv6-6q7h, PYSEC-2026-1471, -1472, -1475
```

Both claims struck. The package does not exist (a slopsquatting target: the study of 16 models found 5.2% to 21.7% of suggested packages were invented), and the pinned jinja2 has six known advisories. The plan now names the real package (`scrapling` 0.5.1) and asks for a jinja2 upgrade.

## Quality gate

- Every success claim has command, exit code and output, or a screenshot for visuals.
- Every finding has a real `path:line` quote.
- No package without a registry check from this session.
- Every uncertain claim is evidence-backed or labelled `UNVERIFIED:`.
- No banned word stands in for evidence.

## Boundaries

This skill inspects and verifies; it installs nothing. It never edits a test or a check to make a claim true. Numbers about models or vendors from memory are `UNVERIFIED:` until a page is read.
