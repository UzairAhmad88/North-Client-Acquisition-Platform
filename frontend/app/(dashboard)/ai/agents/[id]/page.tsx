import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Agents/Detail | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Agents/Detail',
};

export default function AgentDetailPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
