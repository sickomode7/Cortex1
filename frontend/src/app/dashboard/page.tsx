"use client";

import { useEffect, useState, useRef } from "react";
import { useUser, UserButton } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Map, ArrowRight, BookOpen, Zap } from "lucide-react";
import { Toaster, toast } from "sonner";
import api from "@/lib/api";
import { useAuthStore } from "@/store/useAuthStore";
import ProgressRing from "@/components/dashboard/ProgressRing";
import RoadmapModal, { PathItem } from "@/components/dashboard/RoadmapModal";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { ActivityHeatmap } from "@/components/dashboard/ActivityHeatmap";
import { AccuracyTrendChart } from "@/components/dashboard/AccuracyTrendChart";
import { XPBar } from "@/components/dashboard/XPBar";
import { BadgeShelf } from "@/components/dashboard/BadgeShelf";

interface DailyActivity {
  date: string;
  quizzes_taken: number;
  lessons_completed: number;
  avg_accuracy: number | null;
}

interface DashboardData {
  user_id: string;
  domain_key: string;
  total_concepts_mastered: number;
  total_concepts_in_domain: number;
  overall_progress_percentage: number;
  mastery_map: any[];
  weak_areas: any[];
  next_action?: any;
  current_streak_days?: number;
  total_xp?: number;
  level?: number;
  badges?: string[];
  new_badges?: string[];
}

