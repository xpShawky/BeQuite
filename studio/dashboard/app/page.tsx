import { TopBar } from "@/components/TopBar";
import { PhasesSidebar } from "@/components/PhasesSidebar";
import { CommandConsole } from "@/components/CommandConsole";
import { PlanTasksTests } from "@/components/PlanTasksTests";
import { AgentPanel } from "@/components/AgentPanel";
import { ReceiptsList } from "@/components/ReceiptsList";
import { loadProject, getLoaderConfig } from "@/lib/projects";

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
          {/* Top row: command console */}
          <div className="h-[40vh] min-h-[280px]">
            <CommandConsole />
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
          message={snapshot.activeContextSummary}
          status="online"
        />
      </div>
    </div>
  );
}
