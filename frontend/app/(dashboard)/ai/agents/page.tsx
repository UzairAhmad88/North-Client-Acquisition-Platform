import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Agents | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Agents',
};

export default function AgentsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
