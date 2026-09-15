"use client";

import React, { useState } from "react";
import { DataContractItem, DataQualityRuleItem } from "@/lib/api/enterpriseDataOs";

interface Props {
  contracts: DataContractItem[];
  qualityRules: DataQualityRuleItem[];
}

export const DataContractsQualityRadar: React.FC<Props> = ({ contracts, qualityRules }) => {
  const [activeTab, setActiveTab] = useState<"contracts" | "quality_rules">("contracts");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Data Contracts & 6-Dimension Quality Rules</h2>
          <p className="text-xs text-slate-400">
            Producer-consumer interface agreements, freshness SLAs, and multi-factor quality rule assertions
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("contracts")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "contracts"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Data Contracts ({contracts.length})
          </button>
          <button
            onClick={() => setActiveTab("quality_rules")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "quality_rules"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Quality Rules ({qualityRules.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "contracts" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Producer → Consumer</th>
                  <th className="p-3">Dataset / Schema</th>
                  <th className="p-3">Freshness SLA</th>
                  <th className="p-3">Quality Threshold</th>
                  <th className="p-3">Compliance</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {contracts.map((con) => (
                  <tr key={con.contract_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3">
                      <div className="font-semibold text-slate-100">{con.producer_team}</div>
                      <div className="text-[10px] text-indigo-400">→ {con.consumer_team}</div>
                    </td>
                    <td className="p-3">
                      <div className="font-mono text-slate-200">{con.dataset_id}</div>
                      <div className="text-[10px] text-slate-500 font-mono">{con.schema_version}</div>
                    </td>
                    <td className="p-3 font-mono text-slate-300">{con.freshness_sla_minutes} min max lag</td>
                    <td className="p-3 font-mono font-bold text-slate-200">{con.quality_threshold_pct}%</td>
                    <td className="p-3 font-mono font-bold text-emerald-400">{con.sla_compliance_pct}%</td>
                    <td className="p-3">
                      <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">
                        {con.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === "quality_rules" && (
          <div className="space-y-3">
            {qualityRules.map((rul) => (
              <div
                key={rul.rule_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm">{rul.rule_type} Assertion</span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {rul.dimension}
                    </span>
                    <span className="text-[10px] bg-rose-950 text-rose-300 px-1.5 py-0.5 rounded border border-rose-800 font-mono">
                      {rul.severity}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Target Dataset: <span className="font-mono text-indigo-300">{rul.dataset_id}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-xs text-slate-400">Pass Rate</div>
                    <div className="text-sm font-bold text-emerald-400 font-mono">{rul.pass_rate_pct}%</div>
                  </div>
                  <span className="text-[11px] bg-emerald-950/80 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded font-mono">
                    ACTIVE
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
