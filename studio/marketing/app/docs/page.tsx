import Link from "next/link";
import { getAllDocs } from "@/lib/docs";

export const metadata = {
  title: "Docs — BeQuite",
  description:
    "Vibecoder-friendly tutorials for BeQuite. Quickstart, from-scratch, retrofit, multi-model planning, auto-mode, troubleshooting.",
};

export default function DocsIndex() {
  const docs = getAllDocs();

  return (
    <article className="prose-invert max-w-none">
      <header className="mb-12">
        <p className="mb-3 text-xs font-medium uppercase tracking-[0.3em] text-gold">
          Documentation
        </p>
        <h1 className="font-display text-display font-bold leading-[1.05] tracking-tight text-balance text-silver">
          Pick your path.
        </h1>
        <p className="mt-6 max-w-2xl text-body-lg text-silver-soft text-pretty">
          Tutorials are written for vibecoders — no prior CLI or backend
          experience required. Pick the one closest to what you're trying to do.
        </p>
      </header>

      <ul className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {docs.map((doc) => (
          <li key={doc.slug}>
            <Link
              href={`/docs/${doc.slug}`}
              className="group block rounded-2xl border border-ink-edge bg-ink-stage p-6 transition-all duration-cinematic ease-cinematic hover:border-gold-deep hover:shadow-glint"
            >
              <span className="font-mono text-xs uppercase tracking-wider text-gold">
                {String(doc.frontmatter.order ?? 0).padStart(2, "0")}
              </span>
              <h2 className="mt-2 font-display text-h2 font-semibold text-silver group-hover:text-gold-bright">
                {doc.frontmatter.title}
              </h2>
              <p className="mt-3 text-sm text-silver-soft text-pretty">
                {doc.frontmatter.description}
              </p>
              <span className="mt-4 inline-flex items-center gap-1 text-sm text-gold">
                Read <span aria-hidden>→</span>
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </article>
  );
}
