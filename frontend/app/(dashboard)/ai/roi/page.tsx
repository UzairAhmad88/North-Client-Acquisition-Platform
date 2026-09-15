import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Roi | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Roi',
};

export default function RoiPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
