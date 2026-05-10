/**
 * HTTP client for the BeQuite Studio API (v2.0.0-alpha.1 candidate).
 *
 * Talks to `studio/api/` (Hono on Bun, default :3002). Used by the dashboard
 * when `BEQUITE_DASHBOARD_MODE=http` is set; otherwise the dashboard reads
 * the filesystem directly via `lib/projects.ts::loadProjectFilesystem`.
 *
 * Auth: sends `Authorization: Bearer <BEQUITE_API_TOKEN>` when present.
 * Without a token, requests work against an API running in local-dev mode.
 *
 * All endpoints are server-side from the dashboard's perspective (Next.js
 * server components fetch them at request time). Path traversal is enforced
 * by the API; the client passes `?path=` through.
 */

import type {
  PhaseStatus,
  ProjectSnapshot,
  ReceiptSummary,
} from "./projects-types";

export interface ApiClientOptions {
  baseUrl?: string;
  token?: string | null;
  /** Forwarded to the API as ?path=<workspace>. Defaults to API's workspace root. */
  workspacePath?: string;
  /** Cache hint for Next.js's fetch — "no-store" for live data; revalidate seconds for SSG-like behavior. */
  cache?: RequestCache;
  next?: { revalidate?: number; tags?: string[] };
}

export class StudioApiClient {
  private baseUrl: string;
  private token: string | null;
  private workspacePath?: string;
  private cache: RequestCache;
  private next?: { revalidate?: number; tags?: string[] };

  constructor(opts: ApiClientOptions = {}) {
    this.baseUrl = (
      opts.baseUrl ||
      process.env.BEQUITE_API_BASE ||
      "http://localhost:3002"
    ).replace(/\/+$/, "");
    this.token =
      opts.token === undefined
        ? process.env.BEQUITE_API_TOKEN || null
        : opts.token;
    this.workspacePath = opts.workspacePath;
    this.cache = opts.cache ?? "no-store";
    this.next = opts.next;
  }

  private headers(extra: Record<string, string> = {}): Record<string, string> {
    const h: Record<string, string> = {
      accept: "application/json",
      ...extra,
    };
    if (this.token) h["authorization"] = `Bearer ${this.token}`;
    return h;
  }

  private async getJson<T>(pathname: string, params?: URLSearchParams): Promise<T> {
    const url = new URL(this.baseUrl + pathname);
    if (this.workspacePath) url.searchParams.set("path", this.workspacePath);
    if (params) {
      for (const [k, v] of params.entries()) url.searchParams.set(k, v);
    }
    const res = await fetch(url.toString(), {
      method: "GET",
      headers: this.headers(),
      cache: this.cache,
      next: this.next,
    });
    if (!res.ok) {
      throw new ApiError(
        `GET ${url.pathname} → ${res.status} ${res.statusText}`,
        res.status,
        await safeJson(res),
      );
    }
    return (await res.json()) as T;
  }

  async getHealth(): Promise<{ status: string; version: string; uptime_s: number; workspace_root: string }> {
    return this.getJson("/healthz");
  }

  async getAuthStatus(): Promise<{
    mode: "local-dev" | "token" | "device-code";
    identity: string | null;
    token_id: string | null;
    tokens_count: number | null;
    notes: string;
  }> {
    return this.getJson("/api/v1/auth/status");
  }

  async listProjects(): Promise<Array<{ name: string; path: string }>> {
    const r = await this.getJson<{ items: Array<{ name: string; path: string }> }>(
      "/api/v1/projects",
    );
    return r.items;
  }

  async getProjectSnapshot(path?: string): Promise<ProjectSnapshot> {
    const params = new URLSearchParams();
    if (path) params.set("path", path);
    return this.getJson("/api/v1/projects/snapshot", params);
  }

  async listReceipts(path?: string): Promise<{ items: ReceiptSummary[] }> {
    const params = new URLSearchParams();
    if (path) params.set("path", path);
    return this.getJson("/api/v1/receipts", params);
  }

  async getReceipt(sha: string, path?: string): Promise<Record<string, unknown>> {
    if (!/^[a-f0-9]{8,64}$/i.test(sha)) {
      throw new Error("invalid sha (8-64 hex chars required)");
    }
    const params = new URLSearchParams();
    if (path) params.set("path", path);
    return this.getJson(`/api/v1/receipts/${sha}`, params);
  }

  async getReachability(): Promise<
    | { reachable: true; version: string; workspace_root: string; auth_mode: string }
    | { reachable: false; error: string }
  > {
    try {
      const health = await this.getHealth();
      const auth = await this.getAuthStatus();
      return {
        reachable: true,
        version: health.version,
        workspace_root: health.workspace_root,
        auth_mode: auth.mode,
      };
    } catch (e) {
      return { reachable: false, error: String(e) };
    }
  }
}

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(msg: string, status: number, body: unknown) {
    super(msg);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

async function safeJson(res: Response): Promise<unknown> {
  try {
    return await res.json();
  } catch {
    return null;
  }
}

// PhaseStatus type re-export for callers that only need the API client.
export type { PhaseStatus };
