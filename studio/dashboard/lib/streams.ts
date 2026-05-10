/**
 * Client-side SSE stream wrapper (v0.20.0).
 *
 * Browser EventSource doesn't support custom headers (so we can't send
 * Authorization: Bearer ... directly). For token-mode APIs we pass the token
 * as ?token=<hex> query param — the API accepts it on /api/v1/streams/* as
 * an alternative to the Authorization header for SSE consumers.
 *
 * In local-dev mode, the EventSource opens without any auth.
 *
 * The wrapper:
 *   - reconnects on transient failure (exponential backoff capped at 30s)
 *   - exposes connected / disconnected / error status
 *   - tracks last heartbeat and surfaces "stale" when no heartbeat for 60s
 *   - returns a `disconnect()` cleanup function
 */

"use client";

import type { BusEvent } from "./projects-types";

export interface StreamOptions {
  /** API base URL. Default: BEQUITE_API_BASE env or http://localhost:3002 */
  apiBase?: string;
  /** Workspace path. Default: API decides (its own workspace root). */
  workspacePath?: string;
  /** Bearer token for token-mode APIs. Omit in local-dev. */
  apiToken?: string | null;
  /** Stream filter. Default: "all". */
  filter?: "all" | "receipts" | "cost" | "phase";
  /** Called on every parsed event. */
  onEvent?: (event: BusEvent) => void;
  /** Called when the stream connects (or reconnects). */
  onOpen?: () => void;
  /** Called when the stream disconnects. */
  onClose?: () => void;
  /** Called on transport error. */
  onError?: (err: Event | Error) => void;
  /** Called when the heartbeat is stale (no event received in HEARTBEAT_STALE_MS). */
  onStale?: () => void;
}

export interface StreamHandle {
  disconnect(): void;
  /** Snapshot status for the UI. */
  status(): {
    state: "connecting" | "open" | "closed" | "error" | "stale";
    last_event_ts: string | null;
    last_heartbeat_ts: string | null;
    reconnect_attempts: number;
  };
}

const HEARTBEAT_STALE_MS = 60_000;
const RECONNECT_BASE_MS = 1_000;
const RECONNECT_MAX_MS = 30_000;

function defaultBase(): string {
  // The bundler swaps NEXT_PUBLIC_* vars at build time; runtime env not visible.
  // For now, this lib is used in client components — we read process.env via Next's
  // public-env mechanism. The dashboard is expected to set NEXT_PUBLIC_BEQUITE_API_BASE
  // when in HTTP mode.
  if (typeof process !== "undefined" && process.env?.NEXT_PUBLIC_BEQUITE_API_BASE) {
    return process.env.NEXT_PUBLIC_BEQUITE_API_BASE;
  }
  return "http://localhost:3002";
}

export function openStream(opts: StreamOptions = {}): StreamHandle {
  const apiBase = (opts.apiBase ?? defaultBase()).replace(/\/+$/, "");
  const filter = opts.filter ?? "all";
  const route = `/api/v1/streams/${filter}`;

  let es: EventSource | null = null;
  let state: "connecting" | "open" | "closed" | "error" | "stale" = "connecting";
  let reconnectAttempts = 0;
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  let staleTimer: ReturnType<typeof setTimeout> | null = null;
  let lastEventTs: string | null = null;
  let lastHeartbeatTs: string | null = null;
  let disposed = false;

  function buildUrl(): string {
    const url = new URL(apiBase + route);
    if (opts.workspacePath) url.searchParams.set("path", opts.workspacePath);
    if (opts.apiToken) url.searchParams.set("token", opts.apiToken);
    return url.toString();
  }

  function resetStaleTimer() {
    if (staleTimer) clearTimeout(staleTimer);
    staleTimer = setTimeout(() => {
      state = "stale";
      opts.onStale?.();
    }, HEARTBEAT_STALE_MS);
  }

  function scheduleReconnect() {
    if (disposed) return;
    if (reconnectTimer) clearTimeout(reconnectTimer);
    const delay = Math.min(
      RECONNECT_BASE_MS * Math.pow(2, reconnectAttempts),
      RECONNECT_MAX_MS,
    );
    reconnectAttempts += 1;
    reconnectTimer = setTimeout(connect, delay);
  }

  function connect() {
    if (disposed) return;
    state = "connecting";
    es = new EventSource(buildUrl());

    es.addEventListener("open", () => {
      if (disposed) return;
      state = "open";
      reconnectAttempts = 0;
      lastHeartbeatTs = new Date().toISOString();
      resetStaleTimer();
      opts.onOpen?.();
    });

    // Generic message — hello + heartbeat + named events all flow here.
    es.addEventListener("message", (ev) => {
      handleEvent("message", ev);
    });

    // Named events. We listen to the names the server sends.
    for (const name of [
      "hello",
      "heartbeat",
      "receipt",
      "cost",
      "phase",
      "active_context",
      "watcher_error",
      "watcher_started",
      "watcher_stopped",
    ] as const) {
      es.addEventListener(name, (ev) => {
        handleEvent(name, ev as MessageEvent);
      });
    }

    es.addEventListener("error", (ev) => {
      if (disposed) return;
      state = "error";
      opts.onError?.(ev);
      try {
        es?.close();
      } catch {
        // ignore
      }
      es = null;
      scheduleReconnect();
    });
  }

  function handleEvent(name: string, ev: MessageEvent) {
    if (disposed) return;
    const ts = new Date().toISOString();
    lastEventTs = ts;
    if (name === "heartbeat" || name === "hello") {
      lastHeartbeatTs = ts;
    }
    resetStaleTimer();

    let parsed: BusEvent | null = null;
    try {
      const obj = JSON.parse(ev.data);
      // Server sends `{ name, workspace, ts, data }` from the bus, plus
      // hello/heartbeat with their own shapes. Normalize:
      if (obj && typeof obj === "object") {
        parsed = {
          name: (obj.name ?? name) as BusEvent["name"],
          workspace: obj.workspace ?? "",
          ts: obj.ts ?? ts,
          data: obj.data ?? obj,
        };
      }
    } catch {
      // Non-JSON event payload — surface as a watcher_error.
      parsed = {
        name: "watcher_error",
        workspace: "",
        ts,
        data: { error: "non-JSON SSE payload", raw: ev.data?.slice?.(0, 200) },
      };
    }
    if (parsed) {
      opts.onEvent?.(parsed);
    }
  }

  connect();

  return {
    disconnect() {
      disposed = true;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (staleTimer) clearTimeout(staleTimer);
      try {
        es?.close();
      } catch {
        // ignore
      }
      es = null;
      state = "closed";
      opts.onClose?.();
    },
    status() {
      return {
        state,
        last_event_ts: lastEventTs,
        last_heartbeat_ts: lastHeartbeatTs,
        reconnect_attempts: reconnectAttempts,
      };
    },
  };
}
