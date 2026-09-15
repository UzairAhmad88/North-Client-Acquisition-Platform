"""Authoritative Cost Engine for internal labor and external provider operating expenses."""

import os
from typing import Dict, List, Tuple
from agents.estimation.models import EstimateCostItemSchema, EstimateWorkItemSchema


class CostEngine:
    """Calculates internal labor and external operating costs from authoritative configurations."""

    # Server-configured authoritative internal hourly labor rate (defaults to 45.0 USD)
    DEFAULT_INTERNAL_HOURLY_RATE = float(os.getenv("ESTIMATION_INTERNAL_HOURLY_RATE", "45.0"))

    @classmethod
    def calculate_internal_labor_cost(
        cls, total_hours: float, hourly_rate: float = DEFAULT_INTERNAL_HOURLY_RATE
    ) -> float:
        return round(total_hours * hourly_rate, 2)

    @classmethod
    def extract_external_costs(
        cls, work_items: List[EstimateWorkItemSchema]
    ) -> List[EstimateCostItemSchema]:
        costs: List[EstimateCostItemSchema] = []
        categories = {w.category.upper() for w in work_items}

        if "INTEGRATION" in categories or any("PAYMENT" in w.name.upper() for w in work_items):
            costs.append(
                EstimateCostItemSchema(
                    cost_type="PROVIDER",
                    description="Payment Gateway & Transaction Fees (Stripe API)",
                    amount=50.0,
                    currency="USD",
                    source="CONFIGURED_BASELINE",
                )
            )

        if "AI" in categories:
            costs.append(
                EstimateCostItemSchema(
                    cost_type="INFRASTRUCTURE",
                    description="AI Model Provider Token Operating Budget (OpenAI/Anthropic)",
                    amount=75.0,
                    currency="USD",
                    source="CONFIGURED_BASELINE",
                )
            )

        # Base Cloud Hosting & Domain Fee
        costs.append(
            EstimateCostItemSchema(
                cost_type="INFRASTRUCTURE",
                description="Cloud Hosting & SSL Certificate (Vercel / AWS App Runner)",
                amount=35.0,
                currency="USD",
                source="CONFIGURED_BASELINE",
            )
        )

        return costs
