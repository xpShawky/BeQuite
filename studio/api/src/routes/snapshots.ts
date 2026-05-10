/**
 * Memory-Bank snapshot endpoint (v0.19.5).
 *
 * POST /api/v1/snapshots — emit a phase-end snapshot of the Memory Bank
 *   to .bequite/memory/prompts/v<N>/<timestamp>_<phase>_<reason>/.
 *
 * Append-only by Article III + Article IV. The endpoint refuses to:
 *   - overwrite an existing snapshot path
 *   - write outside the workspace root
 *   - skip the Iron Law X re-read probe
 *
 * The snapshot itself is just a copy of the six Memory Bank files at the
 * moment of the call. It's the kind of one-way-door artifact Article III
 * requires at phase end + before one-way operations.
 *
 * GET /api/v1/snapshots/:version — list snapshots under v<N>/.
 */

import { Hono } from "hono";
import fs from "node:fs";
import path from "node:path";
import { z } from "zod";
import { getWorkspaceRoot } from "../lib/fs-loader.js";
import { buildIronLawXBlock } from "../lib/iron-law-x.js";
import { getAuth } from "../lib/auth.js";

export const snapshots = new Hono();

const MEM_FILES = [
  "constitution.md",
  "projectbrief.md",
  "productContext.md",
  "systemPatterns.md",
  "techContext.md",
  "activeContext.md",
  "progress.md",
];

function projectRoot(c: import("hono").Context): { root: string; error?: string } {
  const queryPath = c.req.query("path") ?? getWorkspaceRoot();
  const root = path.resolve(queryPath);
  if (!root.startsWith(getWorkspaceRoot())) {
    return { root, error: "path outside workspace root" };
  }
  return { root };
}

const SnapshotBodySchema = z.object({
  /** Major version directory under prompts/, e.g. "v1", "v2". */
  version: z
    .string()
    .regex(/^v[0-9]+$/i, "version must match /^v[0-9]+$/i (e.g. v1, v2)")
    .default("v1"),
  /** Phase identifier, e.g. P0..P7 or a sub-version like v0.19.5. */
  phase: z
    .string()
    .min(1)
    .max(16)
    .regex(/^[A-Za-z0-9._-]+$/, "phase must be alphanumeric + . _ -"),
  /** Short slug describing why this snapshot was taken. */
  reason: z
    .string()
    .min(2)
    .max(64)
    .regex(/^[A-Za-z0-9-]+$/, "reason must be slug-shaped (alphanumeric + hyphen)"),
});

snapshots.post("/", async (c) => {
  const a = getAuth(c);
  const { root, error } = projectRoot(c);
  if (error) return c.json({ error }, 403);

  let body: unknown;
  try {
    body = await c.req.json();
  } catch {
    return c.json({ error: "body must be JSON" }, 400);
  }
  const parsed = SnapshotBodySchema.safeParse(body);
  if (!parsed.success) {
    return c.json(
      { error: "invalid snapshot request", issues: parsed.error.issues },
      400,
    );
  }
  const { version, phase, reason } = parsed.data;

  const memDir = path.join(root, ".bequite", "memory");
  if (!fs.existsSync(memDir)) {
    return c.json({ error: ".bequite/memory not found at project root" }, 404);
  }

  // UTC timestamp without colons (filesystem-safe across Windows + POSIX).
  const stamp = new Date().toISOString().replace(/[:]/g, "-");
  const snapDir = path.join(
    memDir,
    "prompts",
    version,
    `${stamp}_${phase}_${reason}`,
  );

  if (fs.existsSync(snapDir)) {
    // Append-only — refuse to overwrite. Caller bumps the timestamp by 1s + retries.
    return c.json(
      {
        error:
          "snapshot directory already exists (append-only). Wait 1 second and retry.",
        path: snapDir,
      },
      409,
    );
  }

  fs.mkdirSync(snapDir, { recursive: true });

  const copied: string[] = [];
  const skipped: string[] = [];
  for (const f of MEM_FILES) {
    const src = path.join(memDir, f);
    const dst = path.join(snapDir, f);
    if (!fs.existsSync(src)) {
      skipped.push(f);
      continue;
    }
    fs.copyFileSync(src, dst);
    copied.push(f);
  }

  // Manifest
  const manifest = {
    version,
    phase,
    reason,
    timestamp_utc: new Date().toISOString(),
    copied,
    skipped,
    written_by: a.identity ?? "local-dev",
    schema: "snapshot/v1",
  };
  const manifestPath = path.join(snapDir, "manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

  // Iron Law X verification
  const ironLawX = await buildIronLawXBlock(manifestPath, {
    what: `wrote ${copied.length} Memory Bank files + manifest.json into ${snapDir}`,
    routeAlive: async () => {
      // Probe: all copied files are re-readable
      for (const f of copied) {
        try {
          fs.readFileSync(path.join(snapDir, f), "utf8");
        } catch {
          return false;
        }
      }
      return true;
    },
    callerMust: [
      "GET /api/v1/snapshots/:version to list snapshots under that version",
      "no service restart required",
      "commit this snapshot directory to git when convenient (snapshots ARE tracked)",
    ],
  });

  return c.json(
    {
      ok: true,
      snapshot_path: snapDir,
      version,
      phase,
      reason,
      copied,
      skipped,
      identity: a.identity,
      iron_law_x: ironLawX,
    },
    201,
  );
});

snapshots.get("/:version", (c) => {
  const { root, error } = projectRoot(c);
  if (error) return c.json({ error }, 403);
  const version = c.req.param("version");
  if (!/^v[0-9]+$/i.test(version)) {
    return c.json({ error: "version must match /^v[0-9]+$/i" }, 400);
  }
  const versionDir = path.join(root, ".bequite", "memory", "prompts", version);
  try {
    const entries = fs.readdirSync(versionDir, { withFileTypes: true });
    const items = entries
      .filter((e) => e.isDirectory())
      .map((e) => {
        const dir = path.join(versionDir, e.name);
        let manifest: unknown = null;
        try {
          manifest = JSON.parse(
            fs.readFileSync(path.join(dir, "manifest.json"), "utf8"),
          );
        } catch {
          // Pre-v0.19.5 snapshots have no manifest.json — surface name only.
        }
        return { name: e.name, path: dir, manifest };
      });
    return c.json({ items });
  } catch {
    return c.json({ items: [] });
  }
});
