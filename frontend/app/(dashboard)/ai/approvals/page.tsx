import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Approvals | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Approvals',
};

export default function ApprovalsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
