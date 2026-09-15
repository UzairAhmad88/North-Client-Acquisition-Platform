import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Workspace | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Workspace',
};

export default function WorkspacePage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
