import React from 'react';
import { EngineeringIncidentItem, SelfHealingRunbookItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  incidents: EngineeringIncidentItem[];
  runbooks: SelfHealingRunbookItem[];
}

export const IncidentsSelfHealingRunbooksView: React.FC<Props> = ({ incidents, runbooks }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Incidents & Root Cause Analysis */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🚨</span> Incident Command & Telemetry-Correlated Root Cause Analysis
        </h3>
        {incidents.length === 0 ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: '#10b981', background: '#0f172a', borderRadius: '8px' }}>
            🎉 No active production incidents. All services operating normally within SLO thresholds.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {incidents.map((inc) => (
              <div key={inc.id} style={{ background: '#0f172a', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                  <div>
                    <span style={{ padding: '2px 6px', borderRadius: '4px', background: '#7f1d1d', color: '#fca5a5', fontSize: '0.75rem', fontWeight: 600, marginRight: '8px' }}>
                      {inc.severity}
                    </span>
                    <strong style={{ color: '#f8fafc', fontSize: '1.05rem' }}>{inc.title}</strong>
                    <span style={{ color: '#94a3b8', fontSize: '0.85rem', marginLeft: '8px' }}>({inc.service_name})</span>
                  </div>
                  <span
                    style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: inc.remediation_status === 'REMEDIATED' ? '#065f46' : '#854d0e',
                      color: '#f8fafc',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                    }}
                  >
                    {inc.remediation_status}
                  </span>
                </div>
                {inc.description && <p style={{ fontSize: '0.85rem', color: '#94a3b8', margin: '0.5rem 0' }}>{inc.description}</p>}
                {inc.correlated_root_cause_hypothesis && (
                  <div style={{ background: '#1e293b', padding: '0.75rem', borderRadius: '6px', fontSize: '0.825rem', color: '#cbd5e1', marginTop: '0.5rem' }}>
                    <strong style={{ color: '#f59e0b' }}>🔍 Correlated RCA Hypothesis:</strong> {inc.correlated_root_cause_hypothesis}
                  </div>
                )}
                {inc.mitigation_action_taken && (
                  <div style={{ fontSize: '0.8rem', color: '#34d399', marginTop: '0.5rem' }}>
                    ✅ <strong>Mitigation Executed:</strong> {inc.mitigation_action_taken}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Policy-Checked Self-Healing Runbooks */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>⚡</span> Policy-Checked Autonomous Self-Healing Runbooks
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {runbooks.map((rb) => (
            <div key={rb.id} style={{ background: '#0f172a', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600, color: '#f8fafc' }}>{rb.name}</span>
                <span
                  style={{
                    fontSize: '0.7rem',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    background: rb.is_autonomous_approved ? '#065f46' : '#7f1d1d',
                    color: '#f8fafc',
                  }}
                >
                  {rb.is_autonomous_approved ? 'POLICY APPROVED' : 'HUMAN GATE'}
                </span>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#94a3b8', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div>Trigger: <code style={{ color: '#f59e0b' }}>{rb.trigger_condition}</code></div>
                <div>Target Service: <strong style={{ color: '#cbd5e1' }}>{rb.target_service}</strong></div>
                <div>Action: <strong style={{ color: '#38bdf8' }}>{rb.action_type}</strong></div>
                <div>Executions: <strong style={{ color: '#10b981' }}>{rb.executions_count} ({rb.success_rate_pct}% success)</strong></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
