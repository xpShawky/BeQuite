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

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (npm, pip, cargo, GitHub Actions, GitLab CI, GPG signing, AzureSignTool, Apple notarytool, OIDC Trusted Publisher, twine, etc.) is an EXAMPLE, not a mandatory default.**

The release matrix + CI parity + semver + CHANGELOG hygiene + signing discipline + rollback plan are **universal**. Specific tool picks (package manager, CI provider, signing solution) are candidates per project.

**Do not say:** "Use GitHub Actions."
**Say:** "GitHub Actions is one candidate for CI. Compare against GitLab CI, CircleCI, Buildkite, or self-hosted runners based on this project's repo host, budget, and matrix-build needs. Use it only if it fits."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## When NOT to use this skill (alpha.15)

- The task at hand doesn't touch this skill's domain — defer to the right specialist skill
- A faster / simpler skill covers the same need — pick the simpler one and document why
- The skill's core invariants don't apply to the current project (e.g. regulated-mode rules on a prototype)
- The command that would activate this skill is already running with another specialist that fits better

If unsure, surface the trade-off in the command's output and let the user decide.

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected (not just glanced at)
- [ ] No banned weasel words in any completion claim — `should`, `probably`, `seems to`, `appears to`, `might`, `hopefully`, `in theory`
- [ ] Any tool / library / framework added during this run has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met (or honestly reported as PARTIAL / FAIL)
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended for the run
- [ ] Memory state files (LAST_RUN, WORKFLOW_GATES, CURRENT_PHASE) updated when gate state changed

If any item fails, do not claim done — report PARTIAL with the specific gap.
