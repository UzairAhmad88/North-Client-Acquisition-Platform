"use client";

import React, { useState } from "react";

export default function GlobalHumanAiCollaborationDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0B0F19",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(30, 58, 138, 0.4))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(59, 130, 246, 0.2)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #3B82F6, #8B5CF6)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 92 Operating System
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>Level 5 Governance Active</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #60A5FA)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Global Human-AI Collaboration Network & Collective Intelligence
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "800px", fontSize: "0.95rem" }}>
              Civilization-scale problem solving infrastructure uniting humans, verified domain experts, teams, research networks, Red/Blue team simulations, and AI agents under strict human agency preservation and evidence attribution.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div style={{
              backgroundColor: "rgba(16, 185, 129, 0.1)",
              border: "1px solid rgba(16, 185, 129, 0.3)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#6EE7B7", textTransform: "uppercase" }}>Global Mesh Status</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#10B981" }}>HEALTHY</div>
            </div>
            <div style={{
              backgroundColor: "rgba(99, 102, 241, 0.1)",
              border: "1px solid rgba(99, 102, 241, 0.3)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#A5B4FC", textTransform: "uppercase" }}>Human Agency Gate</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#6366F1" }}>LEVEL 5 SOVEREIGN</div>
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
          { label: "Active Collaborators", value: "14,890", sub: "+12.4% this week", color: "#3B82F6" },
          { label: "Verified Expert Networks", value: "842", sub: "Institutional Proofs", color: "#8B5CF6" },
          { label: "Project Rooms Active", value: "1,204", sub: "Connected Knowledge Graphs", color: "#10B981" },
          { label: "Decision Quality Index", value: "96.4%", sub: "Evidence-backed", color: "#F59E0B" },
          { label: "Argument Maps & Dissent", value: "4,510", sub: "Minority opinions preserved", color: "#EC4899" },
          { label: "Red/Blue Simulations", value: "318", sub: "Zero-Trust Federated", color: "#06B6D4" }
        ].map((stat, idx) => (
          <div key={idx} style={{
            backgroundColor: "rgba(17, 24, 39, 0.7)",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            borderRadius: "14px",
            padding: "1.25rem",
            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.3)"
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
          { id: "overview", label: "Command Center" },
          { id: "fabric", label: "Collaboration Fabric & Identity" },
          { id: "matching", label: "Expert Matching & Team Builder" },
          { id: "rooms", label: "Project Rooms & Knowledge Graph" },
          { id: "attribution", label: "Contribution & Argument Mapping" },
          { id: "federated", label: "Federated Science & Red/Blue Twins" },
          { id: "orchestration", label: "Agent Orchestration & Handoff" },
          { id: "datarooms", label: "Secure Data Rooms & Project RAG" },
          { id: "deliberation", label: "Deliberation & MCDA Voting" },
          { id: "postmortems", label: "Executive Briefings & Postmortems" },
          { id: "workbench", label: "Civilization-Scale Workbench" }
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
              backgroundColor: activeTab === tab.id ? "#3B82F6" : "rgba(31, 41, 55, 0.6)",
              color: activeTab === tab.id ? "#FFFFFF" : "#9CA3AF"
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main Content Panels */}
      <main style={{
        backgroundColor: "rgba(17, 24, 39, 0.6)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "2rem"
      }}>
        {activeTab === "overview" && (
          <div>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#60A5FA" }}>
              Global Human-AI Collective Intelligence Topology
            </h2>
            <div style={{
              display: "grid",
              gridTemplateColumns: "2fr 1fr",
              gap: "1.5rem"
            }}>
              <div style={{
                backgroundColor: "rgba(11, 15, 25, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(59, 130, 246, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Active Civilization Problem Workbenches
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                  {[
                    { name: "Planetary Climate Resilience Workbench", domain: "Environmental Science", human_count: 128, agent_count: 45, status: "GOVERNED_ADVISORY" },
                    { name: "Global Clean Energy Grid Integration", domain: "Energy Infrastructure", human_count: 94, agent_count: 32, status: "SIMULATION_ACTIVE" },
                    { name: "Global Autonomous Supply Chain Stress Test", domain: "Logistics & Trade", human_count: 67, agent_count: 28, status: "RED_TEAM_CRITIQUE" }
                  ].map((wb, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(31, 41, 55, 0.5)",
                      padding: "1rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      borderLeft: "4px solid #3B82F6"
                    }}>
                      <div>
                        <div style={{ fontWeight: 700, color: "#F9FAFB" }}>{wb.name}</div>
                        <div style={{ fontSize: "0.8rem", color: "#9CA3AF" }}>Domain: {wb.domain} • Humans: {wb.human_count} • Agents: {wb.agent_count}</div>
                      </div>
                      <span style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.6rem",
                        borderRadius: "6px",
                        backgroundColor: "rgba(16, 185, 129, 0.2)",
                        color: "#34D399",
                        fontWeight: 600
                      }}>
                        {wb.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(11, 15, 25, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(139, 92, 246, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Recent Structured Decisions
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { title: "Select Zero-Emission Grid Topology", quality: "95%", human_signed: True },
                    { title: "Adopt Quantum-Resistant Encryption Standard", quality: "98%", human_signed: True },
                    { title: "Deploy Federated AI Clinical Study", quality: "94%", human_signed: True }
                  ].map((dec, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(31, 41, 55, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ fontWeight: 600, fontSize: "0.875rem" }}>{dec.title}</div>
                      <div style={{ fontSize: "0.75rem", color: "#A7F3D0", marginTop: "0.25rem" }}>
                        Quality Score: {dec.quality} • Human Approved ✓
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
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#60A5FA", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} INTERFACE ACTIVE
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "600px", margin: "0 auto 1.5rem auto" }}>
              Governed human-AI collective intelligence capabilities, real-time argument maps, multi-agent handoffs, and evidence attribution active for this module.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(59, 130, 246, 0.1)",
              border: "1px solid rgba(59, 130, 246, 0.3)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#93C5FD",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Operational • Level 5 Human Sovereignty Enforced
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
