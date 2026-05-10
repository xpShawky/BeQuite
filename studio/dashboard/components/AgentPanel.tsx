"use client";

import { motion } from "framer-motion";
import Image from "next/image";

interface Props {
  message?: string;
  status?: "online" | "thinking" | "blocked";
}

export function AgentPanel({
  message = "Hi there. Memory loaded. Ready when you are — pick a phase or run a command.",
  status = "online",
}: Props) {
  const statusLabel = status === "online" ? "online" : status === "thinking" ? "thinking" : "blocked";

  return (
    <aside className="flex w-72 shrink-0 flex-col border-l border-ink-edge bg-ink-stage p-5">
      <header className="mb-4 flex items-center justify-between">
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-gold">Agent</p>
        <div className="flex items-center gap-1.5">
          <span
            aria-hidden
            className={`h-2 w-2 rounded-full ${
              status === "online" ? "animate-pulse bg-gold" : status === "thinking" ? "animate-pulse bg-gold-bright" : "bg-red-400"
            }`}
          />
          <span className="font-mono text-[10px] uppercase tracking-wider text-silver-soft">{statusLabel}</span>
        </div>
      </header>

      <motion.div
        animate={{ y: [0, -6, 0] }}
        transition={{ duration: 4, ease: "easeInOut", repeat: Infinity }}
        className="relative mx-auto h-48 w-48"
      >
        <div
          aria-hidden
          className="absolute inset-0 -z-10 rounded-full blur-3xl"
          style={{
            background:
              "radial-gradient(ellipse at center, rgba(229, 181, 71, 0.35) 0%, rgba(229, 181, 71, 0) 60%)",
          }}
        />
        <Image
          src="/brand/02-character-zen.png"
          alt="BeQuite agent"
          width={192}
          height={192}
          className="h-full w-full object-contain"
          priority
        />
      </motion.div>

      <div className="mt-4 rounded-xl border border-gold-deep/30 bg-ink-velvet/40 p-4">
        <p className="text-sm leading-relaxed text-silver text-pretty">{message}</p>
      </div>

      <div className="mt-auto pt-4">
        <p className="font-mono text-[10px] uppercase tracking-wider text-silver-dim">
          recent activity
        </p>
        <ul className="mt-2 space-y-1.5 font-mono text-[11px] text-silver-soft">
          <li>$ bequite verify ✓</li>
          <li>$ bequite plan ✓</li>
          <li>$ bequite freshness ✓</li>
        </ul>
      </div>
    </aside>
  );
}
