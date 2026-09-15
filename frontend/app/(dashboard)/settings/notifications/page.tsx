import React from 'react';
import { NotificationPreferencesManager } from '@/components/communication/NotificationPreferencesManager';

export const metadata = {
  title: 'Notification Preferences | Uzaii',
  description: 'Manage notification channels, recipient routes, and quiet hours schedules.',
};

export default function NotificationSettingsPage() {
  return (
    <div className="p-4 md:p-6 max-w-5xl mx-auto">
      <NotificationPreferencesManager />
    </div>
  );
}
