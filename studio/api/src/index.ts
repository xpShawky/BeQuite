import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { health } from "./routes/health.js";
import { projects } from "./routes/projects.js";
import { receipts } from "./routes/receipts.js";
import { snapshots } from "./routes/snapshots.js";
import { streams } from "./routes/streams.js";
import { auth as authRoutes } from "./routes/auth.js";
import { authMiddleware, getAuthMode } from "./lib/auth.js";
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
      // Production allow-list lands v0.20.x+ once domain is registered.
      return null;
    },
    credentials: true,
    allowHeaders: ["Authorization", "Content-Type", "X-Requested-With"],
    exposeHeaders: ["X-BeQuite-Auth-Mode"],
  }),
);

// Public surface (no auth required) — health + auth/status
app.route("/healthz", health);
app.route("/api/v1/auth", authRoutes);

// Authenticated surface — every /api/v1/* route below this line goes through
// authMiddleware. In local-dev mode the middleware passes through; in token
// mode it enforces Bearer auth.
app.use("/api/v1/projects/*", authMiddleware);
app.use("/api/v1/receipts/*", authMiddleware);
app.use("/api/v1/snapshots/*", authMiddleware);
app.use("/api/v1/streams/*", authMiddleware);

app.route("/api/v1/projects", projects);
app.route("/api/v1/receipts", receipts);
app.route("/api/v1/snapshots", snapshots);
app.route("/api/v1/streams", streams);

app.get("/", (c) =>
  c.json({
    name: "BeQuite Studio API",
    version: "0.20.0",
    docs: "See studio/api/README.md for endpoint surface.",
    workspace_root: getWorkspaceRoot(),
    auth_mode: getAuthMode(),
    endpoints: {
      public: [
        "GET /healthz",
        "GET /api/v1/auth/status",
        "POST /api/v1/auth/token (local-dev bootstrap)",
        "DELETE /api/v1/auth/token/:id",
        "GET /api/v1/auth/tokens",
      ],
      authenticated_read: [
        "GET /api/v1/projects",
        "GET /api/v1/projects/snapshot?path=<abs-path>",
        "GET /api/v1/receipts?path=<abs-path>",
        "GET /api/v1/receipts/:sha?path=<abs-path>",
        "GET /api/v1/snapshots/:version?path=<abs-path>",
      ],
      authenticated_write: [
        "POST /api/v1/receipts (append-only; idempotent on content-hash)",
        "POST /api/v1/snapshots (append-only; refuses overwrite)",
      ],
      authenticated_streams: [
        "GET /api/v1/streams/all?path=<abs-path>      (SSE; all events)",
        "GET /api/v1/streams/receipts?path=<abs-path> (SSE; receipt events)",
        "GET /api/v1/streams/cost?path=<abs-path>     (SSE; cost-ledger events)",
        "GET /api/v1/streams/phase?path=<abs-path>    (SSE; phase + activeContext events)",
      ],
    },
  }),
);

app.notFound((c) => c.json({ error: "not found", path: c.req.path }, 404));

const port = Number(process.env.PORT || 3002);

export default {
  port,
  fetch: app.fetch,
};

// Log on startup (Bun runs this file as the entry point).
if (typeof Bun !== "undefined") {
  console.log(`BeQuite Studio API v0.20.0 listening on http://localhost:${port}`);
  console.log(`Workspace root: ${getWorkspaceRoot()}`);
  console.log(`Auth mode: ${getAuthMode()}`);
  console.log(`SSE streams: /api/v1/streams/{all,receipts,cost,phase}`);
}
