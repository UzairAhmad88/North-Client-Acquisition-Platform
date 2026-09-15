import React from 'react';
import { AutonomousDeploymentItem, ServiceCatalogItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  deployments: AutonomousDeploymentItem[];
  services: ServiceCatalogItem[];
}

export const DeploymentsSreSloView: React.FC<Props> = ({ deployments, services }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Service Catalog & SLO Error Budgets */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🛡️</span> Production Service Catalog & SRE SLO Error Budgets
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
          {services.map((srv) => (
            <div key={srv.id} style={{ background: '#0f172a', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <span style={{ fontWeight: 600, color: '#f8fafc', fontSize: '1rem' }}>{srv.name}</span>
                <span
                  style={{
                    fontSize: '0.75rem',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    background: srv.status === 'HEALTHY' ? '#065f46' : '#991b1b',
                    color: '#f8fafc',
                    fontWeight: 600,
                  }}
                >
                  {srv.status}
                </span>
              </div>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Availability SLO Target:</span>
                  <strong style={{ color: '#cbd5e1' }}>{srv.slo_target_availability_pct}%</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Current Availability:</span>
                  <strong style={{ color: '#10b981' }}>{srv.current_availability_pct}%</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>P95 Latency:</span>
                  <strong style={{ color: '#38bdf8' }}>{srv.p95_latency_ms}ms</strong>
                </div>
                <div style={{ marginTop: '0.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
                    <span>Error Budget Remaining:</span>
                    <strong style={{ color: srv.error_budget_remaining_pct > 30 ? '#34d399' : '#f87171' }}>
                      {srv.error_budget_remaining_pct.toFixed(1)}%
                    </strong>
                  </div>
                  <div style={{ height: '6px', background: '#334155', borderRadius: '3px', overflow: 'hidden' }}>
                    <div
                      style={{
                        height: '100%',
                        width: `${Math.min(100, Math.max(0, srv.error_budget_remaining_pct))}%`,
                        background: srv.error_budget_remaining_pct > 30 ? '#10b981' : '#ef4444',
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Autonomous Deployments */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🚀</span> Canary & Blue-Green Autonomous Deployments
        </h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
                <th style={{ padding: '0.75rem' }}>Service</th>
                <th style={{ padding: '0.75rem' }}>Environment</th>
                <th style={{ padding: '0.75rem' }}>Strategy</th>
                <th style={{ padding: '0.75rem' }}>Version</th>
                <th style={{ padding: '0.75rem' }}>Traffic Weight</th>
                <th style={{ padding: '0.75rem' }}>Verification</th>
              </tr>
            </thead>
            <tbody>
              {deployments.map((dep) => (
                <tr key={dep.id} style={{ borderBottom: '1px solid #1e293b' }}>
                  <td style={{ padding: '0.75rem', fontWeight: 600, color: '#f8fafc' }}>{dep.service_name}</td>
                  <td style={{ padding: '0.75rem', color: '#38bdf8' }}>{dep.environment}</td>
                  <td style={{ padding: '0.75rem', color: '#a855f7' }}>{dep.strategy}</td>
                  <td style={{ padding: '0.75rem', fontFamily: 'monospace', color: '#cbd5e1' }}>{dep.version}</td>
                  <td style={{ padding: '0.75rem', color: '#10b981' }}>{dep.traffic_weight_pct}%</td>
                  <td style={{ padding: '0.75rem' }}>
                    <span
                      style={{
                        padding: '2px 8px',
                        borderRadius: '4px',
                        background: dep.verification_status === 'VERIFIED' ? '#065f46' : '#78350f',
                        color: '#f8fafc',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                      }}
                    >
                      {dep.verification_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
