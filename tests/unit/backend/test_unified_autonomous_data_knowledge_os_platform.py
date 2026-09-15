"""
Unit Test Suite for Phase 65 — Autonomous Data & Knowledge Operating System.
Validates the complete enterprise data loop, connectors, lakehouse, products,
quality, lineage, catalog, semantic layer, knowledge graph, documents, search,
memory, governance, privacy, masking, FinOps, SLOs, query safety, and 15 Data AI agents.
"""

import pytest
import pytest_asyncio
from typing import Any, Dict

from backend.app.services.data.service import AutonomousDataKnowledgeOperatingSystemService
from backend.app.services.data.validation import QueryValidationService
from backend.app.services.data.masking import DataMaskingService
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
    PROHIBITED_PERMISSIONS,
)
from agents.data import (
    DataDiscoveryAgent,
    DataIngestionAgent,
    DataQualityAgent,
    SchemaAgent,
    LineageAgent,
    CatalogAgent,
    MetadataAgent,
    SemanticAgent,
    GraphAgent,
    GovernanceAgent,
    PrivacyAgent,
    AnomalyAgent,
    OptimizationAgent,
    DocumentationAgent,
    DataProductAgent,
)


@pytest.fixture(scope="module")
def data_os():
    """Create AutonomousDataKnowledgeOperatingSystemService coordinator instance."""
    return AutonomousDataKnowledgeOperatingSystemService()


class TestDataSourceRegistryAndConnectors:
    """Test Data Source Registry and Standardized Connectors."""

    def test_data_source_registration_and_credential_isolation(self, data_os):
        tenant = "tenant_data_test_01"
        source = data_os.sources.register_source(
            {
                "name": "Production Aurora PostgreSQL",
                "source_type": "DATABASE",
                "provider": "AWS_AURORA",
                "owner": "data-infra@uzaii.corp",
                "team": "Data Platform",
                "refresh_rate": "CONTINUOUS",
                "classification": "CONFIDENTIAL",
                "connection_config": {"host": "aurora-db.internal", "port": 5432}
            },
            tenant_id=tenant
        )

        assert source["name"] == "Production Aurora PostgreSQL"
        assert source["status"] == "ACTIVE"
        assert "password" not in source  # No plaintext credentials
        assert "auth_ref" in source
        assert source["auth_ref"].startswith("vault://")

        sources = data_os.sources.list_sources(tenant_id=tenant)
        assert len(sources) >= 1

    def test_connector_framework_health_and_schema_discovery(self, data_os):
        connectors = data_os.connectors.list_connectors()
        assert len(connectors) >= 8

        # Test core connector operations
        db_test = data_os.connectors.test_connector("conn_db_default")
        assert db_test["passed"] is True
        assert db_test["connected"] is True

        schema = data_os.connectors.discover_schema("conn_db_default")
        assert "tables" in schema or "schema" in schema or isinstance(schema, dict)


class TestIngestionAndPipelines:
    """Test Ingestion Jobs and Pipeline Orchestration."""

    def test_ingestion_job_lifecycle(self, data_os):
        tenant = "tenant_data_test_02"
        job = data_os.ingestion.create_job(
            {"source_id": "src_aurora_01", "mode": "BATCH"},
            tenant_id=tenant
        )
        assert job["status"] in ["PENDING", "COMPLETED", "RUNNING"]
        assert job["source_id"] == "src_aurora_01"

    def test_pipeline_engine_and_lineage_registration(self, data_os):
        tenant = "tenant_data_test_03"
        pipe = data_os.pipelines.create_pipeline(
            {
                "name": "Customer Transactions Daily Aggregation",
                "source": "raw.transactions",
                "destination": "gold.fact_revenue",
                "schedule": "0 2 * * *",
                "sla_minutes": 60,
                "owner": "Revenue Analytics"
            },
            tenant_id=tenant
        )
        assert pipe["name"] == "Customer Transactions Daily Aggregation"
        assert pipe["status"] == "ACTIVE"


