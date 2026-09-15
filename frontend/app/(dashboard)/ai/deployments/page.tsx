import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Deployments | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Deployments',
};

export default function DeploymentsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
