import React from 'react';
import { SbomPackageItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  sbomPackages: SbomPackageItem[];
}

export const SecuritySbomVulnerabilitiesView: React.FC<Props> = ({ sbomPackages }) => {
  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>🔒</span> Software Bill of Materials (SBOM) & Supply Chain Security
      </h3>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
              <th style={{ padding: '0.75rem' }}>Package Name</th>
              <th style={{ padding: '0.75rem' }}>Version</th>
              <th style={{ padding: '0.75rem' }}>License</th>
              <th style={{ padding: '0.75rem' }}>Compliance</th>
              <th style={{ padding: '0.75rem' }}>Vulnerabilities (CVE)</th>
            </tr>
          </thead>
          <tbody>
            {sbomPackages.map((pkg) => (
              <tr key={pkg.id} style={{ borderBottom: '1px solid #1e293b' }}>
                <td style={{ padding: '0.75rem', fontWeight: 600, color: '#f8fafc' }}>{pkg.package_name}</td>
                <td style={{ padding: '0.75rem', fontFamily: 'monospace', color: '#38bdf8' }}>{pkg.version}</td>
                <td style={{ padding: '0.75rem', color: '#cbd5e1' }}>{pkg.license_type}</td>
                <td style={{ padding: '0.75rem' }}>
                  <span
                    style={{
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: pkg.is_license_compliant ? '#065f46' : '#991b1b',
                      color: '#f8fafc',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                    }}
                  >
                    {pkg.is_license_compliant ? 'COMPLIANT' : 'VIOLATION'}
                  </span>
                </td>
                <td style={{ padding: '0.75rem' }}>
                  <span style={{ color: pkg.vulnerabilities_count === 0 ? '#10b981' : '#ef4444', fontWeight: 600 }}>
                    {pkg.vulnerabilities_count} CVEs detected
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
