import React from 'react';
import AICommandCenterDashboard from '@/components/ai/AICommandCenterDashboard';

export const metadata = {
  title: 'Permissions | AEAI-OS',
  description: 'Autonomous Enterprise AI Operating System - Permissions',
};

export default function PermissionsPage() {
  return (
    <div className="space-y-6">
      <AICommandCenterDashboard />
    </div>
  );
}
