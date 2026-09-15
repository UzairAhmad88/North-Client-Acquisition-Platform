'use client';

import React, { useState, useEffect } from 'react';
import { digitalTwinApi, DigitalTwinOverview, SimulationResult } from '@/lib/api/digitalTwin';
import { TwinOverview } from './TwinOverview';
import { ScenarioBuilder } from './ScenarioBuilder';
import { UncertaintyPanel } from './UncertaintyPanel';
import { SensitivityChart } from './SensitivityChart';
import { DecisionMatrix } from './DecisionMatrix';
import { TwinCopilot } from './TwinCopilot';

export const TwinDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'simulation' | 'sensitivity' | 'decisions' | 'copilot'>('overview');
  const [overview, setOverview] = useState<DigitalTwinOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [latestSimulation, setLatestSimulation] = useState<SimulationResult | null>(null);

  const fetchOverview = async () => {
    setLoading(true);
    try {
      const res = await digitalTwinApi.getOverview();
      setOverview((res as any)?.data || res);
    } catch (err) {
      console.error('Failed to load twin overview', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  const handleSimulationComplete = (result: SimulationResult) => {
    setLatestSimulation(result);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 py-6">
      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-3">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition ${
            activeTab === 'overview'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          Twin Overview & State
        </button>
        <button
          onClick={() => setActiveTab('simulation')}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition ${
            activeTab === 'simulation'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          Scenario & Simulation Sandbox
        </button>
        <button
          onClick={() => setActiveTab('sensitivity')}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition ${
            activeTab === 'sensitivity'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          Sensitivity & Elasticity
        </button>
        <button
          onClick={() => setActiveTab('decisions')}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition ${
            activeTab === 'decisions'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          Strategic Decision Governance
        </button>
        <button
          onClick={() => setActiveTab('copilot')}
          className={`px-4 py-2 rounded-xl text-sm font-semibold transition ${
            activeTab === 'copilot'
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          What-If Copilot
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <TwinOverview overview={overview} loading={loading} onRefresh={fetchOverview} />
      )}

      {activeTab === 'simulation' && (
        <div className="space-y-6">
          <ScenarioBuilder onSimulationComplete={handleSimulationComplete} />
          <UncertaintyPanel result={latestSimulation} />
        </div>
      )}

      {activeTab === 'sensitivity' && <SensitivityChart />}

      {activeTab === 'decisions' && <DecisionMatrix />}

      {activeTab === 'copilot' && <TwinCopilot />}
    </div>
  );
};
