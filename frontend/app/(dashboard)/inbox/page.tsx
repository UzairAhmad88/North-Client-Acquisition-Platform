import React from 'react';
import { CommunicationWorkspace } from '@/components/communication/CommunicationWorkspace';

export const metadata = {
  title: 'Unified Inbox & Communications | Uzaii',
  description: 'Enterprise notification center, messaging, real-time collaboration, and delivery auditing.',
};

export default function InboxPage() {
  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto">
      <CommunicationWorkspace />
    </div>
  );
}
