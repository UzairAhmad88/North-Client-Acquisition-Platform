"use client";

import React, { useState } from "react";

export default function PlanetaryCivilizationDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#040711",
      color: "#F3F4F6",
      fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      padding: "2rem"
    }}>
      {/* Header Banner */}
      <header style={{
        background: "linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(79, 70, 229, 0.3))",
        backdropFilter: "blur(12px)",
        borderRadius: "16px",
        padding: "2rem",
        border: "1px solid rgba(99, 102, 241, 0.35)",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.6)",
        marginBottom: "2rem"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
              <span style={{
                background: "linear-gradient(90deg, #6366F1, #8B5CF6)",
                color: "#FFFFFF",
                fontSize: "0.75rem",
                fontWeight: 700,
                padding: "0.25rem 0.75rem",
                borderRadius: "9999px",
                textTransform: "uppercase",
                letterSpacing: "0.05em"
              }}>
                Phase 96 Civilization Operating Layer
              </span>
              <span style={{ color: "#9CA3AF", fontSize: "0.875rem" }}>Human–AI Collective Intelligence & Knowledge Commons</span>
            </div>
            <h1 style={{
              fontSize: "2.25rem",
              fontWeight: 800,
              background: "linear-gradient(90deg, #F9FAFB, #A5B4FC)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              margin: 0
            }}>
              Planetary Civilization OS & Knowledge Commons
            </h1>
            <p style={{ color: "#9CA3AF", marginTop: "0.5rem", maxWidth: "900px", fontSize: "0.95rem" }}>
              Top-level socio-technical operating environment facilitating global knowledge preservation, evidence-based deliberation, institutional design simulation, problem-solving marketplaces, long-term resource forecasting (1Y–100Y+), and constitutional AI safety.
            </p>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div style={{
              backgroundColor: "rgba(99, 102, 241, 0.12)",
              border: "1px solid rgba(99, 102, 241, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#C7D2FE", textTransform: "uppercase" }}>Civilization Wellbeing</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#818CF8" }}>87.4 INDEX</div>
            </div>
            <div style={{
              backgroundColor: "rgba(139, 92, 246, 0.12)",
              border: "1px solid rgba(139, 92, 246, 0.35)",
              borderRadius: "12px",
              padding: "0.75rem 1.25rem",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "0.75rem", color: "#DDD6FE", textTransform: "uppercase" }}>Constitutional Governance</div>
              <div style={{ fontSize: "1.25rem", fontWeight: 700, color: "#A78BFA" }}>V96.1 PROTECTED</div>
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
          { label: "Global Knowledge Commons", value: "142,800 Nodes", sub: "Provenance & Quality Verified", color: "#6366F1" },
          { label: "Deliberation Argument Maps", value: "1,240 Maps", sub: "Minority View Preserved", color: "#8B5CF6" },
          { label: "Institutional Simulations", value: "94.0 Transparency", sub: "Failure Mode Tested", color: "#10B981" },
          { label: "Human–AI Teams Active", value: "54 Taskforces", sub: "Role-Specialized & Audited", color: "#3B82F6" },
          { label: "Open Problem Marketplace", value: "320 Problems", sub: "Safe-to-Fail Experiments", color: "#F59E0B" },
          { label: "Long-Horizon Scenarios", value: "100Y+ Horizons", sub: "Red-Team Audited", color: "#06B6D4" }
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
          { id: "overview", label: "Civilization State Baseline" },
          { id: "knowledge_commons", label: "Global Knowledge Commons" },
          { id: "deliberation", label: "Evidence Deliberation & Memos" },
          { id: "institutional_lab", label: "Institutional Design Simulator" },
          { id: "collective_int", label: "Human-AI Collective Intelligence" },
          { id: "problem_marketplace", label: "Open Problem Marketplace" },
          { id: "forecasting", label: "Long-Horizon Scenarios (100Y+)" },
          { id: "skills_rights", label: "Skills Graph & Algorithmic Appeal" }
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
              backgroundColor: activeTab === tab.id ? "#6366F1" : "rgba(30, 41, 59, 0.6)",
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
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "1rem", color: "#A5B4FC" }}>
              Multi-Dimensional Civilization Condition Matrix
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
                border: "1px solid rgba(99, 102, 241, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  11 Civilization Core Dimensions
                </h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                  {[
                    { name: "Knowledge", val: "92.4" },
                    { name: "Health", val: "88.0" },
                    { name: "Education", val: "85.5" },
                    { name: "Infrastructure", val: "89.2" },
                    { name: "Economic Capacity", val: "87.8" },
                    { name: "Scientific Progress", val: "94.1" },
                    { name: "Technological Capability", val: "95.0" },
                    { name: "Environmental Stability", val: "76.5" },
                    { name: "Institutional Capacity", val: "84.0" },
                    { name: "Resilience", val: "91.5" }
                  ].map((dim, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.5)",
                      padding: "0.75rem",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}>
                      <span style={{ fontSize: "0.85rem", color: "#9CA3AF" }}>{dim.name}</span>
                      <span style={{ fontWeight: 700, color: "#818CF8" }}>{dim.val}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                backgroundColor: "rgba(6, 9, 17, 0.85)",
                padding: "1.5rem",
                borderRadius: "12px",
                border: "1px solid rgba(139, 92, 246, 0.25)"
              }}>
                <h3 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem", color: "#F3F4F6" }}>
                  Constitutional Safety & Human Sovereignty Controls
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {[
                    { title: "Human Override Protection", status: "Active (Level 5)", desc: "Humans retain unilateral pause, rejection, and disable rights over AI actions." },
                    { title: "Self-Modifying Governance Prohibited", status: "Enforced", desc: "AI systems are forbidden from rewriting their own constitutional rules." },
                    { title: "Disagreement & Pluralism Preservation", status: "Active", desc: "Minority perspectives and model disagreements are preserved without forced consensus." }
                  ].map((ctrl, idx) => (
                    <div key={idx} style={{
                      backgroundColor: "rgba(30, 41, 59, 0.4)",
                      padding: "0.75rem",
                      borderRadius: "8px"
                    }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span style={{ fontWeight: 600, fontSize: "0.875rem" }}>{ctrl.title}</span>
                        <span style={{ fontSize: "0.75rem", color: "#A78BFA", fontWeight: 700 }}>{ctrl.status}</span>
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
            <h3 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#A5B4FC", marginBottom: "0.5rem" }}>
              {activeTab.toUpperCase().replace("_", " ")} MODULE ACTIVE
            </h3>
            <p style={{ color: "#9CA3AF", maxWidth: "640px", margin: "0 auto 1.5rem auto" }}>
              Global knowledge commons, evidence-based argument mapping, institutional lab simulations, reskilling pathways, and constitutional governance active under human leadership.
            </p>
            <div style={{
              display: "inline-block",
              backgroundColor: "rgba(99, 102, 241, 0.12)",
              border: "1px solid rgba(99, 102, 241, 0.35)",
              padding: "0.75rem 1.5rem",
              borderRadius: "8px",
              color: "#C7D2FE",
              fontWeight: 600,
              fontSize: "0.9rem"
            }}>
              Status: Operational • Sovereign Human Governance Enforced
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
