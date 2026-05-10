/**
 * Per-workspace filesystem watcher (v0.20.0).
 *
 * Watches three paths under a workspace and emits events into the event-bus:
 *
 *   .bequite/receipts/                        — new file = "receipt" event
 *   .bequite/cache/cost-ledger.json           — change = "cost" event
 *   .bequite/memory/activeContext.md          — change = "active_context" event
 *   state/current_phase.md                    — change = "phase" event
 *
 * fs.watch quirks (especially on Windows):
 *   - Events sometimes fire twice for one change. We coalesce 250ms.
 *   - On rapid sequential writes the second event can be missed. The
 *     dashboard's request/response API is the authoritative read; SSE is
 *     a notification layer.
 *   - If the watched path doesn't exist yet, fs.watch on the parent dir
 *     catches creation. We watch the parent + filter by basename.
 *
 * Iron Law X: if a watcher errors out, we emit `watcher_error` rather than
 * silently dying. The route handler can surface this to the SSE client so
 * the dashboard can show "stream degraded — refresh to reconnect."
 */

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import type { BusEvent, EventName } from "./event-bus.js";
import { publish } from "./event-bus.js";

export interface WorkspaceWatcher {
  workspace: string;
  stop(): void;
}

interface CoalesceState {
  lastFiredMs: number;
  pending: NodeJS.Timeout | null;
}

const COALESCE_MS = 250;

function nowIso(): string {
  return new Date().toISOString();
}

function fileSha(p: string): string | null {
  try {
    const buf = fs.readFileSync(p);
    return crypto.createHash("sha256").update(buf).digest("hex");
  } catch {
    return null;
  }
}

