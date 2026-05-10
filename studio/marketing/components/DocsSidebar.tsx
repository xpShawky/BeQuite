"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarItem {
  slug: string;
  title: string;
  order: number;
}

interface Props {
  docs: SidebarItem[];
}

export function DocsSidebar({ docs }: Props) {
  const pathname = usePathname();

  return (
    <aside className="sticky top-20 hidden h-[calc(100vh-5rem)] w-64 shrink-0 overflow-y-auto border-r border-ink-edge px-2 py-8 lg:block">
      <p className="mb-4 px-3 text-xs font-medium uppercase tracking-[0.3em] text-gold">
        Docs
      </p>
      <nav>
        <ul className="space-y-1">
          {docs.map((doc) => {
            const href = `/docs/${doc.slug}`;
            const active = pathname === href;
            return (
              <li key={doc.slug}>
                <Link
                  href={href}
                  className={`block rounded-md px-3 py-2 text-sm transition-colors duration-cinematic ease-cinematic ${
                    active
                      ? "bg-ink-stage text-gold"
                      : "text-silver-soft hover:bg-ink-stage hover:text-silver"
                  }`}
                >
                  {doc.title}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      <div className="mt-8 border-t border-ink-edge pt-6 px-3">
        <p className="text-xs text-silver-dim">
          More coming. PRs welcome on{" "}
          <Link
            href="https://github.com/xpShawky/BeQuite"
            target="_blank"
            rel="noopener noreferrer"
            className="text-silver hover:text-gold"
          >
            GitHub
          </Link>
          .
        </p>
      </div>
    </aside>
  );
}
