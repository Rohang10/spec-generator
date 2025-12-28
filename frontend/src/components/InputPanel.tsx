"use client";

interface InputPanelProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}

export default function InputPanel({
  value,
  onChange,
  onSubmit,
  loading,
}: InputPanelProps) {
  return (
    <div
      className="
        bg-(--card)
        rounded-2xl
        p-6
        border border-black/10 dark:border-white/10
        shadow-xl
      "
    >
      <textarea
        id="requirements"
        name="requirements"
        autoComplete="off"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste your messy product requirements here..."
        className="
          w-full h-44 resize-none rounded-xl p-4 leading-relaxed
          transition-all duration-300 outline-none

          bg-white text-slate-900
          placeholder:text-slate-500
          border border-slate-300
          ring-1 ring-slate-200
          hover:border-indigo-500
          focus:border-indigo-500
          focus:ring-4 focus:ring-indigo-500/20

          dark:bg-[#020617]
          dark:text-slate-200
          dark:placeholder:text-slate-500
          dark:border-white/10
          dark:ring-0
          dark:hover:border-indigo-400
          dark:focus:ring-indigo-500/30
        "
      />

      <button
        onClick={onSubmit}
        disabled={loading}
        className="
          mt-5 w-full rounded-xl py-3
          text-white font-semibold
          bg-indigo-600 hover:bg-indigo-500
          shadow-[0_8px_24px_-6px_rgba(79,70,229,0.45)]
          hover:shadow-[0_12px_32px_-4px_rgba(79,70,229,0.55)]
          hover:-translate-y-0.5
          active:scale-[0.97]
          transition-all duration-200 ease-out
        "
      >
        {loading ? "Generating Spec..." : "Generate Spec"}
      </button>
    </div>
  );
}
