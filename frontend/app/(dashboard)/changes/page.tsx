'use client';

import React from 'react';
import { ChangeWorkspace } from '@/components/changes/ChangeWorkspace';

export default function ChangesDashboardPage() {
  return (
    <div className="min-h-screen bg-slate-950">
      <ChangeWorkspace projectId="proj-001" />
    </div>
  );
}
