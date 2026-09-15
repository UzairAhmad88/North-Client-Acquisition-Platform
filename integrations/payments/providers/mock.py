"""Mock payment provider for development and deterministic testing."""

import hashlib
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict
from uuid import uuid4

from integrations.payments.base import (
    BasePaymentProvider,
    PaymentRequest,
    PaymentResult,
    RefundRequest,
    RefundResult,
)


class MockPaymentProvider(BasePaymentProvider):
    """Deterministic in-memory mock payment provider."""

    def __init__(self, force_failure: bool = False) -> None:
        self.force_failure = force_failure
        self._transactions: Dict[str, PaymentResult] = {}
        self._idempotency_map: Dict[str, PaymentResult] = {}

    def create_payment(self, request: PaymentRequest) -> PaymentResult:
        # Check idempotency
        if request.idempotency_key and request.idempotency_key in self._idempotency_map:
            return self._idempotency_map[request.idempotency_key]

        if self.force_failure or request.amount <= Decimal("0.00"):
            tx_id = f"mock_tx_failed_{uuid4().hex[:8]}"
            result = PaymentResult(
                provider_transaction_id=tx_id,
                provider_payment_id=tx_id,
                provider_name="MockPaymentProvider",
                status="FAILED",
                amount=request.amount,
                currency=request.currency,
                invoice_id=request.invoice_id,
                error_message="Simulated mock payment failure",
                raw_response={"mock_error": True},
            )
        else:
            tx_id = f"mock_tx_{uuid4().hex[:12]}"
            # (amount * 0.029) + 0.30 rounded
            fee = (request.amount * Decimal("0.029") + Decimal("0.30")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            result = PaymentResult(
                provider_transaction_id=tx_id,
                provider_payment_id=tx_id,
                provider_name="MockPaymentProvider",
                status="SUCCEEDED",
                amount=request.amount,
                currency=request.currency,
                invoice_id=request.invoice_id,
                fee_amount=fee,
                raw_response={"mock_success": True, "auth_code": "AUTH-12345"},
            )

        self._transactions[result.provider_transaction_id] = result
        if request.idempotency_key:
            self._idempotency_map[request.idempotency_key] = result
        return result

    def get_payment_status(self, provider_transaction_id: str) -> PaymentResult:
        if provider_transaction_id in self._transactions:
            return self._transactions[provider_transaction_id]
        raise ValueError(f"Mock transaction not found: {provider_transaction_id}")

    def verify_webhook_signature(self, payload: bytes, signature_header: str) -> bool:
        expected = hashlib.sha256(b"mock_webhook_secret_" + payload).hexdigest()
        return signature_header == f"sha256={expected}" or signature_header == "valid_mock_signature"

    def refund_payment(self, request: RefundRequest) -> RefundResult:
        if self.force_failure:
            ref_id = f"mock_ref_failed_{uuid4().hex[:8]}"
            return RefundResult(
                provider_refund_id=ref_id,
                provider_name="MockPaymentProvider",
                status="FAILED",
                amount=request.amount,
                currency=request.currency,
                error_message="Simulated mock refund failure",
            )

        ref_id = f"mock_ref_{uuid4().hex[:12]}"
        return RefundResult(
            provider_refund_id=ref_id,
            provider_name="MockPaymentProvider",
            status="SUCCEEDED",
            amount=request.amount,
            currency=request.currency,
            raw_response={"mock_refund_success": True},
        )
