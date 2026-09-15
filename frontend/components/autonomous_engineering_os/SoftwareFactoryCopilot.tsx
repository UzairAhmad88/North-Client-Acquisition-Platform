'use client';

import React, { useState } from 'react';
import { autonomousEngineeringOsApi, CopilotQueryResponse } from '../../lib/api/autonomousEngineeringOs';

export const SoftwareFactoryCopilot: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<CopilotQueryResponse[]>([
    {
      query: 'What is the SLO status of our core services?',
      category: 'RELIABILITY',
      answer: 'All services report healthy SLO error budgets (>80% remaining). The last incident was successfully mitigated via automated canary rollback.',
      citations: ['ServiceCatalogEntryModel', 'AutonomousDeploymentModel'],
      answered_at: new Date().toISOString(),
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const currentQuery = query;
    setQuery('');
    setLoading(true);

    try {
      const res = await autonomousEngineeringOsApi.queryCopilot(currentQuery);
      setHistory((prev) => [res, ...prev]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
      <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span>💬</span> Software Factory Copilot (Natural-Language Engineering Intelligence)
      </h3>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask anything about architecture, PRs, test runs, SLO error budgets, or FinOps..."
          style={{
            flex: 1,
            background: '#0f172a',
            border: '1px solid #334155',
            borderRadius: '6px',
            padding: '0.75rem 1rem',
            color: '#f8fafc',
            fontSize: '0.9rem',
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            background: '#0284c7',
            color: '#fff',
            border: 'none',
            padding: '0.75rem 1.5rem',
            borderRadius: '6px',
            fontWeight: 600,
            cursor: 'pointer',
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? 'Synthesizing...' : 'Ask Copilot'}
        </button>
      </form>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {history.map((item, idx) => (
          <div key={idx} style={{ background: '#0f172a', padding: '1.25rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span style={{ fontWeight: 600, color: '#38bdf8' }}>Q: {item.query}</span>
              <span style={{ fontSize: '0.7rem', background: '#1e293b', color: '#93c5fd', padding: '2px 6px', borderRadius: '4px' }}>
                {item.category}
              </span>
            </div>
            <p style={{ fontSize: '0.9rem', color: '#cbd5e1', margin: '0.5rem 0', lineHeight: '1.4' }}>{item.answer}</p>
            {item.citations && item.citations.length > 0 && (
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.5rem', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <span>Sources:</span>
                {item.citations.map((c, i) => (
                  <span key={i} style={{ background: '#1e293b', padding: '1px 6px', borderRadius: '3px', color: '#94a3b8' }}>
                    {c}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
