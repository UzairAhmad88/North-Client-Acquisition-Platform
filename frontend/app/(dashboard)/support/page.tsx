'use client';

import React from 'react';
import { SupportWorkspace } from '@/components/support/SupportWorkspace';

export default function SupportDashboardPage() {
  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <SupportWorkspace clientAccountId="client-primary" />
    </div>
  );
}
