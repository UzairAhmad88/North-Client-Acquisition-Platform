"""Payment Provider Abstraction Layer."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    """Payment initiation request payload."""
    tenant_id: str
    amount: Decimal
    currency: str = "USD"
    payment_method: str = "credit_card"
    invoice_id: Optional[str] = None
    client_id: Optional[str] = None
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    description: Optional[str] = None
    idempotency_key: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PaymentResult(BaseModel):
    """Standardized response from payment provider."""
    provider_transaction_id: str = ""
    provider_payment_id: Optional[str] = None
    provider_name: str = "MockPaymentProvider"
    status: str = "SUCCEEDED"  # SUCCEEDED, PENDING, FAILED, CANCELLED, REFUNDED
    amount: Decimal = Decimal("0.00")
    currency: str = "USD"
    invoice_id: Optional[str] = None
    fee_amount: Decimal = Decimal("0.00")
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Dict[str, Any] = Field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status.upper() in ("SUCCEEDED", "SUCCESS")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_transaction_id": self.provider_transaction_id or self.provider_payment_id,
            "provider_payment_id": self.provider_payment_id or self.provider_transaction_id,
            "provider_name": self.provider_name,
            "status": self.status,
            "amount": str(self.amount),
            "currency": self.currency,
            "invoice_id": self.invoice_id,
            "fee_amount": str(self.fee_amount),
            "error_code": self.error_code,
            "error_message": self.error_message,
            "raw_response": self.raw_response,
            "is_success": self.is_success,
        }


class RefundRequest(BaseModel):
    """Refund request payload."""
    tenant_id: str
    amount: Decimal
    currency: str = "USD"
    payment_id: Optional[str] = None
    provider_transaction_id: Optional[str] = None
    reason: str = "Customer requested refund"
    idempotency_key: str = ""


class RefundResult(BaseModel):
    """Standardized refund response."""
    provider_refund_id: str = ""
    provider_name: str = "MockPaymentProvider"
    status: str = "SUCCEEDED"  # SUCCEEDED, PENDING, FAILED
    amount: Decimal = Decimal("0.00")
    currency: str = "USD"
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Dict[str, Any] = Field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status.upper() in ("SUCCEEDED", "SUCCESS")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_refund_id": self.provider_refund_id,
            "provider_name": self.provider_name,
            "status": self.status,
            "amount": str(self.amount),
            "currency": self.currency,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "raw_response": self.raw_response,
            "is_success": self.is_success,
        }


class BasePaymentProvider(ABC):
    """Abstract interface for payment gateway providers."""

    @abstractmethod
    def create_payment(self, request: PaymentRequest) -> PaymentResult:
        """Initiate and process a payment."""
        pass

    def charge(self, request: PaymentRequest) -> PaymentResult:
        """Alias for create_payment."""
        return self.create_payment(request)

    @abstractmethod
    def get_payment_status(self, provider_transaction_id: str) -> PaymentResult:
        """Fetch current payment status from provider."""
        pass

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature_header: str) -> bool:
        """Verify webhook authenticity."""
        pass

    @abstractmethod
    def refund_payment(self, request: RefundRequest) -> RefundResult:
        """Issue a refund."""
        pass

    def refund(self, request: RefundRequest) -> RefundResult:
        """Alias for refund_payment."""
        return self.refund_payment(request)
