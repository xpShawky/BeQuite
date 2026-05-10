"use client";

import { ChevronRight } from "lucide-react";

interface Line {
  prompt?: boolean;
  text: string;
  tone?: "out" | "good" | "warn" | "err";
}

const DEFAULT_LINES: Line[] = [
  { prompt: true, text: "bequite init" },
  { tone: "good", text: "✓ Scaffolded .bequite/memory/ + 6 Memory Bank files" },
  { prompt: true, text: "bequite plan" },
  { tone: "good", text: "✓ Generated specs/<feature>/plan.md" },
  { tone: "good", text: "✓ Skeptic kill-shot answered" },
  { prompt: true, text: "bequite verify" },
  { tone: "good", text: "✓ lint  typecheck  unit  playwright  axe  smoke  audit" },
  { tone: "good", text: "✓ 17 receipts emitted ✓ signed ✓" },
];

export function CommandConsole({ lines = DEFAULT_LINES }: { lines?: Line[] }) {
  return (
    <section className="flex h-full flex-col overflow-hidden rounded-xl border border-ink-edge bg-ink-stage">
      <div className="flex items-center justify-between border-b border-ink-edge bg-ink-velvet/40 px-4 py-2.5">
        <p className="font-mono text-[11px] uppercase tracking-[0.25em] text-gold">
          Command Console
        </p>
        <div className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-[#FF5F56]" />
          <span className="h-2 w-2 rounded-full bg-[#FFBD2E]" />
          <span className="h-2 w-2 rounded-full bg-[#27C93F]" />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 font-mono text-sm leading-relaxed">
        {lines.map((line, i) => {
          const cls =
            line.tone === "good"
              ? "text-gold"
              : line.tone === "warn"
              ? "text-[#F59E0B]"
              : line.tone === "err"
              ? "text-red-400"
              : line.prompt
              ? "text-silver"
              : "text-silver-soft";
          return (
            <div key={i} className={`whitespace-pre-wrap ${cls}`}>
              {line.prompt && (
                <span className="mr-1.5 text-gold">
                  <ChevronRight className="inline h-3.5 w-3.5" strokeWidth={3} />
                </span>
              )}
              {line.text}
            </div>
          );
        })}
        <div className="mt-3 flex items-center text-silver">
          <ChevronRight className="mr-1.5 inline h-3.5 w-3.5 text-gold" strokeWidth={3} />
          <span className="animate-pulse">▎</span>
        </div>
      </div>
    </section>
  );
}
