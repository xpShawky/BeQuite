/**
 * SSE event-stream routes (v0.20.0).
 *
 *   GET /api/v1/streams/all?path=<workspace>      — all events
 *   GET /api/v1/streams/receipts?path=<workspace> — only "receipt" events
 *   GET /api/v1/streams/cost?path=<workspace>     — only "cost" events
 *   GET /api/v1/streams/phase?path=<workspace>    — only "phase" + "active_context"
 *
 * Each stream:
 *   - Sends an initial `hello` event with workspace_root + auth_mode.
 *   - Sends a `heartbeat` event every 30 seconds (keeps proxy connections alive,
 *     and lets the dashboard detect a dead stream when no heartbeats arrive).
 *   - Sends `watcher_error` events on the underlying fs.watch failure so the
 *     dashboard can surface "stream degraded" instead of silently going dark.
 *   - Closes cleanly on client disconnect.
 *
 * Auth: gated by the same `authMiddleware` as other /api/v1/* routes.
 *
 * Path-traversal guard: `?path=` resolves under BEQUITE_WORKSPACE_ROOT before
 * the watcher is started.
 */

import { Hono } from "hono";
import { streamSSE } from "hono/streaming";
import path from "node:path";
import { getWorkspaceRoot } from "../lib/fs-loader.js";
import { subscribe, type EventName, type BusEvent } from "../lib/event-bus.js";
import { getAuth, getAuthMode } from "../lib/auth.js";

export const streams = new Hono();

const HEARTBEAT_MS = 30_000;

function projectRoot(c: import("hono").Context): { root: string; error?: string } {
  const queryPath = c.req.query("path") ?? getWorkspaceRoot();
  const root = path.resolve(queryPath);
  if (!root.startsWith(getWorkspaceRoot())) {
    return { root, error: "path outside workspace root" };
  }
  return { root };
}

function streamHandler(filterNames?: EventName[]) {
  return async (c: import("hono").Context) => {
    const a = getAuth(c);
    const { root, error } = projectRoot(c);
    if (error) return c.json({ error }, 403);

    return streamSSE(c, async (stream) => {
      // 1. Hello event
      await stream.writeSSE({
        event: "hello",
        data: JSON.stringify({
          workspace_root: root,
          auth_mode: getAuthMode(),
          identity: a.identity,
          filter: filterNames ?? "all",
          server_version: "0.20.0",
          ts: new Date().toISOString(),
        }),
      });

      // 2. Subscribe to bus
      const unsubscribe = await subscribe(root, async (event: BusEvent) => {
        if (filterNames && !filterNames.includes(event.name)) return;
        try {
          await stream.writeSSE({
            event: event.name,
            data: JSON.stringify(event),
          });
        } catch {
          // Client likely disconnected; teardown handled below.
        }
      });

      // 3. Heartbeat
      const heartbeat = setInterval(async () => {
        try {
          await stream.writeSSE({
            event: "heartbeat",
            data: JSON.stringify({ ts: new Date().toISOString() }),
          });
        } catch {
          // Client gone — interval will be cleared on abort.
        }
      }, HEARTBEAT_MS);

      // 4. Wait for client disconnect
      await new Promise<void>((resolve) => {
        const onAbort = () => {
          clearInterval(heartbeat);
          unsubscribe();
          resolve();
        };
        // Hono's stream context aborts on client close.
        stream.onAbort(onAbort);
      });
    });
  };
}

streams.get("/all", streamHandler());
streams.get(
  "/receipts",
  streamHandler(["receipt", "watcher_error", "watcher_started", "watcher_stopped"]),
);
streams.get(
  "/cost",
  streamHandler(["cost", "watcher_error", "watcher_started", "watcher_stopped"]),
);
streams.get(
  "/phase",
  streamHandler([
    "phase",
    "active_context",
    "watcher_error",
    "watcher_started",
    "watcher_stopped",
  ]),
);
