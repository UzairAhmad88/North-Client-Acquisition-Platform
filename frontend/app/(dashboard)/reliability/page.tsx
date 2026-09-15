import React from 'react';
import { ReliabilityDashboard } from '@/components/reliability/ReliabilityDashboard';

export const metadata = {
  title: 'Platform Reliability, SRE & Disaster Recovery | Uzaii Business OS',
  description: 'Multi-layer health checks, circuit breakers, error budget SLOs, automated backups, and 14-step disaster recovery.',
};

export default function ReliabilityPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <ReliabilityDashboard />
    </div>
  );
}
