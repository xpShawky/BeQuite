---
name: desktop-tauri
version: 1.0.0
applies_to: [desktop, tauri, native]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: desktop-tauri v1.0.0

> Doctrine for native desktop applications built on Tauri v2. Code signing, notarization, license validation, OS keychain for secrets, auto-update with anti-tampering. Loaded by `.bequite/bequite.config.toml::doctrines = ["desktop-tauri"]`.

## 1. Scope

Cross-platform native applications shipping as Windows / macOS / Linux binaries via Tauri v2. Covers code signing, OS-keychain-based secret storage, license validation, auto-update, and anti-tampering. Frontend is typically SvelteKit / React / Vue / Solid running inside the Tauri webview.

**Does NOT cover:** Electron apps (consider `electron` Doctrine when needed; not shipped in v1.0.0). Web SaaS (use `default-web-saas`).

## 2. Rules

### Rule 1 — Tauri v2, never v1
**Kind:** `block`
**Statement:** New projects use Tauri v2 (mobile-capable since Oct 2024). v1 is forbidden for new projects. Migrating v1 projects requires an ADR.
**Check:** `bequite audit` parses `Cargo.toml`; flags `tauri = "1.*"`.
**Why:** v1 is in maintenance; the iOS / Android story is v2-only.

### Rule 2 — OS keychain for secrets, NOT Stronghold
**Kind:** `block`
**Statement:** Secrets (API keys, tokens, license seeds) MUST be stored in the OS keychain via `tauri-plugin-keyring` (or platform-specific equivalents: macOS Keychain, Windows Credential Locker, Linux libsecret). **Stronghold is deprecated in Tauri and being removed in v3 — do not use it for new projects.**
**Check:** `bequite audit` parses `Cargo.toml`; flags `tauri-plugin-stronghold` without an ADR justifying legacy use.
**Why:** Stronghold's removal is a known breakage in v3; OS keychain is the durable answer.

### Rule 3 — License validation in Rust, not JS
**Kind:** `block`
**Statement:** License key validation runs in Rust (the Tauri backend). The JS frontend never sees the validation logic. JS is bypassable; Rust compiled into the binary is harder.
**Check:** `bequite audit` greps the JS bundle for license-validation patterns; flags violations.
**Why:** trivial bypass via DevTools is the default failure mode.

### Rule 4 — Recommended licensing SDK: Keygen
**Kind:** `recommend`
**Statement:** For paid desktop apps, **Keygen** (https://keygen.sh/) is the default. Most mature, offline crypto, multiple SDKs, device fingerprinting + heartbeat + offline JWT. Alternatives: **LicenseSeat** (simpler API), self-hosted (with explicit ADR documenting key rotation, revocation, audit).
**Note:** **Keyforge has no SDK by design** (JWT-only); appropriate for hobbyist tools but not recommended for serious commercial apps. Drop the brief's "Keyforge SDK" framing.
**Check:** advisory; the ADR is the gate.
**Why:** rolling licensing is harder than rolling auth; use a vendor.

### Rule 5 — Code signing: macOS
**Kind:** `block`
**Statement:** macOS builds are signed with an **Apple Developer ID** certificate AND notarised via `xcrun notarytool submit ... --wait`, then stapled with `xcrun stapler staple`. **Use `notarytool`, not `altool`** — `altool` was replaced in Xcode 13+.
**Check:** CI workflow contains `notarytool` invocation; release artifact passes `spctl --assess --verbose`.
**Why:** unsigned/unnotarised binaries trigger Gatekeeper warnings users will reject.

### Rule 6 — Code signing: Windows
**Kind:** `block`
**Statement:** Windows builds are signed with an **OV (Organization Validation) certificate** via **Azure Key Vault + AzureSignTool** (`vcsjones/AzureSignTool`). **EV (Extended Validation) certificates are no longer required** for SmartScreen reputation — Microsoft removed EV-specific OIDs in Aug 2024. **AKV cert validity is capped at 1 year** since Feb 2026; rotate accordingly.
**Check:** CI workflow contains `AzureSignTool` invocation; release artifact passes `signtool verify /pa`.
**Why:** post-Aug-2024, OV is sufficient; EV is more expensive without benefit.

### Rule 7 — Code signing: Linux
**Kind:** `recommend`
**Statement:** Linux distributions don't typically require signing for individual binaries. For .deb/.rpm/.AppImage, sign with a maintainer GPG key. For Snap / Flatpak, use the platform's signing.
**Check:** advisory.
**Why:** Linux convention.

### Rule 8 — Auto-updater gated on valid license
**Kind:** `block`
**Statement:** The auto-updater MUST verify the user's license (via Rule 4's SDK) before downloading or applying an update. Expired-license users continue using the version they last had a valid license for.
**Check:** `bequite audit` parses updater code; flags update-without-license-check.
**Why:** prevents pirated copies from getting updates while paying customers wait.

