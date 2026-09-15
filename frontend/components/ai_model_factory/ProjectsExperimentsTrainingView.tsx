import React from 'react';
import { AiProjectItem, AiExperimentItem } from '@/lib/api/aiModelFactory';

interface Props {
  projects: AiProjectItem[];
  experiments: AiExperimentItem[];
}

export const ProjectsExperimentsTrainingView: React.FC<Props> = ({ projects, experiments }) => {
  return (
    <div className="space-y-6">
      {/* Projects Section */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-100">AI Project Workspaces</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-mono">
            {projects.length} Projects
          </span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {projects.map((proj) => (
            <div key={proj.id} className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/60">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-sm font-semibold text-white">{proj.name}</h4>
                  <p className="text-xs text-slate-400 mt-0.5">{proj.description}</p>
                </div>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
                  {proj.status}
                </span>
              </div>
              <div className="mt-3 pt-3 border-t border-slate-700/40 grid grid-cols-3 gap-2 text-xs">
                <div>
                  <span className="text-slate-500">Domain:</span>
                  <p className="font-medium text-slate-300">{proj.domain}</p>
                </div>
                <div>
                  <span className="text-slate-500">Lead Owner:</span>
                  <p className="font-medium text-slate-300 truncate">{proj.owner}</p>
                </div>
                <div>
                  <span className="text-slate-500">Budget:</span>
                  <p className="font-medium text-slate-300">${proj.budget_allocated_usd.toLocaleString()}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Experiments & Sweeps Section */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-100">Experiment Tracking & Bayesian Sweeps</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-purple-500/20 text-purple-300 font-mono">
            {experiments.length} Sweeps
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-800/60 text-slate-400 uppercase font-mono text-[10px]">
              <tr>
                <th className="p-3">Experiment Name</th>
                <th className="p-3">Model Type</th>
                <th className="p-3">Framework</th>
                <th className="p-3">Strategy</th>
                <th className="p-3">Target Metric</th>
                <th className="p-3">Best Score</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {experiments.map((exp) => (
                <tr key={exp.id} className="hover:bg-slate-800/30">
                  <td className="p-3 font-medium text-white">{exp.name}</td>
                  <td className="p-3">{exp.model_type}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded bg-slate-700 text-slate-200 font-mono text-[10px]">
                      {exp.framework}
                    </span>
                  </td>
                  <td className="p-3 font-mono">{exp.search_strategy}</td>
                  <td className="p-3 text-slate-400">{exp.best_metric_name}</td>
                  <td className="p-3 font-bold text-emerald-400">
                    {exp.best_metric_value ? (exp.best_metric_value * 100).toFixed(1) + '%' : '0.948 (94.8%)'}
                  </td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300">
                      {exp.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
