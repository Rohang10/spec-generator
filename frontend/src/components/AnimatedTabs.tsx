"use client";

import { motion } from "framer-motion";

export default function AnimatedTabs({
  tabs,
  active,
  setActive,
}: {
  tabs: string[];
  active: string;
  setActive: (t: string) => void;
}) {
  return (
    <div
      className="
        flex gap-2 mb-5 p-1 rounded-full
        bg-slate-100 dark:bg-white/5
        text-(--text)
      "
    >
      {tabs.map((tab) => {
        const isActive = active === tab;

        return (
          <button
            key={tab}
            onClick={() => setActive(tab)}
            className="relative px-4 py-2 rounded-full"
          >
            {isActive && (
              <motion.div
                layoutId="active-tab"
                className="absolute inset-0 rounded-full bg-indigo-600 shadow-md"
                transition={{ type: "spring", stiffness: 350, damping: 30 }}
              />
            )}

            <span
              className={`relative z-10 font-medium transition-colors
                ${
                  isActive
                    ? "text-white"
                    : "hover:text-indigo-600 dark:hover:text-indigo-400"
                }
              `}
            >
              {tab}
            </span>
          </button>
        );
      })}
    </div>
  );
}
