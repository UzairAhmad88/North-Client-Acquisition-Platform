'use client';

import React, { useState } from 'react';
import { digitalTwinApi, SimulationResult } from '@/lib/api/digitalTwin';

interface Props {
  onSimulationComplete: (result: SimulationResult) => void;
}

export const ScenarioBuilder: React.FC<Props> = ({ onSimulationComplete }) => {
  const [scenarioName, setScenarioName] = useState('Growth & Pricing Optimization');
  const [simulationMethod, setSimulationMethod] = useState<'MONTE_CARLO' | 'DETERMINISTIC'>('MONTE_CARLO');
  const [iterations, setIterations] = useState(1000);
  const [loading, setLoading] = useState(false);

  // Parameter Overrides
  const [leadConversion, setLeadConversion] = useState(0.10); // 10%
  const [dealValue, setDealValue] = useState(5000); // $5,000
  const [leadVolume, setLeadVolume] = useState(150); // 150 leads
  const [fteCapacity, setFteCapacity] = useState(8.0); // 8 FTE
  const [monthlyOpex, setMonthlyOpex] = useState(22000); // $22,000

  const handleRunSimulation = async () => {
    setLoading(true);
    try {
      const overrides = {
        lead_conversion_rate: leadConversion,
        average_deal_value_usd: dealValue,
        lead_volume_monthly: leadVolume,
        developer_capacity_fte: fteCapacity,
        monthly_operating_cost_usd: monthlyOpex,
      };

      const res = await digitalTwinApi.runSimulation({
        scenario_name: scenarioName,
        simulation_method: simulationMethod,
        iterations: iterations,
        parameter_overrides: overrides,
      });

      onSimulationComplete((res as any)?.data || res);
    } catch (err) {
      console.error('Failed to run simulation', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Scenario Formulation & What-If Sandbox</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Test strategic parameter shifts against the sandboxed digital twin. Zero production mutation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSimulationMethod('MONTE_CARLO')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              simulationMethod === 'MONTE_CARLO'
                ? 'bg-indigo-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            Monte Carlo (P10-P90)
          </button>
          <button
            onClick={() => setSimulationMethod('DETERMINISTIC')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              simulationMethod === 'DETERMINISTIC'
                ? 'bg-indigo-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            Deterministic
          </button>
        </div>
      </div>

      {/* Scenario Name */}
      <div>
        <label className="block text-xs font-medium text-slate-400 mb-1">Scenario Label</label>
        <input
          type="text"
          value={scenarioName}
          onChange={(e) => setScenarioName(e.target.value)}
          className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
        />
      </div>

      {/* Sliders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
        {/* Lead Conversion */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Lead Conversion Rate</span>
            <span className="font-bold text-indigo-400">{(leadConversion * 100).toFixed(1)}% (Base: 8.0%)</span>
          </div>
          <input
            type="range"
            min="0.01"
            max="0.30"
            step="0.005"
            value={leadConversion}
            onChange={(e) => setLeadConversion(parseFloat(e.target.value))}
            className="w-full accent-indigo-500 cursor-pointer"
          />
        </div>

        {/* Deal Value */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Average Deal Value</span>
            <span className="font-bold text-emerald-400">${dealValue.toLocaleString()} (Base: $4,500)</span>
          </div>
          <input
            type="range"
            min="1000"
            max="15000"
            step="250"
            value={dealValue}
            onChange={(e) => setDealValue(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>

        {/* Lead Volume */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Monthly Inbound Leads</span>
            <span className="font-bold text-purple-400">{leadVolume} Leads (Base: 120)</span>
          </div>
          <input
            type="range"
            min="20"
            max="500"
            step="10"
            value={leadVolume}
            onChange={(e) => setLeadVolume(parseInt(e.target.value, 10))}
            className="w-full accent-purple-500 cursor-pointer"
          />
        </div>

        {/* FTE Capacity */}
        <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
          <div className="flex justify-between text-xs mb-1.5">
            <span className="text-slate-300 font-medium">Active Engineering Capacity</span>
            <span className="font-bold text-amber-400">{fteCapacity.toFixed(1)} FTE (Base: 6.0)</span>
          </div>
          <input
            type="range"
            min="2"
            max="25"
            step="0.5"
            value={fteCapacity}
            onChange={(e) => setFteCapacity(parseFloat(e.target.value))}
            className="w-full accent-amber-500 cursor-pointer"
          />
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-slate-800">
        <div className="text-xs text-slate-500 flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
          Simulations are sandboxed and evaluated across 12 monthly cycles.
        </div>
        <button
          onClick={handleRunSimulation}
          disabled={loading}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition flex items-center gap-2 shadow-lg shadow-indigo-600/25"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Simulating {iterations} iterations...
            </>
          ) : (
            <>Run Sandboxed Simulation</>
          )}
        </button>
      </div>
    </div>
  );
};
