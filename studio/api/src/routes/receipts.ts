import { Hono } from "hono";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { z } from "zod";
import { getWorkspaceRoot } from "../lib/fs-loader.js";
import { buildIronLawXBlock } from "../lib/iron-law-x.js";
import { getAuth } from "../lib/auth.js";

export const receipts = new Hono();

const ReceiptShaSchema = z
  .string()
  .regex(/^[a-f0-9]{8,64}$/i, "invalid sha hex");

// ---- READ endpoints (v0.19.0) ---------------------------------------------

function projectRoot(c: import("hono").Context): { root: string; error?: string } {
  const queryPath = c.req.query("path") ?? getWorkspaceRoot();
  const root = path.resolve(queryPath);
  if (!root.startsWith(getWorkspaceRoot())) {
    return { root, error: "path outside workspace root" };
  }
  return { root };
}

receipts.get("/", (c) => {
  const { root, error } = projectRoot(c);
  if (error) return c.json({ error }, 403);
  const dir = path.join(root, ".bequite", "receipts");
  let files: string[];
  try {
    files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  } catch {
    return c.json({ items: [] });
  }
  const items = files
    .map((f) => {
      try {
        const raw = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
        return {
          filename: f,
          phase: raw.phase,
          timestamp_utc: raw.timestamp_utc,
          model: raw.model?.name,
          cost_usd: raw.cost?.usd ?? 0,
          signed: !!raw.signature,
        };
      } catch {
        return null;
      }
    })
    .filter(Boolean)
    .sort((a: any, b: any) => (a.timestamp_utc < b.timestamp_utc ? 1 : -1));
  return c.json({ items });
});

receipts.get("/:sha", (c) => {
  const { root, error } = projectRoot(c);
  if (error) return c.json({ error }, 403);
  const shaParam = c.req.param("sha");
  const sha = ReceiptShaSchema.safeParse(shaParam);
  if (!sha.success) {
    return c.json({ error: "invalid sha", issues: sha.error.issues }, 400);
  }
  const dir = path.join(root, ".bequite", "receipts");
  let match: string | undefined;
  try {
    match = fs
      .readdirSync(dir)
      .find((f) => f.startsWith(sha.data) && f.endsWith(".json"));
  } catch {
    return c.json({ error: "receipts dir not found" }, 404);
  }
  if (!match) return c.json({ error: "receipt not found" }, 404);
  try {
    const raw = JSON.parse(fs.readFileSync(path.join(dir, match), "utf8"));
    return c.json(raw);
  } catch (e) {
    return c.json({ error: "malformed receipt", detail: String(e) }, 500);
  }
});

// ---- WRITE endpoint (v0.19.5; append-only) ---------------------------------

/**
 * Minimal receipt shape accepted by POST. The full Receipt schema lives in
 * cli/bequite/receipts.py (Python emitter); the API doesn't validate every
 * field — that's the emitter's job. We validate the structural minimum so
 * a misaligned client doesn't write garbage that breaks chain validation.
 *
 * Article IV: append-only. No DELETE, no PUT. Filename is determined by
 * content_hash so identical receipts collapse to the same on-disk file
 * (idempotent re-emit is safe).
 */
const ReceiptBodySchema = z.object({
  version: z.literal("1"),
  session_id: z.string().min(1),
  phase: z.string().min(2).max(8),
  timestamp_utc: z.string().min(10),
  model: z.object({
    name: z.string().min(1),
    reasoning_effort: z.string().optional(),
    fallback_model: z.string().nullable().optional(),
  }),
  input: z.object({
    prompt_hash: z.string().regex(/^[a-f0-9]{64}$/i),
    memory_snapshot_hash: z.string().regex(/^[a-f0-9]{64}$/i),
  }),
  output: z.object({
    diff_hash: z.string().regex(/^[a-f0-9]{64}$/i),
    files_touched: z.array(z.string()),
  }),
  tools_invoked: z.array(z.unknown()).default([]),
  tests: z
    .object({
      command: z.string(),
      exit: z.number(),
      stdout_hash: z.string().regex(/^[a-f0-9]{64}$/i),
    })
    .nullable()
    .optional(),
  cost: z.object({
    input_tokens: z.number().int().nonnegative(),
    output_tokens: z.number().int().nonnegative(),
    usd: z.number().nonnegative(),
  }),
  doctrine: z.array(z.string()).default([]),
  constitution_version: z.string().min(1),
  parent_receipt: z.string().nullable().optional(),
  signature: z.string().optional(),
});

