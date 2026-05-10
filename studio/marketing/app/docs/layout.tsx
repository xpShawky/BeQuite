import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";
import { DocsSidebar } from "@/components/DocsSidebar";
import { getAllDocs } from "@/lib/docs";

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const docs = getAllDocs().map((d) => ({
    slug: d.slug,
    title: d.frontmatter.title,
    order: d.frontmatter.order ?? 99,
  }));

  return (
    <>
      <Nav />
      <main className="mx-auto max-w-[1400px] px-6 pt-20 lg:px-10">
        <div className="flex gap-12">
          <DocsSidebar docs={docs} />
          <div className="min-w-0 flex-1 py-8 lg:py-12">{children}</div>
        </div>
      </main>
      <Footer />
    </>
  );
}
