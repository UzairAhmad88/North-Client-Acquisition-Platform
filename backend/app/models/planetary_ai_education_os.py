"""
Phase 91: Planetary AI Education, Human Capability Amplification & Universal Knowledge Access Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class UniversalLearningProfile(Base):
    __tablename__ = "universal_learning_profiles"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    target_role = Column(String, default="PRINCIPAL_AI_ARCHITECT")
    current_mastery_level = Column(String, default="ADVANCED_PRACTITIONER")
    preferred_learning_mode = Column(String, default="SOCRATIC_INTERACTIVE") # SOCRATIC, DIRECT_INSTRUCTION, EXAMPLE_BASED, RESEARCH
    knowledge_gaps = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    daily_time_budget_minutes = Column(Integer, default=45)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class GlobalSkillNode(Base):
    __tablename__ = "global_skill_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    skill_name = Column(String, nullable=False, index=True)
    domain = Column(String, default="AI_ENGINEERING") # AI_ENGINEERING, QUANTUM_COMPUTING, DATA_PLATFORM, STRATEGY
    prerequisite_skill_ids = Column(JSON, default=list)
    knowledge_claim_ids = Column(JSON, default=list) # Connected to Phase 90 Knowledge Graph
    difficulty_rating = Column(Float, default=8.5) # 1 to 10
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PersonalLearningPath(Base):
    __tablename__ = "personal_learning_paths"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    profile_id = Column(String, ForeignKey("universal_learning_profiles.id"), nullable=False)
    path_title = Column(String, nullable=False)
    milestones = Column(JSON, default=list)
    spaced_repetition_schedule = Column(JSON, default=dict)
    estimated_completion_days = Column(Integer, default=30) # ESTIMATE
    completion_percentage = Column(Float, default=42.5)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TutorInteractionSession(Base):
    __tablename__ = "tutor_interaction_sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    tutor_mode = Column(String, default="SOCRATIC") # SOCRATIC, DIRECT_INSTRUCTION, ANALOGY, WORKED_SOLUTION
    concept_topic = Column(String, nullable=False)
    hint_level_reached = Column(Integer, default=1)
    misconceptions_detected = Column(JSON, default=list)
    active_recall_score = Column(Float, default=95.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CompetencyPassportRecord(Base):
    __tablename__ = "competency_passport_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    skill_name = Column(String, nullable=False)
    demonstrated_evidence_hash = Column(String, nullable=False)
    verification_status = Column(String, default="VERIFIED_PORTFOLIO_PROOF")
    credential_issuer = Column(String, default="Uzaii Global Learning Intelligence Fabric")
    is_ai_generated_claim = Column(Boolean, default=False) # MUST NOT MASQUERADE AS UNVERIFIED QUALIFICATION
    issued_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceReskillingMap(Base):
    __tablename__ = "workforce_reskilling_maps"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, nullable=False, index=True)
    target_future_role = Column(String, nullable=False)
    capability_gap_index = Column(Float, default=18.4)
    reskilling_pathways = Column(JSON, default=list)
    projected_readiness_months = Column(Integer, default=6)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EducationalGovernanceAudit(Base):
    __tablename__ = "educational_governance_audits"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    event_type = Column(String, nullable=False) # PRIVACY_AUDIT, MINOR_SAFETY_GATE, HIGH_STAKES_ASSESSMENT_VERIFICATION, AI_DISCLOSURE
    user_id = Column(String, nullable=False)
    compliance_status = Column(String, default="PASSED")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
