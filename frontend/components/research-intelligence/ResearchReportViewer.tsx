'use client';

import React from 'react';
import { FileText, CheckCircle, AlertOctagon, HelpCircle, ArrowRight, ShieldCheck, Download } from 'lucide-react';
import { ResearchReport } from '../../lib/api/research_intelligence';

interface ResearchReportViewerProps {
  report: ResearchReport;
  onSendToDecisionRoom?: (reportId: string) => void;
}

export const ResearchReportViewer: React.FC<ResearchReportViewerProps> = ({ report, onSendToDecisionRoom }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-sm">
      <div className="flex items-start justify-between gap-4 pb-5 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Report v{report.version || 1}.0
            </span>
            <span className="text-xs text-slate-400">
              Generated {report.created_at ? new Date(report.created_at).toLocaleDateString() : 'Recently'}
            </span>
          </div>
          <h2 className="text-lg font-bold text-white">{report.title}</h2>
        </div>

        {onSendToDecisionRoom && (
          <button
            onClick={() => onSendToDecisionRoom(report.id)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white shadow-sm transition-all"
          >
            <span>Promote to Decision Room</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {/* Executive Summary */}
      <div className="my-5">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Executive Summary</h3>
        <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3.5 rounded-lg border border-slate-800">
          {report.executive_summary || 'Autonomous intelligence synthesis executed across discovered primary and secondary domain sources.'}
        </p>
      </div>

      {/* Scope & Methodology */}
      {report.methodology_scope && (
        <div className="mb-5">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Scope & Methodology</h3>
          <p className="text-xs text-slate-400 leading-relaxed bg-slate-950/20 p-3 rounded-lg border border-slate-800/80">
            {report.methodology_scope}
          </p>
        </div>
      )}

      {/* Key Findings */}
      <div className="mb-5">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Key Synthesized Findings</h3>
        <div className="space-y-2">
          {(report.key_findings || []).map((finding, idx) => (
            <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-200 p-2.5 rounded bg-slate-950/30 border border-slate-800/60">
              <CheckCircle className="h-3.5 w-3.5 text-emerald-400 mt-0.5 shrink-0" />
              <span>{finding}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Evidence & Verification Stats */}
      <div className="grid grid-cols-2 gap-3 mb-5">
        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 text-center">
          <div className="text-xs text-slate-400">Verified Evidence Items</div>
          <div className="text-lg font-bold font-mono text-emerald-400 mt-0.5">
            {report.verified_claims_count || 0}
          </div>
        </div>
        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 text-center">
          <div className="text-xs text-slate-400">Conflicts Analyzed</div>
          <div className="text-lg font-bold font-mono text-amber-400 mt-0.5">
            {report.conflicts_analyzed_count || 0}
          </div>
        </div>
      </div>

      {/* Recommendations & Gaps */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-800">
        <div>
          <h4 className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <ShieldCheck className="h-3.5 w-3.5 text-indigo-400" />
            Actionable Recommendations
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-300">
            {(report.recommendations || ['Maintain active monitoring on competitor pricing']).map((r, i) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="text-indigo-400 font-bold">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <HelpCircle className="h-3.5 w-3.5 text-amber-400" />
            Identified Research Gaps
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-400">
            {(report.identified_gaps || ['Direct customer churn sentiment dataset']).map((g, i) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="text-amber-400 font-bold">•</span>
                <span>{g}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
