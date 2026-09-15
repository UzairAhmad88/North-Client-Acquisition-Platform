"""Payment service factory and coordinator."""

import os
from typing import Optional
from integrations.payments.base import (
    BasePaymentProvider,
    PaymentRequest,
    PaymentResult,
    RefundRequest,
    RefundResult,
)
from integrations.payments.models import PaymentProviderType
from integrations.payments.providers.mock import MockPaymentProvider


class PaymentService:
    """Central gateway for payment providers."""

    _instance: Optional["PaymentService"] = None

    def __init__(
        self,
        provider: Optional[BasePaymentProvider] = None,
        default_provider: PaymentProviderType = PaymentProviderType.MOCK,
    ) -> None:
        self.default_provider = default_provider
        self._provider = provider or MockPaymentProvider()

    @property
    def provider(self) -> BasePaymentProvider:
        return self._provider

    def charge(self, request: PaymentRequest, provider_type: Optional[PaymentProviderType] = None) -> PaymentResult:
        return self._provider.create_payment(request)

    def refund(self, request: RefundRequest, provider_type: Optional[PaymentProviderType] = None) -> RefundResult:
        return self._provider.refund_payment(request)

    @classmethod
    def get_instance(cls) -> "PaymentService":
        if cls._instance is None:
            cls._instance = PaymentService()
        return cls._instance

    @classmethod
    def set_instance(cls, instance: "PaymentService") -> None:
        cls._instance = instance
