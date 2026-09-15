import React from 'react';
import { ExecutiveOverview } from '@/components/business-os/ExecutiveOverview';

export const metadata = {
  title: 'Executive Command Center | Uzaii Business OS',
  description: 'Unified Business Operating System combining OKRs, 10-dimension health, decision governance, risk register, and scenario simulations.',
};

export default function ExecutiveCommandCenterPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <ExecutiveOverview />
    </div>
  );
}
