"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

const PHASES = [
  {
    id: "P0",
    name: "Research",
    description:
      "Cross-checked evidence. Freshness probe verifies every package + price + license is fresh < 6 months old. No hallucinated dependencies.",
    accent: "bg-gold/10",
  },
  {
    id: "P1",
    name: "Stack ADR",
    description:
      "An Architectural Decision Record per stack pick. Reasoned. Forkable. Doctrine-aligned. Skeptic-stress-tested.",
    accent: "bg-gold/15",
  },
  {
    id: "P2",
    name: "Plan + Contracts",
    description:
      "Spec → plan → API contracts → data model. Multi-model planning lets Claude + ChatGPT think independently and merge their plans.",
    accent: "bg-gold/20",
  },
  {
    id: "P3",
    name: "Phases",
    description:
      "Decomposed into committable phases. Each with an exit gate. Each with a Skeptic kill-shot question.",
    accent: "bg-gold/15",
  },
  {
    id: "P4",
    name: "Tasks",
    description:
      "Atomic ≤5-min tasks per phase. Dependency-aware. Parallel-eligible (>5) fan out to subagents.",
    accent: "bg-gold/20",
  },
  {
    id: "P5",
    name: "Implement",
    description:
      "TDD discipline. Banned weasel words ('should', 'probably', 'I think it works' = exit code 2). Per-task commit + receipt.",
    accent: "bg-gold/25",
  },
  {
    id: "P6",
    name: "Verify",
    description:
      "Playwright admin + user walks. axe-core gate. Smoke. Audit. Freshness. Receipts archived. The build is operational, not just committed.",
    accent: "bg-gold/30",
  },
  {
    id: "P7",
    name: "Handoff",
    description:
      "HANDOFF.md hand-runnable by a second engineer. Cost estimate. Risk register. Vibe-handoff for non-engineers.",
    accent: "bg-gold/35",
  },
];

export function PhasesScroll() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end end"],
  });

  // Active phase index based on scroll progress
  const activeIndex = useTransform(
    scrollYProgress,
    [0, 1],
    [0, PHASES.length - 0.001],
  );

  return (
    <section
      id="how-it-works"
      ref={ref}
      className="relative"
      style={{ height: `${PHASES.length * 80}vh` }}
      aria-label="The seven phases"
    >
      <div className="sticky top-0 flex h-screen items-center overflow-hidden bg-ink">
        <div className="mx-auto grid w-full max-w-[1400px] grid-cols-1 gap-12 px-6 lg:grid-cols-12 lg:gap-16 lg:px-10">
          {/* Left: pinned chapter title */}
          <div className="lg:col-span-5">
            <p className="mb-3 text-xs font-medium uppercase tracking-[0.3em] text-gold">
              How BeQuite works
            </p>
            <h2 className="font-display text-display font-bold leading-[1.05] tracking-tight text-balance text-silver">
              Seven phases.
              <br />
              <span className="bg-gradient-to-r from-gold-bright to-gold-deep bg-clip-text text-transparent">
                Zero skipped.
              </span>
            </h2>
            <p className="mt-6 max-w-md text-body-lg text-silver-soft text-pretty">
              Each phase has an artifact, a Skeptic kill-shot, a verification
              gate, a receipt, and a per-phase commit. No hand-waving.
            </p>
          </div>

          {/* Right: phase cards */}
          <div className="lg:col-span-7">
            <div className="space-y-4">
              {PHASES.map((phase, i) => {
                const opacity = useTransform(
                  activeIndex,
                  [i - 1.2, i, i + 1],
                  [0.25, 1, 0.4],
                );
                const x = useTransform(
                  activeIndex,
                  [i - 0.5, i, i + 0.5],
                  ["8px", "0px", "-8px"],
                );
                const scale = useTransform(
                  activeIndex,
                  [i - 0.5, i, i + 0.5],
                  [0.98, 1, 0.98],
                );

                return (
                  <motion.article
                    key={phase.id}
                    style={{ opacity, x, scale }}
                    className="group relative rounded-2xl border border-ink-edge bg-ink-stage/60 p-6 backdrop-blur-sm transition-colors duration-cinematic ease-cinematic hover:border-gold-deep"
                  >
                    <div
                      className="absolute inset-0 rounded-2xl opacity-0 transition-opacity duration-cinematic ease-cinematic group-hover:opacity-100"
                      aria-hidden
                      style={{
                        background:
                          "radial-gradient(ellipse 80% 60% at 30% 0%, rgba(229,181,71,0.08) 0%, rgba(229,181,71,0) 60%)",
                      }}
                    />
                    <div className="relative flex items-start gap-5">
                      <div
                        className={`flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl border border-gold-deep/40 ${phase.accent} font-mono text-sm font-medium text-gold-bright`}
                      >
                        {phase.id}
                      </div>
                      <div>
                        <h3 className="font-display text-h2 font-semibold text-silver">
                          {phase.name}
                        </h3>
                        <p className="mt-2 text-body text-silver-soft text-pretty">
                          {phase.description}
                        </p>
                      </div>
                    </div>
                  </motion.article>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