export default function DashboardPage() {
  const { user, isLoaded } = useUser();
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);

  const [syncState, setSyncState] = useState<"syncing" | "done" | "error">("syncing");
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [activityHistory, setActivityHistory] = useState<DailyActivity[]>([]);
  const [pathItems, setPathItems] = useState<PathItem[]>([]);
  const [showRoadmap, setShowRoadmap] = useState(false);
  const hasSynced = useRef(false);

  useEffect(() => {
    if (!isLoaded || !user) return;
    if (hasSynced.current) return;
    hasSynced.current = true;

    async function syncAndLoad() {
      try {
        const email = user!.primaryEmailAddress?.emailAddress ?? "";
        const name = user!.fullName ?? "User";

        const syncRes = await api.post("/users/sync", {
          email,
          full_name: name,
          auth_provider: "clerk",
          auth_subject: user!.id,
        });

        const { user: dbUser, is_onboarded } = syncRes.data;
        setAuth(dbUser.id, email, name);

        if (!is_onboarded) {
          router.push("/onboarding");
          return;
        }

        toast.success("Signed in successfully", {
          description: `Welcome back, ${user!.firstName}.`,
          duration: 3000,
        });

        try {
          const [overviewRes, pathRes, historyRes] = await Promise.all([
            api.get(`/dashboard/overview`),
            api.get(`/curriculum/users/${dbUser.id}/active-path`),
            api.get(`/dashboard/activity-history`).catch(() => ({ data: [] })),
          ]);
          setDashboardData(overviewRes.data);
          setPathItems(pathRes.data.items || []);
          setActivityHistory(historyRes.data || []);

          if (overviewRes.data.new_badges && overviewRes.data.new_badges.length > 0) {
            overviewRes.data.new_badges.forEach((b: string) => {
              toast.success("New Badge Earned!", { description: `You unlocked the ${b} badge.`, duration: 5000 });
            });
          }

          // Auto-show roadmap only on first visit (tracked in localStorage)
          const key = `cortex_roadmap_seen_${dbUser.id}`;
          if (!localStorage.getItem(key)) {
            localStorage.setItem(key, "true");
            setTimeout(() => setShowRoadmap(true), 800); // slight delay so dashboard renders first
          }
        } catch (err: any) {
          console.error("Failed to load dashboard data:", err);
        }

        setSyncState("done");
      } catch (err: any) {
        console.error("Sync failed:", err);
        setSyncState("error");
      }
    }

    syncAndLoad();
  }, [user, isLoaded, setAuth, router]);

  // ── Next active item (in_progress = unlocked, pending = locked) ──
  // If there are multiple unlocked nodes (e.g., a REVIEW node and a new LEARN node),
  // we prioritize showing the new LEARN node as "Up Next" to encourage forward momentum.
  const inProgressItems = pathItems.filter((i) => i.status === "in_progress");
  const nextItem = inProgressItems.find((i) => i.item_type === "learn") 
                   ?? inProgressItems[0] 
                   ?? pathItems.find((i) => i.status === "pending");
  const completedCount = pathItems.filter((i) => i.status === "completed").length;

  if (!isLoaded || syncState === "syncing") {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center text-foreground">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-500 mb-4" />
        <p className="text-zinc-400 text-sm animate-pulse tracking-widest uppercase">
          Synchronizing Cortex Engine...
        </p>
      </div>
    );
  }

  if (syncState === "error") {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center text-foreground">
        <p className="text-red-400 text-sm">Failed to connect to Cortex. Please refresh.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      <Toaster position="top-center" theme="dark" />

      {/* ── Top Nav ── */}
      <header className="flex justify-between items-center px-8 py-5 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="bg-foreground text-background w-7 h-7 rounded-full flex items-center justify-center font-serif italic font-bold text-sm">
            C
          </div>
          <span className="font-serif text-lg tracking-tight">Cortex</span>
        </div>
        <div className="flex items-center gap-4">
          {pathItems.length > 0 && (
            <button
              onClick={() => setShowRoadmap(true)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl border border-border bg-background hover:bg-accent text-sm font-medium text-muted-foreground hover:text-foreground transition-all duration-200"
            >
              <Map className="w-4 h-4 text-indigo-400" />
              View Roadmap
            </button>
          )}
          <ThemeToggle />
          <UserButton />
        </div>
      </header>

      {/* ── Dashboard Content ── */}
      <main className="max-w-5xl mx-auto px-8 py-16">
        {/* Hero Row */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <h1 className="font-serif text-5xl md:text-6xl tracking-tight mb-4">
              Welcome back,{" "}
              <span className="italic">{user?.firstName ?? "Learner"}</span>.
            </h1>
            <p className="text-zinc-500 text-lg">
              {dashboardData?.total_concepts_in_domain
                ? `Your curriculum is calibrated and ready.`
                : `Preparing your learning path...`}
            </p>
          </motion.div>

          {dashboardData && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
              className="flex items-center gap-6"
            >
              <div className="text-right hidden sm:block">
                <p className="text-foreground font-medium text-lg">Overall Progress</p>
                <p className="text-zinc-500 text-sm">
                  {dashboardData.total_concepts_mastered} of {dashboardData.total_concepts_in_domain} concepts mastered
                </p>
              </div>
              <ProgressRing percentage={dashboardData.overall_progress_percentage} size={110} strokeWidth={8} />
            </motion.div>
          )}
        </div>

        {/* ── Action Cards Grid ── */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          {/* Next Lesson Card */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="md:col-span-2"
          >
            {syncState === "done" && nextItem ? (
              <button
                onClick={() => router.push(`/lesson?conceptId=${nextItem.concept_id}`)}
                className="group w-full text-left relative rounded-3xl border border-white/10 bg-white/[0.03] hover:bg-white/[0.06] hover:border-white/20 p-7 transition-all duration-300 overflow-hidden"
              >
                {/* Glow */}
                <div className="absolute top-0 right-0 w-48 h-48 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none" />

                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                    <p className="text-xs font-bold tracking-widest text-indigo-400 uppercase">Up Next</p>
                  </div>
                  <h2 className="font-serif text-2xl text-foreground mb-2">{nextItem.concept_name}</h2>
                  <p className="text-zinc-500 text-sm mb-6">
                    {nextItem.item_type === "quiz"
                      ? "Complete this quiz to unlock your next topic"
                      : "Interactive lesson with code examples and exercises"}
                  </p>
                  <div className="inline-flex items-center gap-2 bg-indigo-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl group-hover:bg-indigo-500 transition-colors">
                    {nextItem.item_type === "quiz" ? <Zap className="w-4 h-4" /> : <BookOpen className="w-4 h-4" />}
                    {nextItem.item_type === "quiz" ? "Take Quiz" : "Start Lesson"}
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </div>
              </button>
            ) : syncState === "done" ? (
              <div className="rounded-3xl border border-white/5 bg-white/[0.02] p-8 text-center h-full flex flex-col items-center justify-center gap-3">
                <p className="text-zinc-400 text-sm">No active lessons found.</p>
                <p className="text-zinc-600 text-xs">Try generating your curriculum again.</p>
              </div>
            ) : (
              <div className="rounded-3xl border border-white/5 bg-white/[0.02] p-8 text-center h-full flex items-center justify-center">
                <Loader2 className="w-5 h-5 animate-spin text-zinc-600" />
              </div>
            )}
          </motion.div>

          {/* Stats Column */}
          <div className="flex flex-col gap-5">
            {/* Progress stat */}
            <motion.div
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.4 }}
              className="rounded-3xl border border-white/8 bg-white/[0.02] p-6 flex-1"
            >
              <p className="text-xs font-bold tracking-widest text-zinc-500 uppercase mb-3">Progress</p>
              <p className="font-serif text-4xl text-foreground mb-1">{completedCount}</p>
              <p className="text-zinc-500 text-sm">of {pathItems.length} concepts mastered</p>
            </motion.div>

            {/* View roadmap CTA */}
            <motion.button
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.5 }}
              onClick={() => setShowRoadmap(true)}
              className="group rounded-3xl border border-indigo-500/20 bg-indigo-500/5 hover:bg-indigo-500/10 hover:border-indigo-500/40 p-6 text-left transition-all duration-300"
            >
              <Map className="w-6 h-6 text-indigo-400 mb-3 group-hover:scale-110 transition-transform" />
              <p className="font-semibold text-foreground text-sm mb-1">View Full Roadmap</p>
              <p className="text-zinc-500 text-xs">See all {pathItems.length} topics in your path</p>
            </motion.button>
          </div>
        </div>

        {/* ── Active Mastery Progress ── */}
        {dashboardData && dashboardData.mastery_map.length > 0 && (
          <div className="mt-12">
            <h3 className="font-serif text-2xl text-foreground mb-6">Your Mastery</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dashboardData.mastery_map.map((item: any) => {
                const pct = Math.round(item.mastery_score * 100);
                const isWeak = dashboardData.weak_areas.some((w: any) => w.concept_id === item.concept_id);
                return (
                  <div key={item.concept_id} className={`rounded-2xl border bg-white/[0.02] p-5 ${isWeak ? 'border-amber-500/20' : 'border-white/5'}`}>
                    <div className="flex justify-between items-end mb-3">
                      <div>
                        <h4 className="font-semibold text-foreground text-base">{item.concept_name}</h4>
                        {isWeak && <span className="text-amber-500 text-[10px] font-bold uppercase tracking-widest mt-1 inline-block">Needs Review</span>}
                      </div>
                      <span className={`text-sm font-bold ${isWeak ? 'text-amber-500' : 'text-indigo-400'}`}>{pct}%</span>
                    </div>
                    <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                        className={`h-full rounded-full ${isWeak ? 'bg-amber-500' : 'bg-indigo-500'}`} 
                      />
                    </div>
                    {item.quiz_accuracy !== null && (
                      <p className="text-xs text-zinc-500 mt-3 flex justify-between">
                        <span>Latest quiz accuracy:</span>
                        <span className="text-zinc-400">{Math.round(item.quiz_accuracy * 100)}%</span>
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── Gamification & Activity ── */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col gap-8">
            <div className="rounded-2xl border bg-white/[0.02] border-white/5 p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-serif text-xl text-foreground">XP & Level</h3>
                {dashboardData?.current_streak_days ? (
                  <div className="text-sm font-medium text-amber-500 bg-amber-500/10 px-3 py-1 rounded-full flex items-center gap-1">
                    🔥 {dashboardData.current_streak_days} Day Streak
                  </div>
                ) : null}
              </div>
              <XPBar level={dashboardData?.level || 0} total_xp={dashboardData?.total_xp || 0} />
            </div>
            <div className="rounded-2xl border bg-white/[0.02] border-white/5 p-6">
              <BadgeShelf badges={dashboardData?.badges || []} />
            </div>
          </div>
          <div className="flex flex-col gap-8">
             <div className="rounded-2xl border bg-white/[0.02] border-white/5 p-6">
               <ActivityHeatmap data={activityHistory} />
             </div>
             <div className="rounded-2xl border bg-white/[0.02] border-white/5 p-6">
               <AccuracyTrendChart data={activityHistory} />
             </div>
          </div>
        </div>
      </main>

      {/* ── Roadmap Modal ── */}
      <AnimatePresence>
        {showRoadmap && pathItems.length > 0 && (
          <RoadmapModal items={pathItems} onClose={() => setShowRoadmap(false)} />
        )}
      </AnimatePresence>
    </div>
  );
}
