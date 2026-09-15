import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Incidents | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Incidents',
};

export default function IncidentsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
