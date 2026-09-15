"use client";

import React, { useState } from "react";

export default function ScientificDiscoveryDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#030712",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(16, 185, 129, 0.3))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(16, 185, 129, 0.35)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.6)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
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
                Phase 97 Discovery Operating Infrastructure
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>Autonomous AI Scientists & Reproducible Labs</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #6EE7B7)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Civilization-Scale Scientific Discovery Engine
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "920px", fontSize: "0.95rem" }}>
              Accelerating research pipeline from Question → Literature → Hypothesis → Experiment → Simulation → Validation → Discovery → Publication → Replication under mandatory human authorization and strict safety bounds.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div style={{
              backgroundColor: "rgba(16, 185, 129, 0.12)",
              border: "1px solid rgba(16, 185, 129, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#A7F3D0", textTransform: "uppercase" }}>Discovery Velocity</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#10B981" }}>4.2x ACCELERATED</div>
            </div>
            <div style={{
              backgroundColor: "rgba(6, 182, 212, 0.12)",
              border: "1px solid rgba(6, 182, 212, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#A5F3FC", textTransform: "uppercase" }}>Lab Safety Gates</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#06B6D4" }}>HUMAN APPROVAL REQUIRED</div>
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
          { label: "Literature Graph Ingested", value: "2.4M Papers", sub: "Claims & Gaps Indexed", color: "#10B981" },
          { label: "AI Hypotheses Ranked", value: "1,840 Generated", sub: "Explicitly Labeled AI", color: "#06B6D4" },
          { label: "Information Gain Score", value: "8.95/10", sub: "Active Learning Loop", color: "#3B82F6" },
          { label: "Virtual Lab Reproducibility", value: "100% Validated", sub: "Environment & Seed Locked", color: "#8B5CF6" },
          { label: "AI Scientist Teams", value: "32 Orchestrations", sub: "Role-Specialized & Audited", color: "#F59E0B" },
          { label: "Discovery Registry", value: "142 Replicated", sub: "Credit Attribution Logged", color: "#EC4899" }
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
          { id: "overview", label: "Discovery Overview" },
          { id: "literature", label: "Literature & Gap Detection" },
          { id: "hypotheses", label: "AI Hypotheses (Labeled)" },
          { id: "experiment_design", label: "Experiment & Active Learning" },
          { id: "digital_lab", label: "Computational Lab & Reproducibility" },
          { id: "ai_scientists", label: "AI Scientist Network" },
          { id: "simulation_math", label: "Multi-Model Sim & Proofs" },
          { id: "replication", label: "Replication & Meta-Analysis" },
          { id: "copilot_safety", label: "Evidence Copilot & Safety" }
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
        backgroundColor: "rgba(15, 23, 42, 0.65)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "2rem"
      }}>
        {activeTab === "overview" && (
          <div>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#6EE7B7" }}>
              Active Scientific Pipelines & Discovery Status
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
                border: "1px solid rgba(16, 185, 129, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Active Research Pipelines & AI Hypotheses
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.85rem" }}>
                  {[
                    { title: "Sub-Kelvin Noise Suppression via Pulse Shaping", domain: "Physics", status: "Replicated", label: "[AI-Generated v1.0]" },
                    { title: "High-Temperature Solid-State Thermal Storage", domain: "Materials", status: "Authorized_Trial", label: "[AI-Generated v1.2]" },
                    { title: "Cryogenic Sensor Drift Calibration", domain: "Engineering", status: "Simulation_Pre_Run", label: "[AI-Generated v2.0]" }
                  ].map((pipe, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.85rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: "#F9FAFB" }}>{pipe.title}</div>
                        <div style={{ fontSize: "0.8rem", color: "#9CA3AF" }}>Domain: {pipe.domain} • <span style={{ color: "#06B6D4" }}>{pipe.label}</span></div>
                      </div>
                      <span style={{
                        fontSize: "0.75rem",
                        padding: "0.25rem 0.6rem",
                        borderRadius: "6px",
                        backgroundColor: "rgba(16, 185, 129, 0.2)",
                        color: "#34D399",
                        fontWeight: 600
                      }}>
                        {pipe.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.85)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(6, 182, 212, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Scientific Safety & Authorization Controls
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { title: "Physical Experiment Authorization", status: "Mandatory Human Gate", desc: "Physical lab trials require explicit human scientist approval." },
                    { title: "Biological Research Safety Boundary", status: "Enforced", desc: "Diagnostics and safe research only. Pathogen optimization strictly prohibited." },
                    { title: "Autonomous Research Limits", status: "Active Sandbox", desc: "No independent material acquisition or safety system modification." }
                  ].map((ctrl, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ fontWeight: 600, fontSize: "0.875rem" }}>{ctrl.title}</span>
                        <span style={{ fontSize: "0.75rem", color: "#A5F3FC", fontWeight: 700 }}>{ctrl.status}</span>
                      </div>
                      <div style={{ fontSize: "0.75rem", color: "#9CA3AF", marginTop: "0.25rem" }}>{ctrl.desc}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab !== "overview" && (
          <div style={{ textAlign: "center", padding: "3rem" }}>
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#6EE7B7", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} MODULE ACTIVE
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "640px", margin: "0 auto 1.5rem auto" }}>
              Question decomposition, literature graph extraction, AI hypothesis generator, virtual lab notebooks, and discovery copilot active under human oversight.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(16, 185, 129, 0.12)",
              border: "1px solid rgba(16, 185, 129, 0.35)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#A7F3D0",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Operational • Human Scientist Review & Safety Gate Enforced
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
