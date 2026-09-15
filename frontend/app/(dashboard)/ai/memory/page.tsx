import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Memory | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Memory',
};

export default function MemoryPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
