"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

/**
 * Cinematic chapter wrapper (Apple-style pinned scroll).
 *
 * Each chapter pins to the viewport. Inside the pinned window, the children
 * (a "stage") receive `progress` (0..1) via render-prop, allowing per-chapter
 * frame-by-frame transitions.
 *
 * Usage:
 *   <Chapter heightVH={300}>
 *     {(progress) => (
 *       <motion.h1 style={{ scale: useTransform(progress, [0, 1], [1, 1.5]) }}>
 *         Hello
 *       </motion.h1>
 *     )}
 *   </Chapter>
 *
 * v0.17.5+ will plug in GLB-loaded 3D scenes that scrub their animation
 * timeline against `progress` (the apple.com/macbook-pro pattern).
 */

interface ChapterProps {
  children: (progress: import("framer-motion").MotionValue<number>) => React.ReactNode;
  heightVH?: number; // total scroll length in viewport heights
  className?: string;
  id?: string;
  ariaLabel?: string;
}

export function Chapter({
  children,
  heightVH = 200,
  className = "",
  id,
  ariaLabel,
}: ChapterProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  return (
    <section
      id={id}
      ref={ref}
      aria-label={ariaLabel}
      className={`relative ${className}`}
      style={{ height: `${heightVH}vh` }}
    >
      <div className="sticky top-0 flex h-screen items-center overflow-hidden">
        {children(scrollYProgress)}
      </div>
    </section>
  );
}

/**
 * Chapter header — uniform per-chapter section title with eyebrow.
 */
export function ChapterHeader({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children?: React.ReactNode;
}) {
  return (
    <div>
      <p className="mb-3 font-mono text-xs uppercase tracking-[0.3em] text-gold">
        {eyebrow}
      </p>
      <h2 className="font-display text-display font-bold leading-[1.05] tracking-tight text-balance text-silver">
        {title}
      </h2>
      {children && (
        <p className="mt-6 max-w-md text-body-lg text-silver-soft text-pretty">
          {children}
        </p>
      )}
    </div>
  );
}
