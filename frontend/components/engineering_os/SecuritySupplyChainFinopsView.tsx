"use client";

import React, { useState } from "react";
import {
  DependencyVulnerabilityItem,
  TechnicalDebtItem,
  FinOpsCostSummary,
  ChangeManagementRecord,
} from "@/lib/api/engineeringOs";

interface Props {
  vulnerabilities: DependencyVulnerabilityItem[];
  technicalDebt: TechnicalDebtItem[];
  finops: FinOpsCostSummary | null;
  changes: ChangeManagementRecord[];
}

export const SecuritySupplyChainFinopsView: React.FC<Props> = ({
  vulnerabilities,
  technicalDebt,
  finops,
  changes,
}) => {
  const [activeTab, setActiveTab] = useState<"security" | "tech_debt" | "finops" | "changes">("security");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">
            Supply Chain Security, FinOps, Debt & Change Risk
          </h2>
          <p className="text-xs text-slate-400">
            CVE vulnerability tracking, FinOps cloud cost allocation, technical debt register, and change management
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("security")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "security"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Vulnerabilities ({vulnerabilities.length})
          </button>
          <button
            onClick={() => setActiveTab("tech_debt")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "tech_debt"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Tech Debt ({technicalDebt.length})
          </button>
          <button
            onClick={() => setActiveTab("finops")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "finops"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            FinOps Costs
          </button>
          <button
            onClick={() => setActiveTab("changes")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "changes"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Changes ({changes.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "security" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">CVE ID</th>
                  <th className="p-3">Package</th>
                  <th className="p-3">Installed / Fixed</th>
                  <th className="p-3">Severity</th>
                  <th className="p-3">Exploitability</th>
                  <th className="p-3">Status / Deadline</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {vulnerabilities.map((vuln) => (
                  <tr key={vuln.vulnerability_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 font-mono font-bold text-rose-400">{vuln.cve_id}</td>
                    <td className="p-3 font-medium text-slate-100">{vuln.package_name}</td>
                    <td className="p-3 font-mono text-slate-400">
                      {vuln.current_version} →{" "}
                      <span className="text-emerald-400">{vuln.fixed_version}</span>
                    </td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          vuln.severity === "CRITICAL" || vuln.severity === "HIGH"
                            ? "bg-rose-950 text-rose-300 border border-rose-800"
                            : "bg-amber-950 text-amber-300 border border-amber-800"
                        }`}
                      >
                        {vuln.severity}
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">{vuln.exploitability}</td>
                    <td className="p-3">
                      <div className="font-semibold text-slate-200">{vuln.remediation_status}</div>
                      <div className="text-[10px] text-slate-500 font-mono">SLA: {vuln.sla_deadline}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === "tech_debt" && (
          <div className="space-y-3">
            {technicalDebt.map((debt) => (
              <div
                key={debt.debt_id}
                className="bg-slate-800/30 border border-slate-700/50 rounded-lg p-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm">{debt.title}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {debt.category} · {debt.component}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Effort to Pay Off: {debt.principal_effort_days} engineer-days · Annual Carry Cost: ${debt.annual_cost_usd.toLocaleString()}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      debt.remediation_priority === "P0" || debt.remediation_priority === "P1"
                        ? "bg-rose-950 text-rose-300 border border-rose-800"
                        : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}
                  >
                    Priority: {debt.remediation_priority}
                  </span>
                  <span className="text-[11px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                    {debt.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "finops" && finops && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Total Monthly Spend</div>
                <div className="text-xl font-bold text-amber-400 font-mono mt-1">
                  ${finops.total_monthly_spend_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Identified Waste</div>
                <div className="text-xl font-bold text-rose-400 font-mono mt-1">
                  ${finops.monthly_waste_estimate_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/60">
                <div className="text-xs text-slate-400">Optimization Actions</div>
                <div className="text-xl font-bold text-emerald-400 font-mono mt-1">
                  {finops.optimization_recommendations.length} Available
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                FinOps Optimization Opportunities
              </h4>
              {finops.optimization_recommendations.map((rec, i) => (
                <div
                  key={i}
                  className="bg-slate-800/30 p-3 rounded-lg border border-slate-700/40 flex items-center justify-between text-xs"
                >
                  <div>
                    <span className="font-bold text-slate-200">{rec.type}: </span>
                    <span className="text-slate-400">{rec.description}</span>
                  </div>
                  <span className="font-mono text-emerald-400 font-bold">
                    +${rec.potential_savings_monthly_usd.toLocaleString()}/mo
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "changes" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Change Title</th>
                  <th className="p-3">Risk Level</th>
                  <th className="p-3">Risk Score</th>
                  <th className="p-3">Systems</th>
                  <th className="p-3">Approval Gate</th>
                  <th className="p-3">State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {changes.map((chg) => (
                  <tr key={chg.change_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 font-medium text-slate-100">{chg.title}</td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          chg.risk_level === "CRITICAL" || chg.risk_level === "HIGH"
                            ? "bg-rose-950 text-rose-300 border border-rose-800"
                            : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        }`}
                      >
                        {chg.risk_level}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-200">{chg.risk_score}/100</td>
                    <td className="p-3 text-slate-400 font-mono">{chg.affected_systems.join(", ")}</td>
                    <td className="p-3">
                      {chg.requires_human_approval ? (
                        <span className="text-amber-400 font-bold">Human Gate Required</span>
                      ) : (
                        <span className="text-slate-500">Standard Change</span>
                      )}
                    </td>
                    <td className="p-3 text-slate-300 font-semibold">{chg.implementation_state}</td>
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
