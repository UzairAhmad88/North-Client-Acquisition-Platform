import React from 'react';
import { EngineeringTaskItem } from '../../lib/api/autonomousEngineeringOs';

interface Props {
  tasks: EngineeringTaskItem[];
}

export const CodeIntelligenceTasksView: React.FC<Props> = ({ tasks }) => {
  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🤖</span> AI Task Planner & Sandboxed Coding Agent Console
          </h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', margin: '4px 0 0 0' }}>
            Traceable task decomposition, agent assignment, and token usage accounting.
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem' }}>
        {tasks.map((task) => (
          <div
            key={task.id}
            style={{
              background: '#0f172a',
              padding: '1.25rem',
              borderRadius: '8px',
              border: '1px solid #334155',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600, color: '#f8fafc', fontSize: '0.95rem' }}>{task.title}</span>
                <span
                  style={{
                    fontSize: '0.75rem',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    background: task.status === 'COMPLETED' ? '#065f46' : '#1e3a8a',
                    color: task.status === 'COMPLETED' ? '#6ee7b7' : '#93c5fd',
                    fontWeight: 500,
                  }}
                >
                  {task.status}
                </span>
              </div>
              <p style={{ fontSize: '0.825rem', color: '#94a3b8', marginBottom: '0.75rem' }}>{task.description}</p>
            </div>

            <div style={{ borderTop: '1px solid #1e293b', paddingTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '4px', fontSize: '0.8rem', color: '#cbd5e1' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Assigned Agent: <strong style={{ color: '#38bdf8' }}>{task.assigned_agent}</strong></span>
                <span>Type: <strong style={{ color: '#f59e0b' }}>{task.task_type}</strong></span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Tokens Consumed: <strong style={{ color: '#10b981' }}>{task.tokens_consumed}</strong></span>
                <span>Priority: <strong style={{ color: task.priority === 'HIGH' ? '#ef4444' : '#94a3b8' }}>{task.priority}</strong></span>
              </div>
              {task.branch_name && (
                <div style={{ fontFamily: 'monospace', color: '#64748b', fontSize: '0.75rem', marginTop: '2px' }}>
                  git checkout {task.branch_name}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
