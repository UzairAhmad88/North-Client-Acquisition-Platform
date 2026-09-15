import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Governance | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Governance',
};

export default function GovernancePage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
