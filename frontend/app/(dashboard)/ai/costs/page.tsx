import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Costs | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Costs',
};

export default function CostsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
