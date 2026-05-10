"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import { AgentCharacter } from "./AgentCharacter";

/**
 * Pinned hero — Apple-style cinematic.
 *
 * The hero pins to the viewport for ~150vh of scroll. Inside that pinned
 * window, headline scales up + silver-to-gold color shift, and the agent
 * character drifts in from the right.
 *
 * v0.16.0: 2D Framer Motion only. v0.17.0+: layer R3F particle starfield
 * + 3D character (Blender GLB) when assets ship.
 */
export function Hero() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  const headlineScale = useTransform(scrollYProgress, [0, 0.5], [1, 1.08]);
  const headlineOpacity = useTransform(scrollYProgress, [0, 0.7], [1, 0]);
  const characterX = useTransform(scrollYProgress, [0, 0.4], ["-12%", "0%"]);
  const characterOpacity = useTransform(scrollYProgress, [0, 0.2], [0.85, 1]);
  const subhedOpacity = useTransform(scrollYProgress, [0, 0.4], [0.7, 0]);
  const overlay = useTransform(
    scrollYProgress,
    [0, 1],
    ["rgba(0,0,0,0)", "rgba(0,0,0,0.6)"],
  );

  return (
    <section
      ref={ref}
      className="relative h-[160vh]"
      aria-label="Hero"
    >
      <div className="sticky top-0 flex h-screen items-center justify-center overflow-hidden">
        {/* Backdrop: starfield-ish gradient */}
        <div
          aria-hidden
          className="absolute inset-0 bg-ink"
          style={{
            backgroundImage:
              "radial-gradient(ellipse 80% 60% at 50% 30%, rgba(229,181,71,0.10) 0%, rgba(229,181,71,0) 60%), radial-gradient(circle at 20% 70%, rgba(229,181,71,0.06) 0%, transparent 40%)",
          }}
        />
        {/* Stars */}
        <div aria-hidden className="absolute inset-0 opacity-50">
          {[...Array(40)].map((_, i) => (
            <span
              key={i}
              className="absolute h-px w-px rounded-full bg-gold-bright"
              style={{
                top: `${(i * 37) % 100}%`,
                left: `${(i * 71) % 100}%`,
                opacity: 0.2 + ((i * 13) % 70) / 100,
                animation: `glint ${2 + ((i * 7) % 5)}s ease-in-out ${
                  ((i * 11) % 30) / 10
                }s infinite`,
              }}
            />
          ))}
        </div>

        {/* Headline + character */}
        <div className="relative z-10 mx-auto flex max-w-[1400px] items-center justify-between gap-12 px-6 lg:px-10">
          <motion.div
            style={{ scale: headlineScale, opacity: headlineOpacity }}
            className="max-w-3xl"
          >
            <p className="mb-6 inline-flex items-center gap-2 rounded-full border border-ink-edge bg-ink-stage/80 px-3 py-1.5 text-xs uppercase tracking-wider text-gold backdrop-blur-sm">
              <span className="h-1.5 w-1.5 rounded-full bg-gold animate-pulse" />
              v0.16 — Studio Edition begins
            </p>
            <h1 className="font-display text-mega font-bold leading-[1.05] tracking-tight text-balance">
              <span className="block text-silver">Plan it.</span>
              <span className="block text-silver">Build it.</span>
              <span className="block bg-gradient-to-br from-gold-bright via-gold to-gold-deep bg-clip-text text-transparent">
                Be quiet.
              </span>
            </h1>
            <motion.p
              style={{ opacity: subhedOpacity }}
              className="mt-8 max-w-xl text-body-lg text-silver-soft text-pretty"
            >
              The AI project operating system. Plans, builds, tests, reviews,
              recovers, and ships projects with fewer errors. Spec-driven.
              Constitution-governed. Receipt-signed. Vibecoder-friendly.
            </motion.p>
            <motion.div
              style={{ opacity: subhedOpacity }}
              className="mt-10 flex flex-wrap gap-4"
            >
              <a
                href="#cta"
                className="inline-flex items-center gap-2 rounded-full bg-gold px-7 py-3 font-medium text-ink shadow-glint transition-all duration-cinematic ease-cinematic hover:bg-gold-bright hover:shadow-glint-strong"
              >
                Get started <span aria-hidden>→</span>
              </a>
              <a
                href="#how-it-works"
                className="inline-flex items-center gap-2 rounded-full border border-ink-edge bg-ink-stage/60 px-7 py-3 font-medium text-silver backdrop-blur-sm transition-colors duration-cinematic ease-cinematic hover:border-silver-dim hover:text-silver-soft"
              >
                How it works
              </a>
            </motion.div>
          </motion.div>

          <motion.div
            style={{ x: characterX, opacity: characterOpacity }}
            className="hidden lg:block"
          >
            <AgentCharacter pose="zen" size={420} />
          </motion.div>
        </div>

        {/* Scroll cue */}
        <motion.div
          style={{ opacity: subhedOpacity }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2 text-xs uppercase tracking-[0.3em] text-silver-dim"
        >
          ↓ scroll
        </motion.div>

        {/* Black-out overlay as user scrolls past */}
        <motion.div
          style={{ background: overlay }}
          aria-hidden
          className="pointer-events-none absolute inset-0"
        />
      </div>
    </section>
  );
}
