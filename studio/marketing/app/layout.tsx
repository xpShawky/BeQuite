import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BeQuite — the AI project operating system",
  description:
    "BeQuite turns Claude (and peer coding agents) into a senior tech-lead capable of shipping software end-to-end. Spec-driven. Constitution-governed. Receipt-signed. Vibecoder-friendly.",
  metadataBase: new URL("https://bequite.dev"),
  openGraph: {
    title: "BeQuite — the AI project operating system",
    description:
      "Plan, build, test, review, recover, and ship projects with fewer errors. Multi-model planning. Auto-mode. 13 Doctrines.",
    type: "website",
    siteName: "BeQuite",
  },
  twitter: {
    card: "summary_large_image",
    creator: "@xpShawky",
  },
  authors: [{ name: "Ahmed Shawky", url: "https://github.com/xpShawky" }],
  keywords: [
    "ai-coding-agent",
    "claude",
    "claude-code",
    "vibe-coding",
    "spec-driven",
    "constitution",
    "doctrine",
    "memory-bank",
    "auto-mode",
    "multi-model-planning",
  ],
};

export const viewport: Viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-ink text-silver antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
