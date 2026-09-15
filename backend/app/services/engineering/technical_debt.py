"""Technical Debt & Refactoring Engine Service."""
from typing import Dict, Any, List, Optional

class TechnicalDebtEngineService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_findings(self, project_id: str, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [
            {"id": "td_1", "title": "Duplicated ORM query logic", "priority": "LOW", "effort_days": 0.5},
            {"id": "td_2", "title": "Upgrade deprecated pydantic v1 methods", "priority": "MEDIUM", "effort_days": 1.0},
        ]
