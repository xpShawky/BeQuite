import { TopBar } from "@/components/TopBar";
import { PhasesSidebar } from "@/components/PhasesSidebar";
import { CommandConsole } from "@/components/CommandConsole";
import { PlanTasksTests } from "@/components/PlanTasksTests";
import { AgentPanel } from "@/components/AgentPanel";
import { ReceiptsList } from "@/components/ReceiptsList";
import { loadProject } from "@/lib/projects";

export default function DashboardHome() {
  // Server-component reads from .bequite/ on every request.
  const snapshot = loadProject();

  return (
    <div className="flex h-screen flex-col bg-ink">
      <TopBar
        projectName={snapshot.projectName}
        workspace="personal"
        signedInUser="xpShawky (local)"
        agentOnline
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
            </div>
            <div>
              <span className="font-mono">BeQuite Studio v0.18.0</span>
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
