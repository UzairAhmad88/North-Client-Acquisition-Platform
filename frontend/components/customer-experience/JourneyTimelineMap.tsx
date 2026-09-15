'use client';

import React from 'react';
import { GitCommit, CheckCircle2, Clock, AlertTriangle, ArrowRight } from 'lucide-react';
import { CustomerJourneyItem } from '../../lib/api/customerExperience';

interface JourneyTimelineMapProps {
  journey: CustomerJourneyItem;
}

export const JourneyTimelineMap: React.FC<JourneyTimelineMapProps> = ({ journey }) => {
  const stages = [
    { name: 'discovery', label: 'Discovery' },
    { name: 'evaluation', label: 'Evaluation' },
    { name: 'purchase', label: 'Purchase' },
    { name: 'onboarding', label: 'Onboarding' },
    { name: 'activation', label: 'Activation' },
    { name: 'adoption', label: 'Adoption' },
    { name: 'value', label: 'Value' },
    { name: 'renewal', label: 'Renewal' },
    { name: 'expansion', label: 'Expansion' },
  ];

  const currentIdx = stages.findIndex((s) => s.name === journey.current_stage.toLowerCase());

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <GitCommit className="h-4 w-4 text-cyan-400" />
            Active Customer Journey Timeline
          </h3>
          <p className="text-xs text-slate-400">
            Type: <span className="font-semibold text-slate-200 capitalize">{journey.journey_type}</span> | Stage: <span className="font-semibold text-indigo-400 capitalize">{journey.current_stage}</span>
          </p>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase font-semibold">
          Progress: {Math.round(journey.completion_rate * 100)}%
        </span>
      </div>

      <div className="overflow-x-auto pb-2">
        <div className="flex items-center min-w-[700px] gap-2">
          {stages.map((stg, index) => {
            const isCompleted = currentIdx > index;
            const isCurrent = currentIdx === index;
            const isPending = currentIdx < index;

            return (
              <React.Fragment key={stg.name}>
                <div
                  className={`flex-1 p-2.5 rounded-lg border text-center transition-all ${
                    isCurrent
                      ? 'bg-indigo-600/20 border-indigo-500 text-indigo-200 shadow-lg shadow-indigo-500/10'
                      : isCompleted
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-slate-800/20 border-slate-800 text-slate-500'
                  }`}
                >
                  <div className="flex justify-center mb-1">
                    {isCompleted && <CheckCircle2 className="h-4 w-4 text-emerald-400" />}
                    {isCurrent && <Clock className="h-4 w-4 text-indigo-400 animate-pulse" />}
                    {isPending && <div className="h-2 w-2 rounded-full bg-slate-700 mt-1" />}
                  </div>
                  <div className="text-[11px] font-semibold">{stg.label}</div>
                  <div className="text-[9px] font-mono uppercase text-slate-400 mt-0.5">
                    {isCompleted ? 'Done' : isCurrent ? 'Active' : 'Pending'}
                  </div>
                </div>
                {index < stages.length - 1 && (
                  <ArrowRight className="h-3 w-3 text-slate-600 flex-shrink-0" />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};
