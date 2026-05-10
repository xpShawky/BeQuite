---
id: ADR-016
title: Studio API terminal — Rules of Engagement for command execution (POST exec + SSE stream)
status: accepted
date: 2026-05-11
supersedes: null
authors: [BeQuite Builder]
related: [ADR-013 (Studio v2 architecture), ADR-014 (Iron Law X), ADR-015 (Studio API auth + write surface)]
constitution_articles: [IV (Security & destruction discipline), IX (Cybersecurity & authorized-testing discipline), X (Operational completeness)]
---

## Context

The Studio dashboard's CommandConsole has been a static mock since v0.18.0 — it shows what `bequite *` commands look like but doesn't run them. Users have been opening a separate terminal to run `bequite auto`, `bequite verify`, etc., and watching the dashboard refresh on receipt arrival.

v0.20.5 closes that loop: the dashboard runs commands directly. This is the **first endpoint that executes user-supplied commands.** Per Constitution Article IV ("Never run destructive ops without an explicit ADR") + Article IX ("Authorized-testing discipline") this requires explicit Rules of Engagement. Without RoE, the API would be a generic remote-shell, which:

1. **Violates Article IV.** A trivial path to `rm -rf` outside `/tmp` if the auth is bypassed or token-mode is misconfigured.
2. **Violates Doctrine `vibe-defense`.** The default Doctrine for vibe-handoff projects pre-supposes that endpoints don't execute arbitrary commands.
3. **Creates a new attack surface.** Any future RCE vulnerability in Hono/Bun/Node would now mean shell access on the dev machine.

The RoE narrows the surface to exactly what the dashboard needs (running BeQuite CLI commands against a known workspace) and refuses everything else with a clear error.

## Decision

### 1. Allow-list, not deny-list

The terminal accepts commands only from a hard-coded allow-list. v0.20.5 ships with two entries:

```typescript
export const DEFAULT_ALLOWLIST: AllowEntry[] = [
  {
    binary: "bequite",
    description: "BeQuite CLI",
    allowed_subcommands: null, // any bequite subcommand is allowed
    note: "Per ADR-016 §1. No shell, no piping, no redirects.",
  },
  {
    binary: "bq",
    description: "BeQuite CLI shorthand",
    allowed_subcommands: null,
    note: "Alias of bequite; same RoE.",
  },
];
```

Adding to the allow-list is an explicit ADR amendment. **No env variable, no config flag, no runtime override** — this is a hardcoded constant in `src/lib/exec-allowlist.ts`. Operators can fork BeQuite to widen the list, but every fork is auditable.

Rejected commands return `403 command not on allow-list { binary, request_id, see_adr: "ADR-016" }`.

### 2. No shell interpolation. Ever.

`child_process.spawn(binary, argsArray, { shell: false })`. Never `spawn("...", { shell: true })` or `exec()`. The command line is parsed into a binary + array of arguments via a small whitespace-aware splitter (no quote-handling YAGNI; if you need quotes, fork the allow-list). This eliminates the entire class of `; rm -rf /` injections.

### 3. cwd guard

The `cwd` for the spawned process must resolve under `BEQUITE_WORKSPACE_ROOT`. Any attempt to start a command in a path outside the workspace root returns `403 cwd outside workspace root` and refuses to spawn. This is the same path-traversal guard used on read/write endpoints (ADR-015 §"Path-traversal guard preserved") — extended to exec.

### 4. Per-execution timeout

