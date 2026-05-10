import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const DOCS_DIR = path.join(process.cwd(), "content", "docs");

export interface DocFrontmatter {
  title: string;
  slug: string;
  order: number;
  description: string;
}

export interface Doc {
  frontmatter: DocFrontmatter;
  content: string;
  slug: string;
}

export function getAllDocSlugs(): string[] {
  if (!fs.existsSync(DOCS_DIR)) return [];
  return fs
    .readdirSync(DOCS_DIR)
    .filter((f) => f.endsWith(".mdx"))
    .map((f) => f.replace(/\.mdx$/, ""));
}

export function getDoc(slug: string): Doc | null {
  const file = path.join(DOCS_DIR, `${slug}.mdx`);
  if (!fs.existsSync(file)) return null;
  const raw = fs.readFileSync(file, "utf8");
  const { data, content } = matter(raw);
  return {
    frontmatter: data as DocFrontmatter,
    content,
    slug,
  };
}

export function getAllDocs(): Doc[] {
  return getAllDocSlugs()
    .map((slug) => getDoc(slug)!)
    .filter(Boolean)
    .sort(
      (a, b) =>
        (a.frontmatter.order ?? 99) - (b.frontmatter.order ?? 99),
    );
}
