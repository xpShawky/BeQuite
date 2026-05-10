"use client";

import { motion } from "framer-motion";
import { AgentCharacter } from "./AgentCharacter";

/**
 * Demo section — terminal preview of the BeQuite CLI in action.
 *
 * v0.16.0: static frames. v0.17.0+: typed-out animation with frame-by-frame
 * scroll scrubbing per Apple-cinematic pattern.
 */
export function Demo() {
  const lines: { content: React.ReactNode; tone?: "prompt" | "out" | "good" | "warn" }[] = [
    { content: "$ bequite init my-bookings-app --doctrine default-web-saas", tone: "prompt" },
    { content: "✓ Scaffolded .bequite/memory/ + 6 Memory Bank files", tone: "good" },
    { content: "✓ Loaded 14 hooks + 2 doctrines (default-web-saas + library-package)", tone: "good" },
    { content: "✓ Generated ed25519 keypair for receipt signing", tone: "good" },
    { content: "" },
    { content: "$ bequite plan --multi-model \"Build a bookings flow\"", tone: "prompt" },
    { content: "✓ docs/planning_runs/RUN-2026-05-10T15-30/", tone: "out" },
    { content: "  → prompts/plan_claude-opus-4-7.md  (paste into Claude)", tone: "out" },
    { content: "  → prompts/plan_gpt-5.md             (paste into ChatGPT)", tone: "out" },
    { content: "" },
    { content: "$ bequite models compare", tone: "prompt" },
    { content: "✓ comparison.md generated. 8 topics. 2 conflicts. 1 user decision pending.", tone: "good" },
    { content: "" },
    { content: "$ bequite verify", tone: "prompt" },
    { content: "✓ lint  pass    typecheck pass    unit pass    integration pass", tone: "good" },
    { content: "✓ playwright admin walk pass    user walk pass    axe pass", tone: "good" },
    { content: "✓ smoke   freshness   audit   receipts emitted ✓ signed ✓", tone: "good" },
  ];

  return (
    <section id="demo" className="relative bg-ink py-32 lg:py-48">
      <div className="mx-auto max-w-[1400px] px-6 lg:px-10">
        <div className="mb-16 grid grid-cols-1 items-end gap-12 lg:grid-cols-12">
          <div className="lg:col-span-7">
            <p className="mb-3 text-xs font-medium uppercase tracking-[0.3em] text-gold">
              See it in action
            </p>
            <h2 className="font-display text-display font-bold leading-[1.05] tracking-tight text-balance text-silver">
              From zero to verified
              <br />
              <span className="bg-gradient-to-r from-gold-bright to-gold bg-clip-text text-transparent">
                in five commands.
              </span>
            </h2>
          </div>
          <p className="max-w-md text-body-lg text-silver-soft lg:col-span-5">
            BeQuite walks the seven phases for you. Manual-paste mode keeps you
            ToS-clean with your Claude + ChatGPT subscriptions.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          className="relative grid grid-cols-1 gap-6 lg:grid-cols-[1fr_auto] lg:items-center"
        >
          {/* Terminal frame */}
          <div className="overflow-hidden rounded-2xl border border-ink-edge bg-ink-stage shadow-2xl">
            {/* Title bar */}
            <div className="flex items-center justify-between border-b border-ink-edge bg-ink-velvet/60 px-5 py-3 backdrop-blur-sm">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-[#FF5F56]" />
                <span className="h-3 w-3 rounded-full bg-[#FFBD2E]" />
                <span className="h-3 w-3 rounded-full bg-[#27C93F]" />
              </div>
              <span className="font-mono text-xs uppercase tracking-wider text-silver-dim">
                bequite — main
              </span>
              <span aria-hidden className="w-12" />
            </div>
            {/* Terminal body */}
            <pre className="overflow-x-auto p-7 font-mono text-sm leading-relaxed">
              {lines.map((line, i) => {
                const cls =
                  line.tone === "prompt"
                    ? "text-silver"
                    : line.tone === "good"
                    ? "text-gold"
                    : line.tone === "warn"
                    ? "text-[#F59E0B]"
                    : "text-silver-soft";
                return (
                  <div
                    key={i}
                    className={`${cls} whitespace-pre-wrap`}
                  >
                    {line.content || " "}
                  </div>
                );
              })}
            </pre>
          </div>

          {/* Pointing character */}
          <div className="hidden flex-shrink-0 lg:block">
            <AgentCharacter pose="pointing" size={300} />
          </div>
        </motion.div>
      </div>
    </section>
  );
}
