"use client";

import React, { useState } from "react";

export default function PlanetaryDigitalTwinDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#060911",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(16, 185, 129, 0.3))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(16, 185, 129, 0.25)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #10B981, #06B6D4)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 94 Planetary Operating System
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>Strategic Foresight & Simulation</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #34D399)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Global Intelligence Infrastructure & Planetary Digital Twin
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "840px", fontSize: "0.95rem" }}>
              Multi-scale decision support and simulation environment representing Earth systems, critical infrastructure twins, climate feedback, macroeconomic contagion, long-horizon foresight (5–100Y), and counterfactual scenario analysis under human governance.
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
              <div style={{ fontSize: "0.75rem", color: "#6EE7B7", textTransform: "uppercase" }}>Planetary Calibration</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#10B981" }}>95.4% ACCURATE</div>
            </div>
            <div style={{
              backgroundColor: "rgba(6, 182, 212, 0.1)",
              border: "1px solid rgba(6, 182, 212, 0.3)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#67E8F9", textTransform: "uppercase" }}>Foresight Horizon</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#06B6D4" }}>100 YEARS</div>
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
          { label: "Planetary Graph Nodes", value: "14,200", sub: "Multi-Scale Provenance", color: "#10B981" },
          { label: "Infrastructure Twins", value: "1,840", sub: "Cascading Risk Graphs", color: "#3B82F6" },
          { label: "Climate Scenarios Active", value: "8 (SSP/RCP)", sub: "Ecosystem Feedbacks", color: "#F59E0B" },
          { label: "Macro Contagion Risk", value: "Low (0.12)", sub: "Financial Stress Buffer", color: "#8B5CF6" },
          { label: "Foresight Matrix Scenarios", value: "12 Scenarios", sub: "5 to 100 Year Horizons", color: "#06B6D4" },
          { label: "Model Calibration MAPE", value: "4.2%", sub: "Continuous Learning Loop", color: "#EC4899" }
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
          { id: "graph", label: "Multi-Scale Planetary Graph" },
          { id: "infrastructure", label: "Infrastructure Digital Twins" },
          { id: "climate", label: "Climate & Ecosystem Simulation" },
          { id: "macro", label: "Macroeconomic & Contagion Risk" },
          { id: "foresight", label: "Strategic Foresight (5–100Y)" },
          { id: "policy", label: "Policy & Crisis Red/Blue Teams" },
          { id: "counterfactual", label: "Counterfactual 'What-If' Engine" },
          { id: "dashboard", label: "Executive Strategic Dashboard" },
          { id: "calibration", label: "Model Calibration & Memory" }
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
              backgroundColor: activeTab === tab.id ? "#10B981" : "rgba(30, 41, 59, 0.6)",
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
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#34D399" }}>
              Planetary System Architecture & Foresight Matrix
            </h2>

            <div style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1.5rem"
            }}>
              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(16, 185, 129, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Long-Horizon Strategic Scenarios (5–100Y)
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.85rem" }}>
                  {[
                    { title: "Abundant Clean Energy & Distributed AI Mesh", type: "OPTIMISTIC", score: "0.91", rev: "REVERSIBLE" },
                    { title: "Resource Scarcity & Fragmented Regional Blocs", type: "ADVERSE", score: "0.84", rev: "PARTIALLY_REVERSIBLE" },
                    { title: "Quantum & Fusion Civilization Breakthrough", type: "TRANSFORMATIVE", score: "0.88", rev: "IRREVERSIBLE" }
                  ].map((sc, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.85rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: "#F9FAFB" }}>{sc.title}</div>
                        <div style={{ fontSize: "0.8rem", color: "#9CA3AF" }}>Robustness: {sc.score} • Reversibility: {sc.rev}</div>
                      </div>
                      <span style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.6rem",
                        borderRadius: "6px",
                        backgroundColor: "rgba(16, 185, 129, 0.2)",
                        color: "#34D399",
                        fontWeight: 600
                      }}>
                        {sc.type}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.8)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(6, 182, 212, 0.2)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Counterfactual Scenario Queries
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { query: "What if global renewable energy adoption accelerates to 80% by 2030?", outcome: "-42% CO2 Emissions", ci: "90% CI" },
                    { query: "What if port automation capacity doubles across top 10 hub ports?", outcome: "+18% Trade Throughput", ci: "95% CI" },
                    { query: "What if commercial fusion produces net energy before 2032?", outcome: "Systemic Energy Paradigm Shift", ci: "85% CI" }
                  ].map((cf, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ fontWeight: 600, fontSize: "0.875rem" }}>{cf.query}</div>
                      <div style={{ fontSize: "0.75rem", color: "#67E8F9", marginTop: "0.25rem" }}>
                        Projected Outcome: {cf.outcome} • Confidence: {cf.ci}
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
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#34D399", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} MODULE ACTIVE
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "600px", margin: "0 auto 1.5rem auto" }}>
              Planetary digital twin layers, causal graph explorers, uncertainty confidence bounds, and decision-support engines active.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(16, 185, 129, 0.1)",
              border: "1px solid rgba(16, 185, 129, 0.3)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#6EE7B7",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Active • Human Decision-Support Mode
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
