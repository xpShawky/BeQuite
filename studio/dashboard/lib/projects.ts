/**
 * Filesystem-based project loader (v0.18.0).
 *
 * v0.18.0 reads BeQuite-managed projects from the local filesystem (a project
 * is any directory with `.bequite/memory/constitution.md`). v0.19.0+ replaces
 * with HTTP calls to `studio/api/` for multi-user / cloud-synced operation.
 */

import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

// Default workspace = the BeQuite repo itself (the dashboard dogfoods)
const DEFAULT_WORKSPACE = path.resolve(process.cwd(), "..", "..");

export interface PhaseStatus {
  id: string; // P0..P7
  name: string;
  status: "done" | "in_progress" | "pending" | "blocked";
}

export interface ReceiptSummary {
  filename: string;
  phase: string;
  timestamp_utc: string;
  model: string;
  cost_usd: number;
  signed: boolean;
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
  costSession: { usd: number; tokens: number; calls: number } | null;
  recoveryPreview: string;
}

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
  // Take first non-empty heading + 2 following lines
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
  // Heuristic: parse "completed_phases" or count tags / current phase marker
  const completedMatch = recoveryMd.match(/Phases shipped:.*?(\d+)\s+tags?/i);
  // We don't have a deterministic mapping; mark all done if v0.16+ tag found, else heuristic
  const allDone = /v0\.1[5-9]\.|v0\.[2-9]/.test(currentPhase) || completedMatch !== null;
  return PHASES_ORDER.map((p) => ({
    ...p,
    status: allDone ? "done" : "pending",
  }));
}

export function loadProject(rootDir: string = DEFAULT_WORKSPACE): ProjectSnapshot {
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

  // Doctrines: look for active doctrines listed in project.yaml or activeContext
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

export function listKnownProjects(): { name: string; path: string }[] {
  // v0.18.0: just the current workspace. v0.19.0+ pulls from API + auth.
  return [
    {
      name: "BeQuite (this repo)",
      path: DEFAULT_WORKSPACE,
    },
  ];
}
