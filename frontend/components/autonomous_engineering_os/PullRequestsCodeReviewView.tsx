import React from 'react';
import { PullRequestItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  pullRequests: PullRequestItem[];
}

export const PullRequestsCodeReviewView: React.FC<Props> = ({ pullRequests }) => {
  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>🔀</span> Pull Request Intelligence & 6-Dimension AI Risk Scorecards
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {pullRequests.map((pr) => {
          const breakdown = pr.risk_breakdown_json || {};
          return (
            <div
              key={pr.id}
              style={{
                background: '#0f172a',
                padding: '1.25rem',
                borderRadius: '8px',
                border: '1px solid #334155',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                <div>
                  <h4 style={{ margin: '0 0 4px 0', fontSize: '1.05rem', color: '#f8fafc' }}>{pr.title}</h4>
                  <div style={{ fontSize: '0.8rem', color: '#94a3b8', display: 'flex', gap: '1rem' }}>
                    <span>Author: <strong style={{ color: '#cbd5e1' }}>{pr.author}</strong></span>
                    <span>Branch: <code style={{ color: '#38bdf8' }}>{pr.source_branch} &rarr; {pr.target_branch}</code></span>
                    <span>CI: <strong style={{ color: pr.ci_pipeline_status === 'PASSED' ? '#10b981' : '#f59e0b' }}>{pr.ci_pipeline_status}</strong></span>
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Composite Risk</div>
                  <div
                    style={{
                      fontSize: '1.25rem',
                      fontWeight: 700,
                      color: pr.risk_score_composite < 0.2 ? '#10b981' : '#f59e0b',
                    }}
                  >
                    {(pr.risk_score_composite * 100).toFixed(0)}%
                  </div>
                </div>
              </div>

              {/* 6-Dimension Risk Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '8px', background: '#1e293b', padding: '0.75rem', borderRadius: '6px' }}>
                {Object.entries(breakdown).map(([riskKey, riskVal]) => (
                  <div key={riskKey} style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'capitalize' }}>
                      {riskKey.replace('_', ' ')}
                    </div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600, color: (riskVal as number) < 0.15 ? '#34d399' : '#f87171' }}>
                      {((riskVal as number) * 100).toFixed(0)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
