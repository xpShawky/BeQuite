/**
 * Auth middleware for the Studio API (v0.19.5).
 *
 * MVP auth layer. Three modes:
 *
 *   local-dev   — pass-through (no token required). Default when
 *                 BEQUITE_AUTH_MODE is unset or explicitly "local-dev".
 *                 Suitable for: running studio/api/ on the same machine
 *                 as studio/dashboard/. Adds X-BeQuite-Auth-Mode header
 *                 to responses so the dashboard can surface a warning.
 *
 *   token       — Bearer token in `Authorization` header. Tokens are
 *                 stored at <workspace>/.bequite/.auth/tokens.json
 *                 (gitignored; file-mode 0600 best-effort on POSIX).
 *                 Suitable for: dev with multiple agents on the same box,
 *                 or local-network access where you want a soft barrier.
 *
 *   device-code — RFC 8628 device-code flow against a remote auth server
 *                 (per ADR-011 Phase-3). The remote auth server stands
 *                 up v0.20.0+; until then, device-code mode falls back
 *                 to rejecting all requests with a 503 + helpful message.
 *
 * Architecture note: this is intentionally minimal. Full Better-Auth
 * integration (per Doctrine `default-web-saas` Rule 9 — Better-Auth or
 * Clerk or Supabase Auth, no custom auth) lands when the multi-user
 * auth-server topology is finalized (v0.20.0+). The shape below is
 * compatible with swapping the token validator out for a Better-Auth
 * `Session` check without touching route handlers.
 *
 * Iron Law X: every write endpoint relies on this middleware. If auth
 * is misconfigured at boot, the middleware returns 503 from the first
 * write attempt rather than silently passing the request — fail-loud.
 */

import type { Context, MiddlewareHandler } from "hono";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { getWorkspaceRoot } from "./fs-loader.js";

export type AuthMode = "local-dev" | "token" | "device-code";

export interface AuthContext {
  mode: AuthMode;
  identity: string | null; // null in local-dev; "token:<uuid-prefix>" in token mode; "user:<sub>" in device-code mode.
  token_id: string | null; // last 8 chars of token, for log line correlation
}

const TOKEN_FILE_REL = path.join(".bequite", ".auth", "tokens.json");

export function getAuthMode(): AuthMode {
  const raw = (process.env.BEQUITE_AUTH_MODE || "local-dev").toLowerCase();
  if (raw === "token" || raw === "device-code") return raw;
  return "local-dev";
}

interface StoredToken {
  id: string;          // first 8 chars of the token (for log correlation)
  hash: string;        // sha256 of the raw token (compared against incoming)
  label: string;       // human-readable label (e.g. "dashboard-local")
  created_utc: string;
  last_used_utc: string | null;
}

interface TokenFile {
  version: "1";
  tokens: StoredToken[];
}

function tokensPath(): string {
  return path.join(getWorkspaceRoot(), TOKEN_FILE_REL);
}

function readTokenFile(): TokenFile {
  const p = tokensPath();
  try {
    const raw = fs.readFileSync(p, "utf8");
    const parsed = JSON.parse(raw) as TokenFile;
    if (parsed.version !== "1" || !Array.isArray(parsed.tokens)) {
      throw new Error("malformed tokens.json (version mismatch or shape error)");
    }
    return parsed;
  } catch (e: unknown) {
    if ((e as NodeJS.ErrnoException).code === "ENOENT") {
      return { version: "1", tokens: [] };
    }
    throw e;
  }
}

function writeTokenFile(tf: TokenFile): void {
  const p = tokensPath();
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(tf, null, 2), { encoding: "utf8" });
  // Best-effort restrict perms on POSIX; no-op on Windows.
  try {
    fs.chmodSync(p, 0o600);
  } catch {
    // Windows or filesystem without chmod — acceptable.
  }
}

function sha256(s: string): string {
  return crypto.createHash("sha256").update(s).digest("hex");
}

/**
 * Generate a fresh token and persist its hash. Returns the raw token
 * (only returned once — callers must store it). The hash is what
 * lives on disk; the raw token is never persisted.
 */
