---
adr_id: ADR-011-cli-authentication
title: CLI Authentication — device-code MVP + secure local storage + CI-mode separation
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
superseded_by: null
constitution_version: 1.2.0
related_articles: [IV]
related_doctrines: [default-web-saas, vibe-defense]
implementation_target: v0.10.x phase-1 docs / v0.10.x+ phase-2 stubs / v0.11.x phase-3 device-code working / v0.12.x phase-4 OAuth optional / v1.x browser callback when BeQuite has a hosted auth server
---

# ADR-011: CLI Authentication

> Status: **accepted (Phase-1 docs only — implementation lands v0.10.x+)** · Date: 2026-05-10 · Decided by: Ahmed Shawky + Claude (architect)

## Context

BeQuite runs locally today. Authentication into the CLI itself was deferred — there was no BeQuite-side identity to authenticate. Three forces now make it the right time to design CLI auth, even before implementation:

1. **Future cloud features** (Layer 2 Studio per ADR-008) need stable user identity before they ship. Designing auth now lets v0.10.x+ slot in cleanly.
2. **Multi-machine workflows** — engineers want their projects + receipts + cost ledger to follow them across devices. That requires identity.
3. **Consumer-subscription pain** — Ahmed wants to use his Claude Pro + ChatGPT Plus subscriptions without managing API keys. Authentication into BeQuite itself is **distinct** from authenticating into LLM providers, but the two intersect: BeQuite identity binds the user's API-key-or-equivalent to a session.

Article IV (Security & destruction) governs how secrets are handled. CLI auth must extend Article IV without replacing any existing rule.

## Three options compared

### Option A — Browser-OAuth-callback

**Flow:** `bequite auth login` opens browser → user signs in to BeQuite cloud → redirects to `http://localhost:<port>/callback` → CLI receives auth code → exchanges for token → stores in OS keychain.

**Pros:**
- Familiar UX (matches `gh auth login`, `gcloud auth login`, `npm login`).
- Browser handles SSO / 2FA / password manager.
- No copy-paste error surface.

**Cons:**
- **Requires a hosted auth server** (BeQuite has none today; Layer 2 v2.0.0+).
- **Doesn't work in headless contexts** (SSH, Docker, CI, dev container without GUI browser).
- Localhost callback is fragile (port collisions; firewalls; corporate proxies).
- Browser launch on Linux is unreliable across distros.

### Option B — Device-code login

**Flow:** `bequite auth login` shows a short user code (e.g. `B3QU-1T3X`) + URL → user opens any device's browser → enters code → CLI polls until session is bound.

**Pros:**
- **Works headless** (SSH / Docker / CI). User can complete auth on phone.
- Same UX as `aws sso login`, `gh auth login --web`, `kubectl login --device-code`.
- No localhost callback — no port collisions, firewall issues.
- Cross-device first-class (auth on phone, complete on laptop).
- Easy to implement against any OAuth 2.0 device-flow server (RFC 8628).

**Cons:**
- Marginally more steps for the user (must type a code).
- Still requires a hosted auth server (same constraint as Option A).

### Option C — Email magic link

**Flow:** `bequite auth login --email <email>` → email arrives with link → click → CLI's polling loop receives confirmation.

**Pros:**
- Familiar UX.
- No password to remember.

**Cons:**
- Slowest of the three (email delivery latency).
- Requires email infrastructure (SES / Resend / Postmark) at BeQuite-cloud — same constraint as A + B.
- Email client friction (corporate spam filters; phone-vs-laptop email split).
- Token-leakage surface (forwarded email containing magic link).

## Decision

**Recommended MVP: Option B — Device-code login.**

The chosen path:

