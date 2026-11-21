# CI hardening (GitHub Actions examples, verified 2026-11-21)

Sources: GitHub "Secure use reference" and "Managing environments"; CISA alert on CVE-2025-30066. Other CI systems have equivalents for each row.

| Check | Fail example | Pass example |
|---|---|---|
| Third-party actions pinned | `uses: some/action@v2` | `uses: some/action@<40-char sha> # v2.3.1` (resolve with `git ls-remote https://github.com/some/action refs/tags/v2.3.1`). Where the repo adopts GitHub's workflow lockfile, that supersedes manual pins. |
| Token scope | no `permissions:` block (inherits the repo default) | `permissions: {}` at top, `permissions: { contents: read }` per job, write only where needed |
| Untrusted triggers | `pull_request_target` + `actions/checkout` with `ref: ${{ github.event.pull_request.head.sha }}` | `pull_request` for PR builds; `pull_request_target` only for labelling with no checkout of PR code |
| Script injection | `run: echo "${{ github.event.issue.title }}"` | `env: { TITLE: "${{ github.event.issue.title }}" }` then `run: echo "$TITLE"` |
| Cloud credentials | long-lived keys in repo secrets | OIDC (`permissions: { id-token: write }`) exchanged for short-lived cloud credentials |
| Production secrets | repo-level secrets usable by every workflow | environment secrets on `production`, released after required reviewers and branch rules |
| Self-hosted runners | public repo on a self-hosted runner | GitHub-hosted runners for untrusted code, or ephemeral self-hosted runners |
| Dependency updates | auto-merge of every bot PR | bot PRs (including action SHA bumps) reviewed; CI must pass |
| Logs | `set -x` around secret use; `env` dumps | masked secrets, no `env` dumps; secrets passed through `env:` only to the step that needs them |

## Environment protection (production)

- Required reviewers: 1 to 6 people or teams; enable "prevent self-review" so the person who triggers cannot approve.
- Deployment branches: only `main` (and release tags) may deploy.
- Wait timer: optional cooling-off period in minutes.
- Clear "allow administrators to bypass" when the owner wants the gate to hold for admins too.
- Private repositories need a paid plan for environments; on a free plan, use a manual `workflow_dispatch` the owner triggers.

## Required CI gates for an app (adapt to the stack)

1. Install from the lockfile, frozen.
2. Lint and type-check.
3. Unit and integration tests.
4. Build.
5. Security: dependency audit, secret scan.
6. Optional: end-to-end, accessibility, bundle size, Lighthouse on key pages.

Block merge when a required gate fails or the lockfile changed without review.

## Caching

Cache keys include the lockfile hash and the OS. Never cache a directory that holds credentials (`~/.npmrc` with a token, `~/.docker/config.json`).
