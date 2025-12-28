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
        grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5
        gap-3 mb-5 p-2 rounded-xl
        bg-slate-100 dark:bg-white/5
        w-full
      "
    >
      {tabs.map((tab) => {
        const isActive = active === tab;

        return (
          <button
            key={tab}
            onClick={() => setActive(tab)}
            className="
              relative 
              px-2 sm:px-3 md:px-4
              py-2.5
              rounded-full
              text-xs sm:text-sm md:text-base
              font-medium
              transition-colors
              min-h-11
              flex items-center justify-center
            "
          >
            {isActive && (
              <motion.div
                layoutId="active-tab"
                className="absolute inset-0 rounded-full bg-indigo-600 shadow-md"
                transition={{ type: "spring", stiffness: 350, damping: 30 }}
              />
            )}

            <span
              className={`
                relative z-10 transition-colors text-center leading-tight
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