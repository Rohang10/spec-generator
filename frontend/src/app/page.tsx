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
import RefinePanel from "@/components/RefinePanel";
import { generateSpec, refineSpec } from "@/lib/api";

type ApiError = {
  status: number;
  code: string;
  message: string;
};

export default function Page() {
  const [text, setText] = useState("");
  const [spec, setSpec] = useState<any>(null);

  const [loading, setLoading] = useState(false);     // generate
  const [refining, setRefining] = useState(false);   // refine
  const [error, setError] = useState<ApiError | null>(null);

  const tabs = [
    "Modules & Features",
    "User Stories",
    "API Endpoints",
    "DB Schema",
    "Open Questions",
  ];

  const [activeTab, setActiveTab] = useState(tabs[0]);

  // ---------------- GENERATE ----------------
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

  // ---------------- REFINE ----------------
  async function handleRefine(instruction: string) {
    setRefining(true);
    setError(null);

    try {
      const data = await refineSpec(spec, instruction);
      setSpec(data.spec);
      setActiveTab(tabs[0]);
    } catch (err: any) {
      setError({
        status: err.status || 400,
        code: err.code || "UNKNOWN_ERROR",
        message: err.message || "Something went wrong",
      });
    } finally {
      setRefining(false);
    }
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-10">
      <Header />

      {/* ✅ Generate Spec input NEVER disappears */}
      <InputPanel
        value={text}
        onChange={setText}
        onSubmit={handleGenerate}
        loading={loading}
      />

      {/* 🔄 Spinner for Generate Spec */}
      {loading && (
        <div className="mt-8 flex justify-center">
          <Spinner />
        </div>
      )}

      {/* ❌ Errors (only when idle) */}
      {error && !loading && !refining && (
        <div className="mt-6">
          <ErrorBanner
            status={error.status}
            code={error.code}
            message={error.message}
          />
        </div>
      )}

      {/* 📄 Spec + Refine UI — hidden ONLY while refining */}
      {spec && (
        <>
          {/* 🔄 Spinner during refine (ONLY thing visible) */}
          {refining ? (
          <div className="mt-16 flex justify-center">
            <Spinner />
          </div>
        ) : (
          <div
            className="
              mt-10
              bg-(--card)
              p-6
              border border-black/10 dark:border-white/10
              shadow-xl
              rounded-2xl
            "
          >
            <AnimatedTabs
             tabs={tabs}
              active={activeTab}
              setActive={setActiveTab}
            />

            <SpecSections spec={spec} activeTab={activeTab} />

            <ExportButtons spec={spec} />

            {/* ✅ RefinePanel STAYS MOUNTED */}
            <RefinePanel onRefine={handleRefine} loading={false} />
          </div>
        )}
        </>
      )}
    </main>
  );
}