1. **Phase-1 (this ADR — v0.9.2):** Author the strategy doc + this ADR. No code yet.
2. **Phase-2 (v0.10.x):** CLI command stubs (`bequite auth login` / `logout` / `whoami` / `status` / `refresh`) that print "auth backend not yet available" with a graceful fallback to local-file identity (a generated UUID stored at `.bequite/.identity.json` so existing receipts have a `session_id`).
3. **Phase-3 (v0.11.x or post-v1.0.0):** Stand up minimal BeQuite-cloud auth server (or use a hosted IdP — Ory, Auth0, WorkOS, Better-Auth-self-hosted) with RFC 8628 device-code flow. CLI implements polling.
4. **Phase-4 (v0.12.x+ or v1.x):** Optional Browser-OAuth-callback alongside device-code; user picks.
5. **Phase-5 (post-v1.0.0):** OAuth 2.1 PKCE + refresh tokens + multi-device session management.

**Why device-code wins as MVP:**
- Works everywhere BeQuite runs (laptop, dev container, CI box, SSH).
- Phone auth is a feature, not a bug — engineers complete the flow without leaving their terminal.
- Same RFC 8628 endpoint used by all major IdPs — switching providers is a config change, not a rewrite.

## Token storage

**Default: Python `keyring` package** (https://pypi.org/project/keyring/).

- macOS: Keychain (sandboxed per-app).
- Windows: Credential Manager.
- Linux: Secret Service (gnome-keyring / kwallet via libsecret).
- Headless Linux fallback: `keyring` plaintext-backend with file mode `0600`, gitignored at `.bequite/.session/token` — flagged with prominent warning.

**Token shape:**

```python
{
  "version": "1",
  "user_id": "user-uuid",
  "user_email": "ahmed@example.com",
  "issued_utc": "2026-05-10T14:00:00Z",
  "expires_utc": "2026-05-17T14:00:00Z",  # 7-day default
  "refresh_token": "<opaque>",            # for silent refresh
  "scopes": ["projects:read", "projects:write", "receipts:write"],
  "device_id": "<machine-uuid>",
  "issuer": "https://auth.bequite.dev/",
  "audience": "bequite-cli"
}
```

## Session refresh

- Active token expires every 7 days (configurable via `bequite.config.toml::auth.session_lifetime_days`).
- Refresh token expires every 90 days.
- On expiry, CLI prompts: "Your BeQuite session expired. Run `bequite auth refresh` to renew (no full re-login required)."
- Silent refresh attempt happens automatically when CLI detects expiry on first command of a session — but only when refresh token is still valid.

## Logout

- `bequite auth logout` revokes the active token at the auth server, deletes from OS keychain, removes session file.
- `bequite auth logout --all-devices` revokes every session bound to the user (requires fresh login on each device next time).

## Offline mode

- CLI continues to operate **without auth** for all local-only commands (audit, freshness, verify, receipts emission, route show).
- Cloud features (project sync, team collaboration when shipped) error gracefully: "This command requires authentication. Run `bequite auth login` (or set `BEQUITE_OFFLINE=true` to suppress this hint)."
- Offline-mode flag in config: `bequite.config.toml::auth.offline_only = true` — CLI never attempts auth-required commands.

## CI mode

**CI must NEVER prompt for human auth.** Three paths:

1. **Service account API key** — `BEQUITE_API_KEY` environment variable. CI provisions via secret manager (GitHub Actions secrets, GitLab variables, etc.). Read-only by default; write scopes opt-in.
2. **Workload identity federation** (post-v1.0.0) — GitHub OIDC / Azure managed identity / GCP workload identity → CI exchange OIDC token for short-lived BeQuite session. No long-lived secret in CI.
3. **`BEQUITE_CI_MODE=true`** flag — CLI runs in CI-friendly mode: no prompts, no browser launches, no interactive polling.

API keys are **never** valid for human-in-the-loop sessions. Human login → device-code only. CI auth → `BEQUITE_API_KEY` only. The two paths never cross.

## Threat model

| Threat | Mitigation |
|---|---|
| Stolen laptop with active session | OS keychain requires user login to unlock; `bequite auth logout --all-devices` from another device. |
| Phishing during device-code flow | The verification URL is shown in the terminal AND is shown again at the auth server before the user clicks "approve" — phishing requires controlling both. |
| Token leakage in shell history | CLI never prints the token. The user-code (e.g. `B3QU-1T3X`) is one-time-use and bound to the device making the request. |
| Replay of old token | Tokens expire (7d default); revoked tokens are checked on every cloud call. |
| MitM on auth.bequite.dev | TLS pinning in CLI; cert-transparency log monitoring on server side. |
| Malicious CI secret | `BEQUITE_API_KEY` keys are scoped (read-only / write / admin) per project; rotation supported; audit logged at server. |
| Local file-based token leakage (headless Linux) | Mode 0600; gitignored; flagged with prominent warning at login time. |

## Failure states (no silent failures)

| Condition | CLI behavior |
|---|---|
| Auth server unreachable | "Cannot reach auth.bequite.dev. Check network or run with `BEQUITE_OFFLINE=true`." |
| Token expired | "Session expired YYYY-MM-DD. Run `bequite auth refresh`." |
| Token revoked | "Session was revoked (likely from another device). Run `bequite auth login`." |
| OS keychain access denied | "Could not access OS keychain. Falling back to file-based session at `.bequite/.session/` (NOT RECOMMENDED — file permissions only, not OS-protected)." (User must opt-in.) |
| Device-code timeout | "Device-code expired (15 min). Run `bequite auth login` again." |
| User cancels in browser | "Login cancelled at auth server. No session created." |

## Test plan

| Test | Type | Where |
|---|---|---|
| `bequite auth login` (mocked server) → token stored | integration | `tests/integration/auth/test_auth_smoke.py` |
| `bequite auth whoami` shows email | integration | same |
| `bequite auth logout` revokes + deletes | integration | same |
| `bequite auth refresh` with valid refresh token | integration | same |
| `bequite auth status` reports `unauthenticated` cleanly | integration | same |
| Expired token → silent refresh attempt | integration | same |
| Expired refresh token → friendly error | integration | same |
| `BEQUITE_API_KEY` set → CI mode skips device-code | integration | same |
| Offline mode → cloud command errors with `BEQUITE_OFFLINE=true` hint | integration | same |
| Token leakage in `git log -p` for any test | security | CI |
| Phishing scenario (URL spoofing) | manual / red-team | post-v1.0.0 |

## CLI command surface

```
bequite auth login [--device-code | --browser]
bequite auth logout [--all-devices]
bequite auth whoami [--json]
bequite auth status [--json]
bequite auth refresh
```

Slash commands (skill-aware hosts):

```
/bequite.auth.login
/bequite.auth.logout
/bequite.auth.whoami
/bequite.auth.status
/bequite.auth.refresh
```

## TUI/CLI dashboard panel

`bequite status` (or the auto-mode dashboard, v0.10.0+) shows:

```
┌─ BeQuite session ──────────────────────────────────────────┐
│ user:        ahmed@example.com                              │
│ workspace:   personal                                        │
│ project:     bequite (this repo)                             │
│ session:     a3f12...e89  (issued 5d ago, expires in 2d)    │
│ device:      ahmed-mac-m4-pro                                │
│ mode:        online                                          │
│ scopes:      projects:read projects:write receipts:write    │
└─────────────────────────────────────────────────────────────┘
```

Color-coded:
- 🟢 green when authenticated + online + token > 24h to expiry
- 🟡 yellow when token < 24h to expiry, or offline
- 🔴 red when unauthenticated or token revoked

## Constitution amendment status

**No new Iron Law required.** Article IV (Security & destruction discipline) covers the security envelope; this ADR is the operational framework that fulfills Article IV for the auth surface specifically. Implementation lands in v0.10.x+ phases per the table at top.

## Status: accepted (Phase-1 docs only; 2026-05-10)

Phase 2-5 land per the implementation_target field. v0.10.x+ Phase-2 ships the CLI command stubs that gracefully degrade until the auth server exists.

## Cross-references

- Strategy doc: `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`
- Constitution Article IV: `.bequite/memory/constitution.md`
- Existing receipts module: `cli/bequite/receipts.py` (v0.7.0; `session_id` field already accommodates user identity)
- Future BeQuite Cloud (Layer 2): `docs/merge/MASTER_MD_MERGE_AUDIT.md` Bucket D
