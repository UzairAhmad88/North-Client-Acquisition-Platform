"use client";

import React, { useState } from "react";
import { DataLineageEdgeItem, FeatureStoreItem, DataFinopsSpendItem } from "@/lib/api/enterpriseDataOs";

interface Props {
  lineage: DataLineageEdgeItem[];
  features: FeatureStoreItem[];
  finops: DataFinopsSpendItem[];
}

export const DataLineageGovernanceMatrix: React.FC<Props> = ({ lineage, features, finops }) => {
  const [activeTab, setActiveTab] = useState<"lineage" | "features" | "finops">("lineage");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Lineage Graph, Feature Store & FinOps</h2>
          <p className="text-xs text-slate-400">
            Source-to-product lineage edges, ML curated feature store, and storage/compute cost allocation
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("lineage")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "lineage"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Lineage ({lineage.length})
          </button>
          <button
            onClick={() => setActiveTab("features")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "features"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Feature Store ({features.length})
          </button>
          <button
            onClick={() => setActiveTab("finops")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "finops"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Data FinOps
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "lineage" && (
          <div className="space-y-3">
            {lineage.map((edge) => (
              <div
                key={edge.edge_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-2"
              >
                <div className="flex items-center gap-3 font-mono text-xs">
                  <span className="text-cyan-300 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                    {edge.source_asset_id}
                  </span>
                  <span className="text-slate-500">──[{edge.relationship_type}]──►</span>
                  <span className="text-emerald-300 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                    {edge.target_asset_id}
                  </span>
                </div>
                <span className="text-xs text-slate-400">{edge.transformation_name || "Direct Sync"}</span>
              </div>
            ))}
          </div>
        )}

        {activeTab === "features" && (
          <div className="space-y-3">
            {features.map((feat) => (
              <div
                key={feat.feature_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm font-mono">{feat.name}</span>
                    <span className="text-[10px] bg-indigo-950 text-indigo-300 px-1.5 py-0.5 rounded font-mono">
                      Entity: {feat.entity_name}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1 font-mono">{feat.transformation_logic}</div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-emerald-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800 font-mono">
                    Online Ready ({feat.freshness_minutes}m SLA)
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "finops" && finops.length > 0 && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Total Monthly Data Spend</div>
                <div className="text-xl font-bold text-amber-400 font-mono mt-1">
                  ${finops[0].total_monthly_spend_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Estimated Lakehouse Waste</div>
                <div className="text-xl font-bold text-rose-400 font-mono mt-1">
                  ${finops[0].waste_estimate_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Optimization Actions</div>
                <div className="text-xl font-bold text-emerald-400 font-mono mt-1">
                  {finops[0].optimization_recommendations.length} Active
                </div>
              </div>
            </div>

            <div className="space-y-2">
              {finops[0].optimization_recommendations.map((rec, i) => (
                <div
                  key={i}
                  className="bg-slate-800/30 p-3 rounded-lg border border-slate-700/40 flex items-center justify-between text-xs"
                >
                  <span className="text-slate-300">💡 {rec}</span>
                  <span className="text-emerald-400 font-bold font-mono">Cost Reduction Opportunity</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
