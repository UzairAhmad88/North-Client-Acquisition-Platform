from fastapi import APIRouter

from app.api.v1.agents import router as agents_router
from app.api.v1.audits import router as audits_router
from app.api.v1.auth import router as auth_router
from app.api.v1.businesses import router as businesses_router
from app.api.v1.change import router as change_router
from app.api.v1.client import router as client_router
from app.api.v1.contacts import router as contacts_router
from app.api.v1.contracts import router as contracts_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.estimates import router as estimates_router
from app.api.v1.leads import router as leads_router
from app.api.v1.outreach import router as outreach_router
from app.api.v1.projects import router as projects_router
from app.api.v1.proposals import router as proposals_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.experiments import router as experiments_router
from app.api.v1.insights import router as insights_router
from app.api.v1.predictive import router as predictive_router
from app.api.v1.governance import router as governance_router
from app.api.v1.orchestration import router as orchestration_router
from app.api.v1.security import router as security_router
from app.api.v1.security_ops import router as security_ops_router
from app.api.v1.qa import router as qa_router
from app.api.v1.qualification import router as qualification_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.requirements import router as requirements_router
from app.api.v1.research import router as research_router
from app.api.v1.risk import router as risk_router
from app.api.v1.scoring import router as scoring_router
from app.api.v1.services import router as services_router
from app.api.v1.solutions import router as solutions_router
from app.api.v1.support import router as support_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.data import router as data_router
from app.api.v1.communication import router as communication_router
from app.api.v1.search import router as search_router
from app.api.v1.command import router as command_router
from app.api.v1.assistant import router as assistant_router
from app.api.v1.files import router as files_router
from app.api.v1.documents import router as documents_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.payments import router as payments_router
from app.api.v1.billing import router as billing_router
from app.api.v1.finance import router as finance_router
from app.api.v1.customer_success import router as customer_success_router
from app.api.v1.client_success import router as client_success_router
from app.api.v1.reliability import router as reliability_router
from app.api.v1.disaster_recovery import router as disaster_recovery_router
from app.api.v1.operations import router as operations_router
from app.api.v1.executive import router as executive_router
from app.api.v1.strategy import router as strategy_router
from app.api.v1.kpi import router as kpi_router
from app.api.v1.decisions import router as decisions_router
from app.api.v1.scenarios import router as scenarios_router
from app.api.v1.risks import router as risks_router
from app.api.v1.administration import router as administration_router
from app.api.v1.grc import router as grc_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.process_intelligence import router as process_intelligence_router
from app.api.v1.digital_twin import router as digital_twin_router
from app.api.v1.workforce import router as workforce_router
from app.api.v1.decision_rooms import router as decision_rooms_router
from app.api.v1.research_intelligence import router as research_intelligence_router
from app.api.v1.innovation import router as innovation_router
from app.api.v1.product_management import router as product_management_router
from app.api.v1.customer_experience import router as customer_experience_router
from app.api.v1.revenue_growth import router as revenue_growth_router
from app.api.v1.marketing import router as marketing_router
from app.api.v1.product_os import router as product_os_router
from app.api.v1.engineering_os import router as engineering_os_router
from app.api.v1.enterprise_data_os import router as enterprise_data_os_router
from app.api.v1.ai_model_factory import router as ai_model_factory_router
from app.api.v1.autonomous_engineering_os import router as autonomous_engineering_os_router
from backend.app.api.v1.autonomous_data_knowledge_os import router as autonomous_data_knowledge_os_router
try:
    from app.api.v1.autonomous_cybersecurity_zero_trust import router as autonomous_cybersecurity_zero_trust_router
except ImportError:
    from backend.app.api.v1.autonomous_cybersecurity_zero_trust import router as autonomous_cybersecurity_zero_trust_router

try:
    from app.api.v1.autonomous_devsecops_software_factory import router as autonomous_devsecops_software_factory_router
except ImportError:
    from backend.app.api.v1.autonomous_devsecops_software_factory import router as autonomous_devsecops_software_factory_router

