"""
Phase 88: Global AI Economic Network Services Package.
"""

from app.services.global_ai_economic_network.entities import EconomicNetworkEntityService
from app.services.global_ai_economic_network.catalog import EconomicCatalogService
from app.services.global_ai_economic_network.commerce import EconomicCommerceService
from app.services.global_ai_economic_network.risk_supply_chain import EconomicSupplyChainService
from app.services.global_ai_economic_network.disputes_audit import EconomicDisputeAuditService
from app.services.global_ai_economic_network.copilot import EconomicCopilotService
from app.services.global_ai_economic_network.autonomy import EconomicAutonomyService

__all__ = [
    "EconomicNetworkEntityService",
    "EconomicCatalogService",
    "EconomicCommerceService",
    "EconomicSupplyChainService",
    "EconomicDisputeAuditService",
    "EconomicCopilotService",
    "EconomicAutonomyService",
]
