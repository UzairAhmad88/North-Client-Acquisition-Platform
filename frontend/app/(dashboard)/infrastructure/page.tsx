import React from 'react';
import { InfrastructureCommandCenterDashboard } from '@/components/infrastructure';

export const metadata = {
  title: 'Cloud Operating System & Autonomous Infrastructure | Uzaii',
  description: 'Autonomous multi-cloud operating system, Kubernetes intelligence, FinOps, and governed self-optimization.',
};

export default function InfrastructurePage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <InfrastructureCommandCenterDashboard />
    </div>
  );
}
