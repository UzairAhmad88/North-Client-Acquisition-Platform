"use client";

import React, { useState } from "react";
import { SemanticMetricItem, BusinessGlossaryTermItem, DataCatalogAssetItem } from "@/lib/api/enterpriseDataOs";

interface Props {
  metrics: SemanticMetricItem[];
  glossary: BusinessGlossaryTermItem[];
  catalog: DataCatalogAssetItem[];
}

export const SemanticMetricStoreExplorer: React.FC<Props> = ({ metrics, glossary, catalog }) => {
  const [activeTab, setActiveTab] = useState<"metrics" | "glossary" | "catalog">("metrics");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Semantic Metrics Store & Business Glossary</h2>
          <p className="text-xs text-slate-400">
            Single source of truth metric definitions, SQL business formulas, and enterprise business glossary
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("metrics")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "metrics"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Semantic Metrics ({metrics.length})
          </button>
          <button
            onClick={() => setActiveTab("glossary")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "glossary"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Glossary ({glossary.length})
          </button>
          <button
            onClick={() => setActiveTab("catalog")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "catalog"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Catalog ({catalog.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "metrics" && (
          <div className="space-y-3">
            {metrics.map((m) => (
              <div
                key={m.metric_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-slate-100 text-sm">{m.name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono font-bold">
                    Authoritative SSoT
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-2">{m.definition}</p>
                <div className="bg-slate-900 p-2 rounded text-[11px] font-mono text-cyan-300 border border-slate-800 mb-2">
                  SQL: {m.formula_sql}
                </div>
                <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-500 pt-1">
                  <span>Source: {m.source_table}</span>
                  <span>Dimensions: {m.dimensions?.join(", ") || "None"}</span>
                  <span className="text-slate-300">Owner: {m.owner_team}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "glossary" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {glossary.map((term) => (
              <div
                key={term.term_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-slate-100 text-sm">{term.term_name}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800 font-mono">
                    {term.domain_name}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-3">{term.definition}</p>
                <div className="text-[11px] text-slate-500 pt-2 border-t border-slate-800 flex justify-between">
                  <span>Owner: {term.owner_email}</span>
                  <span>Synonyms: {term.synonyms?.join(", ")}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "catalog" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Asset</th>
                  <th className="p-3">Type</th>
                  <th className="p-3">Domain</th>
                  <th className="p-3">Classification</th>
                  <th className="p-3">Quality Score</th>
                  <th className="p-3">Tags</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {catalog.map((ast) => (
                  <tr key={ast.asset_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 font-semibold text-slate-100 font-mono">{ast.asset_name}</td>
                    <td className="p-3 text-slate-400">{ast.asset_type}</td>
                    <td className="p-3 text-slate-300">{ast.domain_name}</td>
                    <td className="p-3">
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono">
                        {ast.classification}
                      </span>
                    </td>
                    <td className="p-3 font-bold font-mono text-emerald-400">{ast.quality_score}%</td>
                    <td className="p-3 text-slate-400 font-mono text-[10px]">{ast.tags?.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
