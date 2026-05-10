# Example 03 — Tauri note app (`vault-notes`)

> A local-first encrypted note-taking desktop app demonstrating BeQuite's `desktop-tauri` Doctrine end-to-end: Tauri v2 + SvelteKit + SQLite + OS keychain (NOT deprecated Stronghold).

## What it does

- Local-first: all data lives in `~/Library/Application Support/vault-notes/` (or platform equivalent).
- Notes are AES-GCM encrypted at rest; the encryption key lives in the OS keychain.
- No cloud sync (v1). v2 may add encrypted-at-rest sync via a user-supplied S3-compatible target.
- Searchable, taggable, markdown-rendered.

## Stack (decided in P1)

| Layer | Choice | Why |
|---|---|---|
| Runtime | Tauri v2 | The only mature lightweight desktop runtime for 2026. Per Doctrine: NOT Stronghold (deprecated). |
| Frontend | SvelteKit | Smallest bundles. Pairs well with Tauri's WebView constraints. |
| Database | SQLite (via `tauri-plugin-sql`) | Local-only; no server. |
| Encryption at rest | AES-GCM 256 (via Rust `aes-gcm` crate) | FIPS-friendly when paired with `gov-fedramp` Doctrine. |
| Key management | OS keychain via `tauri-plugin-keyring` | macOS Keychain / Windows Credential Manager / Linux Secret Service. NOT Stronghold (deprecated, removed in Tauri v3). |
| Search | SQLite FTS5 | Built into SQLite; no extra dep. |
| Markdown render | mdsvex (compile-time) + remark (runtime for user notes) | |
| Codesigning (macOS) | `xcrun notarytool submit` | Replaced `altool` since Xcode 13+. |
| Codesigning (Windows) | OV cert + AzureSignTool (vcsjones) | NOT EV — Microsoft removed EV-specific OIDs in Aug 2024. NOT `relic`. |
| Licensing (optional v2+) | Keygen.sh | |
| Build | Tauri CLI v2 + bun for frontend |
| Tests | Playwright (e2e via tauri-driver) + Vitest (unit) + Rust unit (`cargo test`) |

## Phases

### P0 — Discovery
"Why does the world need another note app?" Answer: existing apps either sync to opinionated clouds (Notion, Bear) or lack native cross-platform polish (Obsidian's plugin sprawl). `vault-notes` is single-purpose, local-first, encryption-at-rest by default, no plugin system to audit.

### P1 — Stack ADR
See `.bequite/memory/decisions/ADR-001-stack.md`.

### P2 — Plan + Contracts
- Tauri commands: `notes_list`, `notes_get`, `notes_create`, `notes_update`, `notes_delete`, `notes_search`, `tags_list`.
- DB schema: `notes(id, title, body_encrypted, body_nonce, created_utc, updated_utc)` + `tags(id, name)` + `note_tags(note_id, tag_id)` + FTS5 virtual table.
- Encryption: master key in OS keychain; per-note nonce in DB; AEAD via `aes-gcm`.

### P3 — Phases
- phase-1: Tauri scaffold + SvelteKit boot + SQLite + tokens.css.
- phase-2: Encryption key management + AES-GCM at rest.
- phase-3: Note CRUD (no encryption yet → encryption merge in phase-4).
- phase-4: Tagging + search (FTS5).
- phase-5: Polish + Codesigning + Release pipeline.

### P4 — Tasks
Atomic per-phase; see `specs/notes-crud/tasks.md` (placeholder).

### P5 — Implementation
- Frontend: `src/routes/`, `src/lib/`.
- Backend: `src-tauri/src/lib.rs` (commands + crypto + DB).
- Tests: `tests/` (Vitest), `src-tauri/tests/` (Rust).

### P6 — Verify
- Cargo test (Rust unit tests for crypto + DB).
- Vitest for frontend.
- Playwright via tauri-driver for e2e.
- Smoke: launch app, create note, restart app, decrypt note → assert plaintext matches.
- Codesigning gate: macOS notarytool + Windows AzureSignTool both succeed in CI.

### P7 — Handoff
HANDOFF describes:
- How a user installs (drag to Applications / Programs).
- How a maintainer codesigns + notarizes a release.
- How a developer adds a feature.

## Doctrine compliance (`desktop-tauri`)

- ✅ Tauri v2 (current as of May 2026).
- ✅ OS keychain via `tauri-plugin-keyring` (NOT Stronghold).
- ✅ macOS notarization via `xcrun notarytool submit` (NOT altool).
- ✅ Windows codesigning via OV cert + AzureSignTool (NOT EV; NOT relic).
- ✅ Local-first: no cloud sync v1.
- ✅ Updates via Tauri auto-updater + ed25519 signature verification.
- ✅ User data never logged to console / telemetry.

## Cost

$0/mo runtime (no servers). Codesigning certs are the only operating cost:
- Apple Developer Program: $99/yr
- OV cert (Windows): $200-400/yr (Sectigo / DigiCert)
- (EV is no longer worth it as of Aug 2024.)

## Cross-references

- Doctrine: `../../skill/doctrines/desktop-tauri.md`
- ADR-001: `.bequite/memory/decisions/ADR-001-stack.md`
- Brief reconciliations applied: Stronghold deprecation, EV cert obsolescence, altool → notarytool, AzureSignTool over relic (per BeQuite v0.1.0 brief verification).
