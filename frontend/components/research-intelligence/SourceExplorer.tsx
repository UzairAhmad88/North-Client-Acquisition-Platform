'use client';

import React from 'react';
import { ShieldCheck, ShieldAlert, Globe, FileText, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';
import { ResearchSource } from '../../lib/api/research_intelligence';

interface SourceExplorerProps {
  sources: ResearchSource[];
  onAddSource?: (source: Partial<ResearchSource>) => void;
}

export const SourceExplorer: React.FC<SourceExplorerProps> = ({ sources }) => {
  const getTrustBadge = (trust: string) => {
    switch (trust.toUpperCase()) {
      case 'PRIMARY':
        return { label: 'Primary', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
      case 'OFFICIAL':
      case 'GOVERNMENT':
        return { label: trust, color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
      case 'ACADEMIC':
      case 'PROFESSIONAL':
        return { label: trust, color: 'bg-purple-500/10 text-purple-400 border-purple-500/30' };
      case 'SECONDARY':
        return { label: 'Secondary', color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
      default:
        return { label: 'Community / Unverified', color: 'bg-slate-500/10 text-slate-400 border-slate-500/30' };
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Globe className="h-4 w-4 text-cyan-400" />
            Verified Source Registry
          </h3>
          <p className="text-xs text-slate-400">
            Cataloged sources verified against SSRF, authority weighting, and provenance tracking.
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
          {sources.length} Sources Cataloged
        </span>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
        {sources.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            No research sources registered in this workspace yet.
          </div>
        ) : (
          sources.map((src) => {
            const badge = getTrustBadge(src.trust_level || 'UNKNOWN');
            return (
              <div
                key={src.id}
                className="p-3.5 rounded-lg border border-slate-800/80 bg-slate-950/40 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="text-xs font-semibold text-white truncate">
                        {src.title || src.url || 'Untitled Source'}
                      </h4>
                      <span className={`text-[10px] px-2 py-0.5 rounded border font-medium ${badge.color}`}>
                        {badge.label}
                      </span>
                    </div>
                    {src.url && (
                      <a
                        href={src.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[11px] text-cyan-400 hover:underline flex items-center gap-1 truncate mb-1"
                      >
                        {src.url}
                        <ExternalLink className="h-2.5 w-2.5 inline" />
                      </a>
                    )}
                    {src.publisher && (
                      <span className="text-[10px] text-slate-400">
                        Publisher: <span className="text-slate-300 font-medium">{src.publisher}</span>
                      </span>
                    )}
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-[10px] text-slate-400">Authority:</div>
                    <div className="text-xs font-bold font-mono text-emerald-400">
                      {Math.round((src.authority_score || 0.8) * 100)}%
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
