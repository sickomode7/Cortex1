"use client";

import { motion } from "framer-motion";
import { Check, Lock, BookOpen, Code2, Zap, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";

export interface PathItem {
  id: string;
  concept_id: string;
  concept_slug: string;
  concept_name: string;
  position: number;
  item_type: "module" | "lesson" | "quiz";
  status: "locked" | "active" | "completed";
}

interface SkillTreeProps {
  items: PathItem[];
}

const TYPE_CONFIG = {
  lesson: { label: "Lesson", color: "#6366f1", dimColor: "#312e81", icon: Code2 },
  quiz:   { label: "Quiz",   color: "#8b5cf6", dimColor: "#3b0764", icon: Zap },
  module: { label: "Module", color: "#06b6d4", dimColor: "#164e63", icon: BookOpen },
};

export default function SkillTree({ items }: SkillTreeProps) {
  const router = useRouter();

  const handleClick = (item: PathItem) => {
    if (item.status === "locked") return;
    router.push(`/lesson/${item.concept_id}`);
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      {/* Vertical spine */}
      <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-px bg-white/[0.06] md:-translate-x-1/2" />

      <div className="space-y-2 pb-16">
        {items.map((item, idx) => {
          const isCompleted = item.status === "completed";
          const isActive = item.status === "active";
          const isLocked = item.status === "locked";
          const cfg = TYPE_CONFIG[item.item_type] ?? TYPE_CONFIG.lesson;
          const Icon = cfg.icon;

          // On desktop, odd items go right, even items go left
          const isRight = idx % 2 !== 0;

          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.08, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
              className={`relative flex items-center gap-0 ${
                isRight ? "md:flex-row-reverse" : "md:flex-row"
              } flex-row`}
            >
              {/* ── Spacer (desktop only, takes up half the width) ── */}
              <div className="hidden md:block md:w-1/2" />

              {/* ── Central node dot ── */}
              <div className="relative z-10 flex items-center justify-center flex-shrink-0 ml-0 md:ml-0"
                style={{ width: 64, minWidth: 64 }}
              >
                <div
                  className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                    isLocked ? "opacity-30" : ""
                  }`}
                  style={{
                    background: isCompleted
                      ? "linear-gradient(135deg, #10b981, #059669)"
                      : isActive
                      ? `linear-gradient(135deg, ${cfg.color}, ${cfg.dimColor})`
                      : "#18181b",
                    border: isActive
                      ? `2px solid ${cfg.color}60`
                      : isCompleted
                      ? "2px solid #10b98140"
                      : "2px solid #27272a",
                    boxShadow: isActive
                      ? `0 0 24px ${cfg.color}40, 0 4px 12px rgba(0,0,0,0.5)`
                      : isCompleted
                      ? "0 0 16px rgba(16,185,129,0.25)"
                      : "none",
                  }}
                >
                  {isCompleted
                    ? <Check className="w-6 h-6 text-white" strokeWidth={2.5} />
                    : isLocked
                    ? <Lock className="w-5 h-5 text-zinc-600" />
                    : <Icon className="w-6 h-6 text-white" />
                  }
                </div>

                {/* Active pulse */}
                {isActive && (
                  <div
                    className="absolute inset-0 rounded-2xl animate-ping pointer-events-none"
                    style={{ background: `${cfg.color}20` }}
                  />
                )}
              </div>

              {/* ── Content card ── */}
              <div className={`flex-1 min-w-0 pl-4 md:pl-0 ${isRight ? "md:pr-6 md:pl-0" : "md:pl-6"} py-3`}>
                <button
                  onClick={() => handleClick(item)}
                  disabled={isLocked}
                  className={`group w-full text-left rounded-2xl border transition-all duration-300 ${
                    isActive
                      ? "border-white/15 bg-white/[0.04] hover:bg-white/[0.07] hover:border-white/25 cursor-pointer"
                      : isCompleted
                      ? "border-white/8 bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/15 cursor-pointer"
                      : "border-transparent bg-transparent cursor-not-allowed opacity-35"
                  } p-5`}
                >
                  <div className={`flex items-start justify-between gap-3 ${isRight ? "md:flex-row-reverse" : ""}`}>
                    <div className={`flex-1 ${isRight ? "md:text-right" : ""}`}>
                      {/* Type badge */}
                      <div className={`inline-flex items-center gap-1.5 mb-2 px-2 py-0.5 rounded-full text-[10px] font-bold tracking-widest uppercase ${isRight ? "md:flex-row-reverse" : ""}`}
                        style={{
                          background: isActive || isCompleted ? `${cfg.color}18` : "transparent",
                          color: isActive || isCompleted ? cfg.color : "#52525b",
                          border: `1px solid ${isActive || isCompleted ? cfg.color + "30" : "#27272a"}`,
                        }}
                      >
                        <Icon className="w-3 h-3" />
                        {cfg.label} · {idx + 1}
                      </div>

                      {/* Title */}
                      <h3 className={`font-semibold text-base leading-snug ${
                        isActive ? "text-white" : isCompleted ? "text-zinc-200" : "text-zinc-600"
                      }`}>
                        {item.concept_name}
                      </h3>

                      {/* Subtitle */}
                      {isActive && (
                        <p className="text-sm text-zinc-400 mt-1">
                          Your next lesson is ready
                        </p>
                      )}
                      {isCompleted && (
                        <p className="text-sm text-emerald-500 mt-1 font-medium">
                          ✓ Mastered
                        </p>
                      )}
                    </div>

                    {/* CTA Arrow (active & completed only) */}
                    {(isActive || isCompleted) && (
                      <div className={`flex-shrink-0 self-center w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 group-hover:scale-110 ${isRight ? "md:hidden lg:hidden" : ""}`}
                        style={{
                          background: isActive ? `${cfg.color}25` : "#10b98120",
                          color: isActive ? cfg.color : "#10b981",
                        }}
                      >
                        <ArrowRight className="w-4 h-4" />
                      </div>
                    )}
                  </div>

                  {/* "Start Now" bar for active */}
                  {isActive && (
                    <div className="mt-4 pt-4 border-t border-white/[0.06] flex items-center justify-between">
                      <span className="text-xs text-zinc-500">
                        {item.item_type === "quiz" ? "Answer questions to unlock next topic" : "Read, code, and practice"}
                      </span>
                      <span
                        className="text-xs font-bold uppercase tracking-wider"
                        style={{ color: cfg.color }}
                      >
                        Start →
                      </span>
                    </div>
                  )}
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