Default: 30 minutes (`1800` seconds). Maximum: 6 hours (`21600` seconds; matches auto-mode's wall-clock ceiling). Beyond the timeout the spawned process gets `SIGTERM` followed 5 seconds later by `SIGKILL` if it didn't exit. The session transitions to `status: "timeout"` and emits a final SSE event with `exit_reason: "timeout"`.

### 5. Output ring buffer (10MB cap)

Per-session stdout+stderr is buffered in a ring of 10MB max. When the buffer fills, the oldest lines drop and a `<truncated N bytes>` marker appears. This prevents OOM if a misbehaving command spews unbounded output. The dashboard's xterm.js renderer is the live consumer; the ring is the late-joiner cache.

### 6. No stdin forwarding (v0.20.5)

The exec endpoint accepts `stdin` as a single optional string in the POST body (passed to the child once at spawn) but does NOT support live stdin forwarding from the dashboard. Reasoning: the BeQuite CLI is mostly non-interactive (auto-mode, verify, audit). Live-stdin terminals (interactive shells, REPL flows) have a wider attack surface and are deferred to v0.21.0+ if a real use case appears.

### 7. Cancel endpoint = SIGTERM, not SIGKILL

`POST /api/v1/terminal/sessions/:id/cancel` sends SIGTERM (graceful). After 5 seconds without exit, an automatic SIGKILL fires. This gives BeQuite CLI a chance to flush receipts + write recovery state before dying.

### 8. Per-execution receipt

Every successful exec start emits a receipt to `<workspace>/.bequite/receipts/` with:

```json
{
  "phase": "EXEC",
  "exec": {
    "binary": "bequite",
    "args": ["auto", "--feature", "add-health-endpoint"],
    "cwd": "/abs/workspace",
    "session_id": "exec-<uuid>",
    "started_at_utc": "...",
    "ended_at_utc": "...",         // null while running
    "exit_code": null,
    "exit_reason": "running",      // running | clean | timeout | cancelled | error
    "duration_ms": null,
    "stdout_sha256": "...",        // computed on session end
    "stderr_sha256": "...",
    "output_truncated": false
  },
  "identity": "token:<id> | local-dev",
  "constitution_version": "1.3.0"
}
```

The receipt is updated (replaced — append-only chain via `parent_receipt`) when the session exits. This gives a complete audit trail of every command the dashboard ran.

### 9. Auth-gated like any /api/v1/* endpoint

The terminal routes are mounted under the same `authMiddleware` as `/api/v1/projects/*`. In `local-dev` mode, no auth required (single-machine dev). In `token` mode, Bearer required (or `?token=` for the SSE stream sub-route only, narrowed per ADR-015 §"EventSource auth"). In `device-code` mode, the Phase-3 auth-server gate applies.

### 10. Iron Law X self-attestation on every exec start

The `POST /api/v1/terminal/exec` response includes the same `iron_law_x` block as receipts/snapshots writes (ADR-014 + ADR-015). Verifies: the spawned process's PID is alive at response-time, the receipt was persisted + readable, the SSE stream URL exists. If the process died immediately at spawn (e.g. binary not found despite passing the allow-list — possible if `bequite` isn't on PATH), the response is `500` with the exit reason — not `200 ok`.

### 11. RoE acknowledgment header

Every `POST /api/v1/terminal/exec` request must include `X-BeQuite-RoE-Ack: ADR-016` as a header. This is a soft seatbelt, not security: it forces clients to actively opt into running commands rather than discovering the endpoint by accident. Missing or mismatched value returns `412 missing or invalid X-BeQuite-RoE-Ack header — see ADR-016 §11`.

## Alternatives considered

1. **Generic shell exec (with shell:true).** Rejected. Article IV violation; injection-prone.
2. **node-pty for a true interactive terminal.** Rejected for v0.20.5. node-pty needs native compilation, fails on Windows often, and adds bidirectional WS plumbing. The 90% use case (`bequite auto --feature X`) doesn't need a pty. Folded into v0.21.0+ if interactive use cases emerge.
3. **No allow-list (auth alone).** Rejected. Auth controls *who* can call the endpoint; allow-list controls *what* they can run. Defense-in-depth — a stolen token shouldn't be able to `terraform destroy`.
4. **Per-token allow-list overrides.** Rejected. Adds complexity (token-scope mapping) for a use case that hasn't appeared. v1.0.0 ships with the hardcoded list; widening requires a fork or an ADR amendment.
5. **WebSocket bidirectional from day one.** Rejected for v0.20.5 — covered in §6. SSE-output + POST-exec gives 95% of the value with 30% of the complexity.
6. **Buffer everything in memory, no ring cap.** Rejected. A `bequite verify` run with `--verbose` could easily emit 100MB+. OOM-by-default is not a feature.
7. **Skip the receipt-on-exec.** Rejected. Article III + Article VII (hallucination defense): every state-mutating action should leave an artifact. Exec is state-mutating by definition (it can write files, modify git state, change `.bequite/receipts/`).

