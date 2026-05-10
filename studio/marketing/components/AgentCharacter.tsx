"use client";

import { motion } from "framer-motion";
import Image from "next/image";

interface Props {
  pose?: "zen" | "pointing";
  size?: number;
  className?: string;
  animate?: boolean;
}

/**
 * The astronaut character — the brand's personality anchor.
 *
 * v0.16.0: 2D image with breathing motion. v0.17.0+: optional swap for
 * GLB-loaded 3D character via R3F (Blender pipeline) — the API stays the same.
 */
export function AgentCharacter({
  pose = "zen",
  size = 320,
  className = "",
  animate = true,
}: Props) {
  const src =
    pose === "zen"
      ? "/brand/02-character-zen.png"
      : "/brand/03-character-pointing.png";

  return (
    <motion.div
      className={`relative inline-block ${className}`}
      animate={
        animate
          ? {
              y: [0, -8, 0],
            }
          : undefined
      }
      transition={
        animate
          ? {
              duration: 4,
              ease: "easeInOut",
              repeat: Infinity,
            }
          : undefined
      }
      style={{ width: size, height: size }}
    >
      {/* Gold glow halo behind the character */}
      <div
        aria-hidden
        className="absolute inset-0 -z-10 rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(229, 181, 71, 0.35) 0%, rgba(229, 181, 71, 0) 60%)",
        }}
      />
      <Image
        src={src}
        alt="BeQuite agent"
        width={size}
        height={size}
        priority={pose === "zen"}
        className="h-full w-full object-contain"
      />
    </motion.div>
  );
}
