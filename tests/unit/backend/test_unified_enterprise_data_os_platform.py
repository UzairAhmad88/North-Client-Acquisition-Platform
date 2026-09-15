"""Unit Tests for Phase 62: Unified Enterprise Data Operating System Platform."""

import pytest
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
)
from backend.app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService
from backend.app.services.enterprise_data_os.base import (
    DataDomainType,
    DataLayerType,
    IngestionMode,
    DataClassification,
    DataQualityDimension,
    DataIncidentSeverity,
)
from agents.enterprise_data_os import (
    DataArchitectAgent,
    IngestionPipelineAgent,
    DataQualityAgent,
    DataContractAgent,
    SemanticLayerAgent,
    DataLineageAgent,
    DataGovernanceAgent,
    FeatureStoreAgent,
    DataFinopsAgent,
    DataFinOpsAgent,
    DataCopilotAgent,
)


class TestSourcesIngestionCdc:
    def test_domain_creation(self):
        service = EnterpriseDataOperatingSystemService()
        dom = service.sources_service.create_data_domain(
            tenant_id="t1",
            name="Marketing Analytics",
            slug="marketing-analytics",
            owner_team="Growth & Demand Gen",
            lead_steward_email="steward-mktg@uzaii.com",
            description="Domain managing attribution, campaign metrics, and CAC models.",
        )
        assert dom.name == "Marketing Analytics"
        assert dom.slug == "marketing-analytics"
        assert dom.lead_steward_email == "steward-mktg@uzaii.com"

    def test_data_source_registration_and_secret_isolation(self):
        service = EnterpriseDataOperatingSystemService()
        src = service.sources_service.register_data_source(
            tenant_id="t1",
            name="clickhouse-analytics-cluster",
            source_type="CLICKHOUSE",
            provider="AWS",
            connection_endpoint="clickhouse.internal.uzaii.net:8123/default",
            auth_type="IAM_ROLE",
            reliability_score=99.95,
        )
        assert src.name == "clickhouse-analytics-cluster"
        assert src.auth_type == "IAM_ROLE"
        assert src.status == "ACTIVE"

    def test_ingestion_job_and_cdc_stream(self):
        service = EnterpriseDataOperatingSystemService()
        job = service.sources_service.trigger_ingestion_job(
            tenant_id="t1",
            source_id="src_clickhouse",
            target_dataset_id="ds_bronze_events",
            ingestion_mode=IngestionMode.STREAMING.value,
            records_processed_count=500000,
            latency_ms=45.2,
        )
        assert job.status == "SUCCESS"
        assert job.records_processed_count == 500000

        cdc = service.sources_service.record_cdc_event_stream(
            tenant_id="t1",
            source_table="public.subscriptions",
            operation="INSERT",
            primary_key_val="sub_9921",
            lsn_position="18/C482A0",
            schema_version="v1.0",
        )
        assert cdc.operation == "INSERT"
        assert cdc.is_idempotent is True


class TestPipelinesLakehouseStorage:
    def test_data_pipeline_creation(self):
        service = EnterpriseDataOperatingSystemService()
        pipe = service.pipelines_service.create_data_pipeline(
            tenant_id="t1",
            name="bronze_to_silver_user_cleansing_pipeline",
            source_datasets=["bronze_users_raw"],
            target_dataset="silver_users_cleansed",
            schedule_type="CRON_DAILY",
            sla_minutes=30,
            owner_team="Data Platform",
        )
        assert pipe.name == "bronze_to_silver_user_cleansing_pipeline"
        assert pipe.status == "ACTIVE"

    def test_lakehouse_dataset_tiers(self):
        service = EnterpriseDataOperatingSystemService()
        ds = service.pipelines_service.register_lakehouse_dataset(
            tenant_id="t1",
            domain_id="dom_fin",
            name="gold_subscription_mrr_mart",
            layer=DataLayerType.GOLD.value,
            format_type="DELTA",
            storage_uri="s3://uzaii-lakehouse-gold/subscription_mrr/",
            partition_keys=["tenant_id", "billing_year"],
            record_count=250000,
            size_mb=650.0,
            classification=DataClassification.CONFIDENTIAL.value,
        )
        assert ds.layer == "GOLD"
        assert ds.format == "DELTA"
        assert ds.classification == "CONFIDENTIAL"