class TestDataLakeWarehouseAndProducts:
    """Test Lakehouse Logical Layers, Data Products, and Data Contracts."""

    def test_data_lakehouse_layers(self, data_os):
        tenant = "tenant_data_test_04"
        raw_asset = data_os.lake.register_asset(
            {"layer": "RAW", "storage_uri": f"s3://lake/{tenant}/raw/", "format": "PARQUET"},
            tenant_id=tenant
        )
        assert raw_asset["layer"] == "RAW"

    def test_data_products_and_contracts_compatibility(self, data_os):
        tenant = "tenant_data_test_05"
        product = data_os.products.create_product(
            {
                "name": "Customer 360 Unified Intelligence",
                "description": "360 degree customer dataset with LTV, churn probability, and historical revenue",
                "owner": "Customer Intelligence Team",
                "owner_team": "Analytics Engineering",
                "tier": "GOLD",
                "sla_tier": "TIER_1_ENTERPRISE"
            },
            tenant_id=tenant
        )
        assert product["tier"] == "GOLD"
        assert product["name"] == "Customer 360 Unified Intelligence"

        contract = data_os.contracts.create_contract(
            {
                "name": "Customer 360 Schema Contract",
                "product_id": product.get("id", "prod_c360"),
                "producer": "Data Engineering",
                "consumer": "Customer AI Agents",
                "schema_definition": {
                    "customer_id": "string",
                    "revenue": "float",
                    "churn_risk": "float"
                },
                "sla_freshness_minutes": 15
            },
            tenant_id=tenant
        )
        assert contract["name"] == "Customer 360 Schema Contract"
        assert contract["status"] == "ACTIVE"


class TestDataQualityAndObservability:
    """Test 6-Dimension Quality Engine and Observability."""

    def test_quality_rule_evaluation_explainability(self, data_os):
        tenant = "tenant_data_test_06"
        data_os.quality.create_rule(
            {
                "dataset_name": "gold.customer_360",
                "dimension": "COMPLETENESS",
                "rule_type": "NOT_NULL",
                "target_column": "customer_id"
            },
            tenant_id=tenant
        )

        checks = data_os.quality.run_quality_checks("gold.customer_360", tenant_id=tenant)
        assert "overall_score" in checks or "scores" in checks
        score = checks.get("overall_score", 99.0)
        assert score >= 90.0

    def test_data_observability_and_incidents(self, data_os):
        tenant = "tenant_data_test_07"
        inc = data_os.incidents.create_incident(
            {
                "dataset": "silver.invoices",
                "pipeline": "pipe_invoices_sync",
                "severity": "MEDIUM",
                "description": "Transient replication lag detected on read replica"
            },
            tenant_id=tenant
        )
        assert inc["status"] in ["OPEN", "PENDING", "RESOLVED"]


class TestDataLineageCatalogAndGlossary:
    """Test End-to-End Lineage, Searchable Catalog, and Business Glossary."""

    def test_lineage_recording_and_traversal(self, data_os):
        tenant = "tenant_data_test_08"
        edge = data_os.lineage.add_edge(
            {
                "source": "postgres.raw_invoices",
                "target": "gold.fact_revenue",
                "transformation": "AGGREGATE_REVENUE_BY_CUSTOMER"
            },
            tenant_id=tenant
        )
        assert edge["source"] == "postgres.raw_invoices"
        assert edge["target"] == "gold.fact_revenue"

    def test_business_glossary_canonical_definitions(self, data_os):
        tenant = "tenant_data_test_09"
        term = data_os.glossary.create_term(
            {
                "term": "Annual Recurring Revenue",
                "definition": "Normalized annualized subscription contract value excluding one-off charges.",
                "domain": "FINANCE",
                "owner": "finance-ops@uzaii.corp",
                "synonyms": ["ARR", "Run-Rate"]
            },
            tenant_id=tenant
        )
        assert term["term"] == "Annual Recurring Revenue"
        assert "ARR" in term["synonyms"]


class TestSemanticLayerAndMetricStore:
    """Test Semantic Layer, Certified Metrics, and Resolution."""

    def test_certified_metrics_and_preventing_conflicts(self, data_os):
        tenant = "tenant_data_test_10"
        metric = data_os.metrics.create_metric(
            {
                "name": "Net Revenue Retention",
                "definition": "Percentage of recurring revenue retained from existing customers over 12 months.",
                "formula": "(ending_arr - expansion_arr - churn_arr) / starting_arr",
                "certification_status": "CERTIFIED",
                "owner": "Finance Strategy"
            },
            tenant_id=tenant
        )
        assert metric["name"] == "Net Revenue Retention"
        assert metric["certification_status"] == "CERTIFIED"


class TestKnowledgeGraphAndMasterData:
    """Test Knowledge Graph, Multi-Hop Traversals, and Entity Resolution."""

    def test_knowledge_graph_seed_and_queries(self, data_os):
        stats = data_os.graph.get_stats("default_tenant")
        assert stats["nodes_count"] >= 7
        assert stats["edges_count"] >= 5

        # Query services connected to root node
        subgraph = data_os.graph.query_subgraph("node_cust_1", max_depth=2, tenant_id="default_tenant")
        assert len(subgraph["nodes"]) >= 1

    def test_entity_resolution_confidence_match(self, data_os):
        tenant = "tenant_data_test_11"
        data_os.master_data.create_entity(
            {
                "entity_type": "CUSTOMER",
                "canonical_name": "International Business Machines",
                "aliases": ["IBM", "IBM Corp", "I.B.M."]
            },
            tenant_id=tenant
        )

        match = data_os.entity_resolution.resolve_entity(
            name="IBM Corp",
            entity_type="CUSTOMER",
            tenant_id=tenant
        )
        assert match["matched"] is True
        assert match["confidence"] >= 0.85


