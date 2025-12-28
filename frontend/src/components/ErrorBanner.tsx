"use client";

import { AlertTriangle } from "lucide-react";

export default function ErrorBanner({
  status = 400,
  code,
  message,
}: {
  status?: number;
  code: string;
  message: string;
}) {
  return (
    <div
      className="
        relative overflow-hidden rounded-xl p-5
        border border-red-700/40

        /* LIGHT THEME — DARK RED CARD */
        bg-linear-to-r from-[#4c0519] via-[#7f1d1d] to-[#8a0329]
        text-red-50

        /* DARK THEME */
        dark:from-[#ec3939] dark:via-[#c11d1d] dark:to-[#740101]

        shadow-[0_12px_32px_-6px_rgba(185,28,28,0.6)]
        hover:shadow-[0_16px_44px_-4px_rgba(185,28,28,0.7)]

        transition-all duration-200
      "
    >
      {/* Glow overlay */}
      <div className="absolute inset-0 bg-linear-to-r from-red-600/30 to-transparent pointer-events-none" />

      <div className="relative flex items-start gap-3">
        <AlertTriangle className="mt-0.5 text-red-300" />

        <div className="flex-1">
          {/* Status + Code */}
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-red-600 text-white">
              {status}
            </span>

            <span className="px-2 py-0.5 text-xs font-mono rounded-full bg-black/30 text-red-200">
              {code}
            </span>
          </div>

          {/* Message */}
          <p className="text-sm font-medium text-red-100">
            {message}
          </p>
        </div>
      </div>
    </div>
  );
}
