/* eslint-disable react-hooks/set-state-in-effect */
"use client";

import { useEffect, useState } from "react";
import { useTheme } from "@/context/ThemeContext";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-20 h-10 rounded-full bg-[#F1F5F9]" />
    );
  }

  const isDark = theme === "dark";

  return (
    <div className="relative z-50 isolate">
      <button
        onClick={toggleTheme}
        aria-label="Toggle theme"
        className={`
          relative w-20 h-10 rounded-full
          transition-all duration-500 ease-out
          active:scale-[0.97]
          ${
            isDark
              ? "bg-slate-800 border-transparent shadow-[0_0_22px_rgba(59,130,246,0.55)]"
              : "bg-linear-to-r from-slate-300 to-slate-300 border-blue-100 shadow-lg"
          }
          border
        `}
      >
        {/* Toggle Knob */}
        <span
          className={`
            absolute top-1 left-1 w-8 h-8 rounded-full
            flex items-center justify-center
            text-lg
            transition-all duration-500 ease-out
            shadow-lg
            ${isDark ? "translate-x-10" : "translate-x-0"}
            ${
              isDark
                ? "bg-slate-900"
                : "bg-white"
            }
          `}
        >
          <span
            className={`transition-transform duration-500 ${
              isDark ? "rotate-0" : "rotate-180"
            }`}
          >
            {isDark ? "🌙" : "☀️"}
          </span>
        </span>
      </button>
    </div>
  );
}