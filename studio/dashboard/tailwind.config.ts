import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        gold: {
          50: "#FBF3E0", 100: "#F7E5B5", 200: "#F2D27D", 300: "#ECC050",
          bright: "#F2C76A", DEFAULT: "#E5B547", deep: "#B8861E", shadow: "#6B4F11",
        },
        ink: { DEFAULT: "#000000", stage: "#0A0A0A", velvet: "#141414", edge: "#1F1F1F" },
        silver: { DEFAULT: "#D4D4D4", soft: "#A3A3A3", dim: "#6B6B6B" },
      },
      fontFamily: {
        display: ["Geist", "Inter Display", "Inter", "system-ui", "sans-serif"],
        sans: ["Geist", "Inter", "system-ui", "sans-serif"],
        mono: ["Geist Mono", "JetBrains Mono", "monospace"],
      },
      transitionTimingFunction: { cinematic: "cubic-bezier(0.16, 1, 0.3, 1)" },
      boxShadow: {
        glint: "0 0 24px rgb(229 181 71 / 0.4)",
        focus: "0 0 0 2px #000, 0 0 0 4px #E5B547",
      },
      keyframes: {
        pulse: { "0%,100%": { opacity: "0.8" }, "50%": { opacity: "1" } },
      },
      animation: { "subtle-pulse": "pulse 3s ease-in-out infinite" },
    },
  },
};
export default config;
