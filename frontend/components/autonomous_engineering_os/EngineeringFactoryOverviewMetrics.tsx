import React from 'react';
import { EngineeringFactoryOverviewMetrics as MetricsType } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  metrics: MetricsType | null;
  loading: boolean;
}

export const EngineeringFactoryOverviewMetrics: React.FC<Props> = ({ metrics, loading }) => {
  if (loading || !metrics) {
    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ background: '#1e293b', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155', animation: 'pulse 1.5s infinite' }}>
            <div style={{ height: '14px', background: '#334155', borderRadius: '4px', width: '60%', marginBottom: '8px' }} />
            <div style={{ height: '24px', background: '#475569', borderRadius: '4px', width: '40%' }} />
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    { label: 'Active Projects', value: metrics.active_projects_count, color: '#38bdf8', icon: '🚀' },
    { label: 'Decomposed Tasks', value: metrics.tasks_count, color: '#818cf8', icon: '📋' },
    { label: 'Open Pull Requests', value: metrics.open_pull_requests_count, color: '#f59e0b', icon: '🔀' },
    { label: 'CI/CD Build Runs', value: metrics.total_build_runs_count, color: '#10b981', icon: '⚙️' },
    { label: 'Production Services', value: `${metrics.healthy_services_count}/${metrics.services_count}`, color: '#ec4899', icon: '🛡️' },
    { label: 'Active Incidents', value: metrics.active_incidents_count, color: metrics.active_incidents_count === 0 ? '#10b981' : '#ef4444', icon: '🚨' },
    { label: 'Self-Healing Runbooks', value: metrics.self_healing_runbooks_count, color: '#a855f7', icon: '⚡' },
    { label: 'FinOps Total Spend', value: `$${metrics.total_finops_spend_usd.toFixed(2)}`, color: '#34d399', icon: '💰' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
      {cards.map((card, idx) => (
        <div
          key={idx}
          style={{
            background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
            padding: '1.25rem',
            borderRadius: '10px',
            border: '1px solid #334155',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.875rem', color: '#94a3b8', fontWeight: 500 }}>{card.label}</span>
            <span style={{ fontSize: '1.25rem' }}>{card.icon}</span>
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: card.color }}>{card.value}</div>
        </div>
      ))}
    </div>
  );
};
