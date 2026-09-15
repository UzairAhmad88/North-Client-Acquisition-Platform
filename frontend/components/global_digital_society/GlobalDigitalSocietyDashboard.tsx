"use client";

import React, { useState } from "react";

export default function GlobalDigitalSocietyDashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [emergencyPauseEngaged, setEmergencyPauseEngaged] = useState(false);
  const [killSwitchEngaged, setKillSwitchEngaged] = useState(false);

  const handleToggleEmergencyPause = () => {
    setEmergencyPauseEngaged(!emergencyPauseEngaged);
  };

  const handleToggleKillSwitch = () => {
    if (confirm("WARNING: Activating Global Kill-Switch will instantly pause all active autonomous AI workflows. Proceed?")) {
      setKillSwitchEngaged(true);
      setEmergencyPauseEngaged(true);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#090D16",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Emergency Alert Banner if Kill Switch Engaged */}
      {killSwitchEngaged && (
        <div style={{
          backgroundColor: "rgba(239, 68, 68, 0.2)",
          border: "2px solid #EF4444",
          borderRadius: "12px",
          padding: "1rem 1.5rem",
          marginBottom: "1.5rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}>
          <div style={{ color: "#FCA5A5", fontWeight: 700, fontSize: "1.05rem" }}>
            🚨 GLOBAL KILL-SWITCH ACTIVE — ALL AUTONOMOUS AGENT WORKFLOWS REVOKED AND PAUSED
          </div>
          <button
            onClick={() => { setKillSwitchEngaged(false); setEmergencyPauseEngaged(false); }}
            style={{
              backgroundColor: "#EF4444",
              color: "#FFFFFF",
              border: "none",
              padding: "0.5rem 1rem",
              borderRadius: "8px",
              fontWeight: 700,
              cursor: "pointer"
            }}
          >
            Reset Kill-Switch
          </button>
        </div>
      )}

      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(88, 28, 135, 0.4))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(168, 85, 247, 0.2)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #8B5CF6, #EC4899)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 93 Digital Society OS
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>AI-Native Institutions & DPI</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #C084FC)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Global Digital Society & Networked Economic Coordination
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "820px", fontSize: "0.95rem" }}>
              Governed AI-native institutional infrastructure connecting digital identity, verifiable credentials, AI personas, dynamic org graphs, autonomous workflow contracts, DPI marketplaces, crisis command, and global kill-switch safety controls.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
            <button
              onClick={handleToggleEmergencyPause}
              style={{
                backgroundColor: emergencyPauseEngaged ? "rgba(245, 158, 11, 0.2)" : "rgba(31, 41, 55, 0.8)",
                border: emergencyPauseEngaged ? "1px solid #F59E0B" : "1px solid rgba(255, 255, 255, 0.1)",
                color: emergencyPauseEngaged ? "#FBBF24" : "#D1D5DB",
                borderRadius: "10px",
                padding: "0.75rem 1.25rem",
                fontWeight: 600,
                cursor: "pointer",
                fontSize: "0.875rem"
              }}
            >
              {emergencyPauseEngaged ? "⏸ Pause Active" : "⏸ Emergency Pause"}
            </button>

            <button
              onClick={handleToggleKillSwitch}
              style={{
                backgroundColor: "rgba(239, 68, 68, 0.15)",
                border: "1px solid rgba(239, 68, 68, 0.4)",
                color: "#FCA5A5",
                borderRadius: "10px",
                padding: "0.75rem 1.25rem",
                fontWeight: 700,
                cursor: "pointer",
                fontSize: "0.875rem"
              }}
            >
              🛑 Global Kill-Switch
            </button>
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
          { label: "Active Digital Identities", value: "248,910", sub: "Strongly Verified / SSI", color: "#A855F7" },
          { label: "AI Workers Onboarded", value: "3,420", sub: "Least-Privilege Roles", color: "#3B82F6" },
          { label: "Autonomous Workflows", value: emergencyPauseEngaged ? "0 (PAUSED)" : "814", sub: "Budget & Contract Capped", color: emergencyPauseEngaged ? "#F59E0B" : "#10B981" },
          { label: "Marketplace Volume", value: "$4.25M", sub: "Agent-to-Service Economy", color: "#EC4899" },
          { label: "Digital Trust Rating", value: "99.1%", sub: "Data Residency & SSI", color: "#06B6D4" },
          { label: "Systemic Resilience", value: "98.1%", sub: "Zero SPoF Dependencies", color: "#6366F1" }
        ].map((stat, idx) => (
          <div key={idx} style={{
            backgroundColor: "rgba(15, 23, 42, 0.75)",
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
          { id: "identity", label: "Identity, SSI & Personas" },
          { id: "orgs", label: "AI-Native Org Graph & RACI" },
          { id: "workflows", label: "Autonomous Workflow Contracts" },
          { id: "governance", label: "Digital Governance & Policy" },
          { id: "executive", label: "Executive Operating Center" },
          { id: "marketplace", label: "Agent Economy & Marketplace" },
          { id: "crisis", label: "Crisis Command & Supply Twin" },
          { id: "dpi", label: "DPI & M2M Procurement" },
          { id: "privacy", label: "Digital Trust & Rights Center" },
          { id: "systemic", label: "Systemic Risk & Emergency Mode" }
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
              backgroundColor: activeTab === tab.id ? "#8B5CF6" : "rgba(30, 41, 59, 0.6)",
              color: activeTab === tab.id ? "#FFFFFF" : "#9CA3AF"
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main Content Panels */}
      <main style={{
        backgroundColor: "rgba(15, 23, 42, 0.6)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "2rem"
      }}>
        {activeTab === "overview" && (
          <div>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#C084FC" }}>
              AI-Native Institutions & Digital Society Control Surface
            </h2>

            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem"
            }}>
              <div style={{
                backgroundColor: "rgba(9, 13, 22, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(139, 92, 246, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Active Autonomous Workflow Contracts
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.85rem" }}>
                  {[
                    { name: "Autonomous Cloud Resource Rebalancing", cap: "$15,000 Cap", state: "SANDBOX_VERIFIED" },
                    { name: "Automated Supply Chain Port Routing", cap: "$50,000 Cap", state: "HUMAN_APPROVED" },
                    { name: "Global Treasury Yield Optimization", cap: "$10,000 Cap", state: "DUAL_APPROVAL_ACTIVE" }
                  ].map((wf, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.85rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: "#F9FAFB" }}>{wf.name}</div>
                        <div style={{ fontSize: "0.8rem", color: "#9CA3AF" }}>Spending Limit: {wf.cap}</div>
                      </div>
                      <span style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.6rem",
                        borderRadius: "6px",
                        backgroundColor: "rgba(139, 92, 246, 0.2)",
                        color: "#DDD6FE",
                        fontWeight: 600
                      }}>
                        {wf.state}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(9, 13, 22, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(236, 72, 153, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Agent-to-Service Economy Metrics
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { service: "GPU Cluster Time 100 Hours", cost: "$1,200.00", status: "RELEASED_FROM_ESCROW" },
                    { service: "Federated Medical Data Audit", cost: "$450.00", status: "RELEASED_FROM_ESCROW" },
                    { service: "Quantum Encryption Verification", cost: "$890.00", status: "RELEASED_FROM_ESCROW" }
                  ].map((tx, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ fontWeight: 600, fontSize: "0.875rem" }}>{tx.service}</div>
                      <div style={{ fontSize: "0.75rem", color: "#F472B6", marginTop: "0.25rem" }}>
                        Transaction Value: {tx.cost} • Fraud Score: 0.01 • Status: {tx.status}
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
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#C084FC", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} MODULE OPERATIONAL
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "600px", margin: "0 auto 1.5rem auto" }}>
              Interoperable digital public infrastructure, verifiable credentials, spending policies, dual-approval rules, and global kill-switch hooks active.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(139, 92, 246, 0.1)",
              border: "1px solid rgba(139, 92, 246, 0.3)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#DDD6FE",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Active • Human Authority Preserved
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
