import React from 'react';
import { CiBuildRunItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  buildRuns: CiBuildRunItem[];
}

export const CicdBuildsArtifactsView: React.FC<Props> = ({ buildRuns }) => {
  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>⚙️</span> CI/CD Multi-Stage Pipeline Runs & Artifact Provenance
      </h3>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
              <th style={{ padding: '0.75rem' }}>Build #</th>
              <th style={{ padding: '0.75rem' }}>Commit SHA</th>
              <th style={{ padding: '0.75rem' }}>Branch</th>
              <th style={{ padding: '0.75rem' }}>Duration</th>
              <th style={{ padding: '0.75rem' }}>Artifacts Generated</th>
              <th style={{ padding: '0.75rem' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {buildRuns.map((build) => (
              <tr key={build.id} style={{ borderBottom: '1px solid #1e293b' }}>
                <td style={{ padding: '0.75rem', fontWeight: 600, color: '#38bdf8' }}>#{build.build_number}</td>
                <td style={{ padding: '0.75rem', fontFamily: 'monospace', color: '#cbd5e1' }}>{build.commit_sha.slice(0, 8)}</td>
                <td style={{ padding: '0.75rem', color: '#94a3b8' }}>{build.branch}</td>
                <td style={{ padding: '0.75rem', color: '#94a3b8' }}>{build.duration_seconds.toFixed(1)}s</td>
                <td style={{ padding: '0.75rem', fontSize: '0.75rem', color: '#a855f7' }}>
                  {(build.artifacts_generated || []).join(', ')}
                </td>
                <td style={{ padding: '0.75rem' }}>
                  <span
                    style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: build.status === 'SUCCESS' ? '#065f46' : '#991b1b',
                      color: '#f8fafc',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                    }}
                  >
                    {build.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
