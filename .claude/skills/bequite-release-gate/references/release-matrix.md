# Release matrix and owner command block (verified 2026-11-21)

## Matrix (copy the CI's exact commands; these are examples)

| Row | Node example | Python example | Pass |
|---|---|---|---|
| Clean install | `rm -rf node_modules && npm ci` | `python -m venv .v && .v/bin/pip install -r requirements.txt --require-hashes` | exit 0 |
| Lint | `npm run lint` | `ruff check .` | exit 0 |
| Types | `npx tsc --noEmit` | `mypy .` | exit 0 |
| Tests | `npm test` | `pytest -q` | exit 0, count matches last release or the difference is explained |
| Build | `npm run build` | `python -m build` | artifact produced |
| Smoke | start the built app, `curl -fsS localhost:3000/health` | `pip install dist/*.whl && mytool --version` | expected output |
| Secret scan | a secret scanner over the diff since the last tag | same | no findings |
| Dependency audit | `npm audit --audit-level=high` or an OSV scanner | `pip-audit` or an OSV scanner | below the project's threshold |
| Licences | a licence checker | same | compatible with the project licence |
| Security findings | `.bequite/work/<id>/security.md` | same | no open Critical or High |

Tool names are candidates; use what the project already runs in CI.

## Changelog quality bar

- Yes: "Added CSV export on the bookings page." "Fixed the login button doing nothing on Safari 18."
- No: "Refactored lib/csv.ts." "Fixed typo in comment." (internal; leave to git history)
- Breaking changes:

```markdown
### Changed
- **Breaking:** `--old-flag` renamed to `--new-flag`. Migration: replace `--old-flag` in scripts; the old flag now exits with a message naming the new one.
```

## SemVer quick table (2.0.0)

| Change | Bump |
|---|---|
| Fix, no API change | patch 1.2.3 → 1.2.4 |
| Backward-compatible feature | minor 1.2.3 → 1.3.0 |
| Breaking change | major 1.2.3 → 2.0.0 |
| Pre-release | 2.0.0-rc.1 (ranks below 2.0.0) |
| Build info | 2.0.0+20261121 (ignored for precedence) |

## Provenance by registry (2026-11-21)

| Registry | Route | Notes |
|---|---|---|
| npm | trusted publishing from GitHub Actions, GitLab.com or CircleCI cloud | provenance automatic for public repos and packages on GitHub and GitLab; npm CLI 11.5.1+, Node 22.14.0+; `id-token: write` |
| PyPI | trusted publishers | 15-minute token from an OIDC exchange |
| GitHub releases and images | `actions/attest` | verify with `gh attestation verify <artifact> -R <owner>/<repo>` |

## One-way doors (npm example of why)

Unpublish is allowed within 72 hours only if nothing depends on the package; later only with no dependents, under 300 weekly downloads and a single owner. A published version number can never be used again.

## Command block printed for the owner

```bash
git add <manifest files> CHANGELOG.md
git commit -m "release: v1.3.0"
git tag -a v1.3.0 -m "v1.3.0"
git push origin main
git push origin v1.3.0          # starts the release workflow
# publishing, if the project publishes and CI does not:
npm publish                     # one-way door
```
