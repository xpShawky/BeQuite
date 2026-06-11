# CLI Authentication Strategy

> Architectural strategy doc that fleshes out ADR-011. This is the operational reference for engineers implementing v0.10.x+ Phase-2 stubs and v0.11.x+ Phase-3 device-code flow.
>
> **Status:** Phase-1 (docs-only). Implementation lands v0.10.x+.

---

## 1. Authentication goals

1. **Identify the human user** running BeQuite CLI sessions, separately from the project being worked on.
2. **Bind sessions to receipts** so the existing v0.7.0 receipt chain can attribute work to a real identity (today's `session_id` is a per-process UUID; tomorrow it's a user-bound session).
3. **Enable cross-device workflows** — same engineer signs in on laptop + dev container + CI; their projects, receipts, cost ledger follow.
4. **Enable future BeQuite Cloud** (Layer 2 Studio per ADR-008) without rewriting the auth layer.
5. **Keep API-key auth for CI/automation** — but never as the primary human login path.
6. **Keep BeQuite usable offline** for every local-only command.

## 2. Non-goals

- BeQuite is **not** an identity provider. We use an off-the-shelf IdP (Auth0 / WorkOS / Better-Auth-self-hosted / Ory) when Phase-3 ships.
- We do **not** authenticate into Anthropic / OpenAI / Google — those use their own API keys, configured separately in `bequite.config.toml::providers`.
- We do **not** drive consumer subscriptions (Claude Pro, ChatGPT Plus) by reusing browser session cookies. That path is ToS-grey + brittle (see ADR-012 §Part 3).
- v1.0.0 ships **stubs that gracefully degrade** when no auth backend exists. The actual auth server stands up in Phase-3 (v0.11.x+ or post-v1.0.0).

## 3. Three options compared (full)

See ADR-011 §Three options compared for the canonical comparison. Summary:

| Option | UX | Headless | Time-to-MVP | Server cost |
|---|---|---|---|---|
| A. Browser-OAuth-callback | familiar (`gh auth login`) | ❌ | weeks | medium (callback handling) |
| **B. Device-code (RFC 8628)** | code + URL on phone | ✅ | days | low (RFC8628 standard) |
| C. Email magic link | familiar (Notion / Slack) | ✅ | days | medium (email infra) |

**Decision: Option B for MVP. Option A as alternative for v0.12.x+.**

## 4. Recommended MVP (Option B detailed)

### Sequence diagram

```
User                   BeQuite CLI                BeQuite Auth Server
 │                          │                              │
 │  bequite auth login      │                              │
 │ ──────────────────────▶  │                              │
 │                          │  POST /device/code           │
 │                          │ ───────────────────────────▶│
 │                          │  ◀───────────────────────── │
 │                          │  device_code, user_code,    │
 │                          │  verification_uri, expires  │
 │                          │                              │
 │  ◀────────────────────── │                              │
 │  "Open: https://...      │                              │
 │   Enter code: B3QU-1T3X" │                              │
 │                          │                              │
 │  (opens browser on       │                              │
 │   any device)            │                              │
 │                          │                              │
 │  enter user_code         │                              │
 │ ─────────────────────────────────────────────────────▶ │
 │  approve scopes          │                              │
 │ ─────────────────────────────────────────────────────▶ │
 │                          │                              │
 │                          │  POST /token (poll, every    │
 │                          │  5s, until 'pending' →       │
 │                          │  'authorized')               │
 │                          │ ───────────────────────────▶│
 │                          │  ◀───────────────────────── │
 │                          │  access_token,              │
 │                          │  refresh_token,             │
 │                          │  expires_in                 │
 │                          │                              │
 │                          │  store in OS keychain       │
 │  ◀────────────────────── │                              │
 │  "Signed in as ..."      │                              │
```

### Polling rules

- Initial poll interval: 5 seconds.
- Backoff on `slow_down` response: double the interval (RFC 8628 §3.5).
- Total timeout: 15 minutes (configurable; matches Auth0 / Okta defaults).
- On user cancel: CLI exits 0 with "Login cancelled at the server."

## 5. Secure local token storage

### Primary: OS keychain via Python `keyring` package

Storage backends (auto-selected by `keyring`):

