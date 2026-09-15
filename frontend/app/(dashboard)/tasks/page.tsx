import React from 'react';
import { HumanTaskQueue } from '@/components/orchestration/HumanTaskQueue';

export const metadata = {
  title: 'Human Tasks Queue | Uzaii',
  description: 'Human-in-the-loop review and approval queue.',
};

export default function HumanTasksPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100">Human Approval Queue</h1>
        <p className="text-xs text-slate-400 mt-1">
          Review, approve, or reject sensitive business actions and workflow transitions.
        </p>
      </div>
      <HumanTaskQueue />
    </div>
  );
}
