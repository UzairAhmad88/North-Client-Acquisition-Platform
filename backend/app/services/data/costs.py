"""
Phase 65: Data Cost Management (FinOps) Service
Tracks storage, compute, queries, pipelines, streaming, AI retrieval, and embeddings cost.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataCostModel, DataBudgetModel


class DataCostService:
    def __init__(self, db: Session):
        self.db = db

    def record_cost(
        self,
        tenant_id: str,
        asset_id: str,
        cost_category: str,  # STORAGE, COMPUTE, QUERY, PIPELINE, EMBEDDINGS
        cost_amount: float,
        billing_period: str,
        currency: str = "USD"
    ) -> DataCostModel:
        cost = DataCostModel(
            tenant_id=tenant_id,
            asset_id=asset_id,
            cost_category=cost_category,
            cost_amount=cost_amount,
            billing_period=billing_period,
            currency=currency,
            recorded_at=datetime.now(timezone.utc)
        )
        self.db.add(cost)
        self.db.commit()
        self.db.refresh(cost)
        return cost

    def set_budget(
        self,
        tenant_id: str,
        scope: str,
        monthly_budget_amount: float,
        currency: str = "USD"
    ) -> DataBudgetModel:
        budget = self.db.query(DataBudgetModel).filter(
            DataBudgetModel.tenant_id == tenant_id,
            DataBudgetModel.scope == scope
        ).first()

        if not budget:
            budget = DataBudgetModel(
                tenant_id=tenant_id,
                scope=scope,
                monthly_budget_amount=monthly_budget_amount,
                currency=currency,
                created_at=datetime.now(timezone.utc)
            )
            self.db.add(budget)
        else:
            budget.monthly_budget_amount = monthly_budget_amount

        self.db.commit()
        self.db.refresh(budget)
        return budget

    def get_cost_summary(self, tenant_id: str, billing_period: str) -> Dict[str, Any]:
        costs = self.db.query(DataCostModel).filter(
            DataCostModel.tenant_id == tenant_id,
            DataCostModel.billing_period == billing_period
        ).all()

        category_totals: Dict[str, float] = {}
        total = 0.0
        for c in costs:
            category_totals[c.cost_category] = category_totals.get(c.cost_category, 0.0) + c.cost_amount
            total += c.cost_amount

        return {
            "tenant_id": tenant_id,
            "billing_period": billing_period,
            "total_cost_usd": round(total, 2),
            "breakdown": {k: round(v, 2) for k, v in category_totals.items()}
        }
