import React from 'react';
import { CustomerSuccessDashboard } from '@/components/customer-success/CustomerSuccessDashboard';

export const metadata = {
  title: 'Customer Success & Client Intelligence | Uzaii Platform',
  description: 'Unified client relationship intelligence, multi-factor health scoring, proactive risk matrix, and closed-loop renewals.',
};

export default function CustomerSuccessPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <CustomerSuccessDashboard />
    </div>
  );
}
