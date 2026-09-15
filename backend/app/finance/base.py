"""Base domain models, enums, and dataclasses for Phase 40 Financial Operations."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InvoiceStatus(str, Enum):
    """Lifecycle status of an invoice."""
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ISSUED = "ISSUED"
    SENT = "SENT"
    VIEWED = "VIEWED"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    VOID = "VOID"
    CANCELLED = "CANCELLED"
    DISPUTED = "DISPUTED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    REFUNDED = "REFUNDED"
    WRITTEN_OFF = "WRITTEN_OFF"


class PaymentStatus(str, Enum):
    """Lifecycle status of a payment transaction."""
    PAYMENT_CREATED = "PAYMENT_CREATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentTerms(str, Enum):
    """Commercial payment terms."""
    DUE_ON_RECEIPT = "DUE_ON_RECEIPT"
    NET_7 = "NET_7"
    NET_14 = "NET_14"
    NET_15 = "NET_15"
    NET_30 = "NET_30"
    NET_45 = "NET_45"
    NET_60 = "NET_60"
    NET_90 = "NET_90"
    CUSTOM = "CUSTOM"


class TaxType(str, Enum):
    """Tax classification types."""
    NONE = "NONE"
    VAT = "VAT"
    SALES_TAX = "SALES_TAX"
    WITHHOLDING = "WITHHOLDING"
    SERVICE_TAX = "SERVICE_TAX"
    OTHER = "OTHER"


class LedgerDirection(str, Enum):
    """Accounting entry direction."""
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class FinancialAccountType(str, Enum):
    """Canonical platform financial accounts."""
    CASH = "CASH"
    ACCOUNTS_RECEIVABLE = "ACCOUNTS_RECEIVABLE"
    REVENUE = "REVENUE"
    REFUNDS = "REFUNDS"
    DISCOUNTS = "DISCOUNTS"
    TAX_PAYABLE = "TAX_PAYABLE"
    OPERATING_EXPENSES = "OPERATING_EXPENSES"
    PROJECT_COSTS = "PROJECT_COSTS"
    PAYMENT_FEES = "PAYMENT_FEES"
    EXPENSE = "EXPENSE"


class SubscriptionStatus(str, Enum):
    """Recurring subscription status."""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class FinancialExceptionType(str, Enum):
    """Financial inconsistency and risk exception types."""
    OVER_BILLING = "OVER_BILLING"
    UNDER_BILLING = "UNDER_BILLING"
    DUPLICATE_INVOICE = "DUPLICATE_INVOICE"
    DUPLICATE_PAYMENT = "DUPLICATE_PAYMENT"
    MISSING_PAYMENT = "MISSING_PAYMENT"
    CONTRACT_MISMATCH = "CONTRACT_MISMATCH"
    CURRENCY_MISMATCH = "CURRENCY_MISMATCH"
    TAX_MISMATCH = "TAX_MISMATCH"
    REFUND_MISMATCH = "REFUND_MISMATCH"
    RECONCILIATION_FAILURE = "RECONCILIATION_FAILURE"
    UNAUTHORIZED_ADJUSTMENT = "UNAUTHORIZED_ADJUSTMENT"


class LineItemCalculation(BaseModel):
    """Line item computed figures with explicit Decimal arithmetic."""
    title: str = ""
    description: Optional[str] = None
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal
    discount_amount: Decimal = Decimal("0.00")
    taxable_amount: Decimal = Decimal("0.00")
    tax_rate: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")
    total: Decimal = Decimal("0.00")
    item_type: str = "fixed"
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    contract_id: Optional[str] = None
    source_type: Optional[str] = None
    source_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title or self.description or "Item",
            "description": self.description,
            "quantity": str(self.quantity),
            "unit_price": str(self.unit_price),
            "subtotal": str(self.subtotal),
            "discount_amount": str(self.discount_amount),
            "taxable_amount": str(self.taxable_amount),
            "tax_amount": str(self.tax_amount),
            "total_amount": str(self.total_amount or self.total),
            "item_type": self.item_type,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "contract_id": self.contract_id,
        }


class InvoiceTotals(BaseModel):
    """Invoice aggregate calculations."""
    subtotal: Decimal
    discount_amount: Decimal = Decimal("0.00")
    taxable_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    total_amount: Decimal = Decimal("0.00")
    amount_paid: Decimal = Decimal("0.00")
    balance_due: Decimal = Decimal("0.00")
    total_discount: Decimal = Decimal("0.00")
    total_tax: Decimal = Decimal("0.00")
    amount_due: Decimal = Decimal("0.00")
    currency: str = "USD"
    items: List[LineItemCalculation] = []
