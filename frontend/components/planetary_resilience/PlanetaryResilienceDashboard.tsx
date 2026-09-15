"use client";

import React, { useState } from "react";

export default function PlanetaryResilienceDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#050811",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(225, 29, 72, 0.25))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(225, 29, 72, 0.3)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.6)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #E11D48, #F59E0B)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 95 Civilization Operating System
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>Global Crisis & Existential Risk</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #FB7185)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Planetary Resilience & Global Crisis Coordination
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "880px", fontSize: "0.95rem" }}>
              Unified planetary resilience layer establishing systemic risk monitoring, incident command centers, humanitarian resource matching, healthcare continuity, AI graceful degradation, critical knowledge archives, and existential-risk research under human authority.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div style={{
              backgroundColor: "rgba(225, 29, 72, 0.12)",
              border: "1px solid rgba(225, 29, 72, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#FDA4AF", textTransform: "uppercase" }}>Systemic Preparedness</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#F43F5E" }}>98.6% READY</div>
            </div>
            <div style={{
              backgroundColor: "rgba(245, 158, 11, 0.12)",
              border: "1px solid rgba(245, 158, 11, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#FDE68A", textTransform: "uppercase" }}>Human Authority</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#F59E0B" }}>LEVEL 5 OVERSIGHT</div>
            </div>
          </div>
        </div>
      </header>

      {/* KPI Stat Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: "1.25rem",
        marginBottom: "2rem"
      }}>
        {[
          { label: "Critical Systems Registered", value: "842 Nodes", sub: "Energy, Water, Healthcare, Comms", color: "#F43F5E" },
          { label: "Active Incident Command", value: "Level 1 Stable", sub: "0 Active Critical Emergencies", color: "#10B981" },
          { label: "Humanitarian Inventory", value: "94.2% Match", sub: "Food, Water & Medical Reserves", color: "#3B82F6" },
          { label: "Grid Energy Reserve", value: "72 Hours", sub: "Island Microgrids Standby", color: "#F59E0B" },
          { label: "AI Continuity Degradation", value: "Full AI Mode", sub: "Defined Manual Fallbacks", color: "#8B5CF6" },
          { label: "Knowledge Archive Integrity", value: "100% Hash Valid", sub: "Multi-Region Redundancy", color: "#06B6D4" }
        ].map((stat, idx) => (
          <div key={idx} style={{
            backgroundColor: "rgba(15, 23, 42, 0.8)",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            borderRadius: "14px",
            padding: "1.25rem",
            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.4)"
          }}>
            <div style={{ fontSize: "0.85rem", color: "#9CA3AF", marginBottom: "0.5rem" }}>{stat.label}</div>
            <div style={{ fontSize: "1.75rem", fontWeight: 800, color: stat.color }}>{stat.value}</div>
            <div style={{ fontSize: "0.75rem", color: "#6B7280", marginTop: "0.25rem" }}>{stat.sub}</div>
          </div>
        ))}
      </div>

      {/* Tab Navigation */}
      <nav style={{
        display: "flex",
        gap: "0.5rem",
        overflowX: "auto",
        paddingBottom: "0.75rem",
        marginBottom: "2rem",
        borderBottom: "1px solid rgba(255, 255, 255, 0.1)"
      }}>
        {[
          { id: "overview", label: "Resilience Fabric Overview" },
          { id: "crisis_command", label: "Incident Command Center" },
          { id: "humanitarian", label: "Humanitarian Logistics" },
          { id: "infrastructure", label: "Grid & Healthcare Continuity" },
          { id: "ai_degradation", label: "AI Graceful Degradation" },
          { id: "knowledge_archive", label: "Critical Knowledge Archives" },
          { id: "governance", label: "Governance & Emergency Power" },
          { id: "compound_risk", label: "Compound Risk & Buffers" },
          { id: "existential_research", label: "Existential Risk Workspace" },
          { id: "simulation_lab", label: "Crisis Simulation Lab" }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: "0.6rem 1.1rem",
              borderRadius: "10px",
              border: "none",
              cursor: "pointer",
              fontSize: "0.875rem",
              fontWeight: 600,
              whiteSpace: "nowrap",
              transition: "all 0.2s ease",
              backgroundColor: activeTab === tab.id ? "#E11D48" : "rgba(30, 41, 59, 0.6)",
              color: activeTab === tab.id ? "#FFFFFF" : "#9CA3AF"
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main Content Panels */}
      <main style={{
        backgroundColor: "rgba(15, 23, 42, 0.65)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "2rem"
      }}>
        {activeTab === "overview" && (
          <div>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#FB7185" }}>
              Planetary System Resilience Scorecard & Emergency Matrix
            </h2>

            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem"
            }}>
              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.85)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(225, 29, 72, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Critical Infrastructure Node Registries
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.85rem" }}>
                  {[
                    { name: "Continental Energy Grid Alpha", cat: "Energy", status: "Stable", score: "88/100", mat: "Adaptive" },
                    { name: "Metropolitan Water Purification Hub", cat: "Water", status: "Stable", score: "82/100", mat: "Resilient" },
                    { name: "Regional Trauma Healthcare Net", cat: "Healthcare", status: "Stressed", score: "74/100", mat: "Managed" }
                  ].map((sys, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.85rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: "#F9FAFB" }}>{sys.name}</div>
                        <div style={{ fontSize: "0.8rem", color: "#9CA3AF" }}>Category: {sys.cat} • Score: {sys.score}</div>
                      </div>
                      <span style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.6rem",
                        borderRadius: "6px",
                        backgroundColor: sys.status === "Stable" ? "rgba(16, 185, 129, 0.2)" : "rgba(245, 158, 11, 0.2)",
                        color: sys.status === "Stable" ? "#34D399" : "#FBBF24",
                        fontWeight: 600
                      }}>
                        {sys.status} ({sys.mat})
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.85)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(245, 158, 11, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Existential Risk & Containment Controls
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { scenario: "Goal Misalignment in Autonomous Dispatch", prob: "Plausible", ctrl: "Hardware Override & Key Revocation" },
                    { scenario: "Multi-Region Cyber Grid Disruption", prob: "Plausible", ctrl: "Air-Gapped Offline Mode" },
                    { scenario: "Compound Climate Thermal & Crop Failure", prob: "Speculative", ctrl: "Humanitarian Reserve Dispatch" }
                  ].map((xr, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ fontWeight: 600, fontSize: "0.875rem" }}>{xr.scenario}</div>
                      <div style={{ fontSize: "0.75rem", color: "#FDE68A", marginTop: "0.25rem" }}>
                        Assessment: {xr.prob} • Safeguard: {xr.ctrl}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab !== "overview" && (
          <div style={{ textAlign: "center", padding: "3rem" }}>
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#FB7185", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} MODULE ACTIVE
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "620px", margin: "0 auto 1.5rem auto" }}>
              Planetary crisis monitoring, decision reversibility logs, emergency authority expiration, and existential-risk research active under human control.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(225, 29, 72, 0.12)",
              border: "1px solid rgba(225, 29, 72, 0.35)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#FDA4AF",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Active • Level 5 Human Authority Enforced
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
