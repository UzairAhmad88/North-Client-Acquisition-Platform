'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { ClientWorkspace } from '@/components/client/ClientWorkspace';

export default function ClientProjectDetailPage() {
  const params = useParams();
  const projectId = (params?.id as string) || 'proj-001';

  return (
    <div className="min-h-screen bg-slate-950">
      <ClientWorkspace projectId={projectId} />
    </div>
  );
}
