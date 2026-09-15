'use client';

import React from 'react';
import Link from 'next/link';
import { Building2, ArrowRight, ShieldCheck, FolderGit2, CheckCircle2 } from 'lucide-react';

export default function ClientProjectsPage() {
  const sampleProjects = [
    {
      id: 'proj-001',
      name: 'Enterprise Customer Portal System',
      client: 'Acme Global Corp',
      status: 'IN_PROGRESS',
      phase: 'Sprint 3 Execution',
      updated_at: '2026-09-08',
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-8 max-w-7xl mx-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center space-x-2">
            <Building2 className="w-6 h-6 text-blue-400" />
            <span>Client Projects Directory</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Projects you have client member access to under North's delivery workspace.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {sampleProjects.map((p) => (
          <div
            key={p.id}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 hover:border-slate-700 transition shadow-xl"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-bold text-white text-lg">{p.name}</h3>
                <p className="text-xs text-slate-400 mt-0.5">{p.client} • ID: {p.id}</p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{p.status}</span>
              </span>
            </div>

            <div className="text-xs text-slate-300 space-y-1 bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div>
                <span className="text-slate-400">Current Phase:</span> <strong className="text-slate-200">{p.phase}</strong>
              </div>
              <div>
                <span className="text-slate-400">Last Activity:</span> {p.updated_at}
              </div>
            </div>

            <div className="pt-2">
              <Link
                href={`/client-portal/projects/${p.id}`}
                className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 rounded-xl text-xs font-semibold text-white flex items-center justify-center space-x-2 shadow-lg shadow-blue-600/20 transition"
              >
                <span>Enter Project Workspace</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
