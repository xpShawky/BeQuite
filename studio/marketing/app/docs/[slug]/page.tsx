import { notFound } from "next/navigation";
import Link from "next/link";
import { MDXRemote } from "next-mdx-remote/rsc";
import { getAllDocSlugs, getDoc, getAllDocs } from "@/lib/docs";

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getAllDocSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const doc = getDoc(slug);
  if (!doc) return { title: "Doc not found" };
  return {
    title: `${doc.frontmatter.title} — BeQuite`,
    description: doc.frontmatter.description,
  };
}

const mdxComponents = {
  h1: (props: any) => (
    <h1
      className="mt-12 mb-6 font-display text-display font-bold leading-[1.05] tracking-tight text-silver"
      {...props}
    />
  ),
  h2: (props: any) => (
    <h2
      className="mt-12 mb-4 font-display text-h1 font-semibold text-silver"
      {...props}
    />
  ),
  h3: (props: any) => (
    <h3
      className="mt-8 mb-3 font-display text-h2 font-semibold text-silver"
      {...props}
    />
  ),
  p: (props: any) => (
    <p className="my-4 text-body text-silver-soft leading-relaxed text-pretty" {...props} />
  ),
  ul: (props: any) => (
    <ul className="my-4 ml-6 list-disc text-body text-silver-soft" {...props} />
  ),
  ol: (props: any) => (
    <ol className="my-4 ml-6 list-decimal text-body text-silver-soft" {...props} />
  ),
  li: (props: any) => <li className="my-1.5" {...props} />,
  a: (props: any) => (
    <Link
      className="text-gold underline-offset-4 hover:underline"
      {...props}
    />
  ),
  blockquote: (props: any) => (
    <blockquote
      className="my-6 border-l-2 border-gold/40 bg-ink-stage/50 px-5 py-3 italic text-silver"
      {...props}
    />
  ),
  code: (props: any) => (
    <code
      className="rounded bg-ink-stage px-1.5 py-0.5 font-mono text-[0.9em] text-gold-bright"
      {...props}
    />
  ),
  pre: (props: any) => (
    <pre
      className="my-6 overflow-x-auto rounded-2xl border border-ink-edge bg-ink-stage p-5 font-mono text-sm leading-relaxed text-silver"
      {...props}
    />
  ),
  table: (props: any) => (
    <div className="my-6 overflow-x-auto">
      <table className="min-w-full border-separate border-spacing-0 rounded-lg border border-ink-edge text-sm" {...props} />
    </div>
  ),
  th: (props: any) => (
    <th
      className="border-b border-ink-edge bg-ink-velvet px-4 py-3 text-left font-medium text-silver"
      {...props}
    />
  ),
  td: (props: any) => (
    <td className="border-b border-ink-edge px-4 py-3 text-silver-soft" {...props} />
  ),
  hr: () => <hr className="my-12 border-ink-edge" />,
  strong: (props: any) => <strong className="font-semibold text-silver" {...props} />,
};

export default async function DocPage({ params }: Props) {
  const { slug } = await params;
  const doc = getDoc(slug);
  if (!doc) return notFound();

  const allDocs = getAllDocs();
  const currentIdx = allDocs.findIndex((d) => d.slug === slug);
  const prev = currentIdx > 0 ? allDocs[currentIdx - 1] : null;
  const next =
    currentIdx >= 0 && currentIdx < allDocs.length - 1
      ? allDocs[currentIdx + 1]
      : null;

  return (
    <article>
      <header className="mb-8 border-b border-ink-edge pb-6">
        <p className="mb-2 font-mono text-xs uppercase tracking-[0.3em] text-gold">
          {String(doc.frontmatter.order ?? 0).padStart(2, "0")} ·{" "}
          {doc.frontmatter.slug}
        </p>
        <h1 className="font-display text-h1 font-bold leading-tight tracking-tight text-balance text-silver md:text-display">
          {doc.frontmatter.title}
        </h1>
        <p className="mt-4 max-w-3xl text-body-lg text-silver-soft text-pretty">
          {doc.frontmatter.description}
        </p>
      </header>

      <div className="prose-invert max-w-none">
        <MDXRemote source={doc.content} components={mdxComponents} />
      </div>

      <nav className="mt-16 grid grid-cols-2 gap-4 border-t border-ink-edge pt-8">
        {prev ? (
          <Link
            href={`/docs/${prev.slug}`}
            className="group rounded-xl border border-ink-edge bg-ink-stage p-5 transition-colors duration-cinematic ease-cinematic hover:border-gold-deep"
          >
            <span className="text-xs uppercase tracking-wider text-silver-dim">
              ← Previous
            </span>
            <p className="mt-1 font-display text-h3 font-semibold text-silver group-hover:text-gold-bright">
              {prev.frontmatter.title}
            </p>
          </Link>
        ) : (
          <div />
        )}
        {next ? (
          <Link
            href={`/docs/${next.slug}`}
            className="group rounded-xl border border-ink-edge bg-ink-stage p-5 text-right transition-colors duration-cinematic ease-cinematic hover:border-gold-deep"
          >
            <span className="text-xs uppercase tracking-wider text-silver-dim">
              Next →
            </span>
            <p className="mt-1 font-display text-h3 font-semibold text-silver group-hover:text-gold-bright">
              {next.frontmatter.title}
            </p>
          </Link>
        ) : (
          <div />
        )}
      </nav>
    </article>
  );
}
