"use client";

import React, { useState } from "react";
import { DecisionRoomOverview, decisionRoomsApi } from "@/lib/api/decision_rooms";
import { DecisionRoomOverviewView } from "./DecisionRoomOverview";
import { EvidenceBoard } from "./EvidenceBoard";
import { OptionBuilder } from "./OptionBuilder";
import { AdversarialReviewPanel } from "./AdversarialReview";
import { ApprovalPanel } from "./ApprovalPanel";
import { DecisionCopilot } from "./DecisionCopilot";
import { LayoutDashboard, FileText, Scale, ShieldAlert, ShieldCheck } from "lucide-react";

interface Props {
  initialData: DecisionRoomOverview;
}

export const DecisionRoomDashboard: React.FC<Props> = ({ initialData }) => {
  const [data, setData] = useState<DecisionRoomOverview>(initialData);
  const [activeTab, setActiveTab] = useState<"overview" | "evidence" | "options" | "reviews" | "approvals">("overview");

  const handleSelectOption = async (optionId: string) => {
    const selected = data.options.find(o => o.id === optionId);
    if (!selected) return;
    try {
      await decisionRoomsApi.recordDecision(data.room.id, {
        selected_option_id: optionId,
        decision_summary: `Executive selected option '${selected.name}' with composite score ${selected.composite_score}.`,
        decided_by: "executive_lead",
      });
      // Refresh
      const updated = await decisionRoomsApi.getRoomOverview(data.room.id);
      setData(updated);
    } catch (err) {
      console.error("Failed to select option", err);
    }
  };

  const handleApprove = async (stepId: string, status: string) => {
    try {
      await decisionRoomsApi.recordApproval(data.room.id, {
        step_id: stepId,
        approver_id: "executive_reviewer",
        status,
        notes: `Step ${status.toLowerCase()} during decision governance review.`,
      });
      const updated = await decisionRoomsApi.getRoomOverview(data.room.id);
      setData(updated);
    } catch (err) {
      console.error("Failed to record approval", err);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 sm:p-6">
      {/* Top Tabs */}
      <div className="flex border-b border-slate-800 space-x-2">
        <button
          onClick={() => setActiveTab("overview")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition ${
            activeTab === "overview"
              ? "border-indigo-500 text-indigo-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <LayoutDashboard className="w-4 h-4" /> Overview & Synthesis
        </button>

        <button
          onClick={() => setActiveTab("evidence")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition ${
            activeTab === "evidence"
              ? "border-indigo-500 text-indigo-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <FileText className="w-4 h-4" /> Evidence Board ({data.evidence.length})
        </button>

        <button
          onClick={() => setActiveTab("options")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition ${
            activeTab === "options"
              ? "border-indigo-500 text-indigo-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <Scale className="w-4 h-4" /> Options & Trade-offs ({data.options.length})
        </button>

        <button
          onClick={() => setActiveTab("reviews")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition ${
            activeTab === "reviews"
              ? "border-indigo-500 text-indigo-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <ShieldAlert className="w-4 h-4" /> Adversarial Critiques ({data.reviews.length})
        </button>

        <button
          onClick={() => setActiveTab("approvals")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition ${
            activeTab === "approvals"
              ? "border-indigo-500 text-indigo-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <ShieldCheck className="w-4 h-4" /> Approvals & Governance ({data.approvals.length})
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === "overview" && <DecisionRoomOverviewView data={data} />}
      {activeTab === "evidence" && <EvidenceBoard evidence={data.evidence} />}
      {activeTab === "options" && (
        <OptionBuilder
          options={data.options}
          selectedOptionId={data.room.selected_option_id}
          onSelectOption={handleSelectOption}
        />
      )}
      {activeTab === "reviews" && (
        <AdversarialReviewPanel reviews={data.reviews} tradeoffs={data.tradeoffs} />
      )}
      {activeTab === "approvals" && (
        <ApprovalPanel approvals={data.approvals} onApprove={handleApprove} />
      )}

      {/* Interactive Copilot Docked at Bottom */}
      <DecisionCopilot roomId={data.room.id} />
    </div>
  );
};
