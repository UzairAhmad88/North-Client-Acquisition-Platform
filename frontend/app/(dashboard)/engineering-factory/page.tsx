import React from 'react';
import { Metadata } from 'next';
import { AutonomousEngineeringDashboard } from '@/components/autonomous_engineering_os';

export const metadata: Metadata = {
  title: 'Autonomous Engineering OS & AI Software Factory | Uzaii Develop By North\'s',
  description: 'Closed-loop autonomous engineering lifecycle: Requirements, Architecture, Sandboxed Coding Agents, PR Reviews, CI/CD, SRE SLOs & Self-Healing.',
};

export default function AutonomousEngineeringPage() {
  return <AutonomousEngineeringDashboard />;
}
