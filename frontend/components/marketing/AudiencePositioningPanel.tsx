"use client";

import React from "react";
import { MarketingAudience, MarketingPositioning } from "@/lib/api/marketing";

interface Props {
  audiences: MarketingAudience[];
  positionings: MarketingPositioning[];
}

export const AudiencePositioningPanel: React.FC<Props> = ({ audiences, positionings }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Audiences & ICP */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-200">Target Audiences & ICP Profiles</h3>
          <span className="text-xs bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded-full">
            {audiences.length} Profiles
          </span>
        </div>

        <div className="space-y-4">
          {audiences.map((aud) => (
            <div key={aud.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-sm font-medium text-slate-100">{aud.name}</h4>
                  <p className="text-xs text-slate-400 mt-1">{aud.description}</p>
                </div>
                <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                  {aud.company_size_tier}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-700/40 text-xs">
                <div>
                  <span className="text-slate-400">Total Market Size:</span>
                  <span className="text-slate-200 font-medium ml-1.5">{aud.total_market_size.toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-slate-400">Reachable SAM:</span>
                  <span className="text-cyan-400 font-medium ml-1.5">{aud.reachable_market_size.toLocaleString()}</span>
                </div>
              </div>

              <div className="mt-3 flex flex-wrap gap-1.5">
                {aud.primary_pain_points.map((pain, i) => (
                  <span key={i} className="text-[10px] bg-rose-950/40 text-rose-300 border border-rose-900/50 px-2 py-0.5 rounded">
                    {pain}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Positioning & Message Houses */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-slate-200">Evidence-Grounded Positioning & Proof</h3>
          <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded-full">
            Approved & Governed
          </span>
        </div>

        <div className="space-y-4">
          {positionings.map((pos) => (
            <div key={pos.id} className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-indigo-400">{pos.target_customer}</span>
                <span className="text-[10px] bg-emerald-900/40 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded">
                  v{pos.version} {pos.is_approved ? "Approved" : "Draft"}
                </span>
              </div>

              <div className="text-xs text-slate-300 mb-2 italic">
                "{pos.value_statement}"
              </div>

              <div className="bg-slate-900/80 rounded p-2.5 border border-slate-700/40 text-xs space-y-1.5 mb-3">
                <div className="text-slate-400">
                  <strong className="text-slate-200 font-medium">Problem:</strong> {pos.problem_statement}
                </div>
                <div className="text-slate-400">
                  <strong className="text-slate-200 font-medium">Our Solution:</strong> {pos.our_solution}
                </div>
              </div>

              <div className="space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Verified Proof Points</span>
                {pos.proof_points.map((proof, i) => (
                  <div key={i} className="flex items-center text-xs text-slate-300">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-2" />
                    {proof}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
