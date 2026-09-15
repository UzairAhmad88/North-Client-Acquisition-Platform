'use client';

import React, { useState } from 'react';
import { DRPlan, DRDrill } from '@/lib/api/reliability';

interface Props {
  plans: DRPlan[];
  drills: DRDrill[];
  onRunDrill: (scenario: string, initiatedBy: string) => void;
  isLoading: boolean;
}

export function DisasterRecoveryPlanViewer({ plans, drills, onRunDrill, isLoading }: Props) {
  const [selectedPlan, setSelectedPlan] = useState<DRPlan | null>(plans[0] || null);

  return (
    <div className="space-y-6">
      {/* Plans Section */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-lg font-semibold text-white">14-Step Disaster Recovery Plans & Target RPO / RTO</h3>
            <p className="text-xs text-slate-400">
              Deterministic, dependency-ordered recovery priority matrix with zero circular deadlocks
            </p>
          </div>

          <div className="flex items-center gap-2">
            {plans.map((p) => (
              <button
                key={p.scenario}
                onClick={() => setSelectedPlan(p)}
                className={`px-3 py-1.5 text-xs rounded-xl border transition ${
                  selectedPlan?.scenario === p.scenario
                    ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                    : 'bg-slate-800/60 text-slate-400 border-slate-700 hover:text-white'
                }`}
              >
                {p.plan_name}
              </button>
            ))}
          </div>
        </div>

        {selectedPlan && (
          <div className="space-y-6">
            {/* Plan Metrics Banner */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-slate-950/60 border border-slate-800/80 rounded-xl">
              <div>
                <div className="text-[11px] text-slate-400">Scenario</div>
                <div className="text-sm font-bold text-white uppercase">{selectedPlan.scenario}</div>
              </div>
              <div>
                <div className="text-[11px] text-slate-400">Target RPO (Data Loss Max)</div>
                <div className="text-sm font-bold text-emerald-400 font-mono">
                  {selectedPlan.target_rpo_minutes} minutes
                </div>
              </div>
              <div>
                <div className="text-[11px] text-slate-400">Target RTO (Downtime Max)</div>
                <div className="text-sm font-bold text-cyan-400 font-mono">
                  {selectedPlan.target_rto_minutes} minutes
                </div>
              </div>
              <div>
                <div className="text-[11px] text-slate-400">Failover Region</div>
                <div className="text-sm font-bold text-slate-200">
                  {selectedPlan.primary_region} $\rightarrow$ {selectedPlan.secondary_region}
                </div>
              </div>
            </div>

            {/* 14-Step Recovery Sequence Visualizer */}
            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">
                Recovery Execution Steps ({selectedPlan.recovery_steps.length} Steps)
              </h4>
              <div className="space-y-2">
                {selectedPlan.recovery_steps.map((step) => (
                  <div
                    key={step.step}
                    className="flex items-center justify-between p-3 bg-slate-950/40 border border-slate-800/60 rounded-xl hover:border-slate-700 transition"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-6 h-6 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-xs font-mono font-bold flex items-center justify-center">
                        {step.step}
                      </div>
                      <div>
                        <div className="text-xs font-semibold text-white">{step.name}</div>
                        <div className="text-[10px] text-slate-400">{step.action}</div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-[10px] font-mono text-slate-400">
                        ~{step.expected_duration_seconds}s
                      </span>
                      <span
                        className={`text-[9px] px-2 py-0.5 rounded-full font-semibold ${
                          step.automated
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}
                      >
                        {step.automated ? 'Automated' : 'Manual Signoff'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => onRunDrill(selectedPlan.scenario, 'operator@agencyos.local')}
                disabled={isLoading}
                className="px-4 py-2 bg-rose-600/80 hover:bg-rose-600 text-white text-xs font-semibold rounded-xl transition flex items-center gap-2"
              >
                <span>⚡</span> {isLoading ? 'Simulating...' : `Execute Simulation Drill (${selectedPlan.scenario})`}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* DR Drills Scorecard */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-1">Disaster Recovery Drill Scorecards & Audits</h3>
        <p className="text-xs text-slate-400 mb-4">
          Historical drills with verified RTO timings, zero data loss proof, and lessons learned
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {drills.map((d) => (
            <div key={d.drill_id} className="bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white uppercase">{d.scenario}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  {d.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                <div>
                  <span>Actual RTO: </span>
                  <span className="font-mono text-emerald-400 font-bold">{d.actual_rto_minutes.toFixed(1)} mins</span>
                </div>
                <div>
                  <span>Data Loss (RPO): </span>
                  <span className="font-mono text-emerald-400 font-bold">{d.data_loss_minutes.toFixed(1)} mins</span>
                </div>
              </div>

              <div className="text-[11px] text-slate-300 bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
                <span className="font-semibold text-slate-400 block mb-1">Observations:</span>
                {d.observations}
              </div>

              {d.lessons_learned && d.lessons_learned.length > 0 && (
                <div className="text-[10px] text-slate-400 space-y-1">
                  <span className="font-semibold text-slate-300">Lessons Learned:</span>
                  <ul className="list-disc list-inside space-y-0.5 text-slate-400">
                    {d.lessons_learned.map((l, idx) => (
                      <li key={idx}>{l}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="text-[10px] text-slate-500 pt-1 border-t border-slate-800/40">
                Initiated by {d.initiated_by} at {new Date(d.started_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
