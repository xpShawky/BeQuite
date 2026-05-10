"use client";

import Link from "next/link";
import Image from "next/image";

export function Footer() {
  return (
    <footer className="border-t border-ink-edge bg-ink py-16">
      <div className="mx-auto max-w-[1400px] px-6 lg:px-10">
        <div className="grid grid-cols-1 gap-12 md:grid-cols-4">
          <div className="md:col-span-2">
            <Image
              src="/brand/05-logo-horizontal.png"
              alt="BeQuite"
              width={160}
              height={40}
              className="h-9 w-auto"
            />
            <p className="mt-6 max-w-sm text-sm text-silver-soft text-pretty">
              The AI project operating system. Plans, builds, tests, reviews,
              recovers, and ships projects with fewer errors.
            </p>
            <p className="mt-4 text-xs text-silver-dim">
              v0.16.0 · MIT · by{" "}
              <Link
                href="https://github.com/xpShawky"
                target="_blank"
                rel="noopener noreferrer"
                className="text-silver-soft hover:text-gold"
              >
                Ahmed Shawky (xpShawky)
              </Link>
            </p>
          </div>

          <div>
            <h3 className="font-mono text-xs uppercase tracking-[0.3em] text-gold">
              Product
            </h3>
            <ul className="mt-4 space-y-3 text-sm text-silver-soft">
              <li>
                <Link href="#how-it-works" className="hover:text-silver">
                  How it works
                </Link>
              </li>
              <li>
                <Link href="#features" className="hover:text-silver">
                  Features
                </Link>
              </li>
              <li>
                <Link href="#demo" className="hover:text-silver">
                  Demo
                </Link>
              </li>
              <li>
                <Link href="/docs/quickstart" className="hover:text-silver">
                  Quickstart
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-mono text-xs uppercase tracking-[0.3em] text-gold">
              Resources
            </h3>
            <ul className="mt-4 space-y-3 text-sm text-silver-soft">
              <li>
                <Link
                  href="https://github.com/xpShawky/BeQuite"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-silver"
                >
                  GitHub
                </Link>
              </li>
              <li>
                <Link
                  href="https://github.com/xpShawky/BeQuite/blob/main/.bequite/memory/constitution.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-silver"
                >
                  The Constitution
                </Link>
              </li>
              <li>
                <Link
                  href="https://github.com/xpShawky/BeQuite/blob/main/CHANGELOG.md"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-silver"
                >
                  Changelog
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}