### Rule 9 — Auto-updater: Sparkle (mac) + JSON manifest (Windows / Linux)
**Kind:** `recommend`
**Statement:** macOS: Sparkle 2 (signed appcast XML + EdDSA signatures). Windows / Linux: Tauri's built-in updater with JSON manifest signed via the project's update-key.
**Check:** advisory.
**Why:** the established patterns.

### Rule 10 — Anti-tampering: CSP + checksum verification
**Kind:** `block`
**Statement:** Tauri's CSP is configured strictly (no `unsafe-inline`, no `unsafe-eval`, allowed origins explicit). Every update artifact carries a SHA-256 checksum verified before application; a mismatched checksum aborts update + alerts the user.
**Check:** `bequite audit` parses `tauri.conf.json`; flags loose CSP. Updater test inserts a corrupted checksum; expects update abort.
**Why:** tampering with binaries between download and apply is a real attack vector.

### Rule 11 — Crash reporting + telemetry: opt-in
**Kind:** `block`
**Statement:** Crash reports and analytics are **opt-in** at first run. The user sees the prompt; their answer persists. Approved options: Sentry (privacy-aware config), Aptabase, self-hosted PostHog. **No opt-out telemetry.**
**Check:** `bequite audit` greps for telemetry endpoints; expects gate behind config.
**Why:** desktop apps demand higher privacy bar than web.

### Rule 12 — No reads of `~/.ssh`, `~/.aws`, `~/.config`, `~/.gnupg` without explicit user consent
**Kind:** `block`
**Statement:** The app MUST NOT read sensitive user dotfiles without an explicit user-granted permission scope. Use Tauri's allowlist + scope system to declare exact paths.
**Check:** `bequite audit` parses `tauri.conf.json` allowlist; flags wildcards on `$HOME`.
**Why:** desktop apps have full filesystem access by default; declaring scope reduces blast radius.

### Rule 13 — Bundle size discipline
**Kind:** `recommend`
**Statement:** Tauri bundles SHOULD be < 20 MB on first install (Tauri's headline advantage over Electron). Audit bundle size on every release; investigate when it grows > 30 MB.
**Check:** CI emits bundle size; alarms if growth > 5 MB month-over-month.
**Why:** the value prop.

## 3. Stack guidance

### Frontend (inside Tauri's webview)
| Choice | When |
|---|---|
| SvelteKit | Smallest bundles |
| React + Vite | Largest ecosystem |
| Solid | Performance-critical |
| Vue | Vue teams |

### Local data
| Choice | When |
|---|---|
| SQLite (via `tauri-plugin-sql`) | Default; battle-tested |
| Turso | Sync-friendly SQLite |
| LiteFS / rqlite | Multi-device sync |

### State sync (when multi-device)
| Choice | When |
|---|---|
| Supabase Realtime | When backend is Supabase |
| Liveblocks | Realtime collaborative state |
| Y.js + WebRTC | CRDT-native, peer-to-peer |
| Self-hosted | When privacy-first |

### Background work
- Tauri's `tauri::async_runtime` for async tasks.
- OS-level scheduling (launchd, Task Scheduler, systemd timers) for long-lived tasks the app shouldn't own.

## 4. Verification

`bequite verify` for desktop-tauri projects:

1. **Build smoke** — `tauri build` produces signed artifacts on each target OS.
2. **Signing verification** — macOS: `spctl --assess`; Windows: `signtool verify /pa`; Linux: GPG verify on AppImage / package.
3. **Notarization** (macOS) — `xcrun stapler validate` on the bundle.
4. **License-gated update** — planted "expired license" + "valid license" cases; assert updater behaviour.
5. **CSP strictness** — `tauri.conf.json` parsed; deny `unsafe-inline` / `unsafe-eval`.
6. **Allowlist scope** — assert no wildcard `$HOME` reads in the allowlist.
7. **Bundle size** — assert < 30 MB; warn at > 20 MB.
8. **Auto-update round-trip** (in CI sandbox) — install N-1, trigger update, assert N is running and signed.

## 5. Examples and references

- Tauri v2 docs: https://v2.tauri.app/
- Tauri Stronghold (deprecated): https://v2.tauri.app/plugin/stronghold/
- Tauri keyring plugin: https://v2.tauri.app/plugin/keyring/
- Apple notarization: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
- AzureSignTool: https://github.com/vcsjones/AzureSignTool
- Keygen: https://keygen.sh/
- LicenseSeat: https://licenseseat.com/
- Sparkle 2: https://sparkle-project.org/

## 6. Forking guidance

Common forks:
- **`desktop-electron`** — for teams that must use Electron. Drop the bundle-size discipline (Electron is ~70 MB minimum).
- **`desktop-tauri-mobile`** — adds iOS / Android specifics (App Store / Play Store rules, mobile-specific keychain).
- **`desktop-internal`** — for internal-tool apps without code signing requirements (drop Rules 5–7).

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: desktop-tauri@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–13 ratified. Reflects May 2026 reality (Stronghold deprecated, EV cert no longer privileged, AKV 1-year cap, notarytool replaces altool).
```
