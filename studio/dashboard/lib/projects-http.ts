/**
 * HTTP-mode project loader (v2.0.0-alpha.1 candidate).
 *
 * Reads BeQuite-managed projects via `studio/api/` over HTTP instead of
 * direct filesystem access. Used by the dashboard when
 * `BEQUITE_DASHBOARD_MODE=http` is set.
 *
 * Same `ProjectSnapshot` shape as the filesystem reader — server components
 * get drop-in replacement. The HTTP reader degrades gracefully on API
 * unreachability: it returns a sentinel snapshot with `exists: false` and
 * `recoveryPreview` describing the failure (rather than throwing into the
 * server-component render path).
 */

import { StudioApiClient } from "./api-client";
import type { ProjectSnapshot } from "./projects-types";

const PHASES_ORDER = [
  { id: "P0", name: "Research" },
  { id: "P1", name: "Stack" },
  { id: "P2", name: "Plan" },
  { id: "P3", name: "Phases" },
  { id: "P4", name: "Tasks" },
  { id: "P5", name: "Implement" },
  { id: "P6", name: "Verify" },
  { id: "P7", name: "Handoff" },
];

function unreachableSnapshot(reason: string, rootHint: string): ProjectSnapshot {
  return {
    root: rootHint,
    exists: false,
    projectName: "(api unreachable)",
    doctrineList: [],
    constitutionVersion: "n/a",
    currentPhase: "n/a",
    lastGreenTag: null,
    activeContextSummary: "",
    phases: PHASES_ORDER.map((p) => ({ ...p, status: "pending" })),
    recentReceipts: [],
    costSession: null,
    recoveryPreview: `(HTTP mode — API unreachable: ${reason}. Set BEQUITE_DASHBOARD_MODE=filesystem to fall back, or start studio/api/.)`,
  };
}

export async function loadProjectHttp(
  rootDir?: string,
  apiBase?: string,
  apiToken?: string | null,
): Promise<ProjectSnapshot> {
  const client = new StudioApiClient({
    baseUrl: apiBase,
    token: apiToken,
    workspacePath: rootDir,
    cache: "no-store",
  });

  // Cheap reachability probe first — if the API is down, fail fast with a
  // sentinel snapshot instead of throwing into the server-component render.
  const reach = await client.getReachability();
  if (!reach.reachable) {
    return unreachableSnapshot(reach.error, rootDir ?? "<api workspace>");
  }

  try {
    return await client.getProjectSnapshot(rootDir);
  } catch (e) {
    return unreachableSnapshot(String(e), rootDir ?? "<api workspace>");
  }
}

export async function listProjectsHttp(
  apiBase?: string,
  apiToken?: string | null,
): Promise<{ name: string; path: string }[]> {
  const client = new StudioApiClient({
    baseUrl: apiBase,
    token: apiToken,
    cache: "no-store",
  });
  try {
    return await client.listProjects();
  } catch {
    return [];
  }
}