| Platform | Backend | Encryption |
|---|---|---|
| macOS | macOS Keychain (per-app sandboxed) | AES-256 (system-managed) |
| Windows | Windows Credential Manager | DPAPI (system-managed) |
| Linux (graphical) | GNOME-keyring or KWallet (Secret Service API) | system-managed |
| Linux (headless) | `keyring`'s `PlaintextKeyring` fallback | **plaintext** — flagged with prominent warning |
| Docker / CI | env var `BEQUITE_API_KEY` (CI mode only) | secret manager |

### Token shape stored

```python
class StoredSession(BaseModel):
    version: Literal["1"] = "1"
    user_id: str               # opaque UUID
    user_email: str
    issued_utc: str            # ISO 8601
    expires_utc: str           # ISO 8601 (default 7 days)
    refresh_token: str         # opaque; required for silent refresh
    refresh_expires_utc: str   # ISO 8601 (default 90 days)
    scopes: list[str]          # ["projects:read", ...]
    device_id: str             # generated on first login per machine
    issuer: str                # "https://auth.bequite.dev/"
    audience: str              # "bequite-cli"
```

### Read path (every CLI command)

```python
def get_session() -> StoredSession | None:
    """Return active session or None. Silently refreshes if needed."""
    raw = keyring.get_password("bequite", "session")
    if raw is None:
        return None
    session = StoredSession.model_validate_json(raw)
    if datetime_now_utc() > session.expires_utc:
        if datetime_now_utc() < session.refresh_expires_utc:
            return refresh_session(session)  # silent
        return None  # full re-login required
    return session
```

### Cloud-required commands

A new decorator on Click commands:

```python
@requires_auth(scope="projects:write")
def some_cloud_command():
    ...
```

Local-only commands (audit, freshness, verify, receipts emit / list / show, route show, pricing list) **don't** use `@requires_auth` — they work offline.

## 6. Session refresh strategy

- **Silent refresh** triggered automatically on first CLI command of a session if access_token is expired but refresh_token still valid.
- **Explicit refresh** via `bequite auth refresh` — for users who want to extend their session without waiting for natural expiry.
- **Refresh failure** → friendly error: "Your session can no longer be refreshed. Run `bequite auth login` (no data will be lost)."

## 7. Logout behavior

```
bequite auth logout
```

Steps:
1. Revoke active token at auth server (`POST /token/revoke`).
2. Delete from OS keychain (`keyring.delete_password("bequite", "session")`).
3. Remove `.bequite/.session/` if file-fallback was used.
4. Confirm: "Signed out. Your project data is preserved at `<repo>/.bequite/`."

```
bequite auth logout --all-devices
```

Steps:
1. Revoke ALL active sessions for this user (`POST /sessions/revoke-all`).
2. Same local cleanup.
3. Confirm: "Signed out from all devices. You will need to re-login on each device on next use."

## 8. Offline mode behavior

| Setting | Behavior |
|---|---|
| Default (no env var) | Cloud commands attempt auth → friendly error if unauthenticated. Local commands always work. |
| `BEQUITE_OFFLINE=true` | All cloud commands suppressed; CLI prints "Skipped (offline mode)." |
| `bequite.config.toml::auth.offline_only = true` | Same as `BEQUITE_OFFLINE=true` but per-project. |

## 9. CI mode behavior

**CI must NEVER prompt for human auth.**

```yaml
# .github/workflows/your-workflow.yml
env:
  BEQUITE_API_KEY: ${{ secrets.BEQUITE_API_KEY }}
  BEQUITE_CI_MODE: true
```

Effects of `BEQUITE_CI_MODE=true`:
- No browser launches.
- No interactive polling.
- No `auth login` prompts.
- Identity = service account derived from API key.
- API key scopes (read-only / write / admin) enforced per project.
- Session never persisted (in-memory only).

## 10. Threat model

See ADR-011 §Threat model.

## 11. Failure states (no silent failures)

See ADR-011 §Failure states.

## 12. Test plan

See ADR-011 §Test plan.

## 13. CLI command design

```
bequite auth login [--device-code | --browser]    # device-code default
bequite auth logout [--all-devices]
bequite auth whoami [--json]
bequite auth status [--json]
bequite auth refresh
```

## 14. UI / TUI display design

The auth panel is the leftmost block of the auto-mode dashboard (lands v0.10.0+):

```
┌─ BeQuite session ──────────────────────────────────────────┐
│ user:        ahmed@example.com                              │
│ workspace:   personal                                        │
│ project:     bequite (this repo)                             │
│ session:     a3f12...e89  (issued 5d ago, expires in 2d)    │
│ device:      ahmed-mac-m4-pro                                │
│ mode:        🟢 online                                       │
│ scopes:      projects:read projects:write receipts:write    │
└─────────────────────────────────────────────────────────────┘
```

