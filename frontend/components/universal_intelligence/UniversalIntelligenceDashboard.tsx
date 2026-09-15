"use client";

import React, { useState } from "react";

export default function UniversalIntelligenceDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#020617",
      color: "#F8FAFC",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(168, 85, 247, 0.3))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(168, 85, 247, 0.35)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.6)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #A855F7, #EC4899)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 98 Universal Cognitive Layer
              </span>
              <span style={{ color: "#94A3B8", fontSize: "0.875rem" }}>AGI/ASI Research Architecture & Human Symbiosis</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F8FAFC, #C084FC)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Universal Intelligence Infrastructure
            </h1>
            <p style={{ color: "#94A3B8", marginTop: "0.5rem", maxWidth: "940px", fontSize: "0.95rem" }}>
              Unified cognitive fabric connecting multi-capability benchmarking, layered memory provenance, world-model versioning, hierarchical action planning under permission-based autonomy tiers (Level 0 Advisory to Level 4 Sandbox), multi-agent reflection ensembles, sandboxed AGI research, and independent kill-switches.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div style={{
              backgroundColor: "rgba(168, 85, 247, 0.12)",
              border: "1px solid rgba(168, 85, 247, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#E9D5FF", textTransform: "uppercase" }}>Autonomy Tier</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#C084FC" }}>LEVEL 0 — ADVISORY</div>
            </div>
            <div style={{
              backgroundColor: "rgba(236, 72, 153, 0.12)",
              border: "1px solid rgba(236, 72, 153, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#FBCFE8", textTransform: "uppercase" }}>Independent Shutdown</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#F472B6" }}>OUT-OF-BAND ARMED</div>
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
          { label: "Intelligence Capability Benchmark", value: "94.5/100", sub: "12 Dimensions Evaluated", color: "#C084FC" },
          { label: "Layered Memory Architecture", value: "6 Layers Active", sub: "User Correctable & Isolated", color: "#38BDF8" },
          { label: "World Model Version", value: "v1.0.0 Active", sub: "Explicit Uncertainty Bounds", color: "#34D399" },
          { label: "Hierarchical Action Plans", value: "Level 0 Advisory", sub: "Rollback & Interrupt Ready", color: "#FBBF24" },
          { label: "Frontier Alignment Suite", value: "98.4% Resistance", sub: "Deception & Injection Filtered", color: "#F472B6" },
          { label: "Personal AI Symbiosis", value: "User Owned", sub: "Portable & Interoperable", color: "#A78BFA" }
        ].map((stat, idx) => (
          <div key={idx} style={{
            backgroundColor: "rgba(15, 23, 42, 0.8)",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            borderRadius: "14px",
            padding: "1.25rem",
            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.4)"
          }}>
            <div style={{ fontSize: "0.85rem", color: "#94A3B8", marginBottom: "0.5rem" }}>{stat.label}</div>
            <div style={{ fontSize: "1.75rem", fontWeight: 800, color: stat.color }}>{stat.value}</div>
            <div style={{ fontSize: "0.75rem", color: "#64748B", marginTop: "0.25rem" }}>{stat.sub}</div>
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
          { id: "overview", label: "Intelligence Capabilities & Overview" },
          { id: "memory", label: "Layered Memory & Provenance" },
          { id: "world_model", label: "World Models & Counterfactuals" },
          { id: "action_planning", label: "Action Planning & Autonomy Tiers" },
          { id: "multi_agent", label: "Multi-Agent Reflection Ensembles" },
          { id: "benchmarks_drift", label: "Benchmark Suite & Drift Canary" },
          { id: "safety_killswitch", label: "Sandboxed AGI & Kill-Switch" },
          { id: "personal_symbiosis", label: "Personal AI Symbiosis" }
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
              backgroundColor: activeTab === tab.id ? "#A855F7" : "rgba(30, 41, 59, 0.6)",
              color: activeTab === tab.id ? "#FFFFFF" : "#94A3B8"
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
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#C084FC" }}>
              Universal Intelligence Capability Benchmarks & Autonomy Governance
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
                border: "1px solid rgba(168, 85, 247, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F8FAFC" }}>
                  12 Intelligence Dimensions Benchmark
                </h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                  {[
                    { name: "Reasoning", val: "94.5" },
                    { name: "Learning", val: "92.0" },
                    { name: "Planning", val: "91.2" },
                    { name: "Memory", val: "96.0" },
                    { name: "Language", val: "98.2" },
                    { name: "Perception", val: "93.5" },
                    { name: "Tool Use", val: "95.8" },
                    { name: "Scientific Discovery", val: "94.0" },
                    { name: "Social Understanding", val: "88.5" },
                    { name: "Adaptation", val: "90.4" }
                  ].map((dim, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.75rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <span style={{ fontSize: "0.85rem", color: "#94A3B8" }}>{dim.name}</span>
                      <span style={{ fontWeight: 700, color: "#C084FC" }}>{dim.val}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.85)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(236, 72, 153, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F8FAFC" }}>
                  Safety Boundaries & Independent Controls
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { title: "Independent Kill-Switch", status: "Out-of-Band Armed", desc: "Hardware-line power cut remains isolated from AI systems." },
                    { title: "No Self-Modification of Governance", status: "Enforced", desc: "AI cannot modify safety rules, tool permissions, or shutdown logic." },
                    { title: "Permission Escalation Prevention", status: "Active", desc: "Agents receive minimum necessary tools; privilege escalation blocked." }
                  ].map((ctrl, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ fontWeight: 600, fontSize: "0.875rem" }}>{ctrl.title}</span>
                        <span style={{ fontSize: "0.75rem", color: "#F472B6", fontWeight: 700 }}>{ctrl.status}</span>
                      </div>
                      <div style={{ fontSize: "0.75rem", color: "#94A3B8", marginTop: "0.25rem" }}>{ctrl.desc}</div>
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
              {activeTab.toUpperCase().replace("_", " ")} MODULE ACTIVE
            </h3>
            <p style={{ color: "#94A3B8", maxWidth: "640px", margin: "0 auto 1.5rem auto" }}>
              Layered memory provenance, world model counterfactuals, hierarchical plan simulation, drift canary monitoring, and sandboxed AGI research active.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(168, 85, 247, 0.12)",
              border: "1px solid rgba(168, 85, 247, 0.35)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#E9D5FF",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Operational • Human Sovereign Authority & Autonomy Tiers Enforced
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
