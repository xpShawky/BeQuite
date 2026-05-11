"use client";

import { Check, CircleDashed, Loader2, AlertOctagon, Rocket } from "lucide-react";
import type { PhaseStatus } from "@/lib/projects";

interface Props {
  phases: PhaseStatus[];
  currentPhase: string;
  costSession: { usd: number; tokens: number; calls: number } | null;
}

function StatusIcon({ status }: { status: PhaseStatus["status"] }) {
  if (status === "done") return <Check className="h-4 w-4 text-gold" strokeWidth={2.5} />;
  if (status === "in_progress") return <Loader2 className="h-4 w-4 animate-spin text-gold-bright" strokeWidth={2.5} />;
  if (status === "blocked") return <AlertOctagon className="h-4 w-4 text-red-400" strokeWidth={2.5} />;
  return <CircleDashed className="h-4 w-4 text-silver-dim" strokeWidth={2} />;
}

export function PhasesSidebar({ phases, currentPhase, costSession }: Props) {
  return (
    <aside className="flex w-60 shrink-0 flex-col border-r border-ink-edge bg-ink-stage">
      <div className="px-4 pt-6">
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-gold">Phases</p>
        <p className="mt-1 text-xs text-silver-dim">
          Phase: <span className="font-mono text-silver-soft">{currentPhase}</span>
        </p>
      </div>

      <ul className="mt-4 flex-1 space-y-1 px-2">
        {phases.map((p) => (
          <li key={p.id}>
            <div className="flex items-center gap-3 rounded-md px-3 py-2 transition-colors duration-200 ease-cinematic hover:bg-ink-velvet">
              <StatusIcon status={p.status} />
              <span className="font-mono text-sm font-medium text-silver-soft">{p.id}</span>
              <span className="text-sm text-silver-dim">{p.name}</span>
            </div>
          </li>
        ))}
      </ul>

      <div className="m-4 rounded-xl border border-ink-edge bg-ink-velvet/40 p-4">
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-gold">Dev Status</p>
        <p className="mt-2 text-sm text-silver">
          Ready to deploy
          <span aria-hidden className="ml-1.5 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-gold align-middle" />
        </p>
        <p className="mt-1 text-xs text-silver-dim">
          {costSession
            ? `${costSession.calls} call${costSession.calls === 1 ? "" : "s"} · $${costSession.usd.toFixed(4)}`
            : "no session cost yet"}
        </p>
        <button
          type="button"
          disabled
          title="Deploy lands in v2.0.0-beta.1. For now: run `bequite handoff` to generate the deploy artifacts."
          aria-disabled="true"
          className="mt-3 flex w-full items-center justify-center gap-2 rounded-md bg-ink-edge px-3 py-2 text-sm font-medium text-silver-dim opacity-60 cursor-not-allowed"
        >
          <Rocket className="h-3.5 w-3.5" strokeWidth={2.5} />
          DEPLOY
          <span className="ml-1 rounded-sm bg-ink-velvet px-1 py-0.5 font-mono text-[9px] uppercase tracking-wider text-silver-dim">soon</span>
        </button>
      </div>
    </aside>
  );
}
