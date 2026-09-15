'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { ChangeWorkspace } from '@/components/changes/ChangeWorkspace';

export default function ChangeDetailPage() {
  const params = useParams();
  const projectId = (params?.id as string) || 'proj-001';

  return (
    <div className="min-h-screen bg-slate-950">
      <ChangeWorkspace projectId={projectId} />
    </div>
  );
}
