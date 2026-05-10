import { Hono } from "hono";
import { getWorkspaceRoot } from "../lib/fs-loader.js";

export const health = new Hono();

health.get("/", (c) =>
  c.json({
    status: "ok",
    service: "bequite-api",
    version: "0.20.5",
    workspace_root: getWorkspaceRoot(),
    uptime_s: Math.round(process.uptime()),
  }),
);
