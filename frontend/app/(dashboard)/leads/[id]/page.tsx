"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  archiveLead,
  createContact,
  getLead,
  Lead,
  LeadUpdateInput,
  restoreLead,
  transitionLeadStatus,
  updateLead,
} from "@/lib/api/leads";
import {
  addServiceToLead,
  LeadService as LeadServiceType,
  listLeadServices,
  listServices,
  removeServiceFromLead,
  Service,
} from "@/lib/api/services";
import { LeadScoringView } from "@/components/scoring/lead-scoring-view";
import { RecommendationsView } from "@/components/recommendations/recommendations-view";
import { QualificationCard } from "@/components/qualification/qualification-card";
import { PersonalizationCard } from "@/components/outreach/personalization-card";


export default function LeadDetailPage() {
  const params = useParams();
  const leadId = params.id as string;

  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit Lead Modal
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [editForm, setEditForm] = useState<LeadUpdateInput>({});
  const [saving, setSaving] = useState(false);

  // Add Contact Modal
  const [isContactModalOpen, setIsContactModalOpen] = useState(false);
  const [contactForm, setContactForm] = useState({
    name: "",
    role: "Owner / Manager",
    email: "",
    phone: "",
    is_primary: true,
  });
  const [contactSaving, setContactSaving] = useState(false);

  // Status Transition Modal
  const [transitioning, setTransitioning] = useState(false);
  const [lossReason, setLossReason] = useState("");
  const [isLossModalOpen, setIsLossModalOpen] = useState(false);

  const fetchLeadDetail = useCallback(async () => {
    if (!leadId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getLead(leadId);
      setLead(res.data);
      setEditForm({
        title: res.data.title,
        description: res.data.description || "",
        priority: res.data.priority,
        qualification_status: res.data.qualification_status,
        contactability_status: res.data.contactability_status,
        estimated_value: res.data.estimated_value || undefined,
        currency: res.data.currency,
        next_action: res.data.next_action || "",
        notes: res.data.notes || "",
      });
    } catch (err: any) {
      setError(err.message || "Failed to load lead profile.");
    } finally {
      setLoading(false);
    }
  }, [leadId]);

  useEffect(() => {
    fetchLeadDetail();
  }, [fetchLeadDetail]);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await updateLead(leadId, editForm);
      setLead(res.data);
      setIsEditOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to update lead.");
    } finally {
      setSaving(false);
    }
  };

  const handleTransition = async (status: Lead["status"]) => {
    if (status === "LOST") {
      setIsLossModalOpen(true);
      return;
    }

    setTransitioning(true);
    try {
      const res = await transitionLeadStatus(leadId, status);
      setLead(res.data);
    } catch (err: any) {
      alert(err.message || "Failed to change lead status.");
    } finally {
      setTransitioning(false);
    }
  };

  const handleConfirmLoss = async (e: React.FormEvent) => {
    e.preventDefault();
    setTransitioning(true);
    try {
      const res = await transitionLeadStatus(leadId, "LOST", lossReason);
      setLead(res.data);
      setIsLossModalOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to mark lead as lost.");
    } finally {
      setTransitioning(false);
    }
  };

  const handleAddContact = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!lead) return;
    setContactSaving(true);
    try {
      await createContact({
        business_id: lead.business_id,
        lead_id: lead.id,
        name: contactForm.name,
        role: contactForm.role,
        email: contactForm.email,
        phone: contactForm.phone,
        is_primary: contactForm.is_primary,
      });
      setIsContactModalOpen(false);
      setContactForm({
        name: "",
        role: "Owner / Manager",
        email: "",
        phone: "",
        is_primary: false,
      });
      fetchLeadDetail();
    } catch (err: any) {
      alert(err.message || "Failed to add contact.");
    } finally {
      setContactSaving(false);
    }
  };

  const handleArchive = async () => {
    try {
      const res = await archiveLead(leadId);
      setLead(res.data);
    } catch (err: any) {
      alert(err.message || "Failed to archive lead.");
    }
  };

  const handleRestore = async () => {
    try {
      const res = await restoreLead(leadId);
      setLead(res.data);
    } catch (err: any) {
      alert(err.message || "Failed to restore lead.");
    }
  };

  if (loading) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 text-center text-neutral-500 text-sm">
        Loading lead opportunity...
      </main>
    );
  }

  if (error || !lead) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 space-y-4">
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          <p className="font-semibold">{error || "Lead not found."}</p>
        </div>
        <Link href="/leads" className="text-xs text-neutral-600 font-semibold underline">
          ← Return to Lead Directory
        </Link>
      </main>
    );
  }

  const lifecycleStages: Array<Lead["status"]> = [
    "NEW",
    "RESEARCHING",
    "QUALIFIED",
    "CONTACTED",
    "RESPONDED",
    "INTERESTED",
    "MEETING",
    "PROPOSAL",
    "WON",
  ];

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Breadcrumb */}
      <div>
        <Link
          href="/leads"
          className="text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition"
        >
          ← Back to Leads
        </Link>
      </div>

      {/* Header Profile */}
      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-neutral-900">{lead.title}</h1>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                lead.status === "WON"
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : lead.status === "LOST"
                  ? "bg-red-50 text-red-700 border-red-200"
                  : "bg-blue-50 text-blue-700 border-blue-200"
              }`}
            >
              {lead.status}
            </span>
            <span
              className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
                lead.priority === "URGENT"
                  ? "bg-red-100 text-red-800"
                  : lead.priority === "HIGH"
                  ? "bg-amber-100 text-amber-800"
                  : "bg-neutral-100 text-neutral-600"
              }`}
            >
              {lead.priority}
            </span>
          </div>

          {lead.business && (
            <p className="text-xs text-neutral-600 font-medium">
              Organization:{" "}
              <Link
                href={`/businesses/${lead.business.id}`}
                className="text-blue-600 hover:underline font-semibold"
              >
                🏢 {lead.business.name}
              </Link>
              {lead.business.city ? ` (${lead.business.city})` : ""}
            </p>
          )}
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsEditOpen(true)}
            className="px-4 py-2 border border-neutral-300 hover:bg-neutral-100 text-neutral-800 text-sm font-medium rounded-lg transition"
          >
            Edit Lead
          </button>
          {lead.status === "ARCHIVED" ? (
            <button
              onClick={handleRestore}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition"
            >
              Restore Lead
            </button>
          ) : (
            <button
              onClick={handleArchive}
              className="px-4 py-2 border border-red-300 hover:bg-red-50 text-red-700 text-sm font-medium rounded-lg transition"
            >
              Archive
            </button>
          )}
        </div>
      </div>

      {/* Lifecycle Progress Bar */}
      <div className="bg-white p-4 rounded-xl border border-neutral-200 shadow-sm space-y-3">
        <h3 className="text-xs font-bold text-neutral-500 uppercase tracking-wider">
          Sales Lifecycle Stage
        </h3>
        <div className="flex flex-wrap items-center gap-1 sm:gap-2">
          {lifecycleStages.map((stg) => {
            const isCurrent = lead.status === stg;
            return (
              <button
                key={stg}
                disabled={transitioning}
                onClick={() => handleTransition(stg)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
                  isCurrent
                    ? "bg-neutral-900 text-white border-neutral-900 shadow-sm"
                    : "bg-neutral-50 text-neutral-600 border-neutral-200 hover:bg-neutral-100"
                }`}
              >
                {stg}
              </button>
            );
          })}
          <button
            disabled={transitioning}
            onClick={() => handleTransition("LOST")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
              lead.status === "LOST"
                ? "bg-red-600 text-white border-red-600"
                : "bg-red-50 text-red-700 border-red-200 hover:bg-red-100"
            }`}
          >
            LOST
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Details & Contacts */}
        <div className="lg:col-span-2 space-y-6">
          {/* Opportunity Details */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Opportunity Overview
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-neutral-400 font-medium block">Estimated Value</span>
                <span className="text-neutral-900 font-bold text-base">
                  {lead.estimated_value
                    ? `${lead.currency} ${lead.estimated_value.toLocaleString()}`
                    : "Not specified"}
                </span>
              </div>
              <div>
                <span className="text-neutral-400 font-medium block">Next Action Plan</span>
                <span className="text-neutral-800 font-semibold">
                  {lead.next_action || "No action scheduled"}
                </span>
              </div>
              <div className="sm:col-span-2">
                <span className="text-neutral-400 font-medium block">Description</span>
                <p className="text-neutral-700 leading-relaxed mt-1">
                  {lead.description || "No opportunity description recorded."}
                </p>
              </div>
              {lead.notes && (
                <div className="sm:col-span-2 bg-neutral-50 p-3 rounded-lg border border-neutral-200">
                  <span className="text-neutral-500 font-semibold block mb-1">Internal Notes</span>
                  <p className="text-neutral-700 whitespace-pre-wrap">{lead.notes}</p>
                </div>
              )}
            </div>
          </div>

          {/* Contacts Subsystem */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-100 pb-2">
              <h3 className="text-base font-bold text-neutral-900">Associated Contacts</h3>
              <button
                onClick={() => setIsContactModalOpen(true)}
                className="text-xs font-semibold bg-neutral-100 hover:bg-neutral-200 px-3 py-1.5 rounded-lg text-neutral-800 transition"
              >
                + Add Contact
              </button>
            </div>

            {lead.contacts && lead.contacts.length > 0 ? (
              <div className="space-y-3">
                {lead.contacts.map((c) => (
                  <div
                    key={c.id}
                    className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg flex items-center justify-between text-xs"
                  >
                    <div>
                      <div className="font-semibold text-neutral-900 flex items-center space-x-2">
                        <span>{c.name}</span>
                        {c.is_primary && (
                          <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 text-[10px] rounded font-bold">
                            PRIMARY
                          </span>
                        )}
                      </div>
                      <div className="text-neutral-500">{c.role || "Point of Contact"}</div>
                    </div>
                    <div className="text-right space-y-0.5 text-neutral-600">
                      {c.phone && <div>📞 {c.phone}</div>}
                      {c.email && <div>✉️ {c.email}</div>}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 text-center text-xs text-neutral-500 bg-neutral-50 rounded-lg border border-dashed border-neutral-200">
                No individual contacts linked to this lead opportunity yet.
              </div>
            )}
          </div>

          {/* Lead Catalog Services Manager */}
          <LeadServicesManager leadId={lead.id} />

          {/* Service Recommendations Engine */}
          <RecommendationsView leadId={lead.id} />

          {/* Lead Opportunity Scoring System */}
          <LeadScoringView leadId={lead.id} />

          {/* Qualification Agent Assessment */}
          <QualificationCard leadId={lead.id} />

          {/* Personalization & Communication Draft Agent */}
          <PersonalizationCard leadId={lead.id} />

        </div>

        {/* Right Column: Data Quality & System Metadata */}
        <div className="space-y-6">
          {/* Data Quality Card */}
          {lead.data_quality && (
            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
              <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
                Data Quality
              </h3>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-semibold text-neutral-600">Completeness Score</span>
                  <span className="text-sm font-bold text-neutral-900">{lead.data_quality.score}%</span>
                </div>

                <div className="w-full bg-neutral-200 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-2 rounded-full ${
                      lead.data_quality.score >= 80
                        ? "bg-emerald-500"
                        : lead.data_quality.score >= 50
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                    style={{ width: `${lead.data_quality.score}%` }}
                  />
                </div>

                {lead.data_quality.warnings.length > 0 && (
                  <div className="pt-2 space-y-1">
                    <span className="text-xs font-semibold text-amber-700 block">Warnings:</span>
                    <ul className="text-xs text-neutral-600 list-disc pl-4 space-y-0.5">
                      {lead.data_quality.warnings.map((w, idx) => (
                        <li key={idx}>{w}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Qualification & Contactability Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3 text-xs">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Qualification & Safety
            </h3>

            <div>
              <span className="text-neutral-400 block font-medium">Qualification Status</span>
              <span className="font-semibold text-neutral-800">{lead.qualification_status}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Contactability Status</span>
              <span className="font-semibold text-neutral-800">{lead.contactability_status}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Source</span>
              <span className="font-semibold text-neutral-800">
                {lead.source} {lead.source_detail ? `(${lead.source_detail})` : ""}
              </span>
            </div>
          </div>

          {/* Record Metadata Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3 text-xs">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Record Metadata
            </h3>

            <div>
              <span className="text-neutral-400 block font-medium">Lead ID</span>
              <span className="font-mono text-neutral-700 select-all">{lead.id}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Created At</span>
              <span className="text-neutral-700">{new Date(lead.created_at).toLocaleString()}</span>
            </div>

            {lead.first_contacted_at && (
              <div>
                <span className="text-neutral-400 block font-medium">First Contacted</span>
                <span className="text-neutral-700">
                  {new Date(lead.first_contacted_at).toLocaleString()}
                </span>
              </div>
            )}

            {lead.converted_at && (
              <div>
                <span className="text-neutral-400 block font-medium">Converted At</span>
                <span className="text-emerald-600 font-semibold">
                  {new Date(lead.converted_at).toLocaleString()}
                </span>
              </div>
            )}

            {lead.lost_at && (
              <div>
                <span className="text-neutral-400 block font-medium">Lost At</span>
                <span className="text-red-600">
                  {new Date(lead.lost_at).toLocaleString()} {lead.loss_reason ? `(${lead.loss_reason})` : ""}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      {isEditOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Edit Lead Details</h3>
              <button
                onClick={() => setIsEditOpen(false)}
                className="text-neutral-400 hover:text-neutral-700 font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleUpdate} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Title</label>
                  <input
                    type="text"
                    required
                    value={editForm.title || ""}
                    onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Priority</label>
                  <select
                    value={editForm.priority || "MEDIUM"}
                    onChange={(e) => setEditForm({ ...editForm, priority: e.target.value as any })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="URGENT">URGENT</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Est. Value</label>
                  <input
                    type="number"
                    value={editForm.estimated_value || ""}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        estimated_value: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Next Action Plan
                  </label>
                  <input
                    type="text"
                    value={editForm.next_action || ""}
                    onChange={(e) => setEditForm({ ...editForm, next_action: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Description</label>
                  <textarea
                    rows={3}
                    value={editForm.description || ""}
                    onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3 border-t border-neutral-200">
                <button
                  type="button"
                  onClick={() => setIsEditOpen(false)}
                  className="px-4 py-2 border border-neutral-300 rounded-lg font-medium text-neutral-700 hover:bg-neutral-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-neutral-900 text-white rounded-lg font-medium hover:bg-neutral-800 disabled:opacity-50"
                >
                  {saving ? "Updating..." : "Save Changes"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Contact Modal */}
      {isContactModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Add Lead Contact</h3>
              <button
                onClick={() => setIsContactModalOpen(false)}
                className="text-neutral-400 hover:text-neutral-700 font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddContact} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Contact Name *</label>
                <input
                  type="text"
                  required
                  value={contactForm.name}
                  onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                  placeholder="e.g. John Doe"
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                />
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Role / Title</label>
                <input
                  type="text"
                  value={contactForm.role}
                  onChange={(e) => setContactForm({ ...contactForm, role: e.target.value })}
                  placeholder="Owner, Marketing Manager, CTO"
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                />
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Email Address</label>
                <input
                  type="email"
                  value={contactForm.email}
                  onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                  placeholder="john@example.com"
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                />
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Phone Number</label>
                <input
                  type="text"
                  value={contactForm.phone}
                  onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                  placeholder="+92 300 1234567"
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                />
              </div>

              <div className="flex items-center space-x-2 pt-1">
                <input
                  type="checkbox"
                  id="is_primary"
                  checked={contactForm.is_primary}
                  onChange={(e) => setContactForm({ ...contactForm, is_primary: e.target.checked })}
                />
                <label htmlFor="is_primary" className="font-semibold text-neutral-700">
                  Set as Primary Contact for this lead
                </label>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3 border-t border-neutral-200">
                <button
                  type="button"
                  onClick={() => setIsContactModalOpen(false)}
                  className="px-4 py-2 border border-neutral-300 rounded-lg font-medium text-neutral-700 hover:bg-neutral-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={contactSaving}
                  className="px-4 py-2 bg-neutral-900 text-white rounded-lg font-medium hover:bg-neutral-800 disabled:opacity-50"
                >
                  {contactSaving ? "Saving..." : "Save Contact"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Loss Reason Modal */}
      {isLossModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-md w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-neutral-900">Mark Lead as Lost</h3>
            <form onSubmit={handleConfirmLoss} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-neutral-700 mb-1">Loss Reason</label>
                <select
                  value={lossReason}
                  onChange={(e) => setLossReason(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                >
                  <option value="">-- Select Reason --</option>
                  <option value="NO_BUDGET">NO_BUDGET</option>
                  <option value="NO_NEED">NO_NEED</option>
                  <option value="COMPETITOR">COMPETITOR</option>
                  <option value="NO_RESPONSE">NO_RESPONSE</option>
                  <option value="TIMING">TIMING</option>
                  <option value="NOT_A_FIT">NOT_A_FIT</option>
                  <option value="OTHER">OTHER</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsLossModalOpen(false)}
                  className="px-4 py-2 border border-neutral-300 rounded-lg text-xs font-medium text-neutral-700 hover:bg-neutral-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={transitioning}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg text-xs font-medium hover:bg-red-700 disabled:opacity-50"
                >
                  Confirm Lost
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}

function LeadServicesManager({ leadId }: { leadId: string }) {
  const [leadServices, setLeadServices] = useState<LeadServiceType[]>([]);
  const [availableServices, setAvailableServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedServiceId, setSelectedServiceId] = useState("");
  const [relationshipType, setRelationshipType] = useState<LeadServiceType["relationship_type"]>("CONSIDERED");
  const [submitting, setSubmitting] = useState(false);

  const fetchLeadServices = useCallback(async () => {
    setLoading(true);
    try {
      const res = await listLeadServices(leadId);
      setLeadServices(res.data);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  }, [leadId]);

  useEffect(() => {
    fetchLeadServices();
  }, [fetchLeadServices]);

  const handleOpenModal = async () => {
    try {
      const res = await listServices({ page: 1, page_size: 50, status: "ACTIVE" });
      setAvailableServices(res.data);
      setIsModalOpen(true);
    } catch (err) {
      alert("Failed to load active catalog services.");
    }
  };

  const handleAddService = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedServiceId) return;
    setSubmitting(true);
    try {
      await addServiceToLead(leadId, {
        service_id: selectedServiceId,
        relationship_type: relationshipType,
        source: "HUMAN",
      });
      setIsModalOpen(false);
      setSelectedServiceId("");
      fetchLeadServices();
    } catch (err: any) {
      alert(err.message || "Failed to attach service.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemove = async (serviceId: string) => {
    try {
      await removeServiceFromLead(leadId, serviceId);
      fetchLeadServices();
    } catch (err: any) {
      alert(err.message || "Failed to remove service.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-neutral-100 pb-2">
        <div>
          <h3 className="text-base font-bold text-neutral-900">Offered / Target Services</h3>
          <p className="text-xs text-neutral-500">Catalog services associated with this sales lead.</p>
        </div>
        <button
          onClick={handleOpenModal}
          className="text-xs font-semibold bg-neutral-100 hover:bg-neutral-200 px-3 py-1.5 rounded-lg text-neutral-800 transition"
        >
          + Attach Service
        </button>
      </div>

      {loading ? (
        <div className="text-xs text-neutral-500 py-4 text-center">Loading lead services...</div>
      ) : leadServices.length > 0 ? (
        <div className="space-y-3">
          {leadServices.map((ls) => (
            <div
              key={ls.id}
              className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg flex items-center justify-between text-xs"
            >
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-neutral-900">
                    {ls.service?.name || "Catalog Solution"}
                  </span>
                  <span
                    className={`px-1.5 py-0.5 text-[10px] font-bold rounded ${
                      ls.relationship_type === "SELECTED"
                        ? "bg-emerald-100 text-emerald-800"
                        : ls.relationship_type === "RECOMMENDED"
                        ? "bg-blue-100 text-blue-800"
                        : "bg-neutral-200 text-neutral-700"
                    }`}
                  >
                    {ls.relationship_type}
                  </span>
                </div>
                {ls.service?.short_description && (
                  <div className="text-neutral-500 text-[11px]">{ls.service.short_description}</div>
                )}
              </div>

              <div className="flex items-center space-x-3">
                {ls.service?.base_price && (
                  <span className="font-bold text-neutral-900">
                    ${ls.service.base_price.toLocaleString()}
                  </span>
                )}
                <button
                  onClick={() => handleRemove(ls.service_id)}
                  className="text-neutral-400 hover:text-red-600 font-bold px-1"
                  title="Remove association"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 text-center text-xs text-neutral-500 bg-neutral-50 rounded-lg border border-dashed border-neutral-200">
          No services attached to this opportunity yet. Click &quot;Attach Service&quot; to associate solutions from the catalog.
        </div>
      )}

      {/* Attach Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Attach Catalog Service</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-neutral-400 hover:text-neutral-700 font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddService} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-neutral-700 mb-1">
                  Select Catalog Service *
                </label>
                <select
                  required
                  value={selectedServiceId}
                  onChange={(e) => setSelectedServiceId(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                >
                  <option value="">-- Choose Solution --</option>
                  {availableServices.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} ({s.category.replace("_", " ")})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-neutral-700 mb-1">
                  Relationship Type
                </label>
                <select
                  value={relationshipType}
                  onChange={(e) => setRelationshipType(e.target.value as any)}
                  className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                >
                  <option value="CONSIDERED">CONSIDERED</option>
                  <option value="RECOMMENDED">RECOMMENDED</option>
                  <option value="SELECTED">SELECTED</option>
                  <option value="REJECTED">REJECTED</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3 border-t border-neutral-200">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border border-neutral-300 rounded-lg font-medium text-neutral-700 hover:bg-neutral-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-neutral-900 text-white rounded-lg font-medium hover:bg-neutral-800 disabled:opacity-50"
                >
                  {submitting ? "Attaching..." : "Attach Service"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

