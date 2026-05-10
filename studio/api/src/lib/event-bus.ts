/**
 * Per-workspace event bus (v0.20.0).
 *
 * Reference-counted. Each call to `subscribe(workspace, listener)` increments
 * the ref count for that workspace; the first subscribe lazily starts a
 * filesystem watcher (see `file-watcher.ts`); the last unsubscribe tears it
 * down. This keeps idle workspaces from holding watcher resources.
 *
 * Iron Law X reminder: streams DON'T write state, but they DO promise to
 * deliver every event. Article VI honest reporting: when the watcher errors,
 * the bus emits a `watcher_error` event so the SSE consumer can surface it
 * (rather than the stream silently going dead).
 */

import type { WorkspaceWatcher } from "./file-watcher.js";

export type EventName =
  | "receipt"        // a new receipt JSON file appeared in .bequite/receipts/
  | "cost"           // .bequite/cache/cost-ledger.json changed
  | "phase"          // state/current_phase.md changed
  | "active_context" // .bequite/memory/activeContext.md changed
  | "watcher_error"  // the underlying fs.watch errored
  | "watcher_started" // emitted on first subscriber
  | "watcher_stopped"; // emitted on last unsubscriber

export interface BusEvent {
  name: EventName;
  workspace: string;
  /** ISO 8601 UTC. */
  ts: string;
  /** Free-form payload — receipt filename, cost-ledger snapshot hash, etc. */
  data?: unknown;
}

type Listener = (e: BusEvent) => void;

interface Channel {
  workspace: string;
  refs: number;
  listeners: Set<Listener>;
  watcher: WorkspaceWatcher | null;
}

const channels: Map<string, Channel> = new Map();

/** For tests + lazy-init guard. */
export function _channels(): ReadonlyMap<string, Channel> {
  return channels;
}

/**
 * Subscribe to events for a workspace. First subscriber starts the watcher.
 * Returns an unsubscribe function.
 */
export async function subscribe(
  workspace: string,
  listener: Listener,
): Promise<() => void> {
  const norm = workspace.replace(/\\+/g, "/");
  let ch = channels.get(norm);
  if (!ch) {
    ch = {
      workspace: norm,
      refs: 0,
      listeners: new Set(),
      watcher: null,
    };
    channels.set(norm, ch);
  }
  ch.listeners.add(listener);
  ch.refs += 1;

  if (ch.refs === 1) {
    // First subscriber — start the watcher.
    const { startWorkspaceWatcher } = await import("./file-watcher.js");
    ch.watcher = startWorkspaceWatcher(norm, (busEvent) => {
      // Re-broadcast to all listeners on this channel.
      for (const l of ch!.listeners) {
        try {
          l(busEvent);
        } catch (e) {
          // A misbehaving listener can't take down the whole bus.
          console.error("[event-bus] listener threw:", e);
        }
      }
    });
    publish(norm, {
      name: "watcher_started",
      workspace: norm,
      ts: new Date().toISOString(),
    });
  }

  return function unsubscribe() {
    if (!ch) return;
    ch.listeners.delete(listener);
    ch.refs -= 1;
    if (ch.refs <= 0 && ch.watcher) {
      // Last unsubscribe — tear down.
      try {
        ch.watcher.stop();
      } catch {
        // ignore — best-effort
      }
      ch.watcher = null;
      channels.delete(norm);
      publish(norm, {
        name: "watcher_stopped",
        workspace: norm,
        ts: new Date().toISOString(),
      });
    }
  };
}

/** Direct publish — used by file-watcher to fan events into the bus. */
export function publish(workspace: string, event: BusEvent): void {
  const norm = workspace.replace(/\\+/g, "/");
  const ch = channels.get(norm);
  if (!ch) return; // No subscribers; drop on the floor.
  for (const l of ch.listeners) {
    try {
      l(event);
    } catch (e) {
      console.error("[event-bus] listener threw on publish:", e);
    }
  }
}
