import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Experiments | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Experiments',
};

export default function ExperimentsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
