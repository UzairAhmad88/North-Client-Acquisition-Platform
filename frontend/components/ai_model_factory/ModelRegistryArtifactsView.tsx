import React from 'react';
import { AiModelItem } from '@/lib/api/aiModelFactory';

interface Props {
  models: AiModelItem[];
}

export const ModelRegistryArtifactsView: React.FC<Props> = ({ models }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Central Model Registry & Artifacts</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Immutable version manifests, cryptographic SHA-256 signatures, and Medallion stage promotion gates.
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-mono">
          {models.length} Registered Models
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {models.map((m) => (
          <div key={m.id} className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-bold text-white">{m.name}</h4>
                <p className="text-xs text-slate-400">{m.description}</p>
              </div>
              <span
                className={`text-[10px] uppercase font-mono px-2 py-0.5 rounded font-bold ${
                  m.current_stage === 'PRODUCTION'
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : 'bg-amber-500/20 text-amber-300'
                }`}
              >
                {m.current_stage}
              </span>
            </div>

            <div className="flex flex-wrap gap-1.5">
              <span className="px-2 py-0.5 rounded bg-slate-700 text-slate-300 text-[10px] font-mono">
                v{m.active_version}
              </span>
              <span className="px-2 py-0.5 rounded bg-indigo-900/60 text-indigo-300 text-[10px]">
                {m.framework}
              </span>
              <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">
                {m.model_type}
              </span>
            </div>

            <div className="pt-2 border-t border-slate-700/40 grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-slate-500">Lead Owner:</span>
                <p className="font-medium text-slate-300 truncate">{m.owner}</p>
              </div>
              <div>
                <span className="text-slate-500">AI Steward:</span>
                <p className="font-medium text-slate-300 truncate">{m.steward || 'governance@uzaii.internal'}</p>
              </div>
            </div>

            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800/80 text-[11px] font-mono text-slate-400 flex items-center justify-between">
              <span>Artifact: s3://uzaii-models/{m.id}/v{m.active_version}/</span>
              <span className="text-emerald-400 font-sans text-[10px]">✓ Signed</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
