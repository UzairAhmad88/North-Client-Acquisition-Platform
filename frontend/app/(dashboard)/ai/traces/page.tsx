import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Traces | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Traces',
};

export default function TracesPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
