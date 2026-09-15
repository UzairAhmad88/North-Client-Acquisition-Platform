'use client';

import React from 'react';
import { ClientRequirement } from '@/lib/api/requirements';
import { RequirementCard } from './RequirementCard';

interface RequirementsListProps {
  requirements: ClientRequirement[];
  onConfirmRequirement?: (id: string) => void;
}

export function RequirementsList({ requirements, onConfirmRequirement }: RequirementsListProps) {
  if (!requirements || requirements.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-8 text-center text-slate-400">
        No requirements extracted yet. Click &quot;Analyze Discovery Session&quot; to run intelligence analysis.
      </div>
    );
  }

  const explicitReqs = requirements.filter((r) => r.explicit);
  const inferredReqs = requirements.filter((r) => !r.explicit);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-slate-300">
          Client Explicit Requirements ({explicitReqs.length})
        </h3>
        <div className="space-y-3">
          {explicitReqs.map((req) => (
            <RequirementCard key={req.id} requirement={req} onConfirm={onConfirmRequirement} />
          ))}
        </div>
      </div>

      {inferredReqs.length > 0 && (
        <div>
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-purple-300">
            AI Inferred Requirements ({inferredReqs.length})
          </h3>
          <div className="space-y-3">
            {inferredReqs.map((req) => (
              <RequirementCard key={req.id} requirement={req} onConfirm={onConfirmRequirement} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
