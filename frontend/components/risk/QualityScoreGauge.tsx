import React from 'react';

interface QualityScoreGaugeProps {
  score: number;
}

export function QualityScoreGauge({ score }: QualityScoreGaugeProps) {
  let color = 'text-emerald-400 border-emerald-500/30';
  if (score < 50) {
    color = 'text-rose-400 border-rose-500/30';
  } else if (score < 80) {
    color = 'text-amber-400 border-amber-500/30';
  }

  return (
    <div className="flex flex-col items-center justify-center p-3 rounded-lg bg-zinc-900/60 border border-zinc-800">
      <span className="text-xs text-zinc-400 font-medium">Quality Score</span>
      <span className={`text-2xl font-bold mt-1 ${color}`}>{score.toFixed(1)} / 100</span>
    </div>
  );
}
