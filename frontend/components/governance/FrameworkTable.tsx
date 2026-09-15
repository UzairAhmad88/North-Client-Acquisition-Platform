'use client';

import React from 'react';
import { GovernanceFrameworkItem } from '@/lib/api/governance';
import { BookOpen, CheckCircle, Clock, ShieldAlert } from 'lucide-react';

interface FrameworkTableProps {
  frameworks: GovernanceFrameworkItem[];
  selectedFramework: string;
  onSelect: (code: string) => void;
}

export default function FrameworkTable({ frameworks, selectedFramework, onSelect }: FrameworkTableProps) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-600" />
            <span>Governance Framework Registry</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Pre-seeded regulatory standards & certification frameworks.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg">
          {frameworks.length} Frameworks Active
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              <th className="p-3.5">Code</th>
              <th className="p-3.5">Framework Name</th>
              <th className="p-3.5">Version</th>
              <th className="p-3.5">Category</th>
              <th className="p-3.5">Jurisdiction</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {frameworks.map((fw) => {
              const isSelected = fw.framework_code === selectedFramework;
              return (
                <tr
                  key={fw.framework_code}
                  className={`hover:bg-slate-50/70 transition-colors ${
                    isSelected ? 'bg-indigo-50/60 font-medium' : ''
                  }`}
                >
                  <td className="p-3.5 font-mono font-bold text-slate-900">{fw.framework_code}</td>
                  <td className="p-3.5">
                    <div className="font-semibold text-slate-900">{fw.name}</div>
                    <div className="text-[11px] text-slate-500 truncate max-w-xs">{fw.description}</div>
                  </td>
                  <td className="p-3.5 font-mono">{fw.version}</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium">
                      {fw.category}
                    </span>
                  </td>
                  <td className="p-3.5">{fw.jurisdiction}</td>
                  <td className="p-3.5">
                    <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full font-semibold">
                      <CheckCircle className="w-3 h-3" />
                      {fw.status}
                    </span>
                  </td>
                  <td className="p-3.5">
                    <button
                      onClick={() => onSelect(fw.framework_code)}
                      className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
                        isSelected
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-700'
                      }`}
                    >
                      {isSelected ? 'Viewing' : 'View Requirements'}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
