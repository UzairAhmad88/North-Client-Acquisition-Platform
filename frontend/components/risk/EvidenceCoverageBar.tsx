import React from 'react';

interface EvidenceCoverageBarProps {
  coverage: number;
}

export function EvidenceCoverageBar({ coverage }: EvidenceCoverageBarProps) {
  const percent = Math.min(100, Math.max(0, Math.round(coverage * 100)));
  let barColor = 'bg-emerald-500';
  if (percent < 50) {
    barColor = 'bg-rose-500';
  } else if (percent < 80) {
    barColor = 'bg-amber-500';
  }

  return (
    <div className="flex flex-col p-3 rounded-lg bg-zinc-900/60 border border-zinc-800">
      <div className="flex justify-between items-center text-xs mb-1">
        <span className="text-zinc-400 font-medium">Evidence Coverage</span>
        <span className="text-zinc-200 font-semibold">{percent}%</span>
      </div>
      <div className="w-full bg-zinc-800 rounded-full h-2 overflow-hidden">
        <div className={`h-2 rounded-full ${barColor}`} style={{ width: `${percent}%` }} />
      </div>
    </div>
  );
}
