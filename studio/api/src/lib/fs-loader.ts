/**
 * Filesystem-backed project loader for the Hono API (v0.19.0).
 *
 * Mirrors studio/dashboard/lib/projects.ts but with HTTP-friendly shape +
 * stricter path validation (refuses paths outside an allow-list root).
 */

import fs from "node:fs";
import path from "node:path";
import type { PhaseStatus, ProjectSnapshot, ReceiptSummary } from "../schemas.js";

// Allow-list: only paths under this root are readable. Configurable via env.
const WORKSPACE_ROOT = path.resolve(
  process.env.BEQUITE_WORKSPACE_ROOT || path.join(process.cwd(), "..", ".."),
);

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

function isPathSafe(p: string): boolean {
  const resolved = path.resolve(p);
  return resolved === WORKSPACE_ROOT || resolved.startsWith(WORKSPACE_ROOT + path.sep);
}

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

function extractConstVersion(md: string): string {
  return md.match(/Constitution v(\d+\.\d+\.\d+)/)?.[1] ?? "unknown";
}

function extractCurrentPhase(md: string): string {
  const m =
    md.match(/Just tagged\s*`?v?([0-9.]+)`?/i) ??
    md.match(/Last green sub-version:\s*`?v?([0-9.]+)`?/i);
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
  for (const f of files.slice(0, 50)) {
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

function inferPhaseStatuses(currentPhase: string): PhaseStatus[] {
  const allDone = /v0\.1[6-9]\.|v0\.[2-9]/.test(currentPhase);
  return PHASES_ORDER.map((p) => ({
    ...p,
    status: allDone ? "done" : "pending",
  }));
}

export function loadProject(rootDir: string = WORKSPACE_ROOT): ProjectSnapshot {
  // Path traversal guard
  if (!isPathSafe(rootDir)) {
    return {
      root: rootDir,
      exists: false,
      projectName: "(refused — path outside workspace root)",
      doctrineList: [],
      constitutionVersion: "n/a",
      currentPhase: "n/a",
      lastGreenTag: null,
      activeContextSummary: "",
      phases: PHASES_ORDER.map((p) => ({ ...p, status: "pending" })),
      recentReceipts: [],
      costSession: null,
      recoveryPreview: `(refused — path ${rootDir} is outside workspace root ${WORKSPACE_ROOT})`,
    };
  }

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
      recoveryPreview: "(no project at this path)",
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

  return {
    root: rootDir,
    exists: true,
    projectName,
    doctrineList: doctrineMatches,
    constitutionVersion,
    currentPhase,
    lastGreenTag,
    activeContextSummary,
    phases: inferPhaseStatuses(currentPhase),
    recentReceipts: loadReceipts(rootDir),
    costSession: loadCostLedger(rootDir),
    recoveryPreview,
  };
}

export function listProjects(): { name: string; path: string }[] {
  // v0.19.0: workspace root + any first-level subdirs containing .bequite/memory/
  const out: { name: string; path: string }[] = [];
  // First the root itself if it's a project
  if (safeStat(path.join(WORKSPACE_ROOT, ".bequite", "memory", "constitution.md"))) {
    out.push({ name: path.basename(WORKSPACE_ROOT) + " (root)", path: WORKSPACE_ROOT });
  }
  for (const entry of safeReadDir(WORKSPACE_ROOT)) {
    const sub = path.join(WORKSPACE_ROOT, entry);
    if (!safeStat(sub)?.isDirectory()) continue;
    if (safeStat(path.join(sub, ".bequite", "memory", "constitution.md"))) {
      out.push({ name: entry, path: sub });
    }
  }
  return out;
}

export function getWorkspaceRoot(): string {
  return WORKSPACE_ROOT;
}