function canonicalJSONStringify(obj: unknown): string {
  // Sorted-key, no-whitespace canonical JSON (matches the Python receipts.py
  // content_hash function so the on-disk sha lines up across emitters).
  const seen = new WeakSet();
  const sortKeys = (v: any): any => {
    if (v === null || typeof v !== "object") return v;
    if (Array.isArray(v)) return v.map(sortKeys);
    if (seen.has(v)) throw new Error("cycle in JSON object");
    seen.add(v);
    const sorted: Record<string, any> = {};
    for (const k of Object.keys(v).sort()) {
      sorted[k] = sortKeys(v[k]);
    }
    return sorted;
  };
  return JSON.stringify(sortKeys(obj));
}

function contentHash(receipt: unknown): string {
  // Strip signature before hashing (chain pointer is hash of unsigned content).
  const r = { ...(receipt as Record<string, unknown>) };
  delete r.signature;
  return crypto
    .createHash("sha256")
    .update(canonicalJSONStringify(r))
    .digest("hex");
}

receipts.post("/", async (c) => {
  // Auth is mounted at /api/v1/* by index.ts — getAuth() will surface the
  // identity for the audit trail.
  const a = getAuth(c);

  const { root, error } = projectRoot(c);
  if (error) return c.json({ error }, 403);

  let body: unknown;
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: "body must be JSON" }, 400);
  }

  const parsed = ReceiptBodySchema.safeParse(body);
  if (!parsed.success) {
    return c.json(
      { error: "invalid receipt shape", issues: parsed.error.issues },
      400,
    );
  }

  const dir = path.join(root, ".bequite", "receipts");
  fs.mkdirSync(dir, { recursive: true });

  const sha = contentHash(parsed.data);
  const filename = `${sha}-${parsed.data.phase}.json`;
  const filepath = path.join(dir, filename);

  // Append-only: if the same content already exists, return 200 + existing
  // (idempotent re-emit; receipt content_hash is deterministic).
  if (fs.existsSync(filepath)) {
    const ironLawX = await buildIronLawXBlock(filepath, {
      what: `idempotent re-emit (receipt ${sha.slice(0, 12)} already on disk)`,
      callerMust: [
        "no further action — receipt already persisted; chain pointer stable",
      ],
    });
    return c.json(
      {
        ok: true,
        sha,
        filename,
        idempotent: true,
        identity: a.identity,
        iron_law_x: ironLawX,
      },
      200,
    );
  }

  // Write
  const payload = JSON.stringify(parsed.data, null, 2);
  fs.writeFileSync(filepath, payload, "utf8");

  // Iron Law X verification: re-read + probe sibling GET
  const ironLawX = await buildIronLawXBlock(filepath, {
    what: `persisted receipt for phase ${parsed.data.phase} (sha ${sha.slice(0, 12)})`,
    routeAlive: async () => {
      // Sibling probe: can we read the receipt back via /api/v1/receipts/:sha?
      // We do this by re-reading the file inline (skipping the HTTP layer
      // since we're already inside the handler) + verifying it parses.
      try {
        const raw = fs.readFileSync(filepath, "utf8");
        JSON.parse(raw);
        return true;
      } catch {
        return false;
      }
    },
    callerMust: [
      "GET /api/v1/receipts/:sha to read the persisted receipt back",
      "no service restart required (file-system write is immediately visible to subsequent reads)",
    ],
  });

  return c.json(
    {
      ok: true,
      sha,
      filename,
      idempotent: false,
      identity: a.identity,
      iron_law_x: ironLawX,
    },
    201,
  );
});