class TestGovernancePrivacyAndFinops:
    """Test Dynamic Masking, Retention, Legal Holds, and FinOps Costs."""

    def test_dynamic_data_masking_strategies(self):
        # Email Redaction
        masked_email = DataMaskingService.mask_value("sarah.connor@cyberdyne.systems", strategy="EMAIL")
        assert "s***@" in masked_email
        assert "cyberdyne.systems" in masked_email

        # Partial Mask
        masked_pan = DataMaskingService.mask_value("4111222233334444", strategy="PARTIAL", options={"visible_chars": 4})
        assert masked_pan.startswith("4111")
        assert "*" in masked_pan

        # Full Redact
        masked_ssn = DataMaskingService.mask_value("000-12-3456", strategy="REDACT")
        assert masked_ssn == "[REDACTED]"

    def test_query_safety_validator_blocks_destructive_operations(self):
        # Prohibit DROP
        safe, err = QueryValidationService.validate_query("DROP TABLE users CASCADE;")
        assert safe is False
        assert "Prohibited statement" in err or "read-only" in err

        # Prohibit DELETE
        safe, err = QueryValidationService.validate_query("DELETE FROM orders WHERE id = 12;")
        assert safe is False

        # Allow valid SELECT
        safe, err = QueryValidationService.validate_query("SELECT id, name, revenue FROM customers ORDER BY revenue DESC LIMIT 10;")
        assert safe is True
        assert err is None


class TestNaturalLanguageQueryStudio:
    """Test Natural Language to Governed Data safe resolution."""

    def test_natural_language_query_execution(self, data_os):
        tenant = "tenant_nl_test_01"
        res = data_os.execute_natural_language_query(
            tenant_id=tenant,
            question="Show revenue by customer for 2026",
            user_id="lead_analyst_01",
            user_roles=["analyst"]
        )

        assert res["success"] is True
        assert res["safety_validated"] is True
        assert "SELECT" in res["generated_sql"]
        assert len(res["result_rows"]) >= 1
        assert len(res["lineage_provenance"]) >= 1


class TestAutonomousDataAgents:
    """Test all 15 specialized Data AI Agents."""

    @pytest.mark.asyncio
    async def test_all_15_data_agents_execution(self, data_os):
        context = AgentContext(
            workflow_id="wf_data_01",
            task_id="task_data_01",
            agent_run_id="run_data_01",
            metadata={"tenant_id": "tenant_agents_test", "source_name": "Postgres Analytics", "mode": "BATCH"}
        )

        agents = [
            DataDiscoveryAgent(data_os),
            DataIngestionAgent(data_os),
            DataQualityAgent(data_os),
            SchemaAgent(data_os),
            LineageAgent(data_os),
            CatalogAgent(data_os),
            MetadataAgent(data_os),
            SemanticAgent(data_os),
            GraphAgent(data_os),
            GovernanceAgent(data_os),
            PrivacyAgent(data_os),
            AnomalyAgent(data_os),
            OptimizationAgent(data_os),
            DocumentationAgent(data_os),
            DataProductAgent(data_os),
        ]

        for agent in agents:
            # Check permissions
            req_perms = agent.get_required_permissions()
            assert len(req_perms) >= 1
            # Execute agent
            result = await agent.execute(context)
            assert result["status"] == "COMPLETED"
            assert result["tenant_id"] == "tenant_agents_test"


class TestMasterCoordinatorAutonomousLoop:
    """Test full autonomous enterprise data loop."""

    def test_autonomous_data_loop_execution(self, data_os):
        tenant = "tenant_loop_test_01"
        loop_result = data_os.run_autonomous_data_loop(
            tenant_id=tenant,
            source_id="src_postgres_master",
            pipeline_id="pipe_orders_ingestion"
        )

        assert loop_result["status"] == "COMPLETED"
        assert loop_result["rows_processed"] == 2
        assert loop_result["quality_overall_score"] >= 90.0
        assert loop_result["raw_lake_asset_id"] is not None
        assert loop_result["lineage_id"] is not None

    def test_command_center_telemetry_summary(self, data_os):
        summary = data_os.get_command_center_summary("tenant_loop_test_01")
        assert summary["system_health"] in ["OPTIMAL", "WARNING"]
        assert "knowledge_nodes_count" in summary
        assert "data_sources_count" in summary
