'use client';

import React, { useState, useEffect } from 'react';
import { strategyApi, StrategicInitiative } from '@/lib/api/strategy';

export const InitiativePortfolio: React.FC = () => {
  const [initiatives, setInitiatives] = useState<StrategicInitiative[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [owner, setOwner] = useState('Product Lead');
  const [category, setCategory] = useState('GROWTH');
  const [expectedValue, setExpectedValue] = useState(60000);
  const [estimatedCost, setEstimatedCost] = useState(15000);
  const [fteCapacity, setFteCapacity] = useState(1.5);
  const [durationWeeks, setDurationWeeks] = useState(6);

  const fetchInitiatives = async () => {
    setLoading(true);
    try {
      const res = await strategyApi.listInitiatives();
      setInitiatives(res.data || []);
    } catch (err) {
      console.error('Failed to load initiatives', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInitiatives();
  }, []);

  const handleCreateInitiative = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await strategyApi.createInitiative({
        title,
        owner,
        category,
        expected_value_usd: expectedValue,
        estimated_cost_usd: estimatedCost,
        required_fte_capacity: fteCapacity,
        estimated_duration_weeks: durationWeeks,
      });
      setShowModal(false);
      setTitle('');
      fetchInitiatives();
    } catch (err) {
      console.error('Failed to create initiative', err);
    }
  };

  return (
    <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Strategic Initiatives Portfolio</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Ranked candidate projects evaluated across ROI multiples, FTE capacity demands, and feasibility.
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition flex items-center gap-1.5 shadow-lg shadow-indigo-600/25"
        >
          + Propose Initiative
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center p-8 text-slate-400">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500 mr-3"></div>
          Loading Initiatives...
        </div>
      ) : initiatives.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No initiatives proposed yet.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {initiatives.map((init) => {
            const roi = (init.expected_value_usd / Math.max(1, init.estimated_cost_usd)).toFixed(1);
            return (
              <div key={init.initiative_code} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="text-sm font-bold text-white">{init.title}</h4>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Category: <span className="text-slate-300 font-medium">{init.category}</span> | Owner:{' '}
                      <span className="text-slate-300 font-medium">{init.owner}</span>
                    </p>
                  </div>
                  <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    {roi}x ROI
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-center text-xs py-1 bg-slate-900/60 rounded-lg">
                  <div>
                    <div className="text-slate-500">Est. Cost</div>
                    <div className="font-semibold text-slate-300">${init.estimated_cost_usd.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-slate-500">Exp. Value</div>
                    <div className="font-semibold text-emerald-400">${init.expected_value_usd.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-slate-500">FTE Demand</div>
                    <div className="font-semibold text-amber-400">{init.required_fte_capacity.toFixed(1)} FTE</div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
                  <span>Duration: {init.estimated_duration_weeks} wks</span>
                  <span>Status: <strong className="text-slate-300">{init.status}</strong></span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Proposal Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4">
            <h4 className="text-base font-bold text-white">Propose Strategic Initiative</h4>
            <form onSubmit={handleCreateInitiative} className="space-y-3">
              <div>
                <label className="block text-xs text-slate-400 mb-1">Initiative Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Automated High-Ticket Prospecting Engine"
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Estimated Cost ($)</label>
                  <input
                    type="number"
                    required
                    value={estimatedCost}
                    onChange={(e) => setEstimatedCost(parseFloat(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Expected Value ($)</label>
                  <input
                    type="number"
                    required
                    value={expectedValue}
                    onChange={(e) => setExpectedValue(parseFloat(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-400 mb-1">FTE Capacity (FTE)</label>
                  <input
                    type="number"
                    step="0.5"
                    required
                    value={fteCapacity}
                    onChange={(e) => setFteCapacity(parseFloat(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs text-slate-400 mb-1">Duration (Weeks)</label>
                  <input
                    type="number"
                    required
                    value={durationWeeks}
                    onChange={(e) => setDurationWeeks(parseInt(e.target.value, 10))}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs text-slate-400 mb-1">Owner</label>
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
                  Save Initiative
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
