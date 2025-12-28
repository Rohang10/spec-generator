/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import Header from "@/components/Header";
import InputPanel from "@/components/InputPanel";
import Spinner from "@/components/Spinner";
import ErrorBanner from "@/components/ErrorBanner";
import SpecSections from "@/components/SpecSections";
import ExportButtons from "@/components/ExportButtons";
import AnimatedTabs from "@/components/AnimatedTabs";
import { generateSpec } from "@/lib/api";

// ✅ Correct error type (matches backend + ErrorBanner)
type ApiError = {
  status: number;
  code: string;
  message: string;
};

export default function Page() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [spec, setSpec] = useState<any>(null);
  const [error, setError] = useState<ApiError | null>(null);

  const tabs = [
    "Modules & Features",
    "User Stories",
    "API Endpoints",
    "DB Schema",
    "Open Questions",
  ];

  const [activeTab, setActiveTab] = useState(tabs[0]);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    setSpec(null);

    try {
      const data = await generateSpec(text);
      setSpec(data.spec);
      setActiveTab(tabs[0]);
    } catch (err: any) {
      setError({
        status: err.status || 400,
        code: err.code || "UNKNOWN_ERROR",
        message: err.message || "Something went wrong",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-10">
      <Header />

      <InputPanel
        value={text}
        onChange={setText}
        onSubmit={handleGenerate}
        loading={loading}
      />

      {loading && <Spinner />}

      {error && (
        <div className="mt-6">
          <ErrorBanner
            status={error.status}
            code={error.code}
            message={error.message}
          />
        </div>
      )}

      {spec && (
        <div
          className="
            mt-10
            bg-(--card)
            p-6
            border border-black/10 dark:border-white/10
            shadow-xl
            transition-transform
            hover:-translate-y-0.5
          "
        >
          <AnimatedTabs
            tabs={tabs}
            active={activeTab}
            setActive={setActiveTab}
          />

          <SpecSections spec={spec} activeTab={activeTab} />

          <ExportButtons spec={spec} />
        </div>
      )}
    </main>
  );
}
