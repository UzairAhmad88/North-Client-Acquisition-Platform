import React from 'react';
import { WorkflowWorkspace } from '@/components/orchestration/WorkflowWorkspace';

export const metadata = {
  title: 'Workflow Orchestration | Uzaii',
  description: 'Central workflow orchestration, event bus, and automation control plane.',
};

export default function WorkflowsPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <WorkflowWorkspace />
    </div>
  );
}