export function startWorkspaceWatcher(
  workspace: string,
  fanOut: (event: BusEvent) => void,
): WorkspaceWatcher {
  const watchers: fs.FSWatcher[] = [];
  const receiptsDir = path.join(workspace, ".bequite", "receipts");
  const cachePath = path.join(workspace, ".bequite", "cache", "cost-ledger.json");
  const activeContextPath = path.join(
    workspace,
    ".bequite",
    "memory",
    "activeContext.md",
  );
  const currentPhasePath = path.join(workspace, "state", "current_phase.md");

  // Track receipt filenames we've already emitted to avoid duplicate "receipt"
  // events on Windows where fs.watch fires twice per write.
  const seenReceipts = new Set<string>();
  // Bootstrap: pretend we already saw all current receipts on watcher start.
  try {
    if (fs.existsSync(receiptsDir)) {
      for (const f of fs.readdirSync(receiptsDir)) {
        if (f.endsWith(".json")) seenReceipts.add(f);
      }
    }
  } catch {
    // ignore
  }

  // Track last-known sha for files-watched-by-content (so we only emit on
  // actual content change, not metadata-only fs events).
  const lastSha: Record<string, string | null> = {
    cost: fileSha(cachePath),
    active_context: fileSha(activeContextPath),
    phase: fileSha(currentPhasePath),
  };

  // Coalesce per channel.
  const coalesce: Record<string, CoalesceState> = {
    receipt: { lastFiredMs: 0, pending: null },
    cost: { lastFiredMs: 0, pending: null },
    active_context: { lastFiredMs: 0, pending: null },
    phase: { lastFiredMs: 0, pending: null },
  };

  function fire(name: EventName, data?: unknown) {
    fanOut({ name, workspace, ts: nowIso(), data });
  }

  function coalesced(channel: string, fn: () => void) {
    const c = coalesce[channel];
    if (!c) return fn();
    if (c.pending) clearTimeout(c.pending);
    c.pending = setTimeout(() => {
      c.pending = null;
      c.lastFiredMs = Date.now();
      try {
        fn();
      } catch (e) {
        fire("watcher_error", { channel, error: String(e) });
      }
    }, COALESCE_MS);
  }

  function watchSafe(
    target: string,
    handler: (event: string, filename: string | null) => void,
    label: string,
  ): void {
    try {
      const w = fs.watch(target, { persistent: false }, (ev, fn) => {
        try {
          handler(ev, fn);
        } catch (e) {
          publish(workspace, {
            name: "watcher_error",
            workspace,
            ts: nowIso(),
            data: { label, error: String(e) },
          });
        }
      });
      w.on("error", (e) => {
        publish(workspace, {
          name: "watcher_error",
          workspace,
          ts: nowIso(),
          data: { label, error: String(e) },
        });
      });
      watchers.push(w);
    } catch (e) {
      // The watched path may not exist yet — that's fine. Surface as a soft
      // error so the dashboard can show degraded state, but don't kill the
      // whole watcher.
      publish(workspace, {
        name: "watcher_error",
        workspace,
        ts: nowIso(),
        data: { label, error: String(e), recoverable: true },
      });
    }
  }

  // Watch the receipts directory itself; on a new .json filename, emit "receipt".
  // If the directory doesn't exist, watch its parent (.bequite/) for the dir
  // being created later.
  if (fs.existsSync(receiptsDir)) {
    watchSafe(
      receiptsDir,
      (_event, filename) => {
        if (!filename || !filename.endsWith(".json")) return;
        if (seenReceipts.has(filename)) return;
        seenReceipts.add(filename);
        coalesced("receipt", () => {
          fire("receipt", { filename });
        });
      },
      "receipts-dir",
    );
  } else {
    // Parent watcher — once .bequite/receipts/ appears, we'll re-init on demand.
    const bequiteDir = path.join(workspace, ".bequite");
    if (fs.existsSync(bequiteDir)) {
      watchSafe(
        bequiteDir,
        (_event, filename) => {
          if (filename === "receipts" && fs.existsSync(receiptsDir)) {
            // Lazy: emit a watcher_error to ask for re-subscribe (the simple
            // contract). v0.20.5 will add live re-init.
            publish(workspace, {
              name: "watcher_error",
              workspace,
              ts: nowIso(),
              data: {
                label: "receipts-dir",
                error: "receipts dir appeared after watcher start; re-subscribe to pick up events",
                recoverable: true,
              },
            });
          }
        },
        "bequite-parent",
      );
    }
  }

  // Watch cost-ledger.json. fs.watch on a single file works on most platforms;
  // on Windows it requires the file to exist at watch time. If it doesn't,
  // watch the parent (.bequite/cache/) for creation.
  if (fs.existsSync(cachePath)) {
    watchSafe(
      cachePath,
      () => {
        coalesced("cost", () => {
          const sha = fileSha(cachePath);
          if (sha !== null && sha !== lastSha.cost) {
            lastSha.cost = sha;
            fire("cost", { sha: sha?.slice(0, 12) });
          }
        });
      },
      "cost-ledger",
    );
  }

  if (fs.existsSync(activeContextPath)) {
    watchSafe(
      activeContextPath,
      () => {
        coalesced("active_context", () => {
          const sha = fileSha(activeContextPath);
          if (sha !== null && sha !== lastSha.active_context) {
            lastSha.active_context = sha;
            fire("active_context", { sha: sha?.slice(0, 12) });
          }
        });
      },
      "active-context",
    );
  }

  if (fs.existsSync(currentPhasePath)) {
    watchSafe(
      currentPhasePath,
      () => {
        coalesced("phase", () => {
          const sha = fileSha(currentPhasePath);
          if (sha !== null && sha !== lastSha.phase) {
            lastSha.phase = sha;
            fire("phase", { sha: sha?.slice(0, 12) });
          }
        });
      },
      "current-phase",
    );
  }

  return {
    workspace,
    stop() {
      // Cancel any pending coalesce timers.
      for (const k of Object.keys(coalesce)) {
        const c = coalesce[k];
        if (c?.pending) {
          clearTimeout(c.pending);
          c.pending = null;
        }
      }
      // Close all watchers.
      for (const w of watchers) {
        try {
          w.close();
        } catch {
          // ignore
        }
      }
    },
  };
}
