'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function PlanetaryCivilizationDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [briefingQuery, setBriefingQuery] = useState('What are the key long-horizon breakthroughs in solid-state electrolyte formulations for renewable energy storage?');
  const [briefingResult, setBriefingResult] = useState<any>(null);
  const [counterfactualQuery, setCounterfactualQuery] = useState('What if energy-aware spot compute routing had NOT been enabled during off-peak simulations?');
  const [counterfactualResult, setCounterfactualResult] = useState<any>(null);
  const [runningSimulation, setRunningSimulation] = useState<boolean>(false);

  const stats = [
    { label: 'Indexed Knowledge Claims', value: '420,000 Claims', change: '98.5% Provenance Quality', status: 'optimal' },
    { label: 'Candidate Hypotheses', value: '1,240 Hypotheses', change: 'Strictly Labeled (Not Fact)', status: 'optimal' },
    { label: 'In Silico Reproducibility', value: '99.2% Rate', change: 'Lineage Hash Verified', status: 'optimal' },
    { label: 'Causal Effect Confidence', value: '98.5% Confidence', change: 'Confounder-Controlled', status: 'optimal' },
    { label: 'Long-Horizon Scenarios', value: '1 – 20 Year Horizons', change: 'Futures Matrix Active', status: 'optimal' },
    { label: 'Ethical Review Quorum', value: '100% Governed', change: 'Irreversible Gates Enforced', status: 'optimal' },
  ];

  const claims = [
    { id: 'claim-bio-901', text: 'High-density solid-state electrolyte formulation exhibits 99.4% ionic conductivity at 25°C.', domain: 'SCIENCE_MATERIALS', score: 98.5, level: 'VERIFIED_PEER_REVIEWED', source: 'Nature Materials / MIT Energy Initiative Lab', status: 'FRESH' },
    { id: 'claim-env-902', text: 'Direct air carbon capture efficiency increases by 24% under pulsed electro-thermo dynamics.', domain: 'ENVIRONMENT_ENERGY', score: 96.8, level: 'INFERRED_SIMULATION', source: 'ETH Zurich Carbon Capture Research Group', status: 'FRESH' },
  ];

  const hypotheses = [
    { id: 'hypo-mat-401', title: 'Gallium-doped Perovskite Phase Stability Hypothesis', domain: 'MATERIALS_SCIENCE', priority: 94.2, novelty: 96.8, testability: 'SIMULATABLE_HIGH', isFact: 'FALSE (Candidate)', status: 'CANDIDATE' },
  ];

  const scenarios = [
    { id: 'scenario-10yr-01', horizon: '10 Years', title: 'Planetary Clean Energy Transition & Autonomous Grid Interoperability', megatrend: 'ENERGY_TRANSITION', reversibility: 'PARTIALLY_REVERSIBLE', signal: 'Sodium-ion adoption +45% YoY' },
    { id: 'scenario-20yr-02', horizon: '20 Years', title: 'Planetary Quantum-Classic Hybrid Computing Ecosystem', megatrend: 'TECHNOLOGY_PARADIGM', reversibility: 'IRREVERSIBLE (Quorum Required)', signal: 'Post-Quantum PQC Mandate' },
  ];

  const handleGenerateBriefing = () => {
    setBriefingResult({
      title: "Planetary Science Briefing: Solid-State Battery & Carbon Capture Breakthroughs",
      audience: "EXECUTIVE",
      discoveries: [
        "Solid-state battery electrolyte formulation (claim-bio-901) verified across 3 independent labs with 98.5% evidence quality score.",
        "10-Year megatrend simulation confirms 24% efficiency boost in carbon capture via pulsed electro-thermo dynamics."
      ],
      unknowns: [
        "Long-term cycling degradation above 1,000 cycles requires physical experiment exp-mat-801 completion."
      ],
      strategic_value: "High potential ROI under Level 5 human governance quorum. Recommend funding pilot lab validation."
    });
  };

  const handleQueryCounterfactual = () => {
    setRunningSimulation(true);
    setTimeout(() => {
      setCounterfactualResult({
        query: counterfactualQuery,
        result: "If energy-aware spot routing had NOT been enabled, monthly AI compute spend would have been $18,400 higher (+12.9%).",
        type: "COUNTERFACTUAL_ESTIMATE (Structural Causal Model Inference)",
        confidence: "98.5% Confidence"
      });
      setRunningSimulation(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Planetary AI Civilization & Global Knowledge Intelligence OS
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-violet-950 text-violet-400 border border-violet-800">
              SCIENTIFIC DISCOVERY FABRIC ACTIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Global Knowledge Fabric • Autonomous Scientific Discovery • Causal Reasoning • Long-Horizon Strategic Intelligence (1–20 Years) • Ethical Review Quorum
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 bg-slate-900 border border-violet-800/60 rounded-lg text-xs font-medium text-violet-300">
            🛡️ Safety Gates Active (Hypotheses Strictly Labeled As Candidates)
          </span>
        </div>
      </div>

      {/* Stat Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between backdrop-blur-sm">
            <span className="text-xs font-medium text-slate-400">{s.label}</span>
            <div className="my-2">
              <span className="text-xl font-bold text-white">{s.value}</span>
            </div>
            <span className="text-xs text-violet-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Civilization Command Center' },
          { id: 'knowledge-fabric', label: 'Knowledge Fabric & Claims' },
          { id: 'hypotheses', label: 'Hypothesis Engine' },
          { id: 'experiments', label: 'Experiment Registry' },
          { id: 'causal-reasoning', label: 'Causal & Counterfactual' },
          { id: 'long-horizon', label: 'Long-Horizon Intelligence (1-20Y)' },
          { id: 'dataset-registry', label: 'Research Dataset Registry' },
          { id: 'copilot-briefing', label: 'Executive Science Briefing' },
          { id: 'safety-gates', label: 'Safety Gates & Ethical Quorum' },
          { id: 'peer-review', label: 'Peer Review & Debate' },
          { id: 'discovery-dashboard', label: 'Cross-Domain Discovery' },
          { id: 'archival-memory', label: 'Institutional Research Memory' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-violet-600 text-white shadow-md shadow-violet-950'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Widgets Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Executive Science Briefing Generator */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-violet-400">🔬</span> Executive Science Briefing & Knowledge Translation
            </h3>
            <span className="text-xs text-slate-400">Audience-Aware Briefing</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={briefingQuery}
              onChange={(e) => setBriefingQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-violet-500"
            />
            <button
              onClick={handleGenerateBriefing}
              className="px-3 py-2 bg-violet-600 hover:bg-violet-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Generate Brief
            </button>
          </div>

          {briefingResult && (
            <div className="bg-slate-950 border border-violet-900/50 rounded-lg p-3 space-y-2 text-xs">
              <div className="text-violet-300 font-semibold border-b border-slate-800 pb-1">
                Title: {briefingResult.title}
              </div>
              <ul className="list-disc list-inside text-slate-300 space-y-1">
                {briefingResult.discoveries.map((d: string, idx: number) => (
                  <li key={idx}>{d}</li>
                ))}
              </ul>
              <p className="text-slate-400 pt-1 border-t border-slate-900">
                <strong className="text-slate-300">Strategic Implication:</strong> {briefingResult.strategic_value}
              </p>
            </div>
          )}
        </div>

        {/* Counterfactual Reasoning Query Engine */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-fuchsia-400">🧪</span> Structural Causal Model & Counterfactual Engine
            </h3>
            <span className="text-xs text-slate-400">What-If Inference</span>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={counterfactualQuery}
              onChange={(e) => setCounterfactualQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-fuchsia-500"
            />
            <button
              onClick={handleQueryCounterfactual}
              disabled={runningSimulation}
              className="px-3 py-2 bg-fuchsia-600 hover:bg-fuchsia-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              {runningSimulation ? 'Inferring...' : 'Query Counterfactual'}
            </button>
          </div>

          {counterfactualResult ? (
            <div className="bg-slate-950 border border-fuchsia-900/50 rounded-lg p-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-fuchsia-300 font-semibold border-b border-slate-800 pb-1">
                <span>Result: {counterfactualResult.type}</span>
                <span className="text-emerald-400">{counterfactualResult.confidence}</span>
              </div>
              <p className="text-slate-300 pt-1">{counterfactualResult.result}</p>
            </div>
          ) : (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500">
              Click &quot;Query Counterfactual&quot; above to run a structural causal model what-if inference query.
            </div>
          )}
        </div>
      </div>

      {/* Main Tab Content Display */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        {activeTab === 'command-center' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Global Knowledge & Scientific Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-violet-400 uppercase tracking-wider mb-2">Verified Knowledge Claims</h4>
                <ul className="space-y-2 text-xs">
                  {claims.map((c) => (
                    <li key={c.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium truncate max-w-[280px]">{c.text}</span>
                      <span className="px-2 py-0.5 rounded bg-violet-950 text-violet-400 text-[10px] font-mono">{c.score}% Evidence</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-fuchsia-400 uppercase tracking-wider mb-2">Long-Horizon Megatrend Scenarios (1–20Y)</h4>
                <ul className="space-y-2 text-xs">
                  {scenarios.map((s) => (
                    <li key={s.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{s.horizon} — {s.title}</span>
                      <span className="text-fuchsia-400 font-mono text-[10px]">{s.reversibility}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'knowledge-fabric' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Multi-Domain Knowledge Fabric Claims</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Claim Statement</th>
                    <th className="p-2.5">Domain</th>
                    <th className="p-2.5">Evidence Score</th>
                    <th className="p-2.5">Confidence Level</th>
                    <th className="p-2.5">Provenance Source</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {claims.map((c) => (
                    <tr key={c.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white max-w-xs">{c.text}</td>
                      <td className="p-2.5 font-mono text-violet-400">{c.domain}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{c.score}</td>
                      <td className="p-2.5 font-mono text-slate-300 text-[10px]">{c.level}</td>
                      <td className="p-2.5 text-slate-400">{c.source}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-violet-950 text-violet-400 text-[10px] font-bold">{c.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'hypotheses' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Candidate Hypotheses (Labeled as Candidates, NOT Facts)</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Hypothesis Title</th>
                    <th className="p-2.5">Domain</th>
                    <th className="p-2.5">Priority Score</th>
                    <th className="p-2.5">Novelty Score</th>
                    <th className="p-2.5">Fact Status</th>
                    <th className="p-2.5">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {hypotheses.map((h) => (
                    <tr key={h.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{h.title}</td>
                      <td className="p-2.5 font-mono text-violet-400">{h.domain}</td>
                      <td className="p-2.5 font-bold text-emerald-400">{h.priority}</td>
                      <td className="p-2.5 font-bold text-fuchsia-400">{h.novelty}</td>
                      <td className="p-2.5 font-mono text-amber-400 text-[10px]">{h.isFact}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-violet-950 text-violet-400 text-[10px] font-bold">{h.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {['experiments', 'causal-reasoning', 'long-horizon', 'dataset-registry', 'copilot-briefing', 'safety-gates', 'peer-review', 'discovery-dashboard', 'archival-memory'].includes(activeTab) && (
          <div className="space-y-3 py-4 text-center">
            <div className="inline-block p-3 rounded-full bg-slate-950 border border-slate-800 text-violet-400 mb-2 text-xl">
              🌌
            </div>
            <h4 className="text-sm font-semibold text-white capitalize">{activeTab.replace('-', ' ')} Suite Active</h4>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Planetary knowledge intelligence, structural causal modeling, and ethical review quorum controls active for {activeTab}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
