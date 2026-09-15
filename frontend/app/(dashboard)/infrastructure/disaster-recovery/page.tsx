import React from 'react';
import Link from 'next/link';
import { Cloud, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { InfrastructureCommandCenterDashboard } from '@/components/infrastructure';

export const metadata = {
  title: 'Disaster Recovery | Uzaii Cloud OS',
  description: 'Automated DR plans, failover orchestration, and periodic restore verification.',
};

export default function DisasterRecoveryPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link
          href="/infrastructure"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Infrastructure Command Center
        </Link>
        <div className="text-xs text-slate-500 font-mono">
          Route: /infrastructure/disaster-recovery
        </div>
      </div>

      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-indigo-400">
            <Cloud className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Disaster Recovery</h1>
            <p className="text-xs text-slate-400">Automated DR plans, failover orchestration, and periodic restore verification.</p>
          </div>
        </div>
      </div>

      <InfrastructureCommandCenterDashboard />
    </div>
  );
}
