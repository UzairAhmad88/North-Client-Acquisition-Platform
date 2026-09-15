"""SQLAlchemy ORM Models for Unified Billing, Invoicing, Payments, Financial Operations & Commercial Control."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text

from app.models.base import Base

JSON_TYPE = JSON


class BillingProfileModel(Base):
    """Client and entity billing profiles."""
    __tablename__ = "billing_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    legal_name = Column(String(255), nullable=False)
    tax_id = Column(String(100), nullable=True)
    billing_email = Column(String(255), nullable=False)
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(50), nullable=True)
    country = Column(String(100), nullable=False, default="US")
    default_currency = Column(String(10), nullable=False, default="USD")
    payment_terms = Column(String(50), nullable=False, default="net_30")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class CurrencyModel(Base):
    """Supported transaction and settlement currencies."""
    __tablename__ = "currencies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(10), nullable=False, unique=True, index=True)  # USD, EUR, GBP, etc.
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=False, default="$")
    decimal_places = Column(Integer, nullable=False, default=2)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class TaxProfileModel(Base):
    """Jurisdiction and regional tax calculation rules."""
    __tablename__ = "tax_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    tax_type = Column(String(50), nullable=False, default="sales_tax")  # vat, gst, sales_tax, custom
    rate_pct = Column(Numeric(18, 2), nullable=False, default=0.00)
    country = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    is_compound = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvoiceModel(Base):
    """Core invoice entity managing billing records, balances, terms, and states."""
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    billing_profile_id = Column(String(36), ForeignKey("billing_profiles.id", ondelete="SET NULL"), nullable=True)
    project_id = Column(String(36), nullable=True, index=True)
    contract_id = Column(String(36), nullable=True, index=True)
    proposal_id = Column(String(36), nullable=True, index=True)
    invoice_number = Column(String(100), nullable=False, index=True)
    version = Column(Integer, default=1, nullable=False)
    status = Column(String(50), nullable=False, default="draft", index=True)
    currency = Column(String(10), nullable=False, default="USD")
    payment_terms = Column(String(50), nullable=False, default="net_30")
    custom_terms_days = Column(Integer, nullable=True)
    issue_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    
    # Pure Numeric monetary totals
    subtotal = Column(Numeric(18, 2), nullable=False, default=0.00)
    discount_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    taxable_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    tax_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    amount_paid = Column(Numeric(18, 2), nullable=False, default=0.00)
    balance_due = Column(Numeric(18, 2), nullable=False, default=0.00)

    tax_rate_pct = Column(Numeric(18, 2), nullable=False, default=0.00)
    tax_type = Column(String(50), nullable=False, default="none")
    tax_region = Column(String(100), nullable=True)
    discount_rate_pct = Column(Numeric(18, 2), nullable=False, default=0.00)
    fixed_discount_amount = Column(Numeric(18, 2), nullable=False, default=0.00)

    notes = Column(Text, nullable=True)
    terms_and_conditions = Column(Text, nullable=True)
    created_by_user_id = Column(String(36), nullable=True)
    issued_by_user_id = Column(String(36), nullable=True)
    approved_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class InvoiceVersionModel(Base):
    """Historical immutable snapshots of invoice revisions."""
    __tablename__ = "invoice_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    invoice_data_snapshot = Column(JSON_TYPE, nullable=False)
    changed_by_user_id = Column(String(36), nullable=True)
    change_reason = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvoiceItemModel(Base):
    """Granular line items associated with an invoice."""
    __tablename__ = "invoice_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Numeric(18, 2), nullable=False, default=1.00)
    unit_price = Column(Numeric(18, 2), nullable=False, default=0.00)
    subtotal = Column(Numeric(18, 2), nullable=False, default=0.00)
    discount_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    taxable_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    tax_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    total_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    item_type = Column(String(50), nullable=False, default="fixed")  # milestone, time_material, recurring, expense, custom
    reference_type = Column(String(50), nullable=True)  # contract_milestone, change_request, deliverable, task
    reference_id = Column(String(36), nullable=True)
    contract_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class InvoiceApprovalModel(Base):
    """Formal audit trail of invoice human reviews and approvals."""
    __tablename__ = "invoice_approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id = Column(String(36), nullable=False, index=True)
    approver_user_id = Column(String(36), nullable=False)
    status = Column(String(50), nullable=False)  # approved, rejected
    comments = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BillingScheduleModel(Base):
    """Contractual recurring or milestone-based billing plan."""
    __tablename__ = "billing_schedules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    project_id = Column(String(36), nullable=True, index=True)
    contract_id = Column(String(36), nullable=True, index=True)
    schedule_type = Column(String(50), nullable=False, default="milestone")  # milestone, recurring, retainer
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BillingScheduleItemModel(Base):
    """Individual scheduled billing event in a schedule."""
    __tablename__ = "billing_schedule_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(String(36), ForeignKey("billing_schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    milestone_id = Column(String(36), nullable=True)
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    target_billing_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # pending, invoiced, skipped
    invoice_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SubscriptionModel(Base):
    """Client recurring retainer and SaaS subscriptions."""
    __tablename__ = "subscriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    plan_name = Column(String(255), nullable=False)
    billing_interval = Column(String(50), nullable=False, default="monthly")  # monthly, quarterly, annual
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(50), nullable=False, default="active")  # active, past_due, canceled, paused
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class PaymentModel(Base):
    """Recorded payment transactions."""
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    provider_type = Column(String(50), nullable=False, default="mock")  # stripe, razorpay, mock, manual
    provider_payment_id = Column(String(255), nullable=True, index=True)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(50), nullable=False, default="succeeded", index=True)  # pending, succeeded, failed, refunded
    payment_method = Column(String(50), nullable=False, default="credit_card")  # credit_card, bank_transfer, wire, ach
    fee_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    error_code = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    raw_response = Column(JSON_TYPE, nullable=True)
    idempotency_key = Column(String(255), nullable=True, index=True)
    created_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PaymentProviderEventModel(Base):
    """Webhook and raw transaction events from external payment providers."""
    __tablename__ = "payment_provider_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    provider_type = Column(String(50), nullable=False)
    event_type = Column(String(100), nullable=False)
    provider_event_id = Column(String(255), nullable=False, index=True)
    payload = Column(JSON_TYPE, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PaymentReconciliationModel(Base):
    """Reconciliation matches between provider events and system invoices/payments."""
    __tablename__ = "payment_reconciliations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    payment_id = Column(String(36), ForeignKey("payments.id", ondelete="SET NULL"), nullable=True)
    provider_event_id = Column(String(36), nullable=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), nullable=False, default="matched")  # matched, partial_match, unmatched, mismatch, overpaid
    matched_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    discrepancy_amount = Column(Numeric(18, 2), nullable=False, default=0.00)
    discrepancy_type = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    resolved_by_user_id = Column(String(36), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RefundModel(Base):
    """Refunds issued on payments."""
    __tablename__ = "refunds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    payment_id = Column(String(36), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False, index=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    provider_refund_id = Column(String(255), nullable=True)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    status = Column(String(50), nullable=False, default="succeeded")
    reason = Column(Text, nullable=True)
    error_code = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    created_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CreditNoteModel(Base):
    """Credit notes issued against invoices or for account balance credit."""
    __tablename__ = "credit_notes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_id = Column(String(36), nullable=False, index=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    credit_note_number = Column(String(100), nullable=False, index=True)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    balance = Column(Numeric(18, 2), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="issued")  # draft, issued, applied, void
    created_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FinancialAccountModel(Base):
    """Chart of accounts for internal double-entry ledger."""
    __tablename__ = "financial_accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    account_code = Column(String(50), nullable=False)  # 1000, 1200, 4000, 5000, etc.
    account_name = Column(String(255), nullable=False)
    account_type = Column(String(50), nullable=False)  # asset, liability, equity, revenue, expense, accounts_receivable, cash, tax_payable
    currency = Column(String(10), nullable=False, default="USD")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LedgerEntryModel(Base):
    """Append-only, immutable double-entry journal postings."""
    __tablename__ = "ledger_entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    entry_group_id = Column(String(36), nullable=False, index=True)
    account_id = Column(String(36), ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    account_type = Column(String(50), nullable=True)
    direction = Column(String(20), nullable=False)  # debit, credit
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    reference_type = Column(String(50), nullable=True)  # invoice, payment, refund, credit_note, adjustment
    reference_id = Column(String(36), nullable=True)
    description = Column(String(500), nullable=True)
    is_reversed = Column(Boolean, default=False, nullable=False)
    reversing_entry_id = Column(String(36), nullable=True)
    created_by_user_id = Column(String(36), nullable=True)
    posted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FinancialAdjustmentModel(Base):
    """Non-destructive adjustment records documenting revisions to ledger entries."""
    __tablename__ = "financial_adjustments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    entry_group_id = Column(String(36), nullable=False)
    original_entry_group_id = Column(String(36), nullable=False)
    reason = Column(Text, nullable=False)
    approved_by_user_id = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ProjectCostModel(Base):
    """Direct and indirect cost rollup for projects."""
    __tablename__ = "project_costs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    project_id = Column(String(36), nullable=False, index=True)
    labor_cost = Column(Numeric(18, 2), nullable=False, default=0.00)
    ai_token_cost = Column(Numeric(18, 2), nullable=False, default=0.00)
    infrastructure_cost = Column(Numeric(18, 2), nullable=False, default=0.00)
    subcontractor_cost = Column(Numeric(18, 2), nullable=False, default=0.00)
    other_expenses = Column(Numeric(18, 2), nullable=False, default=0.00)
    total_cost = Column(Numeric(18, 2), nullable=False, default=0.00)
    currency = Column(String(10), nullable=False, default="USD")
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExpenseModel(Base):
    """Individual pass-through, direct, or project operational expenses."""
    __tablename__ = "expenses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    project_id = Column(String(36), nullable=True, index=True)
    category = Column(String(100), nullable=False)  # hosting, software_license, contractor, travel, hardware
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    vendor = Column(String(255), nullable=True)
    receipt_file_id = Column(String(36), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="pending")  # pending, approved, rejected, reimbursed, invoiced
    approved_by_user_id = Column(String(36), nullable=True)
    incurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
