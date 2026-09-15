"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  archiveService,
  getService,
  restoreService,
  Service,
  ServiceUpdateInput,
  updateService,
} from "@/lib/api/services";

export default function ServiceDetailPage() {
  const params = useParams();
  const serviceId = params.id as string;

  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Edit Modal State
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [editForm, setEditForm] = useState<ServiceUpdateInput>({});
  const [saving, setSaving] = useState(false);

  // Archive Confirm State
  const [isArchiveConfirmOpen, setIsArchiveConfirmOpen] = useState(false);
  const [archiving, setArchiving] = useState(false);

  const fetchServiceDetail = useCallback(async () => {
    if (!serviceId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getService(serviceId);
      setService(res.data);
      setEditForm({
        name: res.data.name,
        slug: res.data.slug,
        short_description: res.data.short_description || "",
        description: res.data.description || "",
        category: res.data.category,
        delivery_model: res.data.delivery_model,
        pricing_model: res.data.pricing_model,
        base_price: res.data.base_price || undefined,
        price_min: res.data.price_min || undefined,
        price_max: res.data.price_max || undefined,
        currency: res.data.currency,
        estimated_duration_days: res.data.estimated_duration_days || undefined,
        status: res.data.status,
      });
    } catch (err: any) {
      setError(err.message || "Failed to load service profile.");
    } finally {
      setLoading(false);
    }
  }, [serviceId]);

  useEffect(() => {
    fetchServiceDetail();
  }, [fetchServiceDetail]);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await updateService(serviceId, editForm);
      setService(res.data);
      setIsEditOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to update service.");
    } finally {
      setSaving(false);
    }
  };

  const handleArchive = async () => {
    setArchiving(true);
    try {
      const res = await archiveService(serviceId);
      setService(res.data);
      setIsArchiveConfirmOpen(false);
    } catch (err: any) {
      alert(err.message || "Failed to archive service.");
    } finally {
      setArchiving(false);
    }
  };

  const handleRestore = async () => {
    setArchiving(true);
    try {
      const res = await restoreService(serviceId);
      setService(res.data);
    } catch (err: any) {
      alert(err.message || "Failed to restore service.");
    } finally {
      setArchiving(false);
    }
  };

  if (loading) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 text-center text-neutral-500 text-sm">
        Loading service profile...
      </main>
    );
  }

  if (error || !service) {
    return (
      <main className="max-w-7xl mx-auto px-4 py-12 space-y-4">
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
          <p className="font-semibold">{error || "Service not found."}</p>
        </div>
        <Link href="/services" className="text-xs text-neutral-600 font-semibold underline">
          ← Return to Service Catalog
        </Link>
      </main>
    );
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Breadcrumb */}
      <div>
        <Link
          href="/services"
          className="text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition"
        >
          ← Back to Catalog
        </Link>
      </div>

      {/* Profile Header */}
      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-neutral-900">{service.name}</h1>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                service.status === "ACTIVE"
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : "bg-neutral-100 text-neutral-600 border-neutral-200"
              }`}
            >
              {service.status}
            </span>
          </div>
          <p className="text-xs font-mono text-neutral-400">slug: {service.slug}</p>
          <div className="flex flex-wrap items-center gap-3 text-xs text-neutral-500 pt-1">
            <span>Category: {service.category}</span>
            <span>Delivery: {service.delivery_model}</span>
            <span>Pricing: {service.pricing_model}</span>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsEditOpen(true)}
            className="px-4 py-2 border border-neutral-300 hover:bg-neutral-100 text-neutral-800 text-sm font-medium rounded-lg transition"
          >
            Edit Service
          </button>
          {service.status === "ARCHIVED" ? (
            <button
              onClick={handleRestore}
              disabled={archiving}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition disabled:opacity-50"
            >
              Restore Service
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
        {/* Left Col: Overview, Features & Requirements */}
        <div className="lg:col-span-2 space-y-6">
          {/* Overview */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Service Overview
            </h3>

            <div className="space-y-3 text-xs">
              {service.short_description && (
                <div className="p-3 bg-neutral-50 border border-neutral-200 rounded-lg text-neutral-800 font-medium">
                  {service.short_description}
                </div>
              )}

              <div>
                <span className="text-neutral-400 font-medium block">Detailed Description</span>
                <p className="text-neutral-700 leading-relaxed mt-1 whitespace-pre-wrap">
                  {service.description || "No full description provided."}
                </p>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Service Features
            </h3>

            {service.features && service.features.length > 0 ? (
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                {service.features.map((feat, idx) => (
                  <li
                    key={idx}
                    className="p-2.5 bg-neutral-50 border border-neutral-200 rounded-lg flex items-center space-x-2 text-neutral-800 font-medium"
                  >
                    <span className="text-emerald-500 font-bold">✓</span>
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-xs text-neutral-500 italic">No structured features listed.</div>
            )}
          </div>

          {/* Requirements */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Client Requirements
            </h3>

            {service.requirements && service.requirements.length > 0 ? (
              <ul className="space-y-2 text-xs">
                {service.requirements.map((req, idx) => (
                  <li
                    key={idx}
                    className="p-2.5 bg-amber-50/50 border border-amber-200/60 rounded-lg flex items-center space-x-2 text-neutral-800 font-medium"
                  >
                    <span className="text-amber-600 font-bold">📌</span>
                    <span>{req}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-xs text-neutral-500 italic">No specific client inputs required.</div>
            )}
          </div>
        </div>

        {/* Right Col: Pricing & System Metadata */}
        <div className="space-y-6">
          {/* Pricing & Duration Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Pricing & Duration
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-neutral-400 font-medium block">Pricing Model</span>
                <span className="font-semibold text-neutral-900">{service.pricing_model}</span>
              </div>

              <div>
                <span className="text-neutral-400 font-medium block">Commercial Price</span>
                <span className="text-lg font-bold text-neutral-900">
                  {service.pricing_model === "CUSTOM"
                    ? "Custom Quote Required"
                    : service.base_price
                    ? `${service.currency} ${service.base_price.toLocaleString()}`
                    : "Not specified"}
                </span>
              </div>

              <div>
                <span className="text-neutral-400 font-medium block">Estimated Delivery</span>
                <span className="font-semibold text-neutral-800">
                  {service.estimated_duration_days
                    ? `${service.estimated_duration_days} business days`
                    : "Variable duration"}
                </span>
              </div>

              <div>
                <span className="text-neutral-400 font-medium block">Target Businesses</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {service.target_business_types && service.target_business_types.length > 0 ? (
                    service.target_business_types.map((tb, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-neutral-100 border border-neutral-200 rounded text-[10px] font-bold text-neutral-700"
                      >
                        {tb}
                      </span>
                    ))
                  ) : (
                    <span className="text-neutral-500">All business types</span>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Record Metadata Card */}
          <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm space-y-3 text-xs">
            <h3 className="text-base font-bold text-neutral-900 border-b border-neutral-100 pb-2">
              Record Metadata
            </h3>

            <div>
              <span className="text-neutral-400 block font-medium">Service ID</span>
              <span className="font-mono text-neutral-700 select-all">{service.id}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Created At</span>
              <span className="text-neutral-700">{new Date(service.created_at).toLocaleString()}</span>
            </div>

            <div>
              <span className="text-neutral-400 block font-medium">Updated At</span>
              <span className="text-neutral-700">{new Date(service.updated_at).toLocaleString()}</span>
            </div>

            {service.archived_at && (
              <div>
                <span className="text-neutral-400 block font-medium">Archived At</span>
                <span className="text-red-600">
                  {new Date(service.archived_at).toLocaleString()}
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
              <h3 className="text-lg font-bold text-neutral-900">Edit Catalog Service</h3>
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
                  <label className="block font-semibold text-neutral-700 mb-1">Service Name</label>
                  <input
                    type="text"
                    required
                    value={editForm.name || ""}
                    onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Pricing Model</label>
                  <select
                    value={editForm.pricing_model || "CUSTOM"}
                    onChange={(e) => setEditForm({ ...editForm, pricing_model: e.target.value as any })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="CUSTOM">CUSTOM</option>
                    <option value="STARTING_AT">STARTING_AT</option>
                    <option value="FIXED">FIXED</option>
                    <option value="RANGE">RANGE</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Base Price</label>
                  <input
                    type="number"
                    value={editForm.base_price || ""}
                    onChange={(e) =>
                      setEditForm({
                        ...editForm,
                        base_price: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Short Description</label>
                  <input
                    type="text"
                    value={editForm.short_description || ""}
                    onChange={(e) => setEditForm({ ...editForm, short_description: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Full Description</label>
                  <textarea
                    rows={4}
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

      {/* Archive Modal */}
      {isArchiveConfirmOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-md w-full p-6 space-y-4">
            <h3 className="text-lg font-bold text-neutral-900">Archive Catalog Service?</h3>
            <p className="text-xs text-neutral-600 leading-relaxed">
              Archiving <span className="font-semibold text-neutral-900">{service.name}</span> will mark it as <span className="font-semibold">ARCHIVED</span>. Historical relationships with existing leads will be safely preserved.
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
