import React from 'react';

interface RiskBadgeProps {
  decision: 'PASS' | 'REVIEW' | 'BLOCK' | string;
  riskLevel?: 'LOW' | 'MEDIUM' | 'HIGH' | 'BLOCKED' | string;
}

export function RiskBadge({ decision, riskLevel }: RiskBadgeProps) {
  let badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
  let label = decision;

  if (decision === 'BLOCK' || riskLevel === 'BLOCKED' || riskLevel === 'HIGH') {
    badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
  } else if (decision === 'REVIEW' || riskLevel === 'MEDIUM') {
    badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${badgeColor}`}>
      <span className="mr-1">●</span> {label} {riskLevel ? `(${riskLevel})` : ''}
    </span>
  );
}
