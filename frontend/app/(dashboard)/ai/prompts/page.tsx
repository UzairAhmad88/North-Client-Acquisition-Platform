import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Prompts | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Prompts',
};

export default function PromptsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
