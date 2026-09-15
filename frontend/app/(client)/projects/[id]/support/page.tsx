'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { SupportWorkspace } from '@/components/support/SupportWorkspace';

export default function ClientProjectSupportPage() {
  const params = useParams();
  const projectId = typeof params?.id === 'string' ? params.id : undefined;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <SupportWorkspace projectId={projectId} />
    </div>
  );
}
