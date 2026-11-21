# The eleven research dimensions (load on demand)

Used by `/bq-research` for a product or stack decision. Each dimension ends in a finding with a source, or an `UNVERIFIED:` line. Depth follows the effort: low covers the three dimensions that decide the task; high covers all eleven.

| # | Dimension | Question | First sources |
|---|---|---|---|
| 1 | Stack | Is each candidate alive, licensed for this use, and the right size? | Registry JSON (PyPI, npm, crates.io), GitHub API (`pushed_at`, `archived`, licence), OSV |
| 2 | Product | What is it, for whom, replacing what? | The user's own words; `bequite-product-strategist` |
| 3 | Competitors | Who already solves it, at what price, with which gap? | Competitors' own pricing and docs pages, read today |
| 4 | Failures | What was tried and died, and the specific lesson | Archived repos, post-mortems with numbers |
| 5 | Success | Which reference implementations work, and why here? | Open repos, case studies with numbers |
| 6 | User journey | Trigger, first five minutes, the "why I pay" and "why I cancel" moments | Interviews (past behaviour, not opinions), support forums |
| 7 | UX and UI | Which measured references to follow | `bequite-human-taste`; the live reference sites in the browser |
| 8 | Security | Which risks apply | OWASP Top 10, OWASP LLM Top 10, OSV per dependency |
| 9 | Scale | What load is real now, and in a year? | The user's numbers; never design for 50,000 users when there are 50 |
| 10 | Deployment | Where it runs, limits and price | The host's own limits and pricing pages, read today |
| 11 | Differentiation | Why would a user pick this over the closest alternative? | Concrete capability, a measured 10x, niche fit, language or region fit |

Unacceptable differentiation: "better UX", "modern stack", "AI-powered".

## Registry one-liners

```
curl -s https://pypi.org/pypi/<p>/json            # info.version, releases[v][].upload_time_iso_8601, info.license_expression
curl -s https://registry.npmjs.org/<p>            # dist-tags.latest, time[<v>], license
curl -s https://api.github.com/repos/<o>/<r>      # stargazers_count, license.spdx_id, pushed_at, archived
curl -s -X POST https://api.osv.dev/v1/query -d '{"package":{"name":"<p>","ecosystem":"PyPI"},"version":"<v>"}'
```

A 404 from the registry means the package does not exist: never install a name the model suggested without this check.

## Tie-break between equal candidates

1. More real production use you can cite. 2. Types shipped (JS/TS). 3. A sustainable backer. 4. Smaller install. 5. Still tied: show both and let the user pick.
