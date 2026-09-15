"use client";

import React, { useState } from "react";
import { EngineeringRepository, EngineeringPullRequest } from "@/lib/api/engineeringOs";

interface Props {
  repositories: EngineeringRepository[];
  pullRequests: EngineeringPullRequest[];
}

export const RepositoryPrCodeQualityPanel: React.FC<Props> = ({ repositories, pullRequests }) => {
  const [activeTab, setActiveTab] = useState<"repositories" | "pull_requests">("repositories");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Repositories, Pull Requests & Code Quality</h2>
          <p className="text-xs text-slate-400">
            Source code controls, branch protections, multi-factor static analysis, and PR traceability
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("repositories")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "repositories"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Repositories ({repositories.length})
          </button>
          <button
            onClick={() => setActiveTab("pull_requests")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "pull_requests"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Pull Requests ({pullRequests.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "repositories" ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Repository</th>
                  <th className="p-3">Team</th>
                  <th className="p-3">Stack</th>
                  <th className="p-3">Quality Score</th>
                  <th className="p-3">Protection</th>
                  <th className="p-3">Security State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {repositories.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-4 text-center text-slate-500">
                      No repositories registered in this workspace.
                    </td>
                  </tr>
                ) : (
                  repositories.map((repo) => (
                    <tr key={repo.repository_id} className="hover:bg-slate-800/30 transition">
                      <td className="p-3 font-medium text-slate-100 flex items-center gap-2">
                        <span className="font-mono text-indigo-400">{repo.name}</span>
                        <span className="text-[10px] text-slate-500 bg-slate-800 px-1.5 py-0.5 rounded">
                          {repo.provider}
                        </span>
                      </td>
                      <td className="p-3 text-slate-300">{repo.owner_team}</td>
                      <td className="p-3 text-slate-400">
                        {repo.language} / {repo.framework}
                      </td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded-full font-bold bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">
                          {repo.code_quality_score}/100
                        </span>
                      </td>
                      <td className="p-3">
                        {repo.branch_protection_enabled ? (
                          <span className="text-emerald-400 font-semibold">✓ Enforced</span>
                        ) : (
                          <span className="text-rose-400 font-semibold">⚠ Unprotected</span>
                        )}
                      </td>
                      <td className="p-3">
                        <span className="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                          {repo.security_state}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Pull Request</th>
                  <th className="p-3">Author</th>
                  <th className="p-3">Branches</th>
                  <th className="p-3">Checks</th>
                  <th className="p-3">Risk Level</th>
                  <th className="p-3">Traceability</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {pullRequests.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-4 text-center text-slate-500">
                      No open pull requests.
                    </td>
                  </tr>
                ) : (
                  pullRequests.map((pr) => (
                    <tr key={pr.pr_id} className="hover:bg-slate-800/30 transition">
                      <td className="p-3">
                        <div className="font-semibold text-slate-100">{pr.title}</div>
                        <div className="text-[10px] text-slate-500 font-mono">{pr.pr_id}</div>
                      </td>
                      <td className="p-3 text-slate-300">{pr.author}</td>
                      <td className="p-3 font-mono text-[11px] text-slate-400">
                        {pr.source_branch} → {pr.target_branch}
                      </td>
                      <td className="p-3">
                        {pr.checks_passing ? (
                          <span className="text-emerald-400">✓ All Passing</span>
                        ) : (
                          <span className="text-rose-400">✗ Checks Failing</span>
                        )}
                      </td>
                      <td className="p-3">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            pr.risk_level === "HIGH"
                              ? "bg-rose-950 text-rose-300 border border-rose-800"
                              : pr.risk_level === "MEDIUM"
                              ? "bg-amber-950 text-amber-300 border border-amber-800"
                              : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                          }`}
                        >
                          {pr.risk_level}
                        </span>
                      </td>
                      <td className="p-3 text-slate-400 text-[11px]">
                        {pr.linked_requirements?.length > 0 ? (
                          <span className="text-indigo-300 font-mono">
                            {pr.linked_requirements.join(", ")}
                          </span>
                        ) : (
                          <span className="text-slate-500 italic">No linked requirement</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
