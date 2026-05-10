---
name: library-package
version: 1.0.0
applies_to: [library, package, sdk]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: library-package v1.0.0

> Doctrine for libraries / SDKs / packages published for other developers to consume. Public API discipline, semver, no telemetry without opt-in, license clarity, supply-chain hygiene. Loaded by `.bequite/bequite.config.toml::doctrines = ["library-package"]`.

## 1. Scope

Code published to a registry — npm, PyPI, crates.io, RubyGems, NuGet, Maven Central, Hex, Go modules. The audience is *other developers* who depend on this artifact. Includes runtime libraries, build-tool plugins, type-only packages, and SDKs.

**Does NOT cover:** end-user applications (use `default-web-saas` / `cli-tool` / `desktop-tauri`).

## 2. Rules

### Rule 1 — Semver-strict on public API
**Kind:** `block`
**Statement:** Removing or renaming a public export, changing a public function signature, changing default behaviour — all are major bumps. Adding a non-breaking export is a minor bump. Bug fix is patch.
**Check:** `bequite audit` runs an API-diff tool (`api-extractor` for TS, `pyrightconfig` strict + diff, `cargo public-api`) between commits; flags violations of semver.
**Why:** consumers' lockfiles depend on this contract.

### Rule 2 — Public-API freeze + private internals
**Kind:** `block`
**Statement:** The public API is in `index.ts` / `__init__.py` / `lib.rs` / explicit exports. Anything not exported is private and may change without notice. Internals MUST live in folders/modules the public API does not re-export (e.g. `src/internal/`).
**Check:** `bequite audit` parses imports; flags consumers reaching into `src/internal/`.
**Why:** prevents accidental API surface growth.

### Rule 3 — Type definitions ship with the package
**Kind:** `block`
**Statement:** TypeScript / Python / Rust / Go packages ship type definitions inline (TS), type stubs (`*.pyi` for Python when needed), or strong typing built-in (Rust / Go). No untyped APIs in 2026.
**Check:** `bequite audit` checks `package.json::types` / `pyproject.toml::tool.mypy` / etc.
**Why:** type-safe consumption is the table stakes of 2026.

