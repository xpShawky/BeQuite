---
name: bequite.freshness
description: Knowledge probe. BeQuite-unique. Verifies stack candidates aren't deprecated, EOL'd, replaced, or open-CVE'd. Runs before any stack ADR signs (cross-referenced by /bequite.decide-stack pre-sign mandatory checks). Defends against the brief-rotting problem. Implementation lands in v0.4.3 as cli/bequite/freshness.py.
phase: P1 (mandatory) | quarterly CI (recommended)
persona: research-analyst (read-only verification)
implementation: cli/bequite/freshness.py (v0.4.3)
---

# /bequite.freshness [package?] [--all]

When invoked (or `bequite freshness [--package <name>] [--all] [--since-last-sweep]`):

## Step 1 — Resolve scope

- `--package <name>`: probe one package (with version constraint).
- `--all`: probe every package referenced in `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`.
- `--from-adr <ADR-id>`: probe every candidate listed in an ADR's "Alternatives considered" table (used by `/bequite.decide-stack` pre-sign).
- `--since-last-sweep`: re-probe everything older than 24h (default cache TTL).

## Step 2 — Per-candidate checks

For each package, verify:

1. **Last commit < 6 months ago** (configurable per `state/project.yaml::freshness.github_last_commit_max_age_months`).
   - npm: `npm view <pkg> time.modified`.
   - PyPI: `pip index versions <pkg>` + `pypi.org/pypi/<pkg>/json::time`.
   - crates.io: `crates.io/api/v1/crates/<pkg>::updated_at`.
   - GitHub: `gh api repos/<owner>/<repo>::pushed_at`.
2. **Has a fresh release** — latest version published < the configured age.
3. **No unfixed criticals** — `osv-scanner --packages-only ...` for the locked version. Cross-reference GitHub Security Advisories.
4. **Recorded supply-chain incident**? — match against the known-bad list (PhantomRaven 126 / Shai-Hulud ~700 / Sept 8 attack 18 / future incidents loaded from `skill/references/supply-chain-incidents.md`).
5. **Vendor pricing tier still exists** — `WebFetch` the vendor's pricing page; LLM-extract the tier the project assumes; flag mismatch (this is the "Clerk free tier was 10k MAU, now 50k" check).
6. **License unchanged** — re-fetch license; compare against the recorded license in `state/decision_index.json`.
7. **Maintainer status** — sole maintainer with no recent activity is a yellow flag (e.g. Impeccable bundled snapshot — single maintainer; we vendor pinned to mitigate).

## Step 3 — Cache

24-hour TTL keyed on `<pkg>@<version>`. Cache at `.bequite/cache/freshness/<pkg>@<version>.json`.

`--since-last-sweep` re-probes everything older than the TTL.

`BEQUITE_OFFLINE=1` disables network probes; uses cache only; surfaces a warning per cached entry that's >24h old.

## Step 4 — Verdict per candidate

- `fresh` — last commit + release + no criticals + pricing match + license match.
- `stale-warn` — last commit / release > 6 months but no incidents.
- `stale-block` — deprecated, EOL'd, replaced, has unfixed criticals, or in a recorded incident.
- `pricing-mismatch` — assumed pricing tier no longer exists; user must update assumption.

## Step 5 — Output

`freshness.md` per stack ADR (or per project on `--all`):

```
| Package | Version | Last commit | Latest release | OSV | Pricing | License | Verdict |
|---------|---------|-------------|----------------|-----|---------|---------|---------|
| n8n     | 1.x     | 5d ago      | 1.45.0         | clean | match | fair-code | fresh |
| tauri-plugin-stronghold | 2.x | 11mo ago | EOL | n/a | n/a | MIT | stale-block (deprecated; v3 removes) |
| ...     | ...     | ...         | ...            | ...   | ...   | ...       | ...   |
```

## Step 6 — Wire into `/bequite.decide-stack`

Any `stale-block` candidate **blocks the ADR sign**. The architect either:

- Picks a fresh alternative (re-probe).
- Documents an explicit reason in the ADR's `Why we accept this risk` section + an expiry date by which the candidate must be replaced.

## Step 7 — Save

- Write `freshness.md` to project root (or to `evidence/<phase>/freshness-<YYYY-MM-DD>.md`).
- Update `state/evidence_index.json`.
- For each candidate: cache entry at `.bequite/cache/freshness/<pkg>@<version>.json`.

## Stop condition

- Every candidate probed.
- Verdicts recorded.
- For ADR-pre-sign mode (`--from-adr`): exit 0 if no `stale-block`; exit 1 otherwise.
- For quarterly CI: post findings; alert on regression (a previously-fresh candidate now stale).

## Why this exists

The brief reconciliations applied to BeQuite (Stronghold deprecation, EV cert obsolescence, Roo Code shutdown, Clerk MAU change, Vercel timeout extension, Supavisor on Supabase) prove that stack advice rots. `bequite freshness` defends against shipping rotted advice.

## Anti-patterns

- Skipping freshness because "the package was fresh last week" — TTL is 24h.
- Accepting stale-block without documenting an expiry date.
- Caching network failures (treat them as stale).

## Related

- `/bequite.decide-stack` — calls this in pre-sign mandatory checks.
- `pretooluse-verify-package.sh` — different concern (existence vs freshness).
- `/bequite.audit` — Constitution drift detector (different concern: rule violations vs dependency rot).
