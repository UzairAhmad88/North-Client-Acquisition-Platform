"""Payment integration models."""

from enum import Enum


class PaymentProviderType(str, Enum):
    """Supported payment provider types."""
    MOCK = "MOCK"
    STRIPE = "STRIPE"
    PAYFAST = "PAYFAST"
    BANK_TRANSFER = "BANK_TRANSFER"
