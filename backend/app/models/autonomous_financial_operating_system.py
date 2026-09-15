"""
Phase 72: Autonomous Financial Infrastructure, Treasury, Payments, Capital Intelligence
& Enterprise Financial Operating System Models.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
try:
    from app.models.base import Base
except ImportError:
    from backend.app.models.base import Base


# 1. Multi-Entity & Master Data
class FinEntityModel(Base):
    """Legal entities, operating subsidiaries, and holding corporations."""
    __tablename__ = "fin_entities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_code = Column(String(64), nullable=False, unique=True, index=True)
    legal_name = Column(String(128), nullable=False)
    jurisdiction = Column(String(32), nullable=False, default="US-DE")
    functional_currency = Column(String(8), nullable=False, default="USD")
    parent_entity_id = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinAccountModel(Base):
    """Hierarchical Chart of Accounts (Assets, Liabilities, Equity, Revenue, COGS, OpEx)."""
    __tablename__ = "fin_accounts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    account_number = Column(String(32), nullable=False, unique=True, index=True)
    account_name = Column(String(128), nullable=False)
    account_type = Column(String(32), nullable=False)  # ASSET, LIABILITY, EQUITY, REVENUE, COGS, EXPENSE
    sub_category = Column(String(64), nullable=False, default="CURRENT")
    currency = Column(String(8), nullable=False, default="USD")
    current_balance = Column(Float, nullable=False, default=0.0)
    is_reconcilable = Column(Boolean, nullable=False, default=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinCustomerModel(Base):
    """Enterprise commercial customers with credit limits, payment terms, and exposure."""
    __tablename__ = "fin_customers"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    customer_code = Column(String(64), nullable=False, unique=True, index=True)
    company_name = Column(String(128), nullable=False)
    credit_limit_usd = Column(Float, nullable=False, default=250000.0)
    current_ar_balance = Column(Float, nullable=False, default=0.0)
    payment_terms_days = Column(Integer, nullable=False, default=30)
    risk_score = Column(Float, nullable=False, default=12.0)  # 0 to 100
    credit_hold = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinVendorModel(Base):
    """Approved trade vendors and service providers with verified banking destinations."""
    __tablename__ = "fin_vendors"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    vendor_code = Column(String(64), nullable=False, unique=True, index=True)
    company_name = Column(String(128), nullable=False)
    payment_terms_days = Column(Integer, nullable=False, default=30)
    bank_routing_token = Column(String(128), nullable=False)  # Tokenized
    bank_account_token = Column(String(128), nullable=False)  # Tokenized
    beneficiary_verified = Column(Boolean, nullable=False, default=True)
    compliance_status = Column(String(32), nullable=False, default="COMPLIANT")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinBankAccountModel(Base):
    """Treasury bank accounts with balance monitoring and ingestion synchronization."""
    __tablename__ = "fin_bank_accounts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    account_code = Column(String(64), nullable=False, unique=True, index=True)
    bank_name = Column(String(64), nullable=False)
    account_mask = Column(String(16), nullable=False)  # e.g. "••••4892"
    currency = Column(String(8), nullable=False, default="USD")
    ledger_balance = Column(Float, nullable=False, default=0.0)
    available_balance = Column(Float, nullable=False, default=0.0)
    last_synced_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 2. Accounts Receivable, Billing & Invoicing
class FinInvoiceModel(Base):
    """Accounts receivable customer invoices with revenue recognition triggers."""
    __tablename__ = "fin_invoices"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    invoice_number = Column(String(64), nullable=False, unique=True, index=True)
    customer_id = Column(String(64), nullable=False, index=True)
    entity_id = Column(String(64), nullable=False, default="ent_us_primary")
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    paid_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="ISSUED")  # DRAFT, ISSUED, PAID, OVERDUE, VOID
    issue_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinInvoiceItemModel(Base):
    """Line items for customer invoices."""
    __tablename__ = "fin_invoice_items"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    invoice_id = Column(String(64), nullable=False, index=True)
    sku = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit_price = Column(Float, nullable=False, default=0.0)
    amount = Column(Float, nullable=False, default=0.0)
    account_number = Column(String(32), nullable=False, default="4000")  # Revenue
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 3. Accounts Payable, Bills & 3-Way Matching
class FinVendorBillModel(Base):
    """Accounts payable vendor invoices with 3-way matching against PO and Goods Receipt."""
    __tablename__ = "fin_bills"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    bill_number = Column(String(64), nullable=False, unique=True, index=True)
    vendor_id = Column(String(64), nullable=False, index=True)
    purchase_order_id = Column(String(64), nullable=True)
    goods_receipt_id = Column(String(64), nullable=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    three_way_match_status = Column(String(32), nullable=False, default="MATCHED")  # MATCHED, DISCREPANCY, UNMATCHED
    status = Column(String(32), nullable=False, default="PENDING_APPROVAL")  # PENDING_APPROVAL, APPROVED, PAID
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 4. Payments, Controls & Approvals
class FinPaymentModel(Base):
    """Payment transactions with state machine, idempotency keys, and risk evaluation."""
    __tablename__ = "fin_payments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    payment_reference = Column(String(64), nullable=False, unique=True, index=True)
    idempotency_key = Column(String(128), nullable=False, unique=True, index=True)
    payment_type = Column(String(32), nullable=False, default="VENDOR_DISBURSEMENT")  # VENDOR_DISBURSEMENT, CUSTOMER_RECEIPT, PAYROLL, TRANSFER
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    source_bank_account_id = Column(String(64), nullable=False)
    destination_entity_or_vendor = Column(String(128), nullable=False)
    status = Column(String(32), nullable=False, default="DRAFT")  # DRAFT, VALIDATED, PENDING_APPROVAL, APPROVED, PROCESSING, COMPLETED, REJECTED
    fraud_risk_score = Column(Float, nullable=False, default=2.1)
    requires_dual_approval = Column(Boolean, nullable=False, default=False)
    authorized_by_user_id = Column(String(64), nullable=True)
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinPaymentApprovalModel(Base):
    """Dual-control authorization audit records for high-value financial commitments."""
    __tablename__ = "fin_payment_approvals"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    payment_id = Column(String(64), nullable=False, index=True)
    approver_user_id = Column(String(64), nullable=False)
    approval_tier = Column(String(32), nullable=False, default="TREASURY_DIRECTOR")
    decision = Column(String(16), nullable=False, default="APPROVED")
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 5. Bank Transactions & Reconciliation
class FinBankTransactionModel(Base):
    """Ingested and normalized financial statements from corporate banking feeds."""
    __tablename__ = "fin_bank_transactions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    bank_account_id = Column(String(64), nullable=False, index=True)
    fit_id = Column(String(128), nullable=False, unique=True, index=True)  # Financial Institution Transaction ID
    transaction_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(8), nullable=False, default="USD")
    description = Column(String(256), nullable=False)
    counterparty = Column(String(128), nullable=False)
    reconciliation_status = Column(String(32), nullable=False, default="UNMATCHED")  # UNMATCHED, MATCHED, EXCEPTION
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinReconciliationModel(Base):
    """Automated and human-confirmed reconciliation pairings between bank feed and ledger."""
    __tablename__ = "fin_reconciliation"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    bank_transaction_id = Column(String(64), nullable=False, index=True)
    journal_entry_id = Column(String(64), nullable=False, index=True)
    match_confidence = Column(Float, nullable=False, default=1.0)  # 0.0 to 1.0
    match_type = Column(String(32), nullable=False, default="EXACT_AMOUNT_REFERENCE")
    reconciled_by = Column(String(64), nullable=False, default="sc_reconciliation_agent")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 6. Double-Entry General Ledger, Journals & Accounting Periods
class FinJournalEntryModel(Base):
    """Double-entry General Ledger journal entries (Debit = Credit invariant)."""
    __tablename__ = "fin_journals"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    journal_code = Column(String(64), nullable=False, unique=True, index=True)
    entity_id = Column(String(64), nullable=False, default="ent_us_primary")
    period_code = Column(String(32), nullable=False, index=True)  # e.g. "2026-09"
    entry_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    description = Column(String(256), nullable=False)
    source_module = Column(String(32), nullable=False, default="AR")  # AR, AP, PAYMENTS, REVENUE, ASSETS, PAYROLL
    source_reference_id = Column(String(64), nullable=True)
    total_debit = Column(Float, nullable=False, default=0.0)
    total_credit = Column(Float, nullable=False, default=0.0)
    posting_status = Column(String(32), nullable=False, default="POSTED")  # DRAFT, POSTED, REVERSED
    is_balanced = Column(Boolean, nullable=False, default=True)
    posted_by = Column(String(64), nullable=False, default="sc_accounting_agent")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinJournalLineModel(Base):
    """Individual debit and credit lines belonging to a balanced journal entry."""
    __tablename__ = "fin_journal_lines"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    journal_id = Column(String(64), nullable=False, index=True)
    account_number = Column(String(32), nullable=False, index=True)
    debit_amount = Column(Float, nullable=False, default=0.0)
    credit_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    memo = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinAccountingPeriodModel(Base):
    """Fiscal and accounting periods with status locks preventing unauthorized postings."""
    __tablename__ = "fin_accounting_periods"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    period_code = Column(String(32), nullable=False, unique=True, index=True)  # e.g. "2026-09"
    fiscal_year = Column(Integer, nullable=False, default=2026)
    period_number = Column(Integer, nullable=False, default=9)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, SOFT_CLOSE, CLOSED, LOCKED
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    closed_by = Column(String(64), nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 7. Expenses, Receipts & Fixed Assets
class FinExpenseModel(Base):
    """Employee and operational expense claims with policy checking and OCR categorization."""
    __tablename__ = "fin_expenses"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    expense_code = Column(String(64), nullable=False, unique=True, index=True)
    employee_id = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False, default="TRAVEL")
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    merchant_name = Column(String(128), nullable=False)
    receipt_url = Column(String(256), nullable=True)
    ocr_confidence = Column(Float, nullable=False, default=0.98)
    status = Column(String(32), nullable=False, default="APPROVED")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinFixedAssetModel(Base):
    """Capitalized physical and intangible assets with straight-line depreciation schedules."""
    __tablename__ = "fin_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    asset_tag = Column(String(64), nullable=False, unique=True, index=True)
    asset_name = Column(String(128), nullable=False)
    acquisition_date = Column(DateTime, nullable=False)
    acquisition_cost = Column(Float, nullable=False, default=0.0)
    useful_life_months = Column(Integer, nullable=False, default=36)
    depreciation_method = Column(String(32), nullable=False, default="STRAIGHT_LINE")
    accumulated_depreciation = Column(Float, nullable=False, default=0.0)
    current_book_value = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 8. FP&A, Budgets & Cash Forecasting
class FinBudgetModel(Base):
    """Departmental, initiative, and capital budgets with variance tracking."""
    __tablename__ = "fin_budgets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    budget_code = Column(String(64), nullable=False, unique=True, index=True)
    department = Column(String(64), nullable=False)  # ENGINEERING, MARKETING, OPERATIONS, G&A
    fiscal_year = Column(Integer, nullable=False, default=2026)
    allocated_amount = Column(Float, nullable=False, default=0.0)
    actual_spent_amount = Column(Float, nullable=False, default=0.0)
    committed_amount = Column(Float, nullable=False, default=0.0)
    variance_amount = Column(Float, nullable=False, default=0.0)
    variance_pct = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinCashForecastModel(Base):
    """Multi-horizon probabilistic cash forecast (Opening + Inflows - Outflows = Net Liquidity)."""
    __tablename__ = "fin_cash_forecasts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    forecast_period = Column(String(32), nullable=False, index=True)  # 30_DAYS, 90_DAYS, 12_MONTHS
    opening_cash = Column(Float, nullable=False, default=0.0)
    projected_inflows = Column(Float, nullable=False, default=0.0)
    projected_outflows = Column(Float, nullable=False, default=0.0)
    projected_closing_cash = Column(Float, nullable=False, default=0.0)
    net_monthly_burn_rate = Column(Float, nullable=False, default=0.0)
    estimated_runway_months = Column(Float, nullable=False, default=24.0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinTreasuryPositionModel(Base):
    """Consolidated corporate treasury liquidity, debt covenants, and FX exposures."""
    __tablename__ = "fin_treasury_positions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    total_cash_usd = Column(Float, nullable=False, default=0.0)
    restricted_cash_usd = Column(Float, nullable=False, default=0.0)
    total_debt_principal = Column(Float, nullable=False, default=0.0)
    annual_debt_service = Column(Float, nullable=False, default=0.0)
    net_liquidity_usd = Column(Float, nullable=False, default=0.0)
    eur_exposure_usd = Column(Float, nullable=False, default=0.0)
    jpy_exposure_usd = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 9. Fraud Detection & Risk Intelligence
class FinFraudAlertModel(Base):
    """Financial anomaly detections (amount anomalies, duplicate payments, beneficiary changes)."""
    __tablename__ = "fin_fraud_alerts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    alert_code = Column(String(64), nullable=False, unique=True, index=True)
    fraud_category = Column(String(64), nullable=False)  # BENEFICIARY_CHANGE, VELOCITY_ANOMALY, DUPLICATE_PAYMENT, UNUSUAL_AMOUNT
    severity = Column(String(16), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    entity_reference = Column(String(128), nullable=False)
    anomaly_score = Column(Float, nullable=False, default=0.85)  # 0.0 to 1.0
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, INVESTIGATING, RESOLVED, DISMISSED
    mitigation_action = Column(String(256), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 10. Financial Digital Twin & Agent Run Records
class FinDigitalTwinModel(Base):
    """Simulated financial digital twin model state."""
    __tablename__ = "fin_digital_twins"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    twin_code = Column(String(64), nullable=False, unique=True, index=True)
    revenue_growth_rate_pct = Column(Float, nullable=False, default=24.5)
    gross_margin_pct = Column(Float, nullable=False, default=68.2)
    working_capital_usd = Column(Float, nullable=False, default=4200000.0)
    dso_days = Column(Float, nullable=False, default=38.4)
    dpo_days = Column(Float, nullable=False, default=44.1)
    resilience_rating = Column(String(16), nullable=False, default="HIGH")
    last_synced_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class FinAgentRunModel(Base):
    """Autonomous financial agent action records and cryptographic audit entries."""
    __tablename__ = "fin_agent_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_name = Column(String(64), nullable=False, index=True)
    action_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="COMPLETED")
    dry_run = Column(Boolean, nullable=False, default=True)
    execution_result = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# Convenience Aliases
FinEntity = FinEntityModel
FinAccount = FinAccountModel
FinCustomer = FinCustomerModel
FinVendor = FinVendorModel
FinBankAccount = FinBankAccountModel
FinInvoice = FinInvoiceModel
FinInvoiceItem = FinInvoiceItemModel
FinVendorBill = FinVendorBillModel
FinPayment = FinPaymentModel
FinPaymentApproval = FinPaymentApprovalModel
FinBankTransaction = FinBankTransactionModel
FinReconciliation = FinReconciliationModel
FinJournalEntry = FinJournalEntryModel
FinJournalLine = FinJournalLineModel
FinAccountingPeriod = FinAccountingPeriodModel
FinExpense = FinExpenseModel
FinFixedAsset = FinFixedAssetModel
FinBudget = FinBudgetModel
FinCashForecast = FinCashForecastModel
FinTreasuryPosition = FinTreasuryPositionModel
FinFraudAlert = FinFraudAlertModel
FinDigitalTwin = FinDigitalTwinModel
FinAgentRun = FinAgentRunModel
