/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import { Download, Copy, CheckCircle } from "lucide-react";

export default function ExportButtons({ spec }: { spec: any }) {
  const [copied, setCopied] = useState(false);

  function copyJson() {
    navigator.clipboard.writeText(JSON.stringify(spec, null, 2));
    setCopied(true);

    // auto-hide after 2 seconds
    setTimeout(() => setCopied(false), 2000);
  }

  function downloadJson() {
    const blob = new Blob([JSON.stringify(spec, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "spec.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="mt-6">
      {/* Buttons */}
      <div className="flex gap-4">
        {/* Copy JSON – Indigo */}
        <button
          onClick={copyJson}
          className="
            flex items-center gap-2 px-4 py-2 rounded-lg
            text-white font-medium

            bg-indigo-600 hover:bg-indigo-500

            shadow-[0_8px_24px_-6px_rgba(79,70,229,0.45)]
            hover:shadow-[0_12px_32px_-4px_rgba(79,70,229,0.55)]

            hover:-translate-y-0.5
            active:scale-[0.97]

            transition-all duration-200 ease-out
          "
        >
          <Copy size={16} />
          Copy JSON
        </button>

        {/* Download JSON – Amber */}
        <button
          onClick={downloadJson}
          className="
            flex items-center gap-2 px-4 py-2 rounded-lg
            text-white font-medium

            bg-amber-500/90 dark:bg-amber-400/90
            hover:bg-amber-500 dark:hover:bg-amber-400

            shadow-[0_8px_24px_-6px_rgba(245,158,11,0.45)]
            hover:shadow-[0_12px_32px_-4px_rgba(245,158,11,0.55)]

            hover:-translate-y-0.5
            active:scale-[0.97]

            transition-all duration-200 ease-out
          "
        >
          <Download size={16} />
          Download JSON
        </button>
      </div>

      {/* ✅ Success Message */}
      {copied && (
        <div
          className="
            mt-4 flex items-center gap-2
            rounded-xl px-4 py-3

            bg-emerald-500/10
            border border-emerald-500/30
            text-emerald-700 dark:text-emerald-300

            shadow-[0_8px_30px_-6px_rgba(16,185,129,0.45)]
            animate-fade-in
          "
        >
          <CheckCircle size={18} className="text-emerald-500" />
          <span className="font-medium">
            Full spec JSON copied to clipboard.!
          </span>
        </div>
      )}
    </div>
  );
}
