import React from 'react';
import { AutomationRuleBuilder } from '@/components/orchestration/AutomationRuleBuilder';

export const metadata = {
  title: 'Automation Rules | Uzaii',
  description: 'Event-driven automation rules engine.',
};

export default function AutomationPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100">Automation Engine</h1>
        <p className="text-xs text-slate-400 mt-1">
          Configure declarative WHEN / IF / THEN automation rules across business lifecycles.
        </p>
      </div>
      <AutomationRuleBuilder />
    </div>
  );
}
