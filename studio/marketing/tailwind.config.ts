import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx,mdx}",
    "./components/**/*.{ts,tsx}",
    "./content/**/*.{md,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50:  "#FBF3E0",
          100: "#F7E5B5",
          200: "#F2D27D",
          300: "#ECC050",
          bright: "#F2C76A",
          DEFAULT: "#E5B547",
          deep:    "#B8861E",
          shadow:  "#6B4F11",
        },
        ink: {
          DEFAULT: "#000000",
          stage:   "#0A0A0A",
          velvet:  "#141414",
          edge:    "#1F1F1F",
        },
        silver: {
          DEFAULT: "#D4D4D4",
          soft:    "#A3A3A3",
          dim:     "#6B6B6B",
        },
      },
      fontFamily: {
        display: ['var(--font-display)', "Geist", "Inter Display", "Inter", "system-ui", "sans-serif"],
        sans:    ['var(--font-sans)', "Geist", "Inter", "system-ui", "sans-serif"],
        mono:    ['var(--font-mono)', "Geist Mono", "JetBrains Mono", "monospace"],
      },
      transitionTimingFunction: {
        cinematic: "cubic-bezier(0.16, 1, 0.3, 1)",
        "soft-in": "cubic-bezier(0.4, 0, 0.6, 1)",
      },
      transitionDuration: {
        cinematic: "900ms",
        stage:     "1600ms",
      },
      boxShadow: {
        glint: "0 0 24px rgb(229 181 71 / 0.4)",
        "glint-strong": "0 0 64px rgb(229 181 71 / 0.6)",
        focus: "0 0 0 2px #000, 0 0 0 4px #E5B547",
      },
      keyframes: {
        breathe: {
          "0%, 100%": { transform: "translateY(0px)", filter: "drop-shadow(0 0 24px rgba(229,181,71,0.3))" },
          "50%":      { transform: "translateY(-6px)", filter: "drop-shadow(0 0 32px rgba(229,181,71,0.5))" },
        },
        glint: {
          "0%, 100%": { opacity: "0.6" },
          "50%":      { opacity: "1" },
        },
        "fade-up": {
          from: { opacity: "0", transform: "translateY(24px)" },
          to:   { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        breathe: "breathe 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        glint:   "glint 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-up": "fade-up 900ms cubic-bezier(0.16, 1, 0.3, 1) both",
      },
    },
  },
};

export default config;
