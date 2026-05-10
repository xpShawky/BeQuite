import { Hono } from "hono";
import fs from "node:fs";
import path from "node:path";
import { z } from "zod";
import { getWorkspaceRoot } from "../lib/fs-loader.js";

export const receipts = new Hono();

const ReceiptShaSchema = z
  .string()
  .regex(/^[a-f0-9]{8,64}$/i, "invalid sha hex");

receipts.get("/", (c) => {
  const projectPath = c.req.query("path") ?? getWorkspaceRoot();
  const root = path.resolve(projectPath);
  if (!root.startsWith(getWorkspaceRoot())) {
    return c.json({ error: "path outside workspace root" }, 403);
  }
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
  const projectPath = c.req.query("path") ?? getWorkspaceRoot();
  const root = path.resolve(projectPath);
  if (!root.startsWith(getWorkspaceRoot())) {
    return c.json({ error: "path outside workspace root" }, 403);
  }
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
