/**
 * Shared types for the BeQuite Studio dashboard's project loaders.
 *
 * Used by:
 *   - lib/projects.ts             (the dual-mode entry; v2.0.0-alpha.1 candidate)
 *   - lib/projects-filesystem.ts  (v0.18.0 filesystem-mode reader)
 *   - lib/projects-http.ts        (v2.0.0-alpha.1 HTTP-mode reader)
 *   - lib/api-client.ts           (HTTP client)
 *
 * Keeping the shape stable across modes is what makes the swap drop-in:
 * server components import from `lib/projects` and the implementation
 * picks the right reader based on `BEQUITE_DASHBOARD_MODE`.
 */

export type PhaseId = "P0" | "P1" | "P2" | "P3" | "P4" | "P5" | "P6" | "P7";

export type PhaseStatusValue = "done" | "in_progress" | "pending" | "blocked";

export interface PhaseStatus {
  id: string;
  name: string;
  status: PhaseStatusValue;
}

export interface ReceiptSummary {
  filename: string;
  phase: string;
  timestamp_utc: string;
  model: string;
  cost_usd: number;
  signed: boolean;
}

export interface CostSession {
  usd: number;
  tokens: number;
  calls: number;
}

export interface ProjectSnapshot {
  root: string;
  exists: boolean;
  projectName: string;
  doctrineList: string[];
  constitutionVersion: string;
  currentPhase: string;
  lastGreenTag: string | null;
  activeContextSummary: string;
  phases: PhaseStatus[];
  recentReceipts: ReceiptSummary[];
  costSession: CostSession | null;
  recoveryPreview: string;
}

export type DashboardMode = "filesystem" | "http";

export interface LoaderConfig {
  mode: DashboardMode;
  /** When mode === "http", base URL of the API. Default: http://localhost:3002 */
  apiBase?: string;
  /** When mode === "http" and API in token mode. */
  apiToken?: string | null;
  /** Workspace path to scope reads. Both modes support it. */
  workspacePath?: string;
}

/**
 * Event shape from the SSE stream (`/api/v1/streams/*`). Mirrors the API's
 * `BusEvent` type from `studio/api/src/lib/event-bus.ts` — kept in sync by
 * convention. v0.20.0+ adds richer payload typing as event consumers grow.
 */
export type StreamEventName =
  | "hello"
  | "heartbeat"
  | "receipt"
  | "cost"
  | "phase"
  | "active_context"
  | "watcher_error"
  | "watcher_started"
  | "watcher_stopped";

export interface BusEvent {
  name: StreamEventName;
  workspace: string;
  ts: string;
  data?: unknown;
}
