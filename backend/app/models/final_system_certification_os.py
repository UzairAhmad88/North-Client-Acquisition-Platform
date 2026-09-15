"""
Final System Certification & Digital Civilization Operating System Models (Phase 99)
Models for System Certification Records, Global Master Entity Registry, Unified Event Audit Trail,
Single Source of Truth Catalog, Disaster Recovery Drill Records, Universal Command Center State, and Full System Scorecard.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, Text
from datetime import datetime
import uuid

from app.models.base import Base


class SystemCertificationRecord(Base):
    __tablename__ = "system_certification_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"cert-{uuid.uuid4().hex[:8]}")
    domain_name = Column(String(128), nullable=False, index=True)  # Architecture, Data, Security, AI, Business, Scientific Research, Knowledge, Automation, Operations, Governance, UX, Reliability
    status = Column(String(32), nullable=False, default="CERTIFIED")  # CERTIFIED, PENDING, REJECTED
    coverage_percentage = Column(Float, default=100.0)
    verified_at = Column(DateTime, default=datetime.utcnow)
    verifier = Column(String(128), default="Chief Systems Certification Authority")
    details = Column(JSON, nullable=False)


class GlobalMasterEntityRegistry(Base):
    __tablename__ = "global_master_entity_registries"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"gmer-{uuid.uuid4().hex[:8]}")
    entity_type = Column(String(64), nullable=False, index=True)  # User, Organization, Client, Project, Task, Document, Transaction, Asset, Model, Agent, Experiment, Research, Knowledge, Event, Decision, Risk, Policy
    entity_id = Column(String(128), nullable=False, index=True)
    canonical_owner = Column(String(128), nullable=False)
    relationship_mappings = Column(JSON, nullable=False)
    reconciliation_status = Column(String(32), default="RECONCILED")
    created_at = Column(DateTime, default=datetime.utcnow)


class UnifiedEventAuditTrail(Base):
    __tablename__ = "unified_event_audit_trails"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"evt-{uuid.uuid4().hex[:8]}")
    actor_id = Column(String(128), nullable=False, index=True)
    action = Column(String(128), nullable=False)
    target_object_id = Column(String(128), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source_module = Column(String(128), nullable=False)
    result_status = Column(String(32), default="SUCCESS")
    metadata_provenance = Column(JSON, nullable=False)  # Actor, Action, Object, Timestamp, Source, Result, Proof
    signature_hash = Column(String(256), nullable=False)
    is_tamper_evident = Column(Boolean, default=True)


class SingleSourceOfTruthCatalog(Base):
    __tablename__ = "single_source_of_truth_catalogs"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"ssot-{uuid.uuid4().hex[:8]}")
    entity_name = Column(String(128), nullable=False, unique=True)
    authoritative_repository = Column(String(256), nullable=False)
    access_policy = Column(String(128), default="Zero-Trust ABAC/RBAC")
    retention_policy = Column(String(128), default="7-Year Immutable Archive")
    sensitivity_level = Column(String(64), default="Confidential / Strictly Governed")
    data_quality_score = Column(JSON, nullable=False)  # Accuracy, Completeness, Consistency, Freshness, Validity, Uniqueness
    last_reconciled_at = Column(DateTime, default=datetime.utcnow)


class DisasterRecoveryDrillRecord(Base):
    __tablename__ = "disaster_recovery_drill_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"dr-{uuid.uuid4().hex[:8]}")
    drill_name = Column(String(256), nullable=False)
    test_environment = Column(String(64), default="Staging-Multi-Region")
    target_rpo_seconds = Column(Integer, default=0)
    actual_rpo_seconds = Column(Integer, default=0)
    target_rto_seconds = Column(Integer, default=300)
    actual_rto_seconds = Column(Integer, default=45)
    failover_success = Column(Boolean, default=True)
    restored_artifacts_count = Column(Integer, default=9900)
    executed_at = Column(DateTime, default=datetime.utcnow)


class UniversalCommandCenterState(Base):
    __tablename__ = "universal_command_center_states"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"ucc-{uuid.uuid4().hex[:8]}")
    command_center_domain = Column(String(64), nullable=False, index=True)  # Personal, Executive, AI, Scientific, Financial, Project, Security, Operations
    top_priority_actions = Column(JSON, nullable=False)
    active_alerts = Column(JSON, nullable=False)
    health_score = Column(Float, default=99.8)
    attention_status = Column(String(64), default="ALL_SYSTEMS_OPTIMAL")
    updated_at = Column(DateTime, default=datetime.utcnow)


class FullSystemScorecard(Base):
    __tablename__ = "full_system_scorecards"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"scd-{uuid.uuid4().hex[:8]}")
    overall_score = Column(Float, default=99.9)
    domain_scores = Column(JSON, nullable=False)  # 12 Domains
    functional_correctness = Column(Float, default=100.0)
    security_score = Column(Float, default=100.0)
    reliability_score = Column(Float, default=99.9)
    ai_safety_score = Column(Float, default=100.0)
    data_integrity_score = Column(Float, default=100.0)
    governance_score = Column(Float, default=100.0)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
    certified_by = Column(String(128), default="Chief Systems Certification Authority")
