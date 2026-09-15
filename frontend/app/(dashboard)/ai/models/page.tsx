import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Models | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Models',
};

export default function ModelsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
