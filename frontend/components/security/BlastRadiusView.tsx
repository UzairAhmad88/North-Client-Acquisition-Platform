'use client';

import React from 'react';
import { BlastRadiusData } from '@/lib/api/securityOps';
import { Layers, Users, Building, ShieldAlert, Cpu, Database, DollarSign, FolderGit2, X } from 'lucide-react';

interface BlastRadiusViewProps {
  data: BlastRadiusData | null;
  loading: boolean;
  onClose: () => void;
}

export default function BlastRadiusView({ data, loading, onClose }: BlastRadiusViewProps) {
  if (loading || !data) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 text-center text-slate-500 animate-pulse">
        Calculating multi-dimensional blast radius...
      </div>
    );
  }

  const dimensions = [
    { label: 'Affected Users', items: data.affected_users, icon: Users },
    { label: 'Affected Clients', items: data.affected_clients, icon: Building },
    { label: 'Affected Tenants', items: data.affected_tenants, icon: Layers },
    { label: 'Affected AI Agents', items: data.affected_ai_agents, icon: Cpu },
    { label: 'Affected Documents', items: data.affected_documents, icon: Database },
    { label: 'Financial Records', items: data.affected_financial_records, icon: DollarSign },
    { label: 'Projects', items: data.affected_projects, icon: FolderGit2 },
    { label: 'Workflows', items: data.affected_workflows, icon: Layers },
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
      <div className="flex justify-between items-start border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              Downstream Blast Radius (Section 23)
            </span>
            <span className="text-xs text-slate-400">
              Calculated {new Date(data.calculated_at).toLocaleTimeString()}
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-2">Security Impact & Exposure Assessment</h2>
          <p className="text-xs text-slate-600 mt-1">{data.narrative_summary}</p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">Impact Score</div>
            <div className="text-2xl font-extrabold text-slate-900">
              {data.overall_impact_score} <span className="text-xs text-slate-400 font-normal">/100</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {dimensions.map((dim, idx) => {
          const Icon = dim.icon;
          return (
            <div key={idx} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 space-y-2">
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-2 text-slate-700">
                  <Icon className="w-4 h-4 text-indigo-600" />
                  <span className="text-xs font-semibold">{dim.label}</span>
                </div>
                <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-white text-slate-900 border border-slate-200">
                  {dim.items.length}
                </span>
              </div>
              <div className="max-h-24 overflow-y-auto space-y-1 pt-1">
                {dim.items.length === 0 ? (
                  <span className="text-[11px] text-slate-400 italic">None impacted</span>
                ) : (
                  dim.items.map((item, i) => (
                    <div key={i} className="text-[11px] text-slate-600 font-mono truncate">
                      • {item}
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