try:
    from app.api.v1.autonomous_infrastructure_cloud_os import router as autonomous_infrastructure_cloud_os_router
except ImportError:
    from backend.app.api.v1.autonomous_infrastructure_cloud_os import router as autonomous_infrastructure_cloud_os_router

try:
    from app.api.v1.global_infrastructure import router as global_infrastructure_router
except ImportError:
    from backend.app.api.v1.global_infrastructure import router as global_infrastructure_router

try:
    from app.api.v1.cyber_physical import router as cyber_physical_router
except ImportError:
    from backend.app.api.v1.cyber_physical import router as cyber_physical_router

try:
    from app.api.v1.supply_chain import router as supply_chain_router
except ImportError:
    from backend.app.api.v1.supply_chain import router as supply_chain_router

try:
    from app.api.v1.finance_os import router as finance_os_router
except ImportError:
    from backend.app.api.v1.finance_os import router as finance_os_router

try:
    from app.api.v1.trust_os import router as trust_os_router
except ImportError:
    from backend.app.api.v1.trust_os import router as trust_os_router

try:
    from app.api.v1.operations_os import router as operations_os_router
except ImportError:
    from backend.app.api.v1.operations_os import router as operations_os_router

try:
    from app.api.v1.decision_os import router as decision_os_router
except ImportError:
    from backend.app.api.v1.decision_os import router as decision_os_router

try:
    from app.api.v1.ai_os import router as ai_os_router
except ImportError:
    from backend.app.api.v1.ai_os import router as ai_os_router

try:
    from app.api.v1.enterprise_knowledge import router as enterprise_knowledge_router
except ImportError:
    from backend.app.api.v1.enterprise_knowledge import router as enterprise_knowledge_router

try:
    from app.api.v1.enterprise_process_intelligence import router as enterprise_process_intelligence_router
except ImportError:
    from backend.app.api.v1.enterprise_process_intelligence import router as enterprise_process_intelligence_router

from app.api.v1.data_platform import router as data_platform_router
from app.api.v1.cyber_defense import router as cyber_defense_router
from app.api.v1.it_operations import router as it_operations_router
from app.api.v1.ai_platform import router as ai_platform_router
from app.api.v1.digital_twin import router as digital_twin_api_router
from app.api.v1.autonomous_workforce import router as autonomous_workforce_router
from app.api.v1.ai_workforce_marketplace import router as ai_workforce_marketplace_router
from app.api.v1.ai_federation import router as ai_federation_router
from app.api.v1.global_ai_economic_network import router as global_ai_economic_network_router
from app.api.v1.planetary_ai_infrastructure import router as planetary_ai_infrastructure_router
from app.api.v1.planetary_ai_civilization import router as planetary_ai_civilization_router
from app.api.v1.planetary_ai_education import router as planetary_ai_education_router
from app.api.v1.global_human_ai_collaboration import router as global_human_ai_collaboration_router
from app.api.v1.global_digital_society import router as global_digital_society_router
from app.api.v1.planetary_digital_twin import router as planetary_digital_twin_router






router = APIRouter()

