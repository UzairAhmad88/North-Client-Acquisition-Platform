'use client';

import React from 'react';
import { ScopeItem } from '@/lib/api/requirements';

interface ScopePanelProps {
  scopeItems: ScopeItem[];
}

export function ScopePanel({ scopeItems }: ScopePanelProps) {
  if (!scopeItems || scopeItems.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-center text-xs text-slate-400">
        No scope breakdown items.
      </div>
    );
  }

  const inScope = scopeItems.filter((i) => i.scope_status === 'IN_SCOPE');
  const optional = scopeItems.filter((i) => i.scope_status === 'OPTIONAL');
  const unknown = scopeItems.filter((i) => i.scope_status === 'UNKNOWN');
  const outOfScope = scopeItems.filter((i) => i.scope_status === 'OUT_OF_SCOPE');

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
        Project Scope Matrix
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* IN SCOPE */}
        <div className="rounded-lg border border-emerald-500/30 bg-emerald-950/10 p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            In Scope ({inScope.length})
          </h4>
          <ul className="mt-2 space-y-1.5 text-xs text-slate-300">
            {inScope.map((item) => (
              <li key={item.id} className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                {item.description}
              </li>
            ))}
            {inScope.length === 0 && <li className="text-slate-500 italic">None defined yet</li>}
          </ul>
        </div>

        {/* OPTIONAL */}
        <div className="rounded-lg border border-purple-500/30 bg-purple-950/10 p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400">
            Optional / Phase 2 ({optional.length})
          </h4>
          <ul className="mt-2 space-y-1.5 text-xs text-slate-300">
            {optional.map((item) => (
              <li key={item.id} className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-purple-400" />
                {item.description}
              </li>
            ))}
            {optional.length === 0 && <li className="text-slate-500 italic">None defined yet</li>}
          </ul>
        </div>

        {/* UNKNOWN */}
        <div className="rounded-lg border border-amber-500/30 bg-amber-950/10 p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
            Unknown / Clarification Needed ({unknown.length})
          </h4>
          <ul className="mt-2 space-y-1.5 text-xs text-slate-300">
            {unknown.map((item) => (
              <li key={item.id} className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                {item.description}
              </li>
            ))}
            {unknown.length === 0 && <li className="text-slate-500 italic">None defined yet</li>}
          </ul>
        </div>

        {/* OUT OF SCOPE */}
        <div className="rounded-lg border border-slate-700 bg-slate-900/40 p-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Out of Scope ({outOfScope.length})
          </h4>
          <ul className="mt-2 space-y-1.5 text-xs text-slate-400">
            {outOfScope.map((item) => (
              <li key={item.id} className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-slate-500" />
                {item.description}
              </li>
            ))}
            {outOfScope.length === 0 && <li className="text-slate-500 italic">None defined yet</li>}
          </ul>
        </div>
      </div>
    </div>
  );
}
