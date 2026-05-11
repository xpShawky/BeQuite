import { TopBar } from "@/components/TopBar";
import { PhasesSidebar } from "@/components/PhasesSidebar";
import { CommandConsole } from "@/components/CommandConsole";
import { Terminal } from "@/components/Terminal";
import { PlanTasksTests } from "@/components/PlanTasksTests";
import { AgentPanel } from "@/components/AgentPanel";
import { ReceiptsList } from "@/components/ReceiptsList";
import { loadProject, getLoaderConfig } from "@/lib/projects";

// v2.0.0-alpha.6: force dynamic rendering so loadProject() runs on every
// request (reads BEQUITE_DASHBOARD_MODE + BEQUITE_API_BASE at request time).
// Without this, Next.js caches the server-component at build time, where
// env vars often aren't set, and the dashboard silently falls back to
// filesystem mode forever.
export const dynamic = "force-dynamic";
export const revalidate = 0;

export default async function DashboardHome() {
  // Server-component reads project state on every request. The dispatcher
  // in `lib/projects` picks filesystem or HTTP mode based on
  // BEQUITE_DASHBOARD_MODE (v2.0.0-alpha.1 candidate). Either way the
  // returned shape is the same.
  const snapshot = await loadProject();
  const loaderConfig = getLoaderConfig();

  return (
    <div className="flex h-screen flex-col bg-ink">
      <TopBar
        projectName={snapshot.projectName}
        workspace="personal"
        signedInUser="xpShawky (local)"
        agentOnline
        loaderMode={loaderConfig.mode}
        apiBase={loaderConfig.apiBase}
        workspacePath={snapshot.root}
      />

      <div className="flex flex-1 overflow-hidden">
        <PhasesSidebar
          phases={snapshot.phases}
          currentPhase={snapshot.currentPhase}
          costSession={snapshot.costSession}
        />

        <main className="flex flex-1 flex-col gap-3 overflow-y-auto bg-ink p-4">
          {/* Top row: live terminal (HTTP mode) or static mock (filesystem mode) */}
          <div className="h-[40vh] min-h-[280px]">
            {loaderConfig.mode === "http" ? (
              <Terminal
                mode={loaderConfig.mode}
                apiBase={loaderConfig.apiBase}
                workspacePath={snapshot.root}
              />
            ) : (
              <CommandConsole />
            )}
          </div>

          {/* Middle row: plan / tasks / tests */}
          <div>
            <PlanTasksTests snapshot={snapshot} />
          </div>

          {/* Bottom row: receipts list */}
          <div>
            <ReceiptsList receipts={snapshot.recentReceipts} />
          </div>

          {/* Footer status */}
          <footer className="mt-auto flex items-center justify-between border-t border-ink-edge pt-3 text-xs text-silver-dim">
            <div className="flex items-center gap-4">
              <span>Constitution v{snapshot.constitutionVersion}</span>
              <span>·</span>
              <span>Doctrines: {snapshot.doctrineList.join(", ") || "none active"}</span>
              <span>·</span>
              <span>Last green: {snapshot.lastGreenTag ?? "(none)"}</span>
              <span>·</span>
              <span
                className={
                  loaderConfig.mode === "http"
                    ? "rounded border border-gold-deep px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-gold-bright"
                    : "rounded border border-ink-edge px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-silver-dim"
                }
                title={
                  loaderConfig.mode === "http"
                    ? `HTTP mode — API ${loaderConfig.apiBase}${loaderConfig.hasToken ? " (token)" : " (no token)"}`
                    : "Filesystem mode — direct .bequite/ reads"
                }
              >
                {loaderConfig.mode === "http" ? "HTTP" : "FS"}
              </span>
            </div>
            <div>
              <span className="font-mono">BeQuite Studio v0.20.0 / v2.0.0-alpha.1 (candidate)</span>
            </div>
          </footer>
        </main>

        <AgentPanel
          message={snapshot.activeContextSummary || "Hi there. Memory loaded. Ready when you are — pick a phase or run a command."}
          status="online"
          recentReceipts={snapshot.recentReceipts}
        />
      </div>
    </div>
  );
}
