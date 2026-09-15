import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Knowledge | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Knowledge',
};

export default function KnowledgePage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
