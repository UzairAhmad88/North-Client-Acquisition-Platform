import React from 'react';
import { TestSuiteItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  testSuites: TestSuiteItem[];
}

export const TestingFlakinessImpactView: React.FC<Props> = ({ testSuites }) => {
  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>🧪</span> Automated Testing Platform & Flakiness Monitoring
      </h3>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
        {testSuites.map((suite) => (
          <div key={suite.id} style={{ background: '#0f172a', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span style={{ fontWeight: 600, color: '#f8fafc' }}>{suite.suite_name}</span>
              <span style={{ fontSize: '0.75rem', background: '#1e293b', color: '#93c5fd', padding: '2px 6px', borderRadius: '4px' }}>
                {suite.suite_type}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', margin: '0.75rem 0', fontSize: '0.85rem' }}>
              <span>Total Tests: <strong style={{ color: '#cbd5e1' }}>{suite.total_tests_count}</strong></span>
              <span>Passed: <strong style={{ color: '#10b981' }}>{suite.passed_tests_count}</strong></span>
              <span>Failed: <strong style={{ color: suite.failed_tests_count > 0 ? '#ef4444' : '#10b981' }}>{suite.failed_tests_count}</strong></span>
            </div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #1e293b', paddingTop: '0.5rem' }}>
              <span>Flakiness Rate: <strong style={{ color: suite.flaky_rate_pct === 0 ? '#10b981' : '#f59e0b' }}>{suite.flaky_rate_pct.toFixed(1)}%</strong></span>
              <span>Duration: <strong style={{ color: '#38bdf8' }}>{suite.duration_seconds.toFixed(1)}s</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
