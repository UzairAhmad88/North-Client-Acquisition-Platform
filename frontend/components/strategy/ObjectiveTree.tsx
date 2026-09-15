'use client';

import React, { useState, useEffect } from 'react';
import { strategyApi, StrategicObjective } from '@/lib/api/strategy';

export const ObjectiveTree: React.FC = () => {
  const [objectives, setObjectives] = useState<StrategicObjective[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [name, setName] = useState('');
  const [targetValue, setTargetValue] = useState(250000);
  const [unit, setUnit] = useState('USD');
  const [pillar, setPillar] = useState('GROWTH');
  const [owner, setOwner] = useState('Executive Leadership');

  const fetchObjectives = async () => {
    setLoading(true);
    try {
      const res = await strategyApi.listObjectives();
      setObjectives(Array.isArray(res) ? res : ((res as any)?.data || []));
    } catch (err) {
      console.error('Failed to load objectives', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchObjectives();
  }, []);

  const handleCreateObjective = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await strategyApi.createObjective({
        name,
        target_value: targetValue,
        unit,
        strategic_pillar: pillar,
        owner,
      });
      setShowModal(false);
      setName('');
      fetchObjectives();
    } catch (err) {
      console.error('Failed to create objective', err);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Strategic Objectives & Measurable OKRs</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Pillar-anchored quantitative business targets with verifiable progress telemetry.
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition flex items-center gap-1.5 shadow-lg shadow-indigo-600/25"
        >
          + Add Objective
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center p-8 text-slate-400">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500 mr-3"></div>
          Loading Objectives...
        </div>
      ) : objectives.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No strategic objectives recorded. Create one above.</div>
      ) : (
        <div className="space-y-4">
          {objectives.map((obj) => {
            const statusColor =
              obj.status === 'ACHIEVED'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : obj.status === 'ON_TRACK'
                ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                : obj.status === 'AT_RISK'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                : 'bg-rose-500/10 text-rose-400 border-rose-500/20';

            return (
              <div key={obj.objective_code} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-3">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-white">{obj.name}</span>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${statusColor}`}>
                        {obj.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Pillar: <span className="text-slate-300 font-medium">{obj.strategic_pillar}</span> | Owner:{' '}
                      <span className="text-slate-300 font-medium">{obj.owner}</span>
                    </p>
                  </div>

                  <div className="text-right">
                    <div className="text-xs text-slate-400 font-medium">
                      Current: {obj.unit === 'USD' ? `$${obj.current_value.toLocaleString()}` : `${obj.current_value} ${obj.unit}`} /{' '}
                      <strong className="text-white">
                        {obj.unit === 'USD' ? `$${obj.target_value.toLocaleString()}` : `${obj.target_value} ${obj.unit}`}
                      </strong>
                    </div>
                    <div className="text-xs font-bold text-indigo-400">{obj.progress_percentage.toFixed(1)}% Completed</div>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, Math.max(0, obj.progress_percentage))}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Creation Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4">
            <h4 className="text-base font-bold text-white">Create Strategic Objective</h4>
            <form onSubmit={handleCreateObjective} className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Objective Title</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Accelerate High-Margin AI Retainers"
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Target Value</label>
                  <input
                    type="number"
                    required
                    value={targetValue}
                    onChange={(e) => setTargetValue(parseFloat(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Unit</label>
                  <select
                    value={unit}
                    onChange={(e) => setUnit(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="USD">USD ($)</option>
                    <option value="CLIENTS">Clients</option>
                    <option value="PERCENT">Percent (%)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Strategic Pillar</label>
                <select
                  value={pillar}
                  onChange={(e) => setPillar(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="GROWTH">Growth</option>
                  <option value="PROFITABILITY">Profitability</option>
                  <option value="AI">AI & Automation</option>
                  <option value="RELIABILITY">Reliability & SRE</option>
                  <option value="MARKET_EXPANSION">Market Expansion</option>
                </select>
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Executive Owner</label>
                <input
                  type="text"
                  required
                  value={owner}
                  onChange={(e) => setOwner(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold"
                >
                  Save Objective
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
