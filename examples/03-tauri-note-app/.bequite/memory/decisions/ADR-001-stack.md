---
adr: 001
title: Stack decision for example-03-tauri-note-app (vault-notes)
status: accepted
date: 2026-05-10
deciders: BeQuite v0.9.0 author
supersedes: null
---

# ADR-001 — Stack for `vault-notes` desktop app

## Context

A local-first encrypted note app. Doctrine: `desktop-tauri`. Must:
- Run on macOS, Windows, Linux without per-platform code paths in 90%+ of code.
- Encrypt notes at rest with a key the user owns.
- Codesign + notarize for distribution.
- Pass Doctrine `desktop-tauri` rules.

## Decision

| Layer | Choice |
|---|---|
| Runtime | Tauri v2 |
| Frontend | SvelteKit + bun |
| DB | SQLite via `tauri-plugin-sql` |
| Crypto | AES-GCM-256 (via `aes-gcm` Rust crate) |
| Key store | OS keychain via `tauri-plugin-keyring` |
| Search | SQLite FTS5 |
| Markdown | mdsvex (compile-time) + remark (runtime) |
| macOS sign | `xcrun notarytool submit` |
| Windows sign | OV cert + AzureSignTool (vcsjones) |
| Linux | AppImage + Flatpak (optional) |
| Updater | Tauri auto-updater + ed25519 |
| Tests | Vitest + Playwright (tauri-driver) + Rust unit |
| CI | GitHub Actions (cross-platform matrix) |

## Rationale

**Tauri v2.** The only mature lightweight desktop runtime in 2026. ~3-10MB installer (vs Electron's 80-200MB). Rust backend + WebView frontend. v2 brought stable Plugin v2 API + better cross-platform support.

**SvelteKit.** Smallest bundle of mainstream JS frameworks. Compile-time framework — Tauri's WebView starts faster with smaller JS payloads. Pairs well with Tauri's `invoke()` boundary.

**SQLite via `tauri-plugin-sql`.** Local-only; no server; battle-tested. FTS5 built-in for note search.

**AES-GCM-256 in Rust.** Authenticated encryption; per-note nonce; AEAD. The `aes-gcm` crate is FIPS-validated when configured correctly. For `gov-fedramp` Doctrine layering, swap to `ring` (FIPS 140-3 path).

**OS keychain via `tauri-plugin-keyring`.** Master encryption key never lives on disk in plaintext; lives in the OS-managed keystore (macOS Keychain / Windows Credential Manager / Linux Secret Service). **NOT Stronghold** — deprecated and removed in Tauri v3. (Brief reconciliation #2 from BeQuite v0.1.0.)

**`xcrun notarytool submit` for macOS.** `altool` was deprecated in Xcode 13+ and removed by Apple in 2023. (Brief reconciliation #4.) Notarization is mandatory for distribution; `notarytool` is the modern path.

**OV cert + AzureSignTool for Windows.** EV certs no longer give SmartScreen reputation boost (Microsoft removed EV-specific OIDs Aug 2024). OV cert + AzureSignTool (https://github.com/vcsjones/AzureSignTool) is cheaper + sufficient. **NOT `relic`** — `AzureSignTool` is the cleaner path for AKV-stored certs. AKV certificate validity capped at 1 year since Feb 2026 — note in calendar to renew.

**Tauri auto-updater + ed25519.** Built-in; signs updates with a per-app keypair (gen on first build; verify on download).

**Bun for frontend builds.** Faster than npm/pnpm; matches BeQuite's preference.

## Alternatives considered

- **Electron instead of Tauri.** Rejected: bundle size 10-30x bigger; performance worse; not Doctrine-aligned.
- **Stronghold for key store.** Rejected: deprecated. (Brief reconciliation.)
- **EV cert for Windows.** Rejected: no longer worth the premium since Aug 2024.
- **`relic` for Windows codesigning.** Rejected: AzureSignTool is cleaner for AKV-stored certs.
- **Standalone Rust + egui (no WebView).** Rejected: ecosystem too small; UI work much harder.
- **PostgreSQL via SurrealDB or PocketBase embedded.** Rejected: overkill for single-user; SQLite + FTS5 is sufficient.

## Consequences

- **Positive:** ~5MB installer; sub-second cold start; full cross-platform with one codebase; user data is theirs (no cloud).
- **Negative:** Distribution complexity (codesign + notarize per platform). Mitigation: GitHub Actions matrix runs all three in parallel.
- **Risk:** AKV cert 1-year cap requires annual renewal. Mitigation: calendar reminder + automated CI check that warns 30 days before expiry.
- **Risk:** Tauri v2 → v3 migration when v3 ships. Mitigation: pin to v2.x latest; track v3 alpha/beta releases via context7.

## Doctrine compliance

`desktop-tauri` Doctrine rules:
- ✅ Tauri v2 + OS keychain (NOT Stronghold).
- ✅ Apple notarytool (NOT altool).
- ✅ AzureSignTool (NOT EV cert; NOT relic).
- ✅ Local-first (no cloud sync v1).
- ✅ Tauri auto-updater with ed25519 verification.
- ✅ User data never logged.

## Status: accepted (2026-05-10)