export function mintToken(label = "default"): { token: string; id: string } {
  const raw = crypto.randomBytes(32).toString("hex"); // 64 hex chars
  const id = raw.slice(0, 8);
  const hash = sha256(raw);
  const tf = readTokenFile();
  tf.tokens.push({
    id,
    hash,
    label,
    created_utc: new Date().toISOString(),
    last_used_utc: null,
  });
  writeTokenFile(tf);
  return { token: raw, id };
}

export function revokeToken(id: string): boolean {
  const tf = readTokenFile();
  const before = tf.tokens.length;
  tf.tokens = tf.tokens.filter((t) => t.id !== id);
  if (tf.tokens.length === before) return false;
  writeTokenFile(tf);
  return true;
}

export function listTokens(): Array<Omit<StoredToken, "hash">> {
  const tf = readTokenFile();
  return tf.tokens.map(({ hash: _hash, ...rest }) => rest);
}

function validateBearerToken(rawToken: string): { ok: boolean; id: string | null } {
  const hash = sha256(rawToken);
  const tf = readTokenFile();
  const match = tf.tokens.find((t) => t.hash === hash);
  if (!match) return { ok: false, id: null };
  // Update last_used_utc (best-effort)
  match.last_used_utc = new Date().toISOString();
  try {
    writeTokenFile(tf);
  } catch {
    // ignore — auth check shouldn't fail on a write error
  }
  return { ok: true, id: match.id };
}

/**
 * Hono middleware that enforces the configured auth mode.
 * Attaches `auth: AuthContext` to the Hono context for downstream handlers.
 */
export const authMiddleware: MiddlewareHandler = async (c, next) => {
  const mode = getAuthMode();

  // Always echo the mode so the dashboard can warn the user when it's
  // talking to a local-dev API by accident.
  c.header("X-BeQuite-Auth-Mode", mode);

  if (mode === "local-dev") {
    c.set("auth", { mode, identity: null, token_id: null } as AuthContext);
    return next();
  }

  if (mode === "device-code") {
    // Phase-3 auth server (ADR-011) lands v0.20.0+. Until then, fail loud.
    return c.json(
      {
        error: "device-code auth mode is not yet wired",
        detail:
          "set BEQUITE_AUTH_MODE=token (with .bequite/.auth/tokens.json populated via POST /api/v1/auth/token) or BEQUITE_AUTH_MODE=local-dev for single-machine dev",
        adr: "ADR-011 Phase-3",
      },
      503,
    );
  }

  // mode === "token"
  // Primary: Authorization: Bearer <token>. Fallback: ?token=<hex> (used by
  // browser EventSource on /api/v1/streams/* — EventSource cannot send custom
  // headers). The query-param path is only honored on stream routes to narrow
  // the URL-leak surface (logs, referrers).
  let rawToken = "";
  const header = c.req.header("authorization") || c.req.header("Authorization");
  if (header && header.toLowerCase().startsWith("bearer ")) {
    rawToken = header.slice(7).trim();
  } else if (c.req.path.startsWith("/api/v1/streams/")) {
    const queryToken = c.req.query("token");
    if (queryToken) rawToken = queryToken.trim();
  }
  if (!rawToken) {
    return c.json(
      {
        error: c.req.path.startsWith("/api/v1/streams/")
          ? "missing Authorization: Bearer <token> header (or ?token= query for SSE clients)"
          : "missing Authorization: Bearer <token> header",
        auth_mode: mode,
      },
      401,
    );
  }
  const { ok, id } = validateBearerToken(rawToken);
  if (!ok) {
    return c.json({ error: "invalid or revoked token", auth_mode: mode }, 401);
  }
  c.set("auth", {
    mode,
    identity: `token:${id}`,
    token_id: id,
  } as AuthContext);
  return next();
};

/**
 * Reads the AuthContext attached by `authMiddleware`. Throws if missing
 * — that would indicate a route mounted without the middleware (bug).
 */
export function getAuth(c: Context): AuthContext {
  const auth = c.get("auth") as AuthContext | undefined;
  if (!auth) {
    throw new Error(
      "auth context missing — every write route MUST mount authMiddleware",
    );
  }
  return auth;
}
