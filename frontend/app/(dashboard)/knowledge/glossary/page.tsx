'use client';

import React from 'react';
import Link from 'next/link';

export default function GlossaryPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Link href="/knowledge" className="text-xs text-indigo-400 hover:underline">
              ← Knowledge Fabric
            </Link>
            <span className="text-slate-600">/</span>
            <span className="text-xs text-slate-400">Business Glossary</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">Business Glossary</h1>
        </div>
        <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-xs font-mono">
          Phase 77 Integrated
        </span>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-sm text-slate-300">
        <p>Enterprise Business Glossary operational telemetry, analytics, and policy controls are active.</p>
      </div>
    </div>
  );
}
