"use client";

import { useEffect, useState } from "react";

export default function RefinePanel({
  onRefine,
  loading,
}: {
  onRefine: (instruction: string) => Promise<void> | void;
  loading: boolean;
}) {
  const [instruction, setInstruction] = useState("");
  const [success, setSuccess] = useState(false);

  // 🔁 Auto-hide success message
  useEffect(() => {
    if (!success) return;
    const t = setTimeout(() => setSuccess(false), 3000);
    return () => clearTimeout(t);
  }, [success]);

  async function handleRefine() {
    await onRefine(instruction);
    setInstruction("");
    setSuccess(true);
  }

  return (
    <div
      className="
        mt-6
        rounded-2xl
        bg-(--card)
        border border-black/10 dark:border-white/10
        p-5
        shadow-lg
        space-y-4
      "
    >
      {/* Title */}
      <h2 className="text-sm font-semibold tracking-wide text-black dark:text-white">
        Refine Spec
      </h2>

      {/* Refinement Textbox */}
      <textarea
        value={instruction}
        onChange={(e) => setInstruction(e.target.value)}
        placeholder='e.g. "Add authentication to all APIs"'
        className="
          w-full h-24 resize-none rounded-xl p-4 text-sm
          bg-(--input-bg)
          text-(--input-text)
          placeholder:text-(--placeholder)
          border border-(--input-border)
          outline-none

          transition-all duration-200
          focus:ring-4 focus:ring-indigo-500/20
          focus:border-indigo-500
        "
      />

      {/* Refine Button */}
      <button
        onClick={handleRefine}
        disabled={loading || !instruction.trim()}
        className="
          relative w-full rounded-xl py-3 text-sm font-semibold text-white

          bg-indigo-700 hover:bg-indigo-600

          shadow-[0_10px_30px_-8px_rgba(79,70,229,0.65)]
          hover:shadow-[0_16px_40px_-6px_rgba(79,70,229,0.8)]

          hover:-translate-y-0.5
          active:translate-y-0
          active:scale-[0.97]

          before:absolute before:inset-0
          before:rounded-xl
          before:bg-linear-to-b
          before:from-white/15
          before:to-transparent
          before:pointer-events-none

          transition-all duration-200 ease-out

          disabled:opacity-50
          disabled:cursor-not-allowed
        "
      >
        {loading ? "Refining…" : "Refine Spec"}
      </button>
    </div>
  );
}
