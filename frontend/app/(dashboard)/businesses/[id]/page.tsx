"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import {
  archiveBusiness,
  Business,
  BusinessUpdateInput,
  getBusiness,
  restoreBusiness,
  updateBusiness,
} from "@/lib/api/businesses";
import { BusinessResearchView } from "@/components/research/business-research-view";
import { BusinessAuditView } from "@/components/audits/business-audit-view";



export default function BusinessDetailPage() {
  const params = useParams();
  const router = useRouter();
  const businessId = params.id as string;

  const [business, setBusiness] = useState<Business | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit modal
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [editForm, setEditForm] = useState<BusinessUpdateInput>({});
  const [saving, setSaving] = useState(false);

  // Archive confirm modal
  const [isArchiveConfirmOpen, setIsArchiveConfirmOpen] = useState(false);
  const [archiving, setArchiving] = useState(false);

  const fetchBusinessDetail = useCallback(async () => {
    if (!businessId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getBusiness(businessId);
      setBusiness(res.data);
      setEditForm({
        name: res.data.name,
        legal_name: res.data.legal_name || "",
        description: res.data.description || "",
        business_type: res.data.business_type,
        industry: res.data.industry,
        category: res.data.category || "",
        subcategory: res.data.subcategory || "",
        phone: res.data.phone || "",
        email: res.data.email || "",
        website_url: res.data.website_url || "",
        address: res.data.address || "",
        city: res.data.city || "",
        state: res.data.state || "",
        country: res.data.country || "",
        postal_code: res.data.postal_code || "",
        status: res.data.status,
      });
    } catch (err: any) {
      setError(err.message || "Failed to load business profile.");
    } finally {
      setLoading(false);
    }
  }, [businessId]);

  useEffect(() => {
    fetchBusinessDetail();
  }, [fetchBusinessDetail]);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await updateBusiness(businessId, editForm);
      setBusiness(res.data);
      setIsEditOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to update business.");
    } finally {
      setSaving(false);
    }
  };

  const handleArchive = async () => {
    setArchiving(true);
    try {
      const res = await archiveBusiness(businessId);
      setBusiness(res.data);
      setIsArchiveConfirmOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to archive business.");
    } finally {
      setArchiving(false);
    }
  };

  const handleRestore = async () => {
    setArchiving(true);
    try {
      const res = await restoreBusiness(businessId);
      setBusiness(res.data);
    } catch (err: any) {
      alert(err.message || "Failed to restore business.");
    } finally {
      setArchiving(false);
    }
  };

  if (loading) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 text-center text-neutral-500 text-sm">
        Loading business profile...
      </main>
    );
  }

  if (error || !business) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 space-y-4">
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          <p className="font-semibold">{error || "Business not found."}</p>
        </div>
        <Link href="/businesses" className="text-xs text-neutral-600 font-semibold underline">
          ← Return to Business Directory
        </Link>
      </main>
    );
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Breadcrumb */}
      <div>
        <Link
          href="/businesses"
          className="text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition"
        >
          ← Back to Businesses
        </Link>
      </div>

      {/* Profile Header */}
      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-neutral-900">{business.name}</h1>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                business.status === "ACTIVE"
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : business.status === "INACTIVE"
                  ? "bg-amber-50 text-amber-700 border-amber-200"
                  : "bg-neutral-100 text-neutral-600 border-neutral-200"
              }`}
            >
              {business.status}
            </span>
          </div>
          {business.legal_name && (
            <p className="text-xs text-neutral-500 font-medium">
              Legal: {business.legal_name}
            </p>
          )}
          <div className="flex flex-wrap items-center gap-3 text-xs text-neutral-500 pt-1">
            <span>🏭 {business.industry}</span>
            <span>📍 {business.city || "—"}{business.country ? `, ${business.country}` : ""}</span>
            <span>Type: {business.business_type}</span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsEditOpen(true)}
            className="px-4 py-2 border border-neutral-300 hover:bg-neutral-100 text-neutral-800 text-sm font-medium rounded-lg transition"
          >
            Edit Profile
          </button>
          {business.status === "ARCHIVED" ? (
            <button
              onClick={handleRestore}
              disabled={archiving}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition disabled:opacity-50"
            >
              Restore Business
            </button>
          ) : (
            <button
              onClick={() => setIsArchiveConfirmOpen(true)}
              className="px-4 py-2 border border-red-300 hover:bg-red-50 text-red-700 text-sm font-medium rounded-lg transition"
            >
              Archive
            </button>
          )}
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Details & Metadata */}
        <div className="lg:col-span-2 space-y-6">
          {/* Information Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Business Overview
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-neutral-400 font-medium block">Phone</span>
                <span className="text-neutral-800 font-semibold">{business.phone || "Not recorded"}</span>
              </div>
              <div>
                <span className="text-neutral-400 font-medium block">Email</span>
                <span className="text-neutral-800 font-semibold">{business.email || "Not recorded"}</span>
              </div>
              <div className="sm:col-span-2">
                <span className="text-neutral-400 font-medium block">Website URL</span>
                {business.website_url ? (
                  <a
                    href={
                      business.website_url.startsWith("http")
                        ? business.website_url
                        : `https://${business.website_url}`
                    }
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 font-semibold hover:underline"
                  >
                    {business.website_url}
                  </a>
                ) : (
                  <span className="text-neutral-800 font-semibold">Not recorded</span>
                )}
              </div>
              <div className="sm:col-span-2">
                <span className="text-neutral-400 font-medium block">Address</span>
                <span className="text-neutral-800 font-semibold">
                  {business.address ? `${business.address}, ` : ""}
                  {business.city ? `${business.city}, ` : ""}
                  {business.state ? `${business.state}, ` : ""}
                  {business.country || ""} {business.postal_code || ""}
                </span>
              </div>
              <div className="sm:col-span-2">
                <span className="text-neutral-400 font-medium block">Description</span>
                <p className="text-neutral-700 leading-relaxed mt-1">
                  {business.description || "No description provided."}
                </p>
              </div>
            </div>
          </div>

          {/* Placeholders for Future CRM Modules */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Future CRM Relationships
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg">
                <span className="text-xs text-neutral-500 block">Leads</span>
                <span className="text-lg font-bold text-neutral-400">0</span>
                <span className="text-[10px] text-neutral-400 block">Phase 06</span>
              </div>
              <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg">
                <span className="text-xs text-neutral-500 block">Research</span>
                <span className="text-lg font-bold text-neutral-400">0</span>
                <span className="text-[10px] text-neutral-400 block">Phase 10</span>
              </div>
              <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg">
                <span className="text-xs text-neutral-500 block">Audits</span>
                <span className="text-lg font-bold text-neutral-400">0</span>
                <span className="text-[10px] text-neutral-400 block">Phase 11</span>
              </div>
              <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg">
                <span className="text-xs text-neutral-500 block">Outreach</span>
                <span className="text-lg font-bold text-neutral-400">0</span>
                <span className="text-[10px] text-neutral-400 block">Phase 14</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: Data Quality & Metadata */}
        <div className="space-y-6">
          {/* Data Quality Card */}
          {business.data_quality && (
            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
              <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
                Data Quality
              </h3>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-semibold text-neutral-600">Completeness Score</span>
                  <span className="text-sm font-bold text-neutral-900">
                    {business.data_quality.score}%
                  </span>
                </div>

                <div className="w-full bg-neutral-200 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-2 rounded-full ${
                      business.data_quality.score >= 80
                        ? "bg-emerald-500"
                        : business.data_quality.score >= 50
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                    style={{ width: `${business.data_quality.score}%` }}
                  />
                </div>

                {business.data_quality.warnings.length > 0 && (
                  <div className="pt-2 space-y-1">
                    <span className="text-xs font-semibold text-amber-700 block">Warnings:</span>
                    <ul className="text-xs text-neutral-600 list-disc pl-4 space-y-0.5">
                      {business.data_quality.warnings.map((w, idx) => (
                        <li key={idx}>{w}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* System Metadata Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3 text-xs">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Record Metadata
            </h3>

            <div>
              <span className="text-neutral-400 block font-medium">Business ID</span>
              <span className="font-mono text-neutral-700 select-all">{business.id}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Data Source</span>
              <span className="font-semibold text-neutral-800">{business.source}</span>
            </div>

            {business.source_url && (
              <div>
                <span className="text-neutral-400 block font-medium">Source URL</span>
                <span className="text-blue-600 truncate block">{business.source_url}</span>
              </div>
            )}

            {business.external_id && (
              <div>
                <span className="text-neutral-400 block font-medium">External ID</span>
                <span className="font-mono text-neutral-700">{business.external_id}</span>
              </div>
            )}

            <div>
              <span className="text-neutral-400 block font-medium">Created At</span>
              <span className="text-neutral-700">
                {new Date(business.created_at).toLocaleString()}
              </span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Updated At</span>
              <span className="text-neutral-700">
                {new Date(business.updated_at).toLocaleString()}
              </span>
            </div>

            {business.archived_at && (
              <div>
                <span className="text-neutral-400 block font-medium">Archived At</span>
                <span className="text-red-600">
                  {new Date(business.archived_at).toLocaleString()}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Website & Digital Presence Audit Section */}
      <div className="pt-6 border-t border-neutral-200">
        <BusinessAuditView businessId={business.id} businessWebsite={business.website_url} />
      </div>

      {/* Research System Evidence Profile */}
      <div className="pt-6 border-t border-neutral-200">
        <BusinessResearchView businessId={business.id} businessName={business.name} />
      </div>


      {/* Edit Modal */}
      {isEditOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Edit Business Profile</h3>
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
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Business Name
                  </label>
                  <input
                    type="text"
                    required
                    value={editForm.name || ""}
                    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Legal Name
                  </label>
                  <input
                    type="text"
                    value={editForm.legal_name || ""}
                    onChange={(e) => setEditForm({ ...editForm, legal_name: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Industry</label>
                  <input
                    type="text"
                    value={editForm.industry || ""}
                    onChange={(e) => setEditForm({ ...editForm, industry: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Phone</label>
                  <input
                    type="text"
                    value={editForm.phone || ""}
                    onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={editForm.email || ""}
                    onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Website URL
                  </label>
                  <input
                    type="text"
                    value={editForm.website_url || ""}
                    onChange={(e) => setEditForm({ ...editForm, website_url: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">City</label>
                  <input
                    type="text"
                    value={editForm.city || ""}
                    onChange={(e) => setEditForm({ ...editForm, city: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Status</label>
                  <select
                    value={editForm.status || "ACTIVE"}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        status: e.target.value as "ACTIVE" | "INACTIVE" | "ARCHIVED",
                      })
                    }
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="ACTIVE">ACTIVE</option>
                    <option value="INACTIVE">INACTIVE</option>
                    <option value="ARCHIVED">ARCHIVED</option>
                  </select>
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

      {/* Archive Confirmation Dialog */}
      {isArchiveConfirmOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-md w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-neutral-900">Archive Business Record?</h3>
            <p className="text-xs text-neutral-600 leading-relaxed">
              Archiving <span className="font-semibold text-neutral-900">{business.name}</span> will set its status to <span className="font-semibold">ARCHIVED</span>. Historical relationships and metadata will be safely preserved. You can restore this business at any time.
            </p>
            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setIsArchiveConfirmOpen(false)}
                className="px-4 py-2 border border-neutral-300 rounded-lg text-xs font-medium text-neutral-700 hover:bg-neutral-100"
              >
                Cancel
              </button>
              <button
                onClick={handleArchive}
                disabled={archiving}
                className="px-4 py-2 bg-red-600 text-white rounded-lg text-xs font-medium hover:bg-red-700 disabled:opacity-50"
              >
                {archiving ? "Archiving..." : "Confirm Archive"}
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
