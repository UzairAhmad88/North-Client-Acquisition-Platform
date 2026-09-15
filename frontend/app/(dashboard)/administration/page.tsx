import React from 'react';
import { AdministrationDashboard } from '@/components/administration/AdministrationDashboard';

export const metadata = {
  title: 'Platform Administration & System Control Center | Uzaii Business OS',
  description: 'Centralized configuration registry, dynamic policy engine, feature flags, environment promotion, provider gateways, and emergency controls.',
};

export default function AdministrationPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <AdministrationDashboard />
    </div>
  );
}
