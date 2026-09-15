import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Tools | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Tools',
};

export default function ToolsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
