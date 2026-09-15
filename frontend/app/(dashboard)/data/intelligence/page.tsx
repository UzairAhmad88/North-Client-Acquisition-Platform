import React from 'react';
import { DataCommandCenterDashboard } from '@/components/data_os';

export const metadata = {
  title: 'Data Change Intelligence & Recommendations | Autonomous Data & Knowledge OS',
  description: 'Enterprise Data Change Intelligence & Recommendations component of Uzaii Autonomous Data & Knowledge Operating System',
};

export default function IntelligencePage() {
  return (
    <div className="space-y-4">
      <div className="border-b border-slate-800 pb-3 px-6 pt-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Data Change Intelligence & Recommendations</h2>
        <p className="text-xs text-slate-400">Autonomous Data & Knowledge Operating System Module</p>
      </div>
      <DataCommandCenterDashboard />
    </div>
  );
}