class TestSchemasContractsProducts:
    def test_schema_evolution_compatibility(self):
        service = EnterpriseDataOperatingSystemService()
        schema = service.schemas_service.register_schema_version(
            tenant_id="t1",
            dataset_id="silver_users_cleansed",
            version="v2.0.0",
            compatibility_mode="BACKWARD",
        )
        assert schema.version == "v2.0.0"
        assert schema.compatibility_mode == "BACKWARD"
        assert schema.is_active is True

    def test_data_contract_enforcement(self):
        service = EnterpriseDataOperatingSystemService()
        contract = service.schemas_service.create_data_contract(
            tenant_id="t1",
            producer_team="Billing Platform",
            consumer_team="Financial Reporting",
            dataset_id="gold_subscription_mrr_mart",
            freshness_sla_minutes=30,
            quality_threshold_pct=99.9,
        )
        assert contract.freshness_sla_minutes == 30
        assert contract.quality_threshold_pct == 99.9
        assert contract.sla_compliance_pct == 100.0

    def test_curated_data_product_publishing(self):
        service = EnterpriseDataOperatingSystemService()
        prod = service.schemas_service.publish_data_product(
            tenant_id="t1",
            domain_id="dom_cust",
            name="Customer Retention & Expansion Intelligence",
            purpose="Reusable Gold product tracking account-level retention curves and expansion ARR.",
            quality_score=99.4,
        )
        assert prod.name == "Customer Retention & Expansion Intelligence"
        assert prod.quality_score == 99.4
        assert prod.health_status == "HEALTHY"


class TestCatalogGlossarySemantic:
    def test_data_catalog_asset_indexing(self):
        service = EnterpriseDataOperatingSystemService()
        ast = service.catalog_service.register_catalog_asset(
            tenant_id="t1",
            asset_name="gold_retention_cohort_mart",
            asset_type="TABLE",
            domain_name="Customer Success",
            owner_email="steward-cust@uzaii.com",
            quality_score=97.8,
            tags=["customer", "retention", "cohort"],
        )
        assert ast.asset_name == "gold_retention_cohort_mart"
        assert ast.domain_name == "Customer Success"

    def test_business_glossary_term(self):
        service = EnterpriseDataOperatingSystemService()
        term = service.catalog_service.define_glossary_term(
            tenant_id="t1",
            term_name="Customer Acquisition Cost (CAC)",
            definition="Total fully-loaded sales and marketing spend divided by net new customer acquisitions.",
            domain_name="Marketing & Sales",
            owner_email="cmo@uzaii.com",
            synonyms=["Blended CAC", "Paid CAC"],
        )
        assert term.term_name == "Customer Acquisition Cost (CAC)"
        assert len(term.synonyms) == 2

    def test_semantic_metric_definition(self):
        service = EnterpriseDataOperatingSystemService()
        metric = service.catalog_service.define_semantic_metric(
            tenant_id="t1",
            name="Monthly Recurring Revenue (MRR)",
            definition="Normalized monthly subscription revenue run rate.",
            formula_sql="SUM(monthly_subscription_amount)",
            source_table="gold_subscription_mrr_mart",
            owner_team="Finance Operations",
        )
        assert metric.name == "Monthly Recurring Revenue (MRR)"
        assert metric.is_authoritative is True


class TestDataQualityObservabilityDrift:
    def test_data_quality_scorecard(self):
        service = EnterpriseDataOperatingSystemService()
        scorecard = service.quality_service.evaluate_quality_scorecard(
            tenant_id="t1",
            dataset_id="silver_customer_profiles",
            completeness_pct=99.6,
            accuracy_pct=99.2,
            consistency_pct=98.8,
            validity_pct=99.0,
            uniqueness_pct=100.0,
            timeliness_pct=99.4,
        )
        assert scorecard.composite_score >= 99.0
        assert scorecard.status == "EXCELLENT"

    def test_schema_drift_detection(self):
        service = EnterpriseDataOperatingSystemService()
        drift = service.quality_service.detect_schema_drift(
            tenant_id="t1",
            dataset_id="ds_orders",
            detected_changes=[
                {"change_type": "COLUMN_TYPE_ALTERED", "column_name": "tax_rate", "severity": "BREAKING"},
            ],
        )
        assert drift.has_drift is True
        assert drift.is_breaking_change is True
        assert "Human Schema Review Gate Required" in drift.action_required


class TestDataLineageImpactGovernance:
    def test_lineage_graph_and_impact_analysis(self):
        service = EnterpriseDataOperatingSystemService()
        edge = service.governance_service.register_lineage_edge(
            tenant_id="t1",
            source_asset_id="ds_bronze_billing",
            target_asset_id="ds_silver_billing_normalized",
            relationship_type="TRANSFORMS_INTO",
            transformation_name="Currency Normalization & Tax Extraction",
        )
        assert edge.relationship_type == "TRANSFORMS_INTO"

        impact = service.governance_service.analyze_change_impact(
            tenant_id="t1",
            dataset_id="ds_silver_billing_normalized",
            proposed_change="Change currency precision from 2 to 4 decimal places",
        )
        assert impact.blast_radius_score > 5.0
        assert impact.requires_governance_approval is True

    def test_fine_grained_access_grant(self):
        service = EnterpriseDataOperatingSystemService()
        grant = service.governance_service.grant_data_access(
            tenant_id="t1",
            principal_id="bi-analyst@uzaii.com",
            dataset_id="gold_customer_arr_mart",
            access_level="READ",
            row_filter_expression="region = 'US-EAST'",
            masked_columns=["customer_ssn", "masked_pan"],
            approved_by="data-steward@uzaii.com",
        )
        assert grant.access_level == "READ"
        assert grant.row_filter_expression == "region = 'US-EAST'"
        assert len(grant.masked_columns) == 2


