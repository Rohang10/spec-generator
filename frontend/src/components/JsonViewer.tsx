/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect } from "react";
import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css";
import "prismjs/components/prism-json";

export default function JsonViewer({ data }: { data: any }) {
  useEffect(() => {
    Prism.highlightAll();
  }, [data]);

  return (
    <pre
      className="
        rounded-xl p-5 overflow-auto text-sm font-mono
        border transition-colors

        /* 🌞 LIGHT */
        bg-white text-[#020617]
        border-slate-200

        /* 🌙 DARK */
        dark:bg-[#020617]
        dark:text-slate-100
        dark:border-white/10
      "
    >
      <code className="language-json">
        {JSON.stringify(data, null, 2)}
      </code>
    </pre>
  );
}
