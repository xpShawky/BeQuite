import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BeQuite Studio — Dashboard",
  description: "BeQuite Studio operations console. Reads your BeQuite-managed projects' Memory Bank + receipts + state. Layer 2 Studio Edition.",
};

export const viewport: Viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-ink text-silver antialiased">{children}</body>
    </html>
  );
}
