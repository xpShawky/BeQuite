"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

/**
 * R3F particle starfield (v0.17.0).
 *
 * Replaces the static [...Array(40)] dots in Hero with a real 3D particle
 * system. Tiny gold motes drift slowly upward; subtle parallax. Falls
 * back gracefully on devices that flag prefers-reduced-motion: reduce.
 *
 * v0.17.5+ will swap the procedural scene for a richer GLB-driven one
 * (post-Blender pipeline).
 */

interface StarsProps {
  count?: number;
}

function Stars({ count = 800 }: StarsProps) {
  const mesh = useRef<THREE.Points>(null!);
  const geometry = useRef<THREE.BufferGeometry>(null!);

  // Generate positions once
  const positions = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    positions[i * 3 + 0] = (Math.random() - 0.5) * 20; // x
    positions[i * 3 + 1] = (Math.random() - 0.5) * 12; // y
    positions[i * 3 + 2] = (Math.random() - 0.5) * 10; // z
    sizes[i] = 0.4 + Math.random() * 0.6;
  }

  useFrame((_, delta) => {
    if (!mesh.current) return;
    mesh.current.rotation.y += delta * 0.03;
    mesh.current.rotation.x += delta * 0.005;
  });

  return (
    <points ref={mesh}>
      <bufferGeometry ref={geometry}>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
          count={count}
        />
        <bufferAttribute
          attach="attributes-size"
          args={[sizes, 1]}
          count={count}
        />
      </bufferGeometry>
      <pointsMaterial
        color="#E5B547"
        size={0.04}
        sizeAttenuation
        transparent
        opacity={0.7}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

export function Starfield() {
  // Respect prefers-reduced-motion via CSS (already handled in tokens.css);
  // also disable the canvas entirely if matchMedia says reduce.
  if (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    return null;
  }

  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 -z-0 opacity-80"
    >
      <Canvas
        camera={{ position: [0, 0, 5], fov: 60 }}
        gl={{ antialias: true, alpha: true }}
        dpr={[1, 2]}
        frameloop="always"
      >
        <ambientLight intensity={0.2} />
        <Stars count={800} />
      </Canvas>
    </div>
  );
}
