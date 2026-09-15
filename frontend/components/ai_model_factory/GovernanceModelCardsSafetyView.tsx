import React from 'react';

export const GovernanceModelCardsSafetyView: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Model Cards */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">Compliance Model Card</h3>
          <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">
            Verified
          </span>
        </div>
        <div className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-3 text-xs">
          <div>
            <span className="text-slate-500 uppercase font-mono text-[10px]">Model & Version:</span>
            <p className="font-bold text-white text-sm">Customer Churn Risk Classifier v2.1.0</p>
          </div>
          <div>
            <span className="text-slate-500 uppercase font-mono text-[10px]">Intended Use:</span>
            <p className="text-slate-300">
              Predictive churn probability scoring to assist Customer Success managers in proactive account retention.
            </p>
          </div>
          <div>
            <span className="text-slate-500 uppercase font-mono text-[10px]">Known Limitations:</span>
            <p className="text-slate-400">
              Not calibrated for newly onboarded enterprise accounts with less than 14 days of platform activity.
            </p>
          </div>
          <div>
            <span className="text-slate-500 uppercase font-mono text-[10px]">Ethical & Bias Assessment:</span>
            <p className="text-slate-300">
              Demographic parity checked across account tiers. PII fields scrubbed according to Phase 47/62 governance.
            </p>
          </div>
          <div className="pt-2 border-t border-slate-700/40 grid grid-cols-2 gap-2 text-[11px]">
            <div>
              <span className="text-slate-500">Risk Classification:</span>
              <p className="font-bold text-amber-300">MEDIUM RISK</p>
            </div>
            <div>
              <span className="text-slate-500">Governance Steward:</span>
              <p className="font-medium text-slate-300">marcus.governance@uzaii.internal</p>
            </div>
          </div>
        </div>
      </div>

      {/* Security Scans & SBOM */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">AI Supply Chain & Security Scans</h3>
          <span className="text-xs px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono">
            Clean SBOM
          </span>
        </div>
        <div className="space-y-3">
          <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-white">Supply Chain SBOM Scan</span>
              <span className="text-emerald-400 font-mono font-bold text-[10px]">0 Vulnerabilities</span>
            </div>
            <p className="text-slate-400">Base License: Apache-2.0 (Permissive Commercial Use)</p>
            <div className="bg-slate-900/50 p-2 rounded text-[11px] font-mono text-slate-300">
              Dependencies: torch&gt;=2.1.0, onnxruntime&gt;=1.16.0, lightgbm&gt;=4.1.0
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-white">Prompt Injection Guardrail Test</span>
              <span className="text-emerald-400 font-mono font-bold text-[10px]">100% Defense</span>
            </div>
            <p className="text-slate-400">
              Zero sandbox breakout attempts succeeded across 500 automated adversarial attack vectors.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
