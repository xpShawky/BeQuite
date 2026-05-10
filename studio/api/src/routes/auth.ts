import { Hono } from "hono";
import { z } from "zod";
import {
  getAuthMode,
  getAuth,
  mintToken,
  revokeToken,
  listTokens,
} from "../lib/auth.js";

export const auth = new Hono();

/** GET /api/v1/auth/status — surface current mode + identity (if any). */
auth.get("/status", (c) => {
  const mode = getAuthMode();
  let identity: string | null = null;
  let token_id: string | null = null;
  try {
    const a = getAuth(c);
    identity = a.identity;
    token_id = a.token_id;
  } catch {
    // No middleware mounted on /status (it's public). That's fine.
  }
  return c.json({
    mode,
    identity,
    token_id,
    tokens_count: mode === "token" ? listTokens().length : null,
    notes:
      mode === "local-dev"
        ? "Pass-through. Suitable for single-machine dev. Switch to BEQUITE_AUTH_MODE=token before exposing the API beyond localhost."
        : mode === "token"
          ? "Bearer-token mode. Mint tokens via POST /api/v1/auth/token (allowed only when BEQUITE_AUTH_MODE=local-dev temporarily, or via the CLI `bequite api token mint` in v0.20.0+)."
          : "Device-code mode (RFC 8628). Auth-server lands v0.20.0+ per ADR-011 Phase-3.",
  });
});

const MintTokenSchema = z.object({
  label: z.string().min(1).max(64).default("default"),
});

/**
 * POST /api/v1/auth/token — mint a new bearer token.
 *
 * SECURITY: This endpoint is intentionally restricted. In local-dev mode
 * it works (bootstrap path: the operator sets BEQUITE_AUTH_MODE=local-dev
 * just long enough to mint the first token, then restarts in token mode).
 * In token mode it requires an existing valid token (rotation path). In
 * device-code mode it's rejected (the auth server is the token issuer).
 */
auth.post("/token", async (c) => {
  const mode = getAuthMode();
  if (mode === "device-code") {
    return c.json(
      {
        error:
          "token minting is not available in device-code mode (auth server is the issuer)",
      },
      403,
    );
  }
  // Note: in token mode we still allow minting (rotation). The middleware
  // (mounted at /api/v1/* by the index) already verified the caller's
  // existing token if mode==token. If mode==local-dev, the middleware
  // passes through unauthenticated — that IS the bootstrap path.

  let body: { label?: unknown } = {};
  try {
    body = (await c.req.json()) as { label?: unknown };
  } catch {
    // Empty body is fine — defaults will apply.
  }
  const parsed = MintTokenSchema.safeParse(body);
  if (!parsed.success) {
    return c.json(
      { error: "invalid request body", issues: parsed.error.issues },
      400,
    );
  }
  const { token, id } = mintToken(parsed.data.label);
  return c.json(
    {
      token, // raw token — only returned ONCE. Caller must store it.
      id,
      label: parsed.data.label,
      warning:
        "Store this token now. The server only retains a sha256 hash; the raw value is never returned again. To use it: Authorization: Bearer <token>",
    },
    201,
  );
});

const RevokeTokenSchema = z.object({
  id: z.string().regex(/^[a-f0-9]{8}$/, "token id must be 8 hex chars"),
});

/** DELETE /api/v1/auth/token/:id — revoke a token by its 8-char id. */
auth.delete("/token/:id", (c) => {
  const mode = getAuthMode();
  if (mode === "device-code") {
    return c.json(
      { error: "token revocation is handled by the auth server in device-code mode" },
      403,
    );
  }
  const id = c.req.param("id");
  const parsed = RevokeTokenSchema.safeParse({ id });
  if (!parsed.success) {
    return c.json({ error: "invalid token id", issues: parsed.error.issues }, 400);
  }
  const ok = revokeToken(parsed.data.id);
  if (!ok) {
    return c.json({ error: "token not found", id: parsed.data.id }, 404);
  }
  return c.json({ ok: true, id: parsed.data.id, revoked: true });
});

/** GET /api/v1/auth/tokens — list tokens (without their hashes). */
auth.get("/tokens", (c) => {
  const mode = getAuthMode();
  if (mode === "device-code") {
    return c.json(
      { error: "token list is owned by the auth server in device-code mode" },
      403,
    );
  }
  return c.json({ items: listTokens() });
});
