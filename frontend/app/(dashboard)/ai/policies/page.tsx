import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Policies | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Policies',
};

export default function PoliciesPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
