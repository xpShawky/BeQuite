"use client";

import { Suspense, useEffect, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Environment, useAnimations, useGLTF, OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { AgentCharacter } from "../AgentCharacter";

/**
 * 3D astronaut character (v0.17.5).
 *
 * Loads `public/3d/astronaut.glb` (produced by the Blender pipeline) and
 * plays the matching animation clip per `pose` prop. Falls back to the 2D
 * <AgentCharacter /> if:
 *   - The GLB is missing (404)
 *   - The user prefers reduced motion
 *   - WebGL is unavailable
 *
 * Same prop API as the 2D version — drop-in upgrade.
 */

const GLB_PATH = "/3d/astronaut.glb";

const POSE_TO_CLIP: Record<string, string> = {
  zen: "Idle.Breathe",
  pointing: "Idle.Point",
  waving: "Idle.Wave",
  floating: "Idle.Float",
};

function AstronautModel({ pose }: { pose: string }) {
  const group = useRef<THREE.Group>(null!);
  const { scene, animations } = useGLTF(GLB_PATH);
  const { actions } = useAnimations(animations, group);

  useEffect(() => {
    const clipName = POSE_TO_CLIP[pose] ?? POSE_TO_CLIP.zen;
    const action = actions[clipName];
    if (!action) {
      // Clip not found — fall back to whatever's available
      const fallback = Object.values(actions)[0];
      fallback?.reset().fadeIn(0.4).play();
      return () => {
        fallback?.fadeOut(0.4);
      };
    }
    action.reset().fadeIn(0.4).play();
    return () => {
      action.fadeOut(0.4);
    };
  }, [pose, actions]);

  // Subtle ambient rotation
  useFrame((_, delta) => {
    if (group.current) {
      group.current.rotation.y += delta * 0.06;
    }
  });

  return (
    <group ref={group} dispose={null}>
      <primitive object={scene} />
    </group>
  );
}

function Scene({ pose }: { pose: string }) {
  return (
    <>
      <ambientLight intensity={0.4} color="#FFFFFF" />
      <directionalLight position={[3, 5, 2]} intensity={1.2} color="#FFFFFF" />
      <directionalLight position={[-3, 2, 1]} intensity={0.4} color="#E5B547" />
      <Suspense fallback={null}>
        <AstronautModel pose={pose} />
        <Environment preset="studio" />
      </Suspense>
    </>
  );
}

interface Props {
  pose?: "zen" | "pointing" | "waving" | "floating";
  size?: number;
  className?: string;
  enableControls?: boolean;
  /** When true, use the 3D model. Default: true. Set false during v0.17.0 (no GLB yet). */
  use3D?: boolean;
}

export function AgentCharacter3D({
  pose = "zen",
  size = 420,
  className = "",
  enableControls = false,
  use3D = false, // default off until v0.17.5 ships the GLB
}: Props) {
  // Fallback to 2D in any of these conditions:
  if (!use3D) return <AgentCharacter pose={pose === "waving" || pose === "floating" ? "zen" : pose} size={size} className={className} />;

  if (typeof window !== "undefined") {
    if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) {
      return <AgentCharacter pose={pose === "waving" || pose === "floating" ? "zen" : pose} size={size} className={className} />;
    }
    // WebGL availability check
    try {
      const canvas = document.createElement("canvas");
      if (!canvas.getContext("webgl2") && !canvas.getContext("webgl")) {
        return <AgentCharacter pose={pose === "waving" || pose === "floating" ? "zen" : pose} size={size} className={className} />;
      }
    } catch {
      return <AgentCharacter pose={pose === "waving" || pose === "floating" ? "zen" : pose} size={size} className={className} />;
    }
  }

  return (
    <div
      className={`relative ${className}`}
      style={{ width: size, height: size }}
    >
      {/* Gold halo behind the character */}
      <div
        aria-hidden
        className="absolute inset-0 -z-10 rounded-full blur-3xl"
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(229, 181, 71, 0.35) 0%, rgba(229, 181, 71, 0) 60%)",
        }}
      />
      <Canvas
        camera={{ position: [0, 0.5, 3.5], fov: 35 }}
        gl={{ antialias: true, alpha: true, preserveDrawingBuffer: false }}
        dpr={[1, 2]}
      >
        <Scene pose={pose} />
        {enableControls && <OrbitControls enablePan={false} enableZoom={false} />}
      </Canvas>
    </div>
  );
}

// Preload the GLB so the first render doesn't pop
if (typeof window !== "undefined") {
  // Don't preload until the file actually exists; v0.17.5 will set use3D=true sites-wide
  // useGLTF.preload(GLB_PATH);
}
