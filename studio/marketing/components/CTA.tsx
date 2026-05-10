"use client";

import { motion } from "framer-motion";

export function CTA() {
  return (
    <section id="cta" className="relative bg-ink py-32 lg:py-48">
      <div
        aria-hidden
        className="absolute inset-0 opacity-50"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 50%, rgba(229,181,71,0.18) 0%, rgba(229,181,71,0) 60%)",
        }}
      />
      <div className="relative mx-auto max-w-3xl px-6 text-center lg:px-10">
        <motion.h2
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          className="font-display text-hero font-bold leading-[1.05] tracking-tight text-balance"
        >
          <span className="text-silver">Stop vibe-shipping</span>{" "}
          <span className="bg-gradient-to-br from-gold-bright via-gold to-gold-deep bg-clip-text text-transparent">
            broken half-builds.
          </span>
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          className="mt-6 text-body-lg text-silver-soft text-pretty"
        >
          Install BeQuite into your existing project, or scaffold a new one
          with its discipline baked in. Free. Open source. Forever.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="mt-10 flex flex-wrap items-center justify-center gap-4"
        >
          <a
            href="https://github.com/xpShawky/BeQuite"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full bg-gold px-8 py-3.5 font-medium text-ink shadow-glint transition-all duration-cinematic ease-cinematic hover:bg-gold-bright hover:shadow-glint-strong"
          >
            View on GitHub <span aria-hidden>↗</span>
          </a>
          <a
            href="/docs/quickstart"
            className="inline-flex items-center gap-2 rounded-full border border-ink-edge bg-ink-stage px-8 py-3.5 font-medium text-silver backdrop-blur-sm transition-colors duration-cinematic ease-cinematic hover:border-gold-deep hover:text-gold"
          >
            Read the quickstart
          </a>
        </motion.div>
        <p className="mt-10 font-mono text-sm text-silver-dim">
          # one-liner
          <br />
          <span className="text-silver">
            git clone https://github.com/xpShawky/BeQuite && cd BeQuite/cli && pip install -e .
          </span>
        </p>
      </div>
    </section>
  );
}
