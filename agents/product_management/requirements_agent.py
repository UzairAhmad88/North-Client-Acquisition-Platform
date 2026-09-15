"""
Requirements & Traceability Agent for Phase 56.
Drafts formal PRD requirements, generates acceptance criteria, and enforces requirement traceability.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )
except ImportError:
    from app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )

logger = logging.getLogger(__name__)


class RequirementsAgent(BaseAgent):
    """Manages PRD requirement definitions, acceptance criteria, and traceability verification."""

    agent_id = "requirements_agent"
    name = "Product Requirements & Traceability Agent"
    version = "1.0"
    description = "Drafts structured PRD requirements and analyzes end-to-end traceability graphs to detect orphans."
    permissions = {
        AgentPermission.READ_PRODUCT,
        AgentPermission.CREATE_REQUIREMENT,
    }

    def __init__(self, service: Optional[ProductManagementPlatformService] = None):
        super().__init__()
        self.service = service or global_product_management_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        product_id = context.metadata.get("product_id")
        action = context.metadata.get("action", "audit_traceability")

        if not product_id:
            return {"status": "FAILED", "error": "product_id is required"}

        if action == "create_requirement":
            title = context.metadata.get("title", "New Product Requirement")
            description = context.metadata.get("description", "")
            category = context.metadata.get("category", "functional")
            priority = context.metadata.get("priority", "high")
            acceptance_criteria = context.metadata.get("acceptance_criteria", ["System responds within 200ms."])
            
            req = self.service.requirements_traceability.create_requirement(
                product_id=product_id,
                title=title,
                description=description,
                category=category,
                priority=priority,
                acceptance_criteria=acceptance_criteria,
            )
            return {"status": "SUCCESS", "action": "create_requirement", "requirement": req}

        # Default: audit traceability
        matrix = self.service.requirements_traceability.get_traceability_matrix(product_id=product_id)
        return {
            "status": "SUCCESS",
            "action": "audit_traceability",
            "traceability_matrix": matrix,
            "orphaned_count": len(matrix.get("orphaned_requirements", [])),
            "total_requirements": len(matrix.get("requirements", [])),
        }