### Rule 4 — Changelog discipline (Keep a Changelog)
**Kind:** `block`
**Statement:** `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/) format. Every release has an entry. Sections: Added / Changed / Deprecated / Removed / Fixed / Security.
**Check:** `bequite audit` parses CHANGELOG.md; flags missing entry per release tag.
**Why:** consumers reading "what changed?" need a structured answer.

### Rule 5 — Conventional Commits → automated changelog
**Kind:** `recommend`
**Statement:** Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, `feat!:`, `BREAKING CHANGE:`). Tools (`changesets`, `release-please`, `semantic-release`) auto-generate the CHANGELOG.
**Check:** advisory; commit-lint hook can enforce.
**Why:** reduces manual changelog rot.

### Rule 6 — Deprecation runway
**Kind:** `block`
**Statement:** Deprecated APIs print a deprecation warning at runtime AND are documented in CHANGELOG.md AND continue to work for at least one minor release (or a documented N-month window) before removal.
**Check:** `bequite audit` greps for `@deprecated` annotations; flags hard-removed APIs without a prior `Deprecated` changelog entry.
**Why:** consumers need time to migrate.

### Rule 7 — No telemetry without explicit opt-in
**Kind:** `block`
**Statement:** Libraries do not phone home. If a library wants telemetry, it asks the consumer to opt in via configuration, never via "first-run prompt" (libraries don't have first-run prompts; they're loaded by other code).
**Check:** `bequite audit` greps the library code for HTTP requests to non-API-defined endpoints; flags violations.
**Why:** the next.js / faker.js / event-stream incidents — telemetry-without-consent is a long-term trust killer.

### Rule 8 — License clarity
**Kind:** `block`
**Statement:** Top-level `LICENSE` file is present, machine-detectable (matches an OSI-recognised license: MIT / Apache-2.0 / BSD-3-Clause / MPL-2.0 / GPL-3.0 / AGPL-3.0). Mixed-license code is documented in `LICENSES/` directory with `LICENSING.md` explaining the breakdown.
**Check:** `bequite audit` runs `license-checker` / `cargo-license`; flags missing or non-OSI license.
**Why:** consumers must know whether they can use the library.

### Rule 9 — No GPL contamination in MIT/Apache packages
**Kind:** `block`
**Statement:** MIT / Apache / BSD libraries MUST NOT depend on GPL / AGPL packages at runtime (the dependency graph would force the consumer to GPL too). Use `license-checker --failOn` or `osv-scanner` license filter.
**Check:** `bequite audit` runs license filter; fails on copyleft dependency in permissive package.
**Why:** legal contamination.

### Rule 10 — Supply-chain hygiene
**Kind:** `block`
**Statement:** Every published version's lockfile is committed AND verified pre-publish. The publish workflow:
1. Fresh checkout (no local artifacts).
2. Restore dependencies via lockfile.
3. Run `osv-scanner` / `npm audit` / `pip-audit` / `cargo audit`; fail on unfixed criticals.
4. Build deterministically (use `pnpm`'s `--frozen-lockfile`, `npm ci`, `pip install --require-hashes`, etc.).
5. Run tests on the built artifact, not the source.
6. Sign the package with the publisher's signing key (npm provenance, PyPI sigstore, crates.io).
**Check:** `release.yml` workflow content audited.
**Why:** the PhantomRaven / Shai-Hulud / event-stream / left-pad lessons.

### Rule 11 — Reproducible builds where feasible
**Kind:** `recommend`
**Statement:** Where the toolchain supports it (Rust, Go, Java, Reproducible Builds-aware Python), publish reproducible artifacts. Document the exact toolchain version + commands in `BUILDING.md`.
**Check:** advisory.
**Why:** verifiable supply chain.

### Rule 12 — Public examples + integration tests
**Kind:** `block`
**Statement:** Every release ships at least one runnable example consuming the library (in `examples/`) AND an integration test that imports the *published* artifact (not the source). The integration test runs in CI on a separate workflow.
**Check:** `bequite verify` runs the example end-to-end.
**Why:** "it builds" is not "it works for consumers."

### Rule 13 — Documented `node` / `python` / `rustc` minimum version
**Kind:** `block`
**Statement:** `package.json::engines.node`, `pyproject.toml::requires-python`, `Cargo.toml::rust-version` are explicitly set. Bumping the minimum is a major version bump.
**Check:** `bequite audit` checks for the field; CI matrix tests the declared minimum.
**Why:** breakage on older toolchains.

### Rule 14 — Public security policy
**Kind:** `block`
**Statement:** `SECURITY.md` exists with: how to report a vulnerability, expected response time, GPG key for encrypted disclosure (when applicable), supported versions matrix.
**Check:** `bequite audit` checks for SECURITY.md; validates required sections.
**Why:** OSS triage; CVE coordination.

## 3. Stack guidance

### Build + publish
| Ecosystem | Build tool | Publish path |
|---|---|---|
| TypeScript | `tsup` / `unbuild` / `vite-lib-mode` | `npm publish` (with provenance) |
| Python | `hatchling` (default) / `setuptools` / `poetry` | `twine upload` (with sigstore) |
| Rust | `cargo build --release` | `cargo publish` |
| Go | (none — git-tag-driven) | `go list -m` (post-tag) |

### Versioning automation
| Tool | When |
|---|---|
| changesets | Multi-package npm monorepos |
| release-please | Single-package Conventional Commits |
| semantic-release | Older but stable npm pattern |

### Documentation
| Tool | When |
|---|---|
| TypeDoc | TS API reference |
| pdoc / Sphinx | Python API reference |
| rustdoc | Rust API reference (built-in) |
| Docusaurus / VitePress / Astro Starlight | User-facing site |

## 4. Verification

`bequite verify` for library projects:

1. **API diff** — compare public API to last release; semver-coherent.
2. **Lockfile freshness** — `npm audit` / `pip-audit` / `cargo audit` exit 0.
3. **License audit** — `license-checker` exit 0 against project's allow-list.
4. **Build determinism check** — twice-build, hash-compare (when toolchain supports).
5. **Integration test** — installs the *built* package in a sandbox, runs an example.
6. **CHANGELOG present + valid** — has an entry for the version being released.
7. **SECURITY.md present** — and contains required sections.
8. **Engines / requires-python / rust-version present**.

## 5. Examples and references

- Keep a Changelog: https://keepachangelog.com/
- Conventional Commits: https://www.conventionalcommits.org/
- semver: https://semver.org/
- changesets: https://github.com/changesets/changesets
- release-please: https://github.com/googleapis/release-please
- semantic-release: https://semantic-release.gitbook.io/
- npm provenance: https://docs.npmjs.com/generating-provenance-statements
- PyPI sigstore: https://pypi.org/help/#trusted-publishers
- OSV scanner: https://osv.dev/

Reference libraries that exemplify this Doctrine: `@octokit/rest`, `prettier`, `httpx` (Python), `serde` (Rust).

## 6. Forking guidance

Common forks:
- **`library-package-internal`** — drop public-API discipline (it's internal); keep telemetry + license rules.
- **`library-package-monorepo`** — for multi-package repos using changesets.
- **`library-package-typegen`** — for type-only packages (e.g. `@types/*`).

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: library-package@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–14 ratified.
```
