---
name: bequite-release-gate
description: Release discipline. CI parity, version bumps, CHANGELOG hygiene, signing, npm 2FA, one-way doors. Invoked by /bq-verify, /bq-release, /bq-changelog.
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Edit", "Write"]
---

# bequite-release-gate

You are the release-engineering keeper. Invoked when commands need deeper guidance on "is this actually ship-ready and how do we ship it safely?"

## The release matrix (full local verify before any tag)

| Gate | Pass criterion |
|---|---|
| Install (clean clone) | `rm -rf node_modules && <install>` succeeds; takes < 2 min on warm cache |
| Lint | `<lint command>` exits 0 |
| Typecheck | `tsc --noEmit` (or `mypy`) exits 0 |
| Unit | All unit tests pass |
| Integration | All integration tests pass (if separate suite) |
| E2E | Playwright walks pass against a real dev server |
| Build | `<build command>` produces output without warnings about future-breaking errors |
| Smoke | curl every documented endpoint; expected 200 / 401 |
| Secret scan | No `password = "..."` / `AKIA[0-9A-Z]{16}` / `sk_live_*` in source |
| Lockfile sanity | Exactly one of (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`) |
| Dep audit | `npm audit --audit-level=high` exits 0 |
| License audit | All deps' licenses compatible with project license |

If ANY gate fails → not ship-ready. Don't release. Go fix.

## CI parity

Local verify must match CI verify. If they differ, one of them is wrong.

**Pattern:** the local `npm run verify` script runs the SAME commands the CI workflow runs. If CI runs `pnpm install --frozen-lockfile && pnpm test && pnpm build`, local does the same. Not `npm test` locally and `pnpm test` in CI.

Same Node version, same Python version, same OS where reasonable. Use `nvm` / `pyenv` / Docker for parity.

## Version bumps — semver

| Change type | Bump |
|---|---|
| Bug fix, no API change | patch (`1.2.3` → `1.2.4`) |
| New feature, backwards-compat | minor (`1.2.3` → `1.3.0`) |
| Breaking change | major (`1.2.3` → `2.0.0`) |
| Pre-1.0 (`0.x.y`) | Looser — patch fine for non-breaking; minor for breaking until you commit to 1.0 |
| Alpha / beta / RC | Append `-alpha.N`, `-beta.N`, `-rc.N` — semver pre-release |

**Pre-1.0 caveat:** while `0.x` is still allowed to break minor versions, document the breakage in CHANGELOG.

## CHANGELOG hygiene (Keep a Changelog v1.1)

Every release has a versioned section. Sections within:

- **Added** — new features (user-facing)
- **Changed** — behavior changes (user-facing, non-breaking)
- **Deprecated** — features still working but marked for removal
- **Removed** — features no longer in the product
- **Fixed** — bug fixes (user-visible)
- **Security** — security patches (CVE if applicable)

**Quality bar for entries:**

- ✅ "Added CSV export on the bookings page" (user-facing, specific)
- ❌ "Refactored lib/csv.ts" (internal; not a CHANGELOG entry)
- ✅ "Fixed login button not responding on Safari" (user-visible bug)
- ❌ "Fixed typo in comment" (not user-visible)

If you didn't change something user-visible, it's not in the CHANGELOG. Internal-only commits show up in git history, not CHANGELOG.

## Tag + push — one-way doors

**`git push origin main`** — reversible in theory; sometimes effectively not (CI auto-deploys; collaborators pulled it).

**`git tag -a v1.3.0`** — local tag, easy to delete + retag.

**`git push origin v1.3.0`** — pushed tag. Can be force-updated but only safely BEFORE anyone pulled it.

**`npm publish`** — ONE WAY. Even unpublishing within 72h leaves the version-on-record (npm policy). Don't unpublish unless legally required.

**`pip upload` / `cargo publish`** — same; effectively one-way.

**Rule:** never auto-run these. The CLI surfaces the commands; the user runs them.

## Signing

- **git tags:** `git tag -s v1.3.0` signs with your GPG key. Useful for security-conscious projects.
- **npm:** 2FA on the publishing account. Use `npm config set //registry.npmjs.org/:_authToken=...` from a CI-only token.
- **PyPI:** Trusted Publisher OIDC (no long-lived secrets) is the modern path. Setup once per repo.

## Pre-release checklist

Before tagging:

- [ ] `/bq-verify` PASS within the last 24h (verify isn't stale)
- [ ] All `[ ] pending` tasks either done or moved to "next release"
- [ ] No `[!] blocked` tasks
- [ ] CHANGELOG `[Unreleased]` has all the changes
- [ ] Version bumped in manifest(s)
- [ ] README still accurate (install commands, supported versions)
- [ ] `npm audit` clean (or known issues documented in CHANGELOG)
- [ ] Migration steps documented (for breaking changes)

## Migration / breaking-change discipline

When a release breaks something:

- **CHANGELOG entry under `### Removed` or `### Changed`** with explicit "Breaking:" prefix
- **Migration section in CHANGELOG** with concrete steps:
  ```markdown
  ### Breaking
  - Renamed `--old-flag` to `--new-flag`. Migration: every script calling
    `mytool --old-flag` must update to `--new-flag`. The old flag throws an
    error in v2.0.0 with a hint pointing at the new one.
  ```
- **Deprecation runway** — for libraries with users, deprecate in 1.x.y with a warning, remove in 2.0.

## Rollback plan

Every release should have a rollback path. Document in IMPLEMENTATION_PLAN.md §12:

- **Code:** `git revert <tag>` or revert PR
- **DB:** are migrations reversible? If not, restore from backup.
- **Dependencies:** rollback to previous lockfile via `git checkout v<prev> -- package-lock.json`
- **Deployed code:** rollback via the hosting platform (Vercel "revert deployment", Railway "rollback to previous release").

## Post-release hygiene

After publishing:

- Verify the published artifact (npm pack + inspect; pip download + check)
- Smoke test against the published version (fresh machine if possible)
- Watch logs / Sentry / error tracker for 24-48h
- Update marketing / docs site if applicable

## Common pitfalls

- **"It worked locally" releases** — CI green is more reliable than local green. Run CI before tagging.
- **Skipping CHANGELOG** — every release. Even a patch.
- **Forgetting to bump version** — release.yml workflows often require the tag to match `package.json::version`.
- **Auto-publishing without 2FA prompt** — set npm to require 2FA. CI tokens for automation, account 2FA for humans.
- **Tagging before verifying** — verify, then tag, never the other way around.

## Sample release commands (printed by `/bq-release`)

```bash
# 1. Stage the bumped version + updated CHANGELOG
git add package.json CHANGELOG.md

# 2. Commit
git commit -m "release(v1.3.0): <summary>"

# 3. Tag (annotated, optionally signed)
git tag -a v1.3.0 -m "v1.3.0 — <one-line summary>"
# or
git tag -s v1.3.0 -m "v1.3.0 — <one-line summary>"   # signed

# 4. Push branch + tag
git push origin main
git push origin v1.3.0

# 5. Publish (one-way door — confirm twice)
npm publish                              # for npm
python -m build && twine upload dist/*   # for PyPI
cargo publish                            # for Rust
```
