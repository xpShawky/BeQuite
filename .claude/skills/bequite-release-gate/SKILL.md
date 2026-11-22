---
name: bequite-release-gate
description: Use before tagging, publishing a package, cutting a version, writing release notes or deploying a release, and whenever someone asks whether the work is ready to ship. Runs the same checks CI runs, picks the SemVer bump, checks the changelog, provenance and rollback, and stops at the one-way doors (push, tag, publish) for the owner.
last_verified: 2026-11-21
sources:
  - https://semver.org/ (read 2026-11-21) SemVer 2.0.0 rules
  - https://keepachangelog.com/en/1.1.0/ (read 2026-11-21) change types, Unreleased, yanked
  - https://slsa.dev/spec/v1.2/build-track-basics (read 2026-11-21) SLSA build levels
  - https://docs.npmjs.com/trusted-publishers (read 2026-11-21) OIDC publishing and provenance
  - https://docs.npmjs.com/policies/unpublish (read 2026-11-21) 72 h window, versions never reused
  - https://docs.pypi.org/trusted-publishers/ (read 2026-11-21) short-lived publish tokens
  - https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations (read 2026-11-21) attest and verify
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# bequite-release-gate

A release is the moment a mistake stops being private. Pushed tags get pulled, published versions can never be reused, and a deploy reaches every user. This skill makes "ready" a list of commands with exit codes, and hands the irreversible steps to the owner.

## When to use

- `/bq-release`, `/bq-changelog`, and `/bq-verify` when the next step is a release.
- Any "is this ready to ship?" question.

Not for: deploy mechanics and production config (`bequite-devops-cloud`), the security sweep itself (`bequite-security-reviewer`; this skill reads its findings).

## Procedure

1. **Run what CI runs, locally, the same way.** Read the release workflow and copy its commands and flags exactly (a local `--strict` must match a CI `--strict`). Use the CI's runtime versions.
2. **The matrix** (`references/release-matrix.md`): clean install from the lockfile, lint, type-check, tests, build, smoke test of the built artifact, secret scan, dependency audit at the project's stated threshold, licence check, security findings with no open Critical or High. Paste each command, exit code and the summary line. One red row = not ready.
3. **Pick the bump** (SemVer 2.0.0): breaking = major, new backward-compatible feature = minor, fix = patch. Under `0.y.z` anything may change, but breaking changes still get a minor bump and a "Breaking" line. Pre-releases use `-alpha.N`, `-beta.N`, `-rc.N`.
4. **Changelog** (Keep a Changelog 1.1.0): move `Unreleased` into `## [x.y.z] - YYYY-MM-DD`; entries under Added, Changed, Deprecated, Removed, Fixed, Security; user-visible changes only; breaking changes carry a migration step. Version strings in manifests, README and docs match.
5. **Provenance.** Where the registry supports it, publish from CI with trusted publishing (OIDC) instead of a stored token, and attach provenance or attestations (SLSA build L2 means signed provenance from a hosted builder). Record which level the release reaches.
6. **Rollback written.** Code: the previous tag and how to redeploy it. Database: forward-only, so the roll-forward fix path. Packages: deprecate and publish a fixed version (a version number cannot be reused).
7. **Stop at the one-way doors.** Print the exact commands for the owner: commit, tag, push, publish, deploy. The agent never runs `git push`, `git push --tags`, `npm publish`, `twine upload`, `cargo publish` or a production deploy.
8. **After the owner ships**: verify the published artifact (download it, check the version and the attestation), smoke test it, watch errors for the agreed window, and log the result.

## Worked example (real dry run on this repo, 2026-11-21)

Question: "Could BeQuite tag a release from the development branch today?"

```
$ grep -n "bq_check" .github/workflows/release.yml   -> "run: python3 scripts/bq_check.py --strict"
$ python scripts/bq_check.py            -> exit 0, "8/10 checks passed, 2 warning(s)"
$ python scripts/bq_check.py --strict   -> exit 1, "FAIL size_budgets (55)", "FAIL skill_sources (60)"
$ sed -n 7p CHANGELOG.md                -> "## [Unreleased]"   (A1 entries under Changed and Removed)
$ grep -n "Latest" README.md            -> "**Latest:** `v4.0.0` ..."
$ git status --short | wc -l            -> 0
```

Verdict: **not ready.** Local non-strict green would have looked like a pass, but the release job runs strict, and strict fails on the two warn checks that tracks B, C and D are still clearing. Running step 1 the CI's way caught it. Bump when ready: major (`1.0.0` is a deliberate reset agreed in the plan, a breaking change for installers). Next action: none for the owner yet; re-run this block when the warn counts reach 0.

## Quality gate

- Every matrix row has a command, an exit code and a summary line from this session.
- Local commands and flags match the CI release workflow.
- The bump is justified in one line against SemVer; the changelog section exists with today's date.
- The rollback path is written for code, data and packages.
- No push, tag, publish or deploy was run by the agent; the owner got the exact commands.

## Boundaries

- Release push, tag and publish are hard human gates in every mode.
- Never unpublish or delete a pushed tag to "fix" a release; publish a new version and mark the bad one deprecated or yanked.
- Signing keys and publish tokens are never read, printed or stored by the agent.

## References (load on demand)

- `references/release-matrix.md`: the matrix with example commands per stack, changelog quality bar, breaking-change template, command block printed for the owner.
