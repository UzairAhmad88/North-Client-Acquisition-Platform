import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Settings | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Settings',
};

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
