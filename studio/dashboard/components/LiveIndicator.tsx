"use client";

/**
 * LiveIndicator (v0.20.0).
 *
 * A small client component that opens an SSE stream against the studio/api/
 * `/api/v1/streams/all` endpoint and renders a status pill:
 *
 *   ● LIVE        — connected, heartbeat fresh
 *   ○ CONNECTING  — initial connection in progress
 *   ◐ STALE       — connected but no heartbeat in 60s
 *   ✕ OFFLINE     — error / API unreachable / closed
 *   —             — filesystem mode (no stream to open)
 *
 * Works with router.refresh() so receipt/cost/phase updates trigger a server-
 * component re-render of the dashboard. This is the operational completeness
 * piece for the dashboard side: the user sees changes WITHOUT manually
 * refreshing the page (Iron Law X — "did the user need to restart" answered
 * "no" by construction).
 */

import { useEffect, useRef, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { openStream, type StreamHandle } from "@/lib/streams";
import type { BusEvent, DashboardMode } from "@/lib/projects-types";

export interface LiveIndicatorProps {
  mode: DashboardMode;
  /** Workspace path to subscribe to. Optional — API uses its workspace root if omitted. */
  workspacePath?: string;
  /** API base URL — needed when mode === "http". */
  apiBase?: string;
  /** API token — needed when API runs in token mode. Pass via NEXT_PUBLIC_BEQUITE_API_TOKEN at build/deploy time. */
  apiToken?: string;
  /** Throttle router.refresh() calls — default 2 seconds. */
  refreshThrottleMs?: number;
}

type Status = "connecting" | "live" | "stale" | "offline" | "filesystem";

const REFRESH_THROTTLE_DEFAULT = 2_000;

export function LiveIndicator(props: LiveIndicatorProps) {
  const { mode, workspacePath, apiBase, apiToken } = props;
  const refreshThrottleMs = props.refreshThrottleMs ?? REFRESH_THROTTLE_DEFAULT;
  const router = useRouter();

  const [status, setStatus] = useState<Status>(
    mode === "filesystem" ? "filesystem" : "connecting",
  );
  const [lastEventName, setLastEventName] = useState<string | null>(null);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  const handleRef = useRef<StreamHandle | null>(null);
  const lastRefreshRef = useRef<number>(0);

  const throttledRefresh = useCallback(() => {
    const now = Date.now();
    if (now - lastRefreshRef.current >= refreshThrottleMs) {
      lastRefreshRef.current = now;
      router.refresh();
    }
  }, [router, refreshThrottleMs]);

  useEffect(() => {
    if (mode !== "http") {
      setStatus("filesystem");
      return;
    }
    setStatus("connecting");
    const handle = openStream({
      apiBase,
      workspacePath,
      apiToken: apiToken ?? null,
      filter: "all",
      onOpen: () => {
        setStatus("live");
      },
      onClose: () => {
        setStatus("offline");
      },
      onError: () => {
        setStatus("offline");
        setReconnectAttempts((n) => n + 1);
      },
      onStale: () => {
        setStatus("stale");
      },
      onEvent: (e: BusEvent) => {
        setLastEventName(e.name);
        // Trigger a server-component re-render on state-changing events.
        // Heartbeat / hello are noise — skip them.
        if (
          e.name === "receipt" ||
          e.name === "cost" ||
          e.name === "phase" ||
          e.name === "active_context"
        ) {
          throttledRefresh();
        }
      },
    });
    handleRef.current = handle;
    return () => {
      handle.disconnect();
      handleRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, apiBase, workspacePath, apiToken]);

  // Visual treatment per status.
  const styles: Record<Status, { dot: string; label: string; text: string }> = {
    connecting: {
      dot: "bg-silver-dim animate-pulse",
      label: "CONNECTING",
      text: "text-silver",
    },
    live: {
      dot: "bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.6)] animate-pulse",
      label: "LIVE",
      text: "text-green-300",
    },
    stale: {
      dot: "bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.6)]",
      label: "STALE",
      text: "text-amber-300",
    },
    offline: {
      dot: "bg-red-500",
      label: "OFFLINE",
      text: "text-red-400",
    },
    filesystem: {
      dot: "bg-ink-edge",
      label: "FS",
      text: "text-silver-dim",
    },
  };

  const s = styles[status];
  const titleParts = [
    `mode: ${mode}`,
    `status: ${status}`,
    lastEventName ? `last event: ${lastEventName}` : null,
    reconnectAttempts > 0 ? `reconnects: ${reconnectAttempts}` : null,
  ].filter(Boolean);

  return (
    <div
      className="inline-flex items-center gap-1.5 rounded border border-ink-edge px-2 py-1 font-mono text-[10px] uppercase tracking-wider"
      title={titleParts.join(" · ")}
      data-testid="live-indicator"
    >
      <span className={`h-1.5 w-1.5 rounded-full ${s.dot}`} />
      <span className={s.text}>{s.label}</span>
    </div>
  );
}
