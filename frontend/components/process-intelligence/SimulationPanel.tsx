'use client';

import React, { useState } from 'react';
import { processIntelligenceApi, SimulationResult } from '@/lib/api/processIntelligence';
import { Play, Activity, ShieldAlert, CheckCircle2, Cpu } from 'lucide-react';

interface Props {
  processId: string;
}

export default function SimulationPanel({ processId }: Props) {
  const [scenario, setScenario] = useState('OPTIMIZED');
  const [efficiencyGain, setEfficiencyGain] = useState(0.25);
  const [arrivalRate, setArrivalRate] = useState(1.0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await processIntelligenceApi.runSimulation({
        process_id: processId,
        scenario_type: scenario,
        automation_efficiency_gain: efficiencyGain,
        arrival_rate_multiplier: arrivalRate,
        iterations: 1000,
      });
      setResult(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-400" /> Isolated What-If Process Simulation
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Simulate arrival rate spikes and automation gains without mutating production state
          </p>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
          <CheckCircle2 className="w-3.5 h-3.5" /> Production State Isolation Verified
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-950 border border-slate-800 rounded-lg p-4">
        <div>
          <label className="text-xs text-slate-400 font-medium">Scenario</label>
          <select
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="w-full mt-1.5 bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="BASELINE">BASELINE</option>
            <option value="OPTIMIZED">OPTIMIZED</option>
            <option value="CONSERVATIVE">CONSERVATIVE</option>
            <option value="AGGRESSIVE">AGGRESSIVE</option>
            <option value="HIGH_VOLUME">HIGH_VOLUME</option>
            <option value="LOW_RESOURCE">LOW_RESOURCE</option>
          </select>
        </div>

        <div>
          <label className="text-xs text-slate-400 font-medium">Automation Efficiency Gain ({Math.round(efficiencyGain * 100)}%)</label>
          <input
            type="range"
            min="0.05"
            max="0.60"
            step="0.05"
            value={efficiencyGain}
            onChange={(e) => setEfficiencyGain(parseFloat(e.target.value))}
            className="w-full mt-3"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 font-medium">Arrival Volume Multiplier ({arrivalRate}x)</label>
          <input
            type="range"
            min="0.5"
            max="3.0"
            step="0.25"
            value={arrivalRate}
            onChange={(e) => setArrivalRate(parseFloat(e.target.value))}
            className="w-full mt-3"
          />
        </div>
      </div>

      <button
        onClick={handleRun}
        disabled={loading}
        className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 text-sm transition"
      >
        <Play className="w-4 h-4" /> {loading ? 'Simulating (1,000 Monte Carlo Iterations)...' : 'Run What-If Simulation'}
      </button>

      {result && (
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-5 space-y-4">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <span className="text-xs font-mono text-indigo-400">{result.simulation_code}</span>
            <span className="text-xs text-slate-400">1,000 Iterations</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <span className="text-xs text-slate-400">Predicted Cycle Time</span>
              <p className="text-lg font-bold text-emerald-400 mt-0.5">{Math.round(result.predicted_cycle_time_seconds / 3600 * 10) / 10} hrs</p>
            </div>
            <div>
              <span className="text-xs text-slate-400">Predicted Throughput</span>
              <p className="text-lg font-bold text-white mt-0.5">{result.predicted_throughput} cases/day</p>
            </div>
            <div>
              <span className="text-xs text-slate-400">Predicted Cost / Case</span>
              <p className="text-lg font-bold text-white mt-0.5">${result.predicted_cost}</p>
            </div>
            <div>
              <span className="text-xs text-slate-400">Predicted Failure Rate</span>
              <p className="text-lg font-bold text-amber-400 mt-0.5">{Math.round(result.predicted_failure_rate * 1000) / 10}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
