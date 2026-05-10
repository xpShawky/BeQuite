import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { health } from "./routes/health.js";
import { projects } from "./routes/projects.js";
import { receipts } from "./routes/receipts.js";
import { getWorkspaceRoot } from "./lib/fs-loader.js";

const app = new Hono();

app.use("*", logger());
app.use(
  "*",
  cors({
    origin: (origin) => {
      // Allow localhost dev (marketing on :3000, dashboard on :3001) and any explicit origins.
      if (!origin) return "*";
      if (
        origin.startsWith("http://localhost:") ||
        origin.startsWith("http://127.0.0.1:")
      )
        return origin;
      // Production allow-list lands v0.19.x+ once domain is registered.
      return null;
    },
    credentials: true,
  }),
);

app.route("/healthz", health);
app.route("/api/v1/projects", projects);
app.route("/api/v1/receipts", receipts);

app.get("/", (c) =>
  c.json({
    name: "BeQuite Studio API",
    version: "0.19.0",
    docs: "See studio/api/README.md for endpoint surface.",
    workspace_root: getWorkspaceRoot(),
    endpoints: [
      "GET /healthz",
      "GET /api/v1/projects",
      "GET /api/v1/projects/snapshot?path=<abs-path>",
      "GET /api/v1/receipts?path=<abs-path>",
      "GET /api/v1/receipts/:sha?path=<abs-path>",
    ],
  }),
);

app.notFound((c) =>
  c.json({ error: "not found", path: c.req.path }, 404),
);

const port = Number(process.env.PORT || 3002);

export default {
  port,
  fetch: app.fetch,
};

// Log on startup (Bun runs this file as the entry point).
if (typeof Bun !== "undefined") {
  console.log(`BeQuite Studio API v0.19.0 listening on http://localhost:${port}`);
  console.log(`Workspace root: ${getWorkspaceRoot()}`);
}
