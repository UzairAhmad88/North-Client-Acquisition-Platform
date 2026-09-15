import React from 'react';
import { DataCommandCenterDashboard } from '@/components/data_os';

export const metadata = {
  title: 'Data Lakehouse Layers (Raw, Bronze, Silver, Gold) | Autonomous Data & Knowledge OS',
  description: 'Enterprise Data Lakehouse Layers (Raw, Bronze, Silver, Gold) component of Uzaii Autonomous Data & Knowledge Operating System',
};

export default function LakePage() {
  return (
    <div className="space-y-4">
      <div className="border-b border-slate-800 pb-3 px-6 pt-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Data Lakehouse Layers (Raw, Bronze, Silver, Gold)</h2>
        <p className="text-xs text-slate-400">Autonomous Data & Knowledge Operating System Module</p>
      </div>
      <DataCommandCenterDashboard />
    </div>
  );
}
