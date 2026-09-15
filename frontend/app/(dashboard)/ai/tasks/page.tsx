import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Tasks | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Tasks',
};

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
