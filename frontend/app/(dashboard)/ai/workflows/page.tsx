import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Workflows | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Workflows',
};

export default function WorkflowsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
