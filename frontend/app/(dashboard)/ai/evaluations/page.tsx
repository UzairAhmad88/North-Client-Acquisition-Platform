import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Evaluations | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Evaluations',
};

export default function EvaluationsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
