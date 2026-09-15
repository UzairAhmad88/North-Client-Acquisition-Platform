"""
Phase 85: Enterprise Autonomous Workforce, AI Employees, Multi-Agent Organization & Human–AI Collaboration Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class WorkforceAiEmployee(Base):
    __tablename__ = "workforce_ai_employees"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    role_title = Column(String, nullable=False) # e.g. Senior Data Analyst, SRE Specialist, Security Auditor
    department = Column(String, default="Engineering & AI Ops")
    human_supervisor = Column(String, nullable=False) # e.g. Alex Rivera (Director of Engineering)
    persona_prompt = Column(Text, nullable=True)
    allowed_tools = Column(JSON, default=list)
    monthly_budget_usd = Column(Float, default=1500.00)
    monthly_spent_usd = Column(Float, default=320.00)
    autonomy_level = Column(Integer, default=3) # Level 0 to 5
    task_success_rate = Column(Float, default=99.2)
    status = Column(String, default="ACTIVE") # ACTIVE, ON_LEAVE, SUSPENDED, DEPRECATED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class WorkforceDepartment(Base):
    __tablename__ = "workforce_departments"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    head_title = Column(String, nullable=False)
    ai_employee_count = Column(Integer, default=5)
    human_count = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceTeam(Base):
    __tablename__ = "workforce_teams"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    department_id = Column(String, ForeignKey("workforce_departments.id"), nullable=True)
    name = Column(String, nullable=False, index=True)
    team_lead_ai = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceTask(Base):
    __tablename__ = "workforce_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    assigned_employee_id = Column(String, ForeignKey("workforce_ai_employees.id"), nullable=True)
    priority = Column(String, default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="IN_PROGRESS") # PENDING, IN_PROGRESS, REVIEW, COMPLETED, ESCALATED
    autonomy_level = Column(Integer, default=3)
    duration_minutes = Column(Float, default=4.5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceConsensusRun(Base):
    __tablename__ = "workforce_consensus_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    topic = Column(String, nullable=False)
    participating_agents = Column(JSON, default=list)
    consensus_reached = Column(Boolean, default=True)
    final_decision = Column(Text, nullable=True)
    confidence_score = Column(Float, default=0.97)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceReviewRun(Base):
    __tablename__ = "workforce_review_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("workforce_tasks.id"), nullable=False)
    reviewer_employee_id = Column(String, ForeignKey("workforce_ai_employees.id"), nullable=False)
    review_status = Column(String, default="PASSED") # PASSED, REJECTED, CHANGES_REQUESTED
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkforceAgentTask(Base):
    __tablename__ = "workforce_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2)
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