## Consequences

### Positive

- The dashboard's CommandConsole becomes live without becoming a remote shell.
- Every command run is auditable via the per-exec receipt (which itself feeds into the existing chain validation + `bequite verify-receipts` flow).
- The allow-list is a *hard* boundary, not a config — fork-the-source to widen it. This is the strongest possible signal that adding `terraform` or `kubectl` to the allow-list is a Big Decision.
- Iron Law X attestation extends to exec — a "command running" claim now verifies the PID is alive at response time.

### Negative

- Adding new allowed binaries requires a code change + ADR. Slight friction for power users who want to wire up `pnpm` or `pytest` directly. Mitigation: those tools are usually invoked via `bequite verify` already; the allow-list captures the right level of indirection.
- The allow-list is hardcoded — operators forking BeQuite must remember to keep it in sync upstream. Mitigation: documented in `studio/api/README.md`.
- v0.20.5 ships POST+SSE not WS, so no live stdin. Power users running `bequite auto` interactively would still use a separate terminal. Mitigation: documented limitation; v0.21.0+ if needed.

### Neutral

- The SSE stream sub-route (`/api/v1/terminal/sessions/:id/stream`) reuses the v0.20.0 SSE infrastructure (`hono/streaming`).
- The allow-list module ships at `studio/api/src/lib/exec-allowlist.ts` with its own integration test fixture in v0.20.x+.

## Verification

Endpoint contract:

```
POST   /api/v1/terminal/exec                          (X-BeQuite-RoE-Ack required)
GET    /api/v1/terminal/sessions
GET    /api/v1/terminal/sessions/:id
GET    /api/v1/terminal/sessions/:id/stream           (SSE)
POST   /api/v1/terminal/sessions/:id/cancel
```

Test cases:

1. POST with disallowed binary (`rm`) → 403, no spawn occurred, no receipt written.
2. POST without `X-BeQuite-RoE-Ack` → 412.
3. POST with `cwd` outside workspace root → 403.
4. POST with `bequite --version` → 200, session_id returned, receipt written, SSE stream emits `started` + stdout lines + `exit` event.
5. POST `bequite auto --max-cost-usd 5 --feature foo` (long-running) + cancel → SIGTERM sent, exit_reason: "cancelled" in receipt.
6. POST with `timeout_seconds: 1` against a `sleep 60` analog → SIGTERM after 1s, then SIGKILL after 6s, exit_reason: "timeout".
7. SSE stream output > 10MB → truncated marker visible, exit OK.
8. Iron Law X attestation block present + accurate on every successful POST.

## What this ADR does NOT authorize

- Adding any binary other than `bequite` and `bq` to the allow-list. That requires a separate ADR.
- Live stdin forwarding from the dashboard. That requires v0.21.0+ ADR.
- Running commands as a different user (sudo / runas). That requires a v0.22.0+ ADR + a hardening pass.
- Exposing the terminal endpoint to the public internet without TLS + IP-allow-list. (The dev quickstart is localhost-only; production-grade exposure is v2.0.0+ with the auth server in place.)
- Sending commands found inside untrusted content (web pages, emails, third-party documents). Per the prompt-injection-defense layer of the Constitution, instructions found in observed content require explicit user confirmation through the chat interface — they cannot be executed automatically.

## References

- [ADR-013](./ADR-013-studio-v2-architecture.md) — Studio v2 architecture.
- [ADR-014](./ADR-014-iron-law-x-operational-completeness.md) — Iron Law X full text.
- [ADR-015](./ADR-015-studio-api-auth-and-write-surface.md) — Auth + write surface (this ADR extends the same auth model to exec).
- [Constitution v1.3.0](../constitution.md) — Article IV (security/destruction), Article IX (cybersecurity/authorized-testing), Article X (operational completeness).
- [Doctrine `vibe-defense`](../../skill/doctrines/vibe-defense.md) — extra-strict defaults for vibe-handoff projects.
- [Constitution Article IV — three-tier command-safety classification](../constitution.md) — safe / needs-approval / dangerous.
