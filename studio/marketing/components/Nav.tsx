"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import Link from "next/link";
import Image from "next/image";

export function Nav() {
  const { scrollY } = useScroll();
  const bg = useTransform(
    scrollY,
    [0, 80],
    ["rgba(0,0,0,0)", "rgba(10,10,10,0.85)"],
  );
  const border = useTransform(
    scrollY,
    [0, 80],
    ["rgba(31,31,31,0)", "rgba(31,31,31,1)"],
  );

  return (
    <motion.header
      style={{ background: bg, borderColor: border }}
      className="fixed inset-x-0 top-0 z-50 backdrop-blur-md border-b transition-colors"
    >
      <nav className="mx-auto flex max-w-[1400px] items-center justify-between gap-8 px-6 py-4 lg:px-10">
        <Link href="/" className="group flex items-center gap-2.5">
          <Image
            src="/brand/05-logo-horizontal.png"
            alt="BeQuite"
            width={140}
            height={36}
            priority
            className="h-7 w-auto"
          />
        </Link>

        <ul className="hidden items-center gap-8 text-[15px] text-silver-soft md:flex">
          <li>
            <Link
              className="transition-colors duration-cinematic ease-cinematic hover:text-silver"
              href="#how-it-works"
            >
              How it works
            </Link>
          </li>
          <li>
            <Link
              className="transition-colors duration-cinematic ease-cinematic hover:text-silver"
              href="#features"
            >
              Features
            </Link>
          </li>
          <li>
            <Link
              className="transition-colors duration-cinematic ease-cinematic hover:text-silver"
              href="#demo"
            >
              Demo
            </Link>
          </li>
          <li>
            <Link
              className="transition-colors duration-cinematic ease-cinematic hover:text-silver"
              href="https://github.com/xpShawky/BeQuite"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </Link>
          </li>
        </ul>

        <Link
          href="#cta"
          className="rounded-full bg-gold px-5 py-2 text-sm font-medium text-ink transition-all duration-cinematic ease-cinematic hover:bg-gold-bright hover:shadow-glint"
        >
          Get BeQuite
        </Link>
      </nav>
    </motion.header>
  );
}
