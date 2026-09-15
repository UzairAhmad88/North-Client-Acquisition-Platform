'use client';

import React from 'react';
import { QAWorkspace } from '@/components/qa/QAWorkspace';

export default function QADashboardPage() {
  return (
    <div className="min-h-screen bg-slate-950">
      <QAWorkspace projectId="proj-001" />
    </div>
  );
}
