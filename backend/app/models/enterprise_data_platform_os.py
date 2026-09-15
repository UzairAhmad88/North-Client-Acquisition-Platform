"""
Phase 82: Enterprise Data Platform, Data Engineering, Data Governance, Data Lakehouse, MDM & Autonomous Data Operations Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class DataPlatformSource(Base):
    __tablename__ = "data_platform_sources"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    source_type = Column(String, nullable=False) # Database, API, SaaS, Stream, File, CloudStorage
    environment = Column(String, default="Production")
    owner = Column(String, nullable=False)
    data_classification = Column(String, default="Confidential")
    criticality = Column(String, default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DataPlatformPipeline(Base):
    __tablename__ = "data_platform_pipelines"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    pipeline_type = Column(String, default="ETL") # ETL, ELT, CDC, Streaming, Batch
    owner = Column(String, nullable=False)
    schedule_cron = Column(String, nullable=True)
    source_id = Column(String, ForeignKey("data_platform_sources.id"), nullable=True)
    target_layer = Column(String, default="Silver") # Bronze, Silver, Gold, Platinum
    sla_minutes = Column(Integer, default=60)
    status = Column(String, default="IDLE") # IDLE, RUNNING, SUCCESS, FAILED, RETRYING
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformPipelineRun(Base):
    __tablename__ = "data_platform_pipeline_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    pipeline_id = Column(String, ForeignKey("data_platform_pipelines.id"), nullable=False)
    status = Column(String, default="RUNNING") # RUNNING, SUCCESS, FAILED, ROLLED_BACK
    records_processed = Column(Integer, default=0)
    bytes_processed = Column(Float, default=0.0)
    duration_seconds = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class DataPlatformDataset(Base):
    __tablename__ = "data_platform_datasets"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False) # Finance, Sales, HR, Customer, Product
    layer = Column(String, default="Gold") # Raw, Bronze, Silver, Gold, Platinum
    storage_format = Column(String, default="Parquet") # Iceberg, Delta, Parquet, Postgres
    row_count = Column(Integer, default=0)
    size_bytes = Column(Float, default=0.0)
    quality_score = Column(Float, default=98.5)
    freshness_minutes = Column(Integer, default=15)
    sensitivity = Column(String, default="Internal")
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformCatalogAsset(Base):
    __tablename__ = "data_platform_catalog_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    asset_name = Column(String, nullable=False, index=True)
    asset_type = Column(String, nullable=False) # Table, View, API, Metric, Model, Feature
    dataset_id = Column(String, ForeignKey("data_platform_datasets.id"), nullable=True)
    description = Column(Text, nullable=True)
    business_term = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    views_count = Column(Integer, default=0)
    rating = Column(Float, default=4.8)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformLineage(Base):
    __tablename__ = "data_platform_lineages"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    source_asset_id = Column(String, nullable=False)
    target_asset_id = Column(String, nullable=False)
    transformation_type = Column(String, default="SQL_SELECT")
    pipeline_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformQualityRule(Base):
    __tablename__ = "data_platform_quality_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    dataset_id = Column(String, ForeignKey("data_platform_datasets.id"), nullable=False)
    rule_name = Column(String, nullable=False)
    rule_type = Column(String, nullable=False) # NOT_NULL, UNIQUE, RANGE, ENUM, FRESHNESS
    expression = Column(String, nullable=False)
    severity = Column(String, default="HIGH")
    passed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MdmGoldenRecord(Base):
    __tablename__ = "mdm_golden_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    domain = Column(String, nullable=False) # Customer, Product, Organization, Supplier
    entity_key = Column(String, nullable=False, index=True)
    canonical_attributes = Column(JSON, default=dict)
    matched_sources_count = Column(Integer, default=1)
    confidence_score = Column(Float, default=0.99)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DataPlatformFeature(Base):
    __tablename__ = "data_platform_features"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    feature_name = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False) # Customer, Product, Transaction
    data_type = Column(String, nullable=False) # FLOAT, INT, STRING, VECTOR
    version = Column(String, default="v1.0")
    owner = Column(String, nullable=False)
    is_online_ready = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformCost(Base):
    __tablename__ = "data_platform_costs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    category = Column(String, nullable=False) # Storage, Compute, Pipeline, Query, Transfer
    monthly_spend_usd = Column(Float, default=0.0)
    resource_id = Column(String, nullable=True)
    unit_cost_per_tb = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataPlatformAgentTask(Base):
    __tablename__ = "data_platform_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2) # 0 to 5
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
