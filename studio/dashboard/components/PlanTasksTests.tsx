"use client";

import { CheckCircle2, CircleDashed, GitCommit } from "lucide-react";
import type { ProjectSnapshot } from "@/lib/projects";

interface Props {
  snapshot: ProjectSnapshot;
}

export function PlanTasksTests({ snapshot }: Props) {
  const planItems = [
    "Architecture decided · ADR-001",
    "Stack: Next.js + Hono + Supabase",
    "Auth: Better-Auth",
    "Doctrine: " + (snapshot.doctrineList[0] ?? "default-web-saas"),
  ];

  const taskItems = [
    "T-1.1  scaffold apps/web      ✓",
    "T-1.2  scaffold apps/api      ✓",
    "T-1.3  drop tokens.css        ✓",
    "T-1.4  wire Better-Auth       ✓",
    "T-1.5  Supabase migrations    ✓",
    "T-1.6  hello-world page       ✓",
    "T-1.7  CI green               ⏳",
  ];

  const testItems = [
    { label: "lint", pass: true },
    { label: "typecheck", pass: true },
    { label: "unit", pass: true },
    { label: "playwright admin", pass: true },
    { label: "playwright user", pass: true },
    { label: "axe-core", pass: true },
    { label: "smoke", pass: true },
    { label: "audit", pass: true },
  ];

  return (
    <section className="grid grid-cols-1 gap-3 md:grid-cols-3">
      <Panel title="Plan" subtitle="from specs/" icon={<GitCommit className="h-3.5 w-3.5" />}>
        <ul className="space-y-2">
          {planItems.map((t) => (
            <li key={t} className="flex items-start gap-2 text-sm text-silver-soft">
              <span aria-hidden className="mt-1.5 h-1 w-1 flex-shrink-0 rounded-full bg-gold" />
              <span>{t}</span>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Tasks" subtitle="atomic, ≤5min each" icon={<CircleDashed className="h-3.5 w-3.5" />}>
        <ul className="space-y-1 font-mono text-xs leading-relaxed text-silver-soft">
          {taskItems.map((t) => (
            <li key={t} className="whitespace-pre">
              {t.replace("✓", "")}<span className="text-gold">{t.includes("✓") ? "✓" : ""}</span><span className="text-gold-bright">{t.includes("⏳") ? "" : ""}</span>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Tests" subtitle="bequite verify" icon={<CheckCircle2 className="h-3.5 w-3.5" />}>
        <ul className="grid grid-cols-2 gap-1.5">
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
