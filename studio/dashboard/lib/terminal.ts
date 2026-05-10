/**
 * Terminal exec client (v0.20.5).
 *
 * Wraps the studio/api/ /api/v1/terminal/* surface for the dashboard's
 * xterm.js Terminal component. Two phases:
 *
 *   1. exec()   — POSTs the command to the API. Returns the session_id.
 *                  Sends X-BeQuite-RoE-Ack: ADR-016 (per ADR-016 §11).
 *   2. stream() — opens an EventSource against
 *                  /api/v1/terminal/sessions/:id/stream and yields
 *                  output lines + the terminal exit event.
 *
 * Both functions are CLIENT-side ("use client" components only). The token
 * (when API is in token mode) comes from NEXT_PUBLIC_BEQUITE_API_TOKEN. In
 * local-dev mode the auth header is omitted.
 */

"use client";

export interface ExecRequest {
  command: string;
  cwd?: string;
  timeout_seconds?: number;
  stdin?: string;
}

export interface ExecLine {
  channel: "stdout" | "stderr";
  text: string;
  ts: string;
}

export interface ExecSessionMeta {
  session_id: string;
  binary: string;
  args: string[];
  cwd: string;
  identity: string | null;
  started_at_utc: string;
  ended_at_utc: string | null;
  exit_code: number | null;
  exit_reason:
    | "running"
    | "clean"
    | "timeout"
    | "cancelled"
    | "error"
    | "killed";
  duration_ms: number | null;
  output_truncated: boolean;
  stdout_sha256: string | null;
  stderr_sha256: string | null;
  pid: number | null;
}

export interface ExecResponse {
  ok: boolean;
  session: ExecSessionMeta;
  receipt_path?: string;
  iron_law_x?: unknown;
  error?: string;
}

export interface TerminalClientOptions {
  apiBase?: string;
  apiToken?: string | null;
}

function defaultBase(): string {
  if (
    typeof process !== "undefined" &&
    process.env?.NEXT_PUBLIC_BEQUITE_API_BASE
  ) {
    return process.env.NEXT_PUBLIC_BEQUITE_API_BASE;
  }
  return "http://localhost:3002";
}

export async function execCommand(
  req: ExecRequest,
  opts: TerminalClientOptions = {},
): Promise<ExecResponse> {
  const apiBase = (opts.apiBase ?? defaultBase()).replace(/\/+$/, "");
  const headers: Record<string, string> = {
    "content-type": "application/json",
    accept: "application/json",
    "x-bequite-roe-ack": "ADR-016",
  };
  const token = opts.apiToken ?? null;
  if (token) headers["authorization"] = `Bearer ${token}`;

  const res = await fetch(apiBase + "/api/v1/terminal/exec", {
    method: "POST",
    headers,
    body: JSON.stringify(req),
  });

  let body: unknown = null;
  try {
    body = await res.json();
  } catch {
    body = null;
  }

  if (!res.ok) {
    const errorMsg =
      (body as { error?: string })?.error ?? `HTTP ${res.status}`;
    return {
      ok: false,
      session: {
        session_id: "",
        binary: "",
        args: [],
        cwd: "",
        identity: null,
        started_at_utc: new Date().toISOString(),
        ended_at_utc: new Date().toISOString(),
        exit_code: null,
        exit_reason: "error",
        duration_ms: 0,
        output_truncated: false,
        stdout_sha256: null,
        stderr_sha256: null,
        pid: null,
      },
      error: errorMsg,
    };
  }
  return body as ExecResponse;
}

export async function cancelCommand(
  sessionId: string,
  opts: TerminalClientOptions = {},
): Promise<{ ok: boolean }> {
  const apiBase = (opts.apiBase ?? defaultBase()).replace(/\/+$/, "");
  const headers: Record<string, string> = { accept: "application/json" };
  if (opts.apiToken) headers["authorization"] = `Bearer ${opts.apiToken}`;
  const res = await fetch(
    apiBase + `/api/v1/terminal/sessions/${encodeURIComponent(sessionId)}/cancel`,
    { method: "POST", headers },
  );
  return { ok: res.ok };
}

export interface StreamHandlers {
  onHello?: (meta: { session: ExecSessionMeta; replayed_lines: number }) => void;
  onLine?: (line: ExecLine) => void;
  onExit?: (session: ExecSessionMeta) => void;
  onError?: (err: Event | Error) => void;
  onHeartbeat?: () => void;
}

export interface StreamHandle {
  disconnect(): void;
}

export function streamSession(
  sessionId: string,
  handlers: StreamHandlers,
  opts: TerminalClientOptions = {},
): StreamHandle {
  const apiBase = (opts.apiBase ?? defaultBase()).replace(/\/+$/, "");
  const url = new URL(
    apiBase + `/api/v1/terminal/sessions/${encodeURIComponent(sessionId)}/stream`,
  );
  if (opts.apiToken) url.searchParams.set("token", opts.apiToken);

  const es = new EventSource(url.toString());

  es.addEventListener("hello", (ev) => {
    try {
      const data = JSON.parse((ev as MessageEvent).data);
      handlers.onHello?.(data);
    } catch (e) {
      handlers.onError?.(e as Error);
    }
  });
  es.addEventListener("line", (ev) => {
    try {
      const data = JSON.parse((ev as MessageEvent).data) as ExecLine;
      handlers.onLine?.(data);
    } catch (e) {
      handlers.onError?.(e as Error);
    }
  });
  es.addEventListener("exit", (ev) => {
    try {
      const data = JSON.parse((ev as MessageEvent).data);
      handlers.onExit?.(data.session as ExecSessionMeta);
    } catch (e) {
      handlers.onError?.(e as Error);
    }
    try {
      es.close();
    } catch {
      // ignore
    }
  });
  es.addEventListener("heartbeat", () => {
    handlers.onHeartbeat?.();
  });
  es.addEventListener("error", (ev) => {
    handlers.onError?.(ev);
  });

  return {
    disconnect() {
      try {
        es.close();
      } catch {
        // ignore
      }
    },
  };
}
