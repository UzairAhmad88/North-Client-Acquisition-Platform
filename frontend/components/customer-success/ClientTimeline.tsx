'use client';

import React from 'react';
import { ClientTimelineEvent } from '@/lib/api/customer_success';

interface ClientTimelineProps {
  events: ClientTimelineEvent[];
}

export function ClientTimeline({ events }: ClientTimelineProps) {
  if (!events || events.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center text-slate-500">
        No recent relationship timeline events recorded.
      </div>
    );
  }

  const getCategoryBadge = (cat?: string, type?: string) => {
    const key = (cat || type || '').toUpperCase();
    if (key.includes('SUPPORT') || key.includes('TICKET')) {
      return <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded text-[10px] font-medium">SUPPORT</span>;
    }
    if (key.includes('PROJECT') || key.includes('MILESTONE')) {
      return <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded text-[10px] font-medium">DELIVERY</span>;
    }
    if (key.includes('PAYMENT') || key.includes('INVOICE') || key.includes('FINANCE')) {
      return <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[10px] font-medium">FINANCIAL</span>;
    }
    if (key.includes('CONTRACT') || key.includes('RENEWAL')) {
      return <span className="px-2 py-0.5 bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded text-[10px] font-medium">CONTRACT</span>;
    }
    return <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded text-[10px] font-medium">ENGAGEMENT</span>;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white">Client Activity Timeline</h3>
          <p className="text-xs text-slate-400 mt-0.5">Chronological stream across delivery, finance, support, and success.</p>
        </div>
        <span className="text-xs text-slate-500 font-mono">{events.length} events logged</span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-800">
        {events.map((evt, idx) => (
          <div key={evt.id || idx} className="relative group">
            <div className="absolute -left-[29px] top-1 w-3 h-3 rounded-full bg-slate-700 border-2 border-slate-900 group-hover:bg-indigo-500 transition-colors" />
            <div className="bg-slate-950/50 border border-slate-800/80 p-3.5 rounded-xl hover:border-slate-700 transition">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-white">{evt.title}</span>
                  {getCategoryBadge(evt.event_category, evt.event_type)}
                </div>
                <span className="text-[11px] text-slate-500">
                  {new Date(evt.occurred_at).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </span>
              </div>
              {evt.description || evt.summary ? (
                <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{evt.description || evt.summary}</p>
              ) : null}
              {evt.actor_name ? (
                <div className="text-[10px] text-slate-500 mt-2">Actor: {evt.actor_name}</div>
              ) : null}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
