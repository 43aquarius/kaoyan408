"use client";

import { useEffect } from "react";
import { useApp, type View } from "@/lib/store";
import { ReadingProgress } from "@/components/site/progress-bar";
import { Navbar } from "@/components/site/navbar";
import { Footer } from "@/components/site/footer";
import { HomeView } from "@/components/views/home";
import { LibraryView } from "@/components/views/library";
import { PracticeView } from "@/components/views/practice";
import { MockView } from "@/components/views/mock";
import { WrongBookView } from "@/components/views/wrong-book";
import { StatsView } from "@/components/views/stats";
import { NotesView } from "@/components/views/notes";

const VIEWS: Record<View, React.ComponentType> = {
  home: HomeView,
  library: LibraryView,
  practice: PracticeView,
  mock: MockView,
  wrong: WrongBookView,
  stats: StatsView,
  notes: NotesView,
};

export default function Page() {
  const view = useApp((s) => s.view);

  // 支持 ?v=xxx 直达 & 浏览器前进后退
  useEffect(() => {
    const applyFromUrl = () => {
      const v = new URLSearchParams(window.location.search).get("v") as View | null;
      if (v && v in VIEWS && v !== "practice") {
        useApp.setState({ view: v });
      } else if (!v) {
        useApp.setState({ view: "home" });
      }
    };
    applyFromUrl();
    window.addEventListener("popstate", applyFromUrl);
    return () => window.removeEventListener("popstate", applyFromUrl);
  }, []);

  const Active = VIEWS[view] ?? HomeView;

  return (
    <div className="flex min-h-screen flex-col">
      <ReadingProgress />
      <Navbar />
      <main className="flex-1">
        <Active />
      </main>
      <Footer />
    </div>
  );
}
