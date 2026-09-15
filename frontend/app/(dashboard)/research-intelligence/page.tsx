'use client';

import React from 'react';
import { ResearchDashboard } from '../../../components/research-intelligence';

export default function ResearchIntelligencePage() {
  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="max-w-7xl mx-auto">
        <ResearchDashboard />
      </div>
    </div>
  );
}
