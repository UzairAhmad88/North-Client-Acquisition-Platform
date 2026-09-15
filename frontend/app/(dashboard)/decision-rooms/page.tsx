"use client";

import React, { useEffect, useState } from "react";
import { decisionRoomsApi, DecisionRoomOverview } from "@/lib/api/decision_rooms";
import { DecisionRoomDashboard } from "@/components/decision";
import { Loader2, Plus, DoorOpen, ShieldCheck } from "lucide-react";

export default function DecisionRoomsPage() {
  const [overview, setOverview] = useState<DecisionRoomOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadInitialRoom() {
      try {
        const rooms = await decisionRoomsApi.listRooms();
        if (rooms.length > 0) {
          const roomData = await decisionRoomsApi.getRoomOverview(rooms[0].id);
          setOverview(roomData);
        } else {
          // Create seed if none exists
          const newRoom = await decisionRoomsApi.createRoom({
            title: "Launch Enterprise AI Solutions Tier",
            question: "Should North's launch a dedicated Enterprise AI Solutions tier?",
          });
          const roomData = await decisionRoomsApi.getRoomOverview(newRoom.id);
          setOverview(roomData);
        }
      } catch (err: any) {
        setError(err.message || "Failed to load decision room workspace");
      } finally {
        setLoading(false);
      }
    }
    loadInitialRoom();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-slate-400 space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
        <p className="text-sm">Loading Decision Room Workspace & Augmented Intelligence Layer...</p>
      </div>
    );
  }

  if (error || !overview) {
    return (
      <div className="max-w-4xl mx-auto my-12 p-6 bg-rose-950/20 border border-rose-800/40 rounded-xl text-center space-y-3">
        <h2 className="text-lg font-bold text-rose-300">Decision Room Error</h2>
        <p className="text-sm text-slate-300">{error || "No active decision room found."}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <DecisionRoomDashboard initialData={overview} />
    </div>
  );
}
