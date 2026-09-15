import React from 'react';
import { EventExplorer } from '@/components/orchestration/EventExplorer';

export const metadata = {
  title: 'Event Bus Explorer | Uzaii',
  description: 'Transactional event bus explorer and controlled replay.',
};

export default function EventsPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100">Domain Event Bus</h1>
        <p className="text-xs text-slate-400 mt-1">
          Explore historical domain events, inspected payloads, and trigger controlled replay.
        </p>
      </div>
      <EventExplorer />
    </div>
  );
}