Panel states:
- 🟢 green: authenticated + online + token > 24h to expiry.
- 🟡 yellow: authenticated + token < 24h to expiry, OR offline mode.
- 🔴 red: unauthenticated OR token revoked.

When unauthenticated:
```
┌─ BeQuite session ──────────────────────────────────────────┐
│ 🔴 not signed in                                            │
│                                                              │
│ Run `bequite auth login` to sign in.                        │
│ Or `BEQUITE_OFFLINE=true bequite ...` to suppress.          │
└─────────────────────────────────────────────────────────────┘
```

## 15. Integration with existing modules

### Receipts (v0.7.0)

Receipt's existing `session_id` field is a per-process UUID today. Post-v0.11.x:

```diff
@dataclass
class Receipt:
    version: str
    session_id: str          # per-process UUID
+   user_id: Optional[str]   # set when authenticated; None in offline mode
+   workspace_id: Optional[str]  # set when org-scoped (post-v1.0.0)
    phase: str
    ...
```

Backward-compatible: receipts emitted in offline mode (no `user_id`) still validate cleanly.

### Cost ledger (v0.8.0)

`bequite ledger show` will, when authenticated, fetch the user's organization-scoped ledger from BeQuite Cloud (post-v0.11.x) — useful for tracking team-wide spend. Today, ledger is local-only.

### Hooks (v0.3.0)

A new hook `sessionstart-load-auth.sh` (lands v0.10.x+ Phase-2) will run on session start:
1. Check if a session exists in OS keychain.
2. If yes + valid → echo `🟢 authenticated as <email>` to the agent's session-start context.
3. If yes + expired → echo `🟡 session expired; cloud commands will prompt for re-login`.
4. If no → echo `🔴 unauthenticated; cloud commands disabled`.

The hook never blocks; it's informational.

### Constitution Article IV

This module **extends** Article IV (Security & destruction). It does not replace any rule. Specific Article IV obligations honored:

- **Never read `.env*`.** Tokens never live in `.env`. They live in OS keychain or (fallback) `.bequite/.session/` (gitignored).
- **Never commit secrets.** Token storage paths are gitignored from v0.10.x+ Phase-2 onward (`.bequite/.session/` joins the existing `.bequite/.keys/` gitignore additions).
- **Hooks enforce.** `pretooluse-secret-scan.sh` already blocks secret commits; it'll stay green for token paths because they're gitignored.

## 16. Failure modes + recovery (operations runbook)

| Symptom | Likely cause | Recovery |
|---|---|---|
| `bequite auth login` hangs at polling | Auth server unreachable | Cancel; check network; try again with `--browser` if available. |
| `bequite auth whoami` shows wrong email | Multi-account confusion | `bequite auth logout && bequite auth login` to reauthenticate. |
| `bequite auth refresh` fails after laptop sleep | Refresh token expired | `bequite auth login` (full re-login required). |
| Cloud command says "scope insufficient" | Token granted with read-only scopes | `bequite auth login --scopes projects:write` to upgrade. |
| OS keychain locked (Linux) | Session daemon not started | `gnome-keyring-daemon --replace --start`. |
| Token stuck in keychain after laptop loss | (laptop is gone; can't logout from there) | From any other device: `bequite auth logout --all-devices` invalidates everywhere. |

## 17. Future paths

- **v1.x — Browser-OAuth-callback** as an alternative to device-code (better UX for desktop users; users on dev containers / SSH continue with device-code).
- **v1.x — OAuth 2.1 with PKCE.**
- **v1.x — SSO / SAML via WorkOS.** When BeQuite has team org features.
- **v2.x — Workload identity federation.** GitHub OIDC / Azure managed identity / GCP workload identity for CI.
- **v2.x — Hardware token / passkey login** (WebAuthn).

## 18. Cross-references

- ADR: `.bequite/memory/decisions/ADR-011-cli-authentication.md`
- Constitution: `.bequite/memory/constitution.md` (Article IV)
- Receipts: `cli/bequite/receipts.py` (v0.7.0)
- Cost ledger: `cli/bequite/cost_ledger.py` (v0.8.0)
- Hooks: `skill/hooks/`
- Master plan: `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`
