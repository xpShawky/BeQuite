import { Nav } from "@/components/Nav";
import { Hero } from "@/components/Hero";
import { PhasesScroll } from "@/components/PhasesScroll";
import { Features } from "@/components/Features";
import { Demo } from "@/components/Demo";
import { CTA } from "@/components/CTA";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="overflow-x-hidden">
        <Hero />
        <PhasesScroll />
        <Features />
        <Demo />
        <CTA />
      </main>
      <Footer />
    </>
  );
}
