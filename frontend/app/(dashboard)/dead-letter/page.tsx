import React from 'react';
import { DeadLetterQueueViewer } from '@/components/orchestration/DeadLetterQueueViewer';

export const metadata = {
  title: 'Dead Letter Queue | Uzaii',
  description: 'DLQ message inspection and retry triage.',
};

export default function DeadLetterPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100">Dead Letter Queue (DLQ)</h1>
        <p className="text-xs text-slate-400 mt-1">
          Triage poisoned or failing domain event messages and schedule safe retries.
        </p>
      </div>
      <DeadLetterQueueViewer />
    </div>
  );
}
