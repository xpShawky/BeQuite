---
name: bequite.release
description: Phase 7 — handoff + release prep. Loads devops-engineer + tech-writer. Produces HANDOFF.md (hand-runnable by a second engineer), release notes, rollback plan, version bump, screencast checklist. Refuses to publish (PyPI / npm / git push to main) without explicit owner approval per session.
phase: P7
persona: devops-engineer + tech-writer
prompt_pack: master_prompt.md (cross-references)
---

# /bequite.release [version-bump?]

When invoked (or `bequite release [patch|minor|major]`):

## Step 1 — Read context

- `CHANGELOG.md` — what's in this release.
- All accepted ADRs since the last release.
- All receipts since the last release tag.
- `state/project.yaml::scale_tier, mode, audience, compliance`.
- All loaded Doctrines.

## Step 2 — Pre-release checklist (master §27 release definition-of-done)

A release is done only when:

- [ ] Build passes (`pnpm build` / `pip install -e .` / `cargo build --release`).
- [ ] E2E passes (Playwright walks across all roles × viewports × locales).
- [ ] Security checklist passes (semgrep + osv-scanner + secret-scan + supply-chain review).
- [ ] Backup + rollback documented.
- [ ] Version updated per semver.
- [ ] Changelog updated.
- [ ] Release notes written.
- [ ] HANDOFF.md hand-runnable by a second engineer (test by handing it to someone who didn't write the project).

## Step 3 — devops-engineer: produce HANDOFF.md

Sections (per `skill/templates/handoff.md.tpl`):

- **Run locally** — `git clone && <one command> && open localhost:<port>`.
- **Deploy to production** — concrete commands; references infra config.
- **Run the test suite** — full validation mesh.
- **Roll back** — concrete commands per failure mode.
- **Where secrets live** — references env / Doppler / Vault / KMS.
- **Who to contact** — actual maintainer's contact (NOT hallucinated).
- **Known issues** — open `risks.md` entries; deferred POA&M items.

For `audience: vibe-handoff` projects (v2.0.0+ Studio): a separate `HANDOFF-FOR-NON-ENGINEERS.md` with screenshots + plain-English explanations.

## Step 4 — tech-writer: produce release notes

`docs/release-notes/<version>.md`:

- What's in (features delivered).
- What's out (deferred items + reason).
- Breaking changes (with migration steps).
- Known issues.
- Acknowledgments (contributors, peer skills, references).

## Step 5 — Version bump (semver discipline)

Per `library-package` Doctrine Rule 1:

- Patch: bug fixes, small UI improvements, doc fixes.
- Minor: new commands / modules / screens / providers / evidence types.
- Major: data model breaking, public API breaking, workflow change, security model change.

Bump `package.json::version` / `pyproject.toml::version` / `Cargo.toml::version` accordingly. Commit `chore(release): vX.Y.Z`.

## Step 6 — Tag

`git tag -a vX.Y.Z -m "vX.Y.Z - <release title>"`.

## Step 7 — Pause for owner — one-way doors

Auto-mode pauses for owner approval before:

- `git push` to remote (especially `main`).
- `pnpm publish` / `pip upload` / `npm publish` / `cargo publish`.
- Submitting to AGENTS.md ecosystem registry / Anthropic plugin marketplace / Cursor marketplace.
- Any blog-post / press content for publication.

Owner approves explicitly per session; receipt records the approval.

## Step 8 — Update state

- `state/recovery.md` — "Release vX.Y.Z complete; ready for next sub-version."
- `.bequite/memory/progress.md::Evolution log` — entry for the release.
- `.bequite/memory/prompts/v<N>/` — phase snapshot.

## Stop condition

- Pre-release checklist all checked.
- HANDOFF.md verified hand-runnable.
- Release notes written.
- Version bumped + committed + tagged.
- Owner-approved publish (if applicable).
- Receipt emitted.

## Anti-patterns

- Releasing without rollback plan.
- Releasing without verifying HANDOFF.md is hand-runnable.
- Auto-pushing to main / publishing without owner approval per session.
- Using `latest` tag in production Docker images.
- Weasel words in release notes ("This should improve performance" — measure or omit).

## Related

- `/bequite.validate` — Phase 6 (must pass before release).
- `/bequite.handoff` — alias when only the HANDOFF doc is needed without a version bump.
