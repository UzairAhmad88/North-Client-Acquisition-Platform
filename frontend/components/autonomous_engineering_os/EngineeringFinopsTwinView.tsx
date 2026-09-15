'use client';

import React, { useState } from 'react';

export const EngineeringFinopsTwinView: React.FC = () => {
  const [trafficMultiplier, setTrafficMultiplier] = useState(2);
  const [simulationResult, setSimulationResult] = useState<{
    latency: number;
    errorRate: number;
    costIncrease: number;
    recommendation: string;
  } | null>({
    latency: 48.5,
    errorRate: 0.015,
    costIncrease: 30.0,
    recommendation: 'Pre-scale horizontal pod autoscalers from 3 to 6 replicas ahead of traffic peak.',
  });

  const handleSimulate = () => {
    const lat = Number((32.0 * Math.pow(trafficMultiplier, 0.6)).toFixed(1));
    const err = Number((0.01 * Math.pow(trafficMultiplier, 0.8)).toFixed(3));
    const cost = Number((15.0 * trafficMultiplier).toFixed(2));
    setSimulationResult({
      latency: lat,
      errorRate: err,
      costIncrease: cost,
      recommendation: `Pre-scale horizontal pod autoscalers from 3 to ${Math.round(3 * trafficMultiplier)} replicas ahead of traffic peak.`,
    });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* FinOps Allocation */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>💰</span> Granular Engineering FinOps Spend Breakdown
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>CI Build Minutes</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#38bdf8' }}>$420.50</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>8,410 runner minutes</div>
          </div>
          <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>AI Coding Agent Tokens</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#818cf8' }}>$185.20</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>9.26M tokens consumed</div>
          </div>
          <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Kubernetes Compute (K8s)</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#34d399' }}>$1,240.00</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Production cluster nodes</div>
          </div>
          <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155' }}>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Testing & Preview Infra</div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f59e0b' }}>$95.00</div>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Ephemeral PR environments</div>
          </div>
        </div>
      </div>

      {/* Engineering Digital Twin Simulator */}
      <div style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '10px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🌐</span> Engineering Digital Twin: "What-If" Scenario Simulation Engine
        </h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
          <label style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>
            Traffic Multiplier: <strong>{trafficMultiplier}x</strong>
          </label>
          <input
            type="range"
            min="1"
            max="10"
            step="1"
            value={trafficMultiplier}
            onChange={(e) => setTrafficMultiplier(Number(e.target.value))}
            style={{ flex: 1, maxWidth: '250px' }}
          />
          <button
            onClick={handleSimulate}
            style={{
              background: '#0284c7',
              color: '#fff',
              border: 'none',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Run Simulation
          </button>
        </div>

        {simulationResult && (
          <div style={{ background: '#0f172a', padding: '1rem', borderRadius: '8px', border: '1px solid #334155', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Predicted P95 Latency</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#38bdf8' }}>{simulationResult.latency} ms</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Predicted Error Rate</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f59e0b' }}>{simulationResult.errorRate}%</div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Cost Delta (USD/day)</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#34d399' }}>+${simulationResult.costIncrease}</div>
            </div>
            <div style={{ gridColumn: '1 / -1', background: '#1e293b', padding: '0.75rem', borderRadius: '6px', fontSize: '0.85rem', color: '#cbd5e1' }}>
              💡 <strong style={{ color: '#f8fafc' }}>Autonomous Capacity Recommendation:</strong> {simulationResult.recommendation}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
