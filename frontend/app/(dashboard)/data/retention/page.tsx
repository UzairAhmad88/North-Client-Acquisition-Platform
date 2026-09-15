import React from 'react';
import { DataCommandCenterDashboard } from '@/components/data_os';

export const metadata = {
  title: 'Retention Policies & Legal Holds | Autonomous Data & Knowledge OS',
  description: 'Enterprise Retention Policies & Legal Holds component of Uzaii Autonomous Data & Knowledge Operating System',
};

export default function RetentionPage() {
  return (
    <div className="space-y-4">
      <div className="border-b border-slate-800 pb-3 px-6 pt-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Retention Policies & Legal Holds</h2>
        <p className="text-xs text-slate-400">Autonomous Data & Knowledge Operating System Module</p>
      </div>
      <DataCommandCenterDashboard />
    </div>
  );
}
