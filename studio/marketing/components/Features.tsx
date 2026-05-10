"use client";

import { motion } from "framer-motion";
import {
  ShieldCheck,
  Sparkles,
  GitBranch,
  Cpu,
  FileText,
  Layers,
} from "lucide-react";

const FEATURES = [
  {
    icon: ShieldCheck,
    title: "Constitution-governed",
    description:
      "10 Iron Laws. 13 Doctrines. Every action traceable to a binding rule. Never bypass-able under any flag.",
  },
  {
    icon: GitBranch,
    title: "Multi-model planning",
    description:
      "Two or more models think through your project independently. BeQuite compares + merges. Manual-paste mode works with your Claude Pro + ChatGPT Plus subscriptions today.",
  },
  {
    icon: Sparkles,
    title: "Auto-mode",
    description:
      "One-click P0 → P7 with safety rails. Cost ceiling. Wall-clock ceiling. Banned-word check. Hook-block respect. One-way doors always pause.",
  },
  {
    icon: FileText,
    title: "Receipts (signed)",
    description:
      "Every model invocation emits a chain-hashed JSON receipt. ed25519-signed. Replay-able. Cost-roll-up-able. Auditable.",
  },
  {
    icon: Cpu,
    title: "Five providers",
    description:
      "Anthropic + OpenAI + Google + DeepSeek + Ollama. Cost-aware routing per phase × persona. Graceful fallback.",
  },
  {
    icon: Layers,
    title: "Nine hosts",
    description:
      "Claude Code, Cursor, Codex, Cline, Kilo, Continue, Aider, Windsurf, Gemini. One AGENTS.md. One install.",
  },
];

export function Features() {
  return (
    <section id="features" className="relative bg-ink py-32 lg:py-48">
      <div className="mx-auto max-w-[1400px] px-6 lg:px-10">
        <div className="mb-16 max-w-3xl">
          <p className="mb-3 text-xs font-medium uppercase tracking-[0.3em] text-gold">
            What's in the box
          </p>
          <h2 className="font-display text-display font-bold leading-[1.05] tracking-tight text-balance text-silver">
            Everything you need.
            <br />
            <span className="text-silver-soft">Nothing you don't.</span>
          </h2>
        </div>

        <ul className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((feature, i) => (
            <motion.li
              key={feature.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{
                duration: 0.9,
                delay: i * 0.06,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="group relative overflow-hidden rounded-2xl border border-ink-edge bg-ink-stage p-7 transition-all duration-cinematic ease-cinematic hover:border-gold-deep hover:shadow-glint"
            >
              <div
                aria-hidden
                className="absolute -right-12 -top-12 h-40 w-40 rounded-full opacity-0 blur-3xl transition-opacity duration-cinematic ease-cinematic group-hover:opacity-100"
                style={{ background: "rgba(229,181,71,0.25)" }}
              />
              <div className="relative">
                <feature.icon
                  className="h-7 w-7 text-gold transition-colors duration-cinematic ease-cinematic group-hover:text-gold-bright"
                  strokeWidth={1.5}
                />
                <h3 className="mt-5 font-display text-h2 font-semibold text-silver">
                  {feature.title}
                </h3>
                <p className="mt-2 text-body text-silver-soft text-pretty">
                  {feature.description}
                </p>
              </div>
            </motion.li>
          ))}
        </ul>
      </div>
    </section>
  );
}
