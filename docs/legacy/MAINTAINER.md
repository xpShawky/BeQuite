# Maintainer

> Operations runbook for BeQuite maintainers. PyPI publishing + signing keys + release engineering.

## Repo layout

```
bequite/                          ← repo root
├── skill/                        ← source of truth (skills + doctrines + agents + hooks + templates)
├── cli/                          ← Python CLI (hatchling)
├── template/                     ← rendered for `bequite init`
├── examples/                     ← three worked examples
├── tests/integration/            ← 125+ tests across 8 modules
├── docs/                         ← this directory
└── .bequite/memory/              ← BeQuite-eats-its-own-food memory bank
```

## Release process (post-v1.0.0 / pending Ahmed sign-off)

> v1.0.0 is the **final release** target. Ahmed reviews everything before tagging.

### Pre-release checklist

- [ ] All 125+ integration tests green on CI matrix (Python 3.11 / 3.12 / 3.13 / 3.14).
- [ ] `bequite audit --repo .` returns clean.
- [ ] `bequite freshness` returns clean (all stack candidates ≤ 6 months old).
- [ ] CHANGELOG entry for the release tag.
- [ ] Constitution version unchanged (or bumped via ADR if amended).
- [ ] `state/recovery.md` reflects current state.
- [ ] No `BEQUITE_OFFLINE=true` env required for the test suite.

### Tagging + publishing

```bash
# 1. Bump version in cli/pyproject.toml + cli/bequite/__init__.py.
# 2. Update CHANGELOG.
# 3. Commit + tag.
git commit -am "release: v<X.Y.Z>"
git tag -a v<X.Y.Z> -m "v<X.Y.Z>: <short summary>"

# 4. Push (Ahmed-supervised; one-way door per Iron Law IV).
git push origin main && git push origin --tags

# 5. Publish PyPI (Ahmed-supervised; one-way door — PyPI account ownership pending).
cd cli/
python -m build
twine upload dist/*

# 6. Publish thin npm shell (Ahmed-supervised; pending npm account ownership).
cd ../npm/   # placeholder; npm shell ships v1.0.0
npm publish

# 7. GitHub Release.
gh release create v<X.Y.Z> --title "v<X.Y.Z>" --notes-file .bequite/memory/release-notes/v<X.Y.Z>.md
```

### One-way doors (always Ahmed-approved)

- `git push` to remote (any branch).
- `git push --force` (any).
- PyPI publish.
- npm publish.
- `terraform apply` against shared infra.
- DB migrations against shared DBs.
- Generating publishable press / blog content.

## PyPI account ownership

PyPI requires a single account that owns the package. This is one-way-door (transferring ownership is supported but cumbersome). Ahmed's call:

- Account name proposal: `xpshawky` or `bequite-cli` (TBD).
- 2FA: TOTP + WebAuthn recommended.
- Trusted publisher: GitHub Actions OIDC (so CI publishes without long-lived credentials).

## npm thin shell

For users who reach for `npm install @xpshawky/bequite`:

```js
#!/usr/bin/env node
// thin shell — execve into uvx bequite
require('child_process').spawn('uvx', ['bequite', ...process.argv.slice(2)], {
  stdio: 'inherit'
}).on('exit', code => process.exit(code));
```

Publish under `@xpshawky/bequite` (org-scoped; reserves Ahmed's brand).

## ed25519 signing keys

Per-project keypair generated on `bequite init` (v0.7.1+). Maintainer obligation: BeQuite repo's own keypair lives at `.bequite/.keys/private.pem` (gitignored) + `.bequite/keys/public.pem` (committed). Receipt-chain integrity for the BeQuite repo's own work depends on this key surviving across maintainer machines.

If the maintainer's machine is lost:

```bash
# 1. From a backup, restore .bequite/.keys/private.pem.
# 2. OR: regenerate (invalidates previous signatures; document in ADR).
bequite keygen --overwrite
```

## License audit

Run before every release:

```bash
osv-scanner --recursive .                   # vuln scan
license-checker --json | jq '.[] | .licenses' | sort -u   # license diversity
```

License flags to investigate:

- AGPL — review for copyleft impact on commercial users.
- BSL/FSL (Sentry post-2023) — review redistribution.
- Custom-EULA — never auto-vendor.

## Open contributor checklist

When external contributors PR:

- [ ] Sign Contributor License Agreement (CLA) — TBD; pending Ahmed.
- [ ] All tests pass on CI.
- [ ] `bequite audit` clean on diffed files.
- [ ] No new Iron Law (those need ADR + Ahmed's review).
- [ ] CHANGELOG entry under [Unreleased].
- [ ] ADR for any architectural decision.

## Cross-references

- CHANGELOG: `CHANGELOG.md`
- License audit pattern: `docs/SECURITY.md`
- Release engineering CI: `.github/workflows/release.yml` (lands v0.15.0)
- BeQuite-itself memory bank: `.bequite/memory/`
