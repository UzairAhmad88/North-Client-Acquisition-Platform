'use client';

import React, { useState } from 'react';
import { ScenarioSimulationResult, businessOSApi } from '@/lib/api/business_os';

export const ScenarioBuilder: React.FC = () => {
  const [scenarioName, setScenarioName] = useState<string>('Q4 Retainer Expansion & Pricing Adjustment');
  const [priceChange, setPriceChange] = useState<number>(10.0);
  const [conversionChange, setConversionChange] = useState<number>(0.0);
  const [clientChurn, setClientChurn] = useState<number>(0.0);
  const [newHires, setNewHires] = useState<number>(1);
  const [simulationResult, setSimulationResult] = useState<ScenarioSimulationResult | null>(null);
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const handleRun = async () => {
    try {
      setIsRunning(true);
      const res = await businessOSApi.runScenario({
        scenario_name: scenarioName,
        price_change_pct: priceChange,
        conversion_change_pct: conversionChange,
        client_churn_revenue: clientChurn,
        new_hires_count: newHires,
      });
      setSimulationResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="border-b border-slate-800 pb-4 mb-6">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <span>🧪</span> Scenario Planning & What-If Simulation Sandbox
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Isolated sandbox testing pricing, churn, and hiring without mutating production records.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Controls */}
        <div className="space-y-4 bg-slate-950/60 border border-slate-800 rounded-lg p-5">
          <h3 className="text-sm font-bold text-slate-200">Simulation Variables</h3>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Scenario Name</label>
            <input
              type="text"
              value={scenarioName}
              onChange={(e) => setScenarioName(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-200"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Price Delta (%): {priceChange}%</label>
              <input
                type="range"
                min="-30"
                max="50"
                step="5"
                value={priceChange}
                onChange={(e) => setPriceChange(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">Conversion Delta (%): {conversionChange}%</label>
              <input
                type="range"
                min="-50"
                max="50"
                step="5"
                value={conversionChange}
                onChange={(e) => setConversionChange(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-slate-400 mb-1">Client Churn Revenue Loss (PKR)</label>
              <input
                type="number"
                value={clientChurn}
                onChange={(e) => setClientChurn(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-200"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">New Senior Hires (+40h cap)</label>
              <input
                type="number"
                min="0"
                max="10"
                value={newHires}
                onChange={(e) => setNewHires(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-200"
              />
            </div>
          </div>

          <button
            onClick={handleRun}
            disabled={isRunning}
            className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-md text-xs font-semibold transition-all mt-2"
          >
            {isRunning ? 'Running Simulation...' : '▶ Run Isolated Simulation'}
          </button>
        </div>

        {/* Results */}
        <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-5">
          <h3 className="text-sm font-bold text-slate-200 mb-4">Simulated Forecast Outcomes</h3>
          {simulationResult ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Simulated Revenue</div>
                  <div className="text-lg font-bold text-emerald-400">PKR {Number(simulationResult.simulated_revenue).toLocaleString()}</div>
                </div>
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Simulated Gross Margin</div>
                  <div className="text-lg font-bold text-indigo-400">{Number(simulationResult.simulated_margin_pct).toFixed(1)}%</div>
                </div>
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Capacity Utilization</div>
                  <div className="text-lg font-bold text-amber-400">{Number(simulationResult.capacity_utilization_pct).toFixed(1)}%</div>
                </div>
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <div className="text-xs text-slate-400">Cash Buffer Needed (3mo)</div>
                  <div className="text-lg font-bold text-slate-200">PKR {Number(simulationResult.cash_requirement).toLocaleString()}</div>
                </div>
              </div>

              {/* Sensitivity Ranking */}
              <div className="mt-4">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Sensitivity Impact Rankings</h4>
                <div className="space-y-1.5">
                  {simulationResult.sensitivity_rankings.map((s, idx) => (
                    <div key={idx} className="flex items-center justify-between text-xs p-2 bg-slate-900/80 rounded border border-slate-800/80">
                      <div>
                        <strong className="text-slate-200">{s.variable}</strong>
                        <p className="text-[11px] text-slate-400">{s.impact_description}</p>
                      </div>
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                        {s.sensitivity_level}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center text-xs text-slate-500 italic">
              Adjust variables and click 'Run Isolated Simulation' to view forecast impacts.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
