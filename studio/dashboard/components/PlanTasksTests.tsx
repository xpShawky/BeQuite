"use client";

import { CheckCircle2, CircleDashed, GitCommit } from "lucide-react";
import type { ProjectSnapshot } from "@/lib/projects";

interface Props {
  snapshot: ProjectSnapshot;
}

/**
 * Three-panel grid: Plan / Tasks / Tests.
 *
 * v2.0.0-alpha.6: Wired to real ProjectSnapshot fields instead of the
 * hardcoded literals that shipped in v0.18.0. When the project has no
 * plan/tasks/tests data on disk, the panels surface that honestly with
 * an "(empty — run `bequite plan`)" message instead of pretending.
 */
export function PlanTasksTests({ snapshot }: Props) {
  // Plan panel — drawn from the snapshot's project facts.
  const planItems: string[] = [];
  if (snapshot.exists) {
    planItems.push(`Project: ${snapshot.projectName}`);
    planItems.push(`Constitution: v${snapshot.constitutionVersion}`);
    planItems.push(`Current phase: ${snapshot.currentPhase}`);
    if (snapshot.doctrineList.length > 0) {
      planItems.push(`Doctrines: ${snapshot.doctrineList.slice(0, 3).join(", ")}`);
    }
    if (snapshot.lastGreenTag) {
      planItems.push(`Last green: ${snapshot.lastGreenTag}`);
    }
  }

  // Tasks panel — derived from phase status. We surface each phase + its
  // status icon. When real tasks.md parsing is wired (v2.0.0-beta.1+), this
  // becomes the live task list.
  const taskItems = snapshot.phases.map((p) => ({
    label: `${p.id}  ${p.name}`,
    status: p.status,
  }));

  // Tests panel — derived from the latest verify-receipt if present.
  // No receipt yet = "(awaiting bequite verify)".
  const verifyReceipt = snapshot.recentReceipts.find((r) => r.phase === "P6" || r.phase === "VERIFY");
  const testItems = verifyReceipt
    ? [
        { label: "verify", pass: verifyReceipt.signed },
        { label: `cost $${verifyReceipt.cost_usd.toFixed(4)}`, pass: true },
        { label: `model ${verifyReceipt.model}`, pass: true },
      ]
    : [
        { label: "(awaiting bequite verify)", pass: false },
      ];

  return (
    <section className="grid grid-cols-1 gap-3 md:grid-cols-3">
      <Panel
        title="Plan"
        subtitle={snapshot.exists ? "from .bequite/memory/" : "(no project)"}
        icon={<GitCommit className="h-3.5 w-3.5" />}
      >
        {planItems.length === 0 ? (
          <p className="text-sm text-silver-dim italic">
            No project loaded — run <code className="font-mono text-gold">bequite init</code>
          </p>
        ) : (
          <ul className="space-y-2">
            {planItems.map((t) => (
              <li key={t} className="flex items-start gap-2 text-sm text-silver-soft">
                <span aria-hidden className="mt-1.5 h-1 w-1 flex-shrink-0 rounded-full bg-gold" />
                <span>{t}</span>
              </li>
            ))}
          </ul>
        )}
      </Panel>

      <Panel
        title="Phases"
        subtitle="7-phase workflow"
        icon={<CircleDashed className="h-3.5 w-3.5" />}
      >
        <ul className="space-y-1 font-mono text-xs leading-relaxed">
          {taskItems.map((t) => {
            const indicator =
              t.status === "done" ? <span className="text-gold">✓</span>
              : t.status === "in_progress" ? <span className="text-gold-bright animate-pulse">⏳</span>
              : t.status === "blocked" ? <span className="text-red-400">!</span>
              : <span className="text-silver-dim">·</span>;
            return (
              <li key={t.label} className="flex items-start gap-2 whitespace-pre text-silver-soft">
                {indicator}
                <span>{t.label}</span>
              </li>
            );
          })}
        </ul>
      </Panel>

      <Panel
        title="Tests"
        subtitle={verifyReceipt ? "last verify receipt" : "no receipt yet"}
        icon={<CheckCircle2 className="h-3.5 w-3.5" />}
      >
        <ul className="space-y-1.5">
          {testItems.map((t) => (
            <li key={t.label} className="flex items-center gap-1.5 text-xs text-silver-soft">
              <span
                aria-hidden
                className={`h-1.5 w-1.5 rounded-full ${t.pass ? "bg-gold" : "bg-silver-dim"}`}
              />
              <span>{t.label}</span>
            </li>
          ))}
        </ul>
      </Panel>
    </section>
  );
}

function Panel({
  title,
  subtitle,
  icon,
  children,
}: {
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col rounded-xl border border-ink-edge bg-ink-stage p-4">
      <header className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-gold">{icon}</span>
          <h3 className="font-mono text-[11px] uppercase tracking-[0.25em] text-gold">{title}</h3>
        </div>
        <span className="text-[10px] text-silver-dim">{subtitle}</span>
      </header>
      <div className="flex-1">{children}</div>
    </div>
  );
}
