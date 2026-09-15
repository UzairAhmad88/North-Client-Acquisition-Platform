"use client";

import React, { useState } from "react";
import { DevSecOpsSoftwareFactoryDashboard } from "@/components/devsecops";
import { EngineeringDashboard } from "@/components/engineering_os";
import { Zap, Layers } from "lucide-react";

export default function EngineeringPage() {
  const [platformMode, setPlatformMode] = useState<"devsecops" | "engineering_os">("devsecops");

  return (
    <div className="flex flex-col min-h-screen">
      {/* Top Banner Mode Selector */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-400 font-medium">Active Platform View:</span>
          <span className="font-semibold text-white">
            {platformMode === "devsecops"
              ? "Phase 67 — Autonomous DevSecOps & AI Software Factory"
              : "Phase 61 — Unified Engineering OS & Technical Operations"}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPlatformMode("devsecops")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all ${
              platformMode === "devsecops"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            <Zap className="h-3.5 w-3.5" />
            Phase 67: DevSecOps Software Factory
          </button>
          <button
            onClick={() => setPlatformMode("engineering_os")}
            className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-all ${
              platformMode === "engineering_os"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            <Layers className="h-3.5 w-3.5" />
            Phase 61: Engineering OS
          </button>
        </div>
      </div>

      {/* Main View */}
      <div className="flex-1">
        {platformMode === "devsecops" ? (
          <DevSecOpsSoftwareFactoryDashboard />
        ) : (
          <EngineeringDashboard />
        )}
      </div>
    </div>
  );
}
