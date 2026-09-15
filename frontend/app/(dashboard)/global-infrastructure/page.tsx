import React from 'react';
import { GlobalInfrastructureCommandCenterDashboard } from '@/components/global_infrastructure';

export const metadata = {
  title: 'Global Infrastructure & Planet-Scale Reliability | Uzaii',
  description: 'Autonomous data center facilities, edge computing, global traffic steering, and distributed systems intelligence.',
};

export default function GlobalInfrastructurePage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <GlobalInfrastructureCommandCenterDashboard />
    </div>
  );
}
