/**
 * Project loader entry point — dual-mode dispatcher (v2.0.0-alpha.1 candidate).
 *
 * Server components import `loadProject` from here. Implementation picks
 * filesystem OR HTTP mode based on env:
 *
 *   BEQUITE_DASHBOARD_MODE=filesystem  (default) — direct filesystem reads
 *                                                  via lib/projects-filesystem
 *   BEQUITE_DASHBOARD_MODE=http                  — HTTP fetch to studio/api/
 *                                                  via lib/projects-http
 *
 * Additional env knobs (HTTP mode only):
 *
 *   BEQUITE_API_BASE   — default http://localhost:3002
 *   BEQUITE_API_TOKEN  — Bearer token if API is in token mode (else omit)
 *
 * Server components should `await loadProject(path?)` — the return type is
 * the same whether the underlying mode is filesystem or HTTP. This is the
 * seam that v2.0.0-alpha.1 enables without rewriting every consumer.
 *
 * Re-exports the canonical types so consumers can import them from this
 * single module (`import { ProjectSnapshot, loadProject } from "@/lib/projects"`).
 */

import {
  loadProjectFilesystem,
  listProjectsFilesystem,
} from "./projects-filesystem";
import { loadProjectHttp, listProjectsHttp } from "./projects-http";
import type {
  ProjectSnapshot,
  PhaseStatus,
  ReceiptSummary,
  DashboardMode,
} from "./projects-types";

export type {
  ProjectSnapshot,
  PhaseStatus,
  ReceiptSummary,
  DashboardMode,
} from "./projects-types";

function getDashboardMode(): DashboardMode {
  const raw = (process.env.BEQUITE_DASHBOARD_MODE || "filesystem").toLowerCase();
  return raw === "http" ? "http" : "filesystem";
}

/**
 * Load a single project snapshot. Mode-aware:
 *   - filesystem (default): synchronous filesystem read (returns Promise for API parity)
 *   - http: fetch against studio/api/
 *
 * Server components should always `await` this — even in filesystem mode the
 * signature returns a Promise to keep the swap transparent.
 */
export async function loadProject(rootDir?: string): Promise<ProjectSnapshot> {
  const mode = getDashboardMode();
  if (mode === "http") {
    return loadProjectHttp(
      rootDir,
      process.env.BEQUITE_API_BASE,
      process.env.BEQUITE_API_TOKEN || null,
    );
  }
  return Promise.resolve(loadProjectFilesystem(rootDir));
}

/**
 * Backwards-compatible synchronous filesystem-mode loader. Kept for any
 * pre-v2.0.0-alpha.1 server-component callsites that don't yet await.
 * Always reads the filesystem regardless of `BEQUITE_DASHBOARD_MODE` —
 * use `loadProject` (async) for mode-aware loading.
 *
 * @deprecated since v2.0.0-alpha.1 — prefer `await loadProject(rootDir)`.
 */
export function loadProjectSync(rootDir?: string): ProjectSnapshot {
  return loadProjectFilesystem(rootDir);
}

export async function listKnownProjects(): Promise<{ name: string; path: string }[]> {
  const mode = getDashboardMode();
  if (mode === "http") {
    return listProjectsHttp(
      process.env.BEQUITE_API_BASE,
      process.env.BEQUITE_API_TOKEN || null,
    );
  }
  return Promise.resolve(listProjectsFilesystem());
}

/**
 * Surface the current loader configuration so the dashboard can show a
 * "filesystem mode" / "HTTP mode (api: ...)" badge in the TopBar.
 */
export function getLoaderConfig(): {
  mode: DashboardMode;
  apiBase: string | null;
  hasToken: boolean;
} {
  const mode = getDashboardMode();
  if (mode === "http") {
    return {
      mode,
      apiBase: process.env.BEQUITE_API_BASE || "http://localhost:3002",
      hasToken: !!process.env.BEQUITE_API_TOKEN,
    };
  }
  return { mode, apiBase: null, hasToken: false };
}
