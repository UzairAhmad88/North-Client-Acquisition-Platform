import React from 'react';
import {
  EngineeringProjectItem,
  EngineeringRequirementItem,
  ArchitectureComponentItem,
} from '../../lib/api/autonomousEngineeringOs';

interface Props {
  projects: EngineeringProjectItem[];
  requirements: EngineeringRequirementItem[];
  architectureComponents: ArchitectureComponentItem[];
}

export const RequirementsArchitectureView: React.FC<Props> = ({
  projects,
  requirements,
  architectureComponents,
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Projects Section */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🚀</span> Engineering Project Workspaces
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
          {projects.map((proj) => (
            <div key={proj.id} style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600, color: '#38bdf8' }}>{proj.name}</span>
                <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '4px', background: '#0369a1', color: '#e0f2fe' }}>
                  {proj.status}
                </span>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.75rem' }}>{proj.description}</p>
              <div style={{ fontSize: '0.8rem', color: '#cbd5e1', display: 'flex', justifyContent: 'space-between' }}>
                <span>Team: <strong>{proj.team}</strong></span>
                <span>Budget: <strong>${proj.budget_spent_usd.toFixed(0)} / ${proj.budget_allocated_usd.toFixed(0)}</strong></span>
              </div>
              <div style={{ marginTop: '0.5rem', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                {(proj.tech_stack || []).map((tech, i) => (
                  <span key={i} style={{ fontSize: '0.7rem', background: '#334155', color: '#93c5fd', padding: '1px 6px', borderRadius: '3px' }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Requirements Traceability */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>📜</span> Versioned Requirements & AI Ambiguity Scoring
        </h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
                <th style={{ padding: '0.75rem' }}>ID</th>
                <th style={{ padding: '0.75rem' }}>Title</th>
                <th style={{ padding: '0.75rem' }}>Type</th>
                <th style={{ padding: '0.75rem' }}>Priority</th>
                <th style={{ padding: '0.75rem' }}>Ambiguity Score</th>
                <th style={{ padding: '0.75rem' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {requirements.map((req) => (
                <tr key={req.id} style={{ borderBottom: '1px solid #1e293b' }}>
                  <td style={{ padding: '0.75rem', fontFamily: 'monospace', color: '#94a3b8' }}>{req.id.slice(0, 12)}</td>
                  <td style={{ padding: '0.75rem', fontWeight: 500, color: '#f8fafc' }}>{req.title}</td>
                  <td style={{ padding: '0.75rem', color: '#38bdf8' }}>{req.requirement_type}</td>
                  <td style={{ padding: '0.75rem', color: req.priority === 'CRITICAL' ? '#ef4444' : '#f59e0b' }}>{req.priority}</td>
                  <td style={{ padding: '0.75rem' }}>
                    <span style={{ padding: '2px 6px', borderRadius: '4px', background: req.ambiguity_score < 0.1 ? '#065f46' : '#78350f', color: '#f8fafc', fontSize: '0.75rem' }}>
                      {(req.ambiguity_score * 100).toFixed(0)}% ambiguity
                    </span>
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <span style={{ color: '#10b981', fontWeight: 600 }}>{req.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Architecture Components Topology */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🏛️</span> System Architecture Registry & Runtime Topology
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {architectureComponents.map((comp) => (
            <div key={comp.id} style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600, color: '#a855f7' }}>{comp.name}</span>
                <span style={{ fontSize: '0.75rem', background: '#581c87', color: '#f3e8ff', padding: '2px 6px', borderRadius: '4px' }}>
                  {comp.component_type}
                </span>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#94a3b8', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div>Owner Team: <strong style={{ color: '#cbd5e1' }}>{comp.owner_team}</strong></div>
                <div>Runtime: <strong style={{ color: '#cbd5e1' }}>{comp.runtime_environment}</strong></div>
                <div>SLO Availability: <strong style={{ color: '#10b981' }}>{comp.slo_target_availability_pct}%</strong></div>
                <div>SLO P95 Latency: <strong style={{ color: '#38bdf8' }}>{comp.slo_target_latency_p95_ms}ms</strong></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
