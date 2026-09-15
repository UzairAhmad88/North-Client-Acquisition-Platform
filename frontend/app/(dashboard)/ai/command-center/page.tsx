import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Command Center | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Command Center',
};

export default function CommandCenterPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