router.include_router(auth_router)
router.include_router(security_router)
router.include_router(businesses_router)
router.include_router(leads_router)
router.include_router(contacts_router)
router.include_router(services_router)
router.include_router(dashboard_router)
router.include_router(research_router)
router.include_router(audits_router)
router.include_router(scoring_router)
router.include_router(recommendations_router)
router.include_router(qualification_router)
router.include_router(outreach_router)
router.include_router(risk_router)
router.include_router(conversations_router)
router.include_router(webhooks_router)
router.include_router(agents_router)
router.include_router(requirements_router)
router.include_router(solutions_router)
router.include_router(proposals_router)
router.include_router(estimates_router)
router.include_router(contracts_router)
router.include_router(projects_router)
router.include_router(client_router)
router.include_router(change_router)
router.include_router(qa_router)
router.include_router(support_router, prefix="/support", tags=["support"])
router.include_router(analytics_router)
router.include_router(insights_router)
router.include_router(experiments_router)
router.include_router(predictive_router)
router.include_router(governance_router)
router.include_router(orchestration_router)
router.include_router(data_router)
router.include_router(communication_router)
router.include_router(search_router)
router.include_router(command_router)
router.include_router(assistant_router)
router.include_router(files_router)
router.include_router(documents_router)
router.include_router(invoices_router)
router.include_router(payments_router)
router.include_router(billing_router)
router.include_router(finance_router)
router.include_router(customer_success_router)
router.include_router(client_success_router)
router.include_router(reliability_router)
router.include_router(disaster_recovery_router)
router.include_router(operations_router)
router.include_router(executive_router)
router.include_router(strategy_router)
router.include_router(kpi_router)
router.include_router(decisions_router)
router.include_router(scenarios_router)
router.include_router(risks_router)
router.include_router(administration_router)
router.include_router(security_ops_router)
router.include_router(grc_router)
router.include_router(knowledge_router)
router.include_router(process_intelligence_router)
router.include_router(digital_twin_router)
router.include_router(workforce_router)
router.include_router(decision_rooms_router)
router.include_router(research_intelligence_router)
router.include_router(innovation_router)
router.include_router(product_management_router)
router.include_router(customer_experience_router)
router.include_router(revenue_growth_router)
router.include_router(marketing_router)
router.include_router(product_os_router)
router.include_router(engineering_os_router)
router.include_router(enterprise_data_os_router)
router.include_router(ai_model_factory_router)
router.include_router(autonomous_engineering_os_router)
router.include_router(autonomous_data_knowledge_os_router)
router.include_router(autonomous_cybersecurity_zero_trust_router)
router.include_router(autonomous_devsecops_software_factory_router)
router.include_router(autonomous_infrastructure_cloud_os_router)
router.include_router(global_infrastructure_router)
router.include_router(cyber_physical_router)
router.include_router(supply_chain_router)
router.include_router(finance_os_router)
router.include_router(trust_os_router)
router.include_router(operations_os_router)
router.include_router(decision_os_router)
router.include_router(ai_os_router)
router.include_router(enterprise_knowledge_router)
router.include_router(enterprise_process_intelligence_router)
router.include_router(data_platform_router)
router.include_router(cyber_defense_router)
router.include_router(it_operations_router)
router.include_router(ai_platform_router)
router.include_router(digital_twin_api_router)
router.include_router(autonomous_workforce_router)
router.include_router(ai_workforce_marketplace_router)
router.include_router(ai_federation_router)
router.include_router(global_ai_economic_network_router)
router.include_router(planetary_ai_infrastructure_router)
router.include_router(planetary_ai_civilization_router)
router.include_router(planetary_ai_education_router)
router.include_router(global_human_ai_collaboration_router)
router.include_router(global_digital_society_router)
try:
    from app.api.v1.planetary_resilience import router as planetary_resilience_router
except ImportError:
    from backend.app.api.v1.planetary_resilience import router as planetary_resilience_router

try:
    from app.api.v1.planetary_civilization import router as planetary_civilization_router
except ImportError:
    from backend.app.api.v1.planetary_civilization import router as planetary_civilization_router

try:
    from app.api.v1.scientific_discovery import router as scientific_discovery_router
except ImportError:
    from backend.app.api.v1.scientific_discovery import router as scientific_discovery_router

try:
    from app.api.v1.universal_intelligence import router as universal_intelligence_router
except ImportError:
    from backend.app.api.v1.universal_intelligence import router as universal_intelligence_router

try:
    from app.api.v1.final_integration import router as final_integration_router
except ImportError:
    from backend.app.api.v1.final_integration import router as final_integration_router

router.include_router(planetary_digital_twin_router)
router.include_router(planetary_resilience_router)
router.include_router(planetary_civilization_router)
router.include_router(scientific_discovery_router)
router.include_router(universal_intelligence_router)
router.include_router(final_integration_router)






























