import React from 'react';
import { AiDriftEventItem } from '@/lib/api/aiModelFactory';

interface Props {
  driftEvents: AiDriftEventItem[];
}

export const MonitoringDriftRetrainingView: React.FC<Props> = ({ driftEvents }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Live Drift Monitoring & Continuous Retraining</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Statistical distribution shifts (PSI, KS-Statistic), concept drift alerts, and automated retraining triggers.
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-mono">
          {driftEvents.length} Drift Sensors
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-800/60 text-slate-400 uppercase font-mono text-[10px]">
            <tr>
              <th className="p-3">Deployment ID</th>
              <th className="p-3">Drift Type</th>
              <th className="p-3">Metric</th>
              <th className="p-3">Current Value</th>
              <th className="p-3">Warning Threshold</th>
              <th className="p-3">Status</th>
              <th className="p-3">Triggered Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {driftEvents.map((evt) => (
              <tr key={evt.id} className="hover:bg-slate-800/30">
                <td className="p-3 font-mono text-slate-400">{evt.deployment_id}</td>
                <td className="p-3 font-medium text-white">{evt.drift_type}</td>
                <td className="p-3 font-mono">{evt.metric_name}</td>
                <td className="p-3 font-bold text-emerald-400">{evt.metric_value.toFixed(3)}</td>
                <td className="p-3 font-mono text-slate-400">{evt.threshold.toFixed(2)}</td>
                <td className="p-3">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      evt.is_breached
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        : 'bg-emerald-500/20 text-emerald-300'
                    }`}
                  >
                    {evt.is_breached ? 'BREACH DETECTED' : 'HEALTHY'}
                  </span>
                </td>
                <td className="p-3 text-slate-400 font-mono text-[11px]">{evt.suggested_action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
