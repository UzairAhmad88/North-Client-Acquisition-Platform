import React from 'react';
import Link from 'next/link';
import { Globe, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { GlobalInfrastructureCommandCenterDashboard } from '@/components/global_infrastructure';

export const metadata = {
  title: 'Planetary Infrastructure Map | Uzaii Global Infrastructure',
  description: 'Interactive geographic visualization of data centers, POPs, and subsea cable backbones.',
};

export default function MapPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link
          href="/global-infrastructure"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Global Command Center
        </Link>
        <div className="text-xs text-slate-500 font-mono">
          Route: /global-infrastructure/map
        </div>
      </div>

      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-sky-500/10 border border-sky-500/20 rounded-lg text-sky-400">
            <Globe className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Planetary Infrastructure Map</h1>
            <p className="text-xs text-slate-400">Interactive geographic visualization of data centers, POPs, and subsea cable backbones.</p>
          </div>
        </div>
      </div>

      <GlobalInfrastructureCommandCenterDashboard />
    </div>
  );
}