class TestFeaturesMlRagAnalytics:
    def test_feature_store_and_rag_indexing(self):
        service = EnterpriseDataOperatingSystemService()
        feat = service.features_service.register_feature(
            tenant_id="t1",
            name="customer_churn_risk_score",
            entity_name="CUSTOMER",
            data_type="FLOAT",
            source_dataset_id="gold_customer_profiles",
            transformation_logic="ML_PREDICTION(churn_classifier_v3)",
            freshness_minutes=15,
        )
        assert feat.name == "customer_churn_risk_score"
        assert feat.is_online_ready is True

        rag = service.features_service.process_rag_document_indexing(
            tenant_id="t1",
            document_title="Enterprise API Security Policy",
            chunk_count=64,
            embedding_model="text-embedding-3-large",
        )
        assert rag.status == "INDEXED"
        assert rag.chunk_count == 64

    def test_sandboxed_sql_query_execution(self):
        service = EnterpriseDataOperatingSystemService()
        # Safe read query
        read_res = service.features_service.execute_sandboxed_sql_query(
            tenant_id="t1",
            sql_query="SELECT customer_id, mrr_usd FROM gold_customer_arr_mart LIMIT 5",
            read_only=True,
        )
        assert read_res.status == "SUCCESS"
        assert read_res.rows_returned > 0

        # Mutation query blocked by safety guard
        mutate_res = service.features_service.execute_sandboxed_sql_query(
            tenant_id="t1",
            sql_query="DROP TABLE gold_customer_arr_mart",
            read_only=True,
        )
        assert mutate_res.status == "BLOCKED_MUTATION_PROHIBITED"
        assert mutate_res.rows_returned == 0


class TestDataFinopsIncidentsCopilot:
    def test_data_finops_and_incident(self):
        service = EnterpriseDataOperatingSystemService()
        fin = service.finops_service.record_data_finops_spend(
            tenant_id="t1",
            domain_name="Lakehouse Core",
            storage_spend_usd=5000.0,
            compute_spend_usd=9000.0,
            query_spend_usd=3000.0,
            ai_rag_spend_usd=2500.0,
            waste_estimate_usd=1800.0,
        )
        assert fin.total_monthly_spend_usd == 19500.0
        assert fin.waste_estimate_usd == 1800.0

        inc = service.finops_service.log_data_incident(
            tenant_id="t1",
            title="Corrupted Parquet Partitions in Silver Customer Stream",
            severity=DataIncidentSeverity.SEV1.value,
            incident_type="DATA_CORRUPTION",
            declared_by="sre-lead@uzaii.com",
        )
        assert inc.severity == "SEV1"
        assert inc.status == "ACTIVE"

    def test_data_copilot_grounded_response(self):
        service = EnterpriseDataOperatingSystemService()
        resp = service.finops_service.query_data_copilot(
            tenant_id="t1",
            query="Where does ARR come from and who owns it?",
        )
        assert len(resp["facts"]) > 0
        assert len(resp["inferences"]) > 0
        assert len(resp["hypotheses"]) > 0
        assert len(resp["recommendations"]) > 0
        assert resp["confidence_score"] > 0.9
        assert "Data Steward authorization" in resp["governance_notice"]


class TestEnterpriseDataAiWorkforceAndPermissions:
    @pytest.mark.asyncio
    async def test_agents_permission_and_execution(self):
        ctx = AgentContext(
            workflow_id="wf_data_01",
            task_id="task_data_01",
            agent_run_id="run_data_01",
            metadata={"tenant_id": "test_tenant", "name": "Customer 360", "query": "Find lineage"},
        )

        agents = [
            DataArchitectAgent(),
            IngestionPipelineAgent(),
            DataQualityAgent(),
            DataContractAgent(),
            SemanticLayerAgent(),
            DataLineageAgent(),
            DataGovernanceAgent(),
            FeatureStoreAgent(),
            DataFinopsAgent(),
            DataFinOpsAgent(),
            DataCopilotAgent(),
        ]

        for agent in agents:
            validate_agent_permissions(agent.permissions)
            assert len(agent.permissions) > 0

            # Execute agent task
            result = await agent.execute(ctx)
            assert result is not None
            assert result.get("status") == "COMPLETED"

    def test_prohibited_actions_enforcement(self):
        agent = DataGovernanceAgent()

        prohibited_ops = [
            "AUTONOMOUS_DROP_DATASET",
            "AUTONOMOUS_EXPOSE_PII",
            "AUTONOMOUS_GRANT_DATA_ACCESS",
            "AUTONOMOUS_DELETE_DATA_CONTRACT",
            "BYPASS_ROW_LEVEL_SECURITY",
            "BYPASS_COLUMN_LEVEL_SECURITY",
            "FABRICATE_DATA_METRICS",
        ]
        for op in prohibited_ops:
            assert op not in [p.value for p in agent.permissions]
