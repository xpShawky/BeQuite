/**
 * Filesystem-mode project loader (v0.18.0 → preserved in v2.0.0-alpha.1).
 *
 * Reads BeQuite-managed projects directly from the local filesystem. Used by
 * the dashboard when `BEQUITE_DASHBOARD_MODE=filesystem` (or unset, default).
 *
 * v2.0.0-alpha.1 introduces `lib/projects-http.ts` as the alternative reader
 * that talks to `studio/api/` over HTTP. The two readers share the same
 * `ProjectSnapshot` shape (in `lib/projects-types.ts`), so the swap is
 * drop-in for server components.
 *
 * NOTE: This file is identical in behavior to the original v0.18.0
 * `lib/projects.ts`. It was moved here so `lib/projects.ts` can dispatch
 * between filesystem and HTTP modes.
 */

import fs from "node:fs";
import path from "node:path";
import type {
  PhaseStatus,
  ProjectSnapshot,
  ReceiptSummary,
} from "./projects-types.js";

// Default workspace = the BeQuite repo itself (the dashboard dogfoods)
const DEFAULT_WORKSPACE = path.resolve(process.cwd(), "..", "..");

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

function safeRead(p: string, fallback = ""): string {
  try {
    return fs.readFileSync(p, "utf8");
  } catch {
    return fallback;
  }
}

function safeStat(p: string): fs.Stats | null {
  try {
    return fs.statSync(p);
  } catch {
    return null;
  }
}

function safeReadDir(p: string): string[] {
  try {
    return fs.readdirSync(p);
  } catch {
    return [];
  }
}

function extractConstVersion(constitutionMd: string): string {
  const m = constitutionMd.match(/Constitution v(\d+\.\d+\.\d+)/);
  return m?.[1] ?? "unknown";
}

function extractCurrentPhase(currentPhaseMd: string): string {
  const m =
    currentPhaseMd.match(/Sub-version:\s*Just tagged\s*`?v?([0-9.]+)`?/i) ??
    currentPhaseMd.match(/Last green sub-version:\s*`?v?([0-9.]+)`?/i);
  return m?.[1] ? `v${m[1]}` : "(unknown)";
}

function parseRecovery(md: string): { lastGreenTag: string | null; summary: string } {
  const tagMatch =
    md.match(/Last successful tag.*:\s*\*\*v?([0-9.]+)/i) ??
    md.match(/Last green sub-version:\s*\*\*v?([0-9.]+)/i);
  const lines = md.split("\n").map((l) => l.trim()).filter(Boolean).slice(0, 6);
  return {
    lastGreenTag: tagMatch?.[1] ? `v${tagMatch[1]}` : null,
    summary: lines.join("\n"),
  };
}

function loadReceipts(rootDir: string): ReceiptSummary[] {
  const dir = path.join(rootDir, ".bequite", "receipts");
  const files = safeReadDir(dir).filter((f) => f.endsWith(".json"));
  const out: ReceiptSummary[] = [];
  for (const f of files.slice(0, 20)) {
    try {
      const raw = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
      out.push({
        filename: f,
        phase: raw.phase ?? "?",
        timestamp_utc: raw.timestamp_utc ?? "",
        model: raw.model?.name ?? "?",
        cost_usd: raw.cost?.usd ?? 0,
        signed: !!raw.signature,
      });
    } catch {
      // skip malformed
    }
  }
  return out.sort((a, b) => (a.timestamp_utc < b.timestamp_utc ? 1 : -1)).slice(0, 10);
}

function loadCostLedger(rootDir: string): ProjectSnapshot["costSession"] {
  const p = path.join(rootDir, ".bequite", "cache", "cost-ledger.json");
  if (!safeStat(p)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(p, "utf8"));
    return {
      usd: data.session_total_usd ?? 0,
      tokens: data.session_total_tokens ?? 0,
      calls: data.calls_this_session ?? 0,
    };
  } catch {
    return null;
  }
}

function inferPhaseStatuses(currentPhase: string, recoveryMd: string): PhaseStatus[] {
  const completedMatch = recoveryMd.match(/Phases shipped:.*?(\d+)\s+tags?/i);
  const allDone = /v0\.1[5-9]\.|v0\.[2-9]/.test(currentPhase) || completedMatch !== null;
  return PHASES_ORDER.map((p) => ({
    ...p,
    status: allDone ? "done" : "pending",
  }));
}

export function loadProjectFilesystem(
  rootDir: string = DEFAULT_WORKSPACE,
): ProjectSnapshot {
  const memDir = path.join(rootDir, ".bequite", "memory");
  const constitutionPath = path.join(memDir, "constitution.md");
  const exists = !!safeStat(constitutionPath);

  if (!exists) {
    return {
      root: rootDir,
      exists: false,
      projectName: path.basename(rootDir),
      doctrineList: [],
      constitutionVersion: "n/a",
      currentPhase: "n/a",
      lastGreenTag: null,
      activeContextSummary: "",
      phases: PHASES_ORDER.map((p) => ({ ...p, status: "pending" })),
      recentReceipts: [],
      costSession: null,
      recoveryPreview: "(no project found at this path)",
    };
  }

  const constitution = safeRead(constitutionPath);
  const projectbrief = safeRead(path.join(memDir, "projectbrief.md"));
  const projectName = projectbrief.match(/^#\s+(.+)$/m)?.[1] ?? path.basename(rootDir);

  const constitutionVersion = extractConstVersion(constitution);

  const currentPhaseMd = safeRead(path.join(rootDir, "state", "current_phase.md"));
  const currentPhase = extractCurrentPhase(currentPhaseMd);

  const recoveryMd = safeRead(path.join(rootDir, "state", "recovery.md"));
  const { lastGreenTag, summary: recoveryPreview } = parseRecovery(recoveryMd);

  const activeContext = safeRead(path.join(memDir, "activeContext.md"));
  const activeContextSummary =
    activeContext
      .split("\n")
      .filter((l) => l.trim() && !l.startsWith("#") && !l.startsWith(">"))
      .slice(0, 4)
      .join(" · ") || "(no active context)";

  const doctrineMatches =
    activeContext.match(/Active doctrines.*?:\s*([^\n]+)/i)?.[1]
      ?.split(/[,/]/)
      .map((s) => s.trim().replace(/[`*_]/g, ""))
      .filter((s) => s.length > 0 && s.length < 50)
      .slice(0, 6) ?? [];

  const receipts = loadReceipts(rootDir);
  const costSession = loadCostLedger(rootDir);
  const phases = inferPhaseStatuses(currentPhase, recoveryMd);

  return {
    root: rootDir,
    exists: true,
    projectName,
    doctrineList: doctrineMatches,
    constitutionVersion,
    currentPhase,
    lastGreenTag,
    activeContextSummary,
    phases,
    recentReceipts: receipts,
    costSession,
    recoveryPreview,
  };
}

export function listProjectsFilesystem(): { name: string; path: string }[] {
  return [
    {
      name: "BeQuite (this repo)",
      path: DEFAULT_WORKSPACE,
    },
  ];
}

export const DEFAULT_FILESYSTEM_WORKSPACE = DEFAULT_WORKSPACE;
