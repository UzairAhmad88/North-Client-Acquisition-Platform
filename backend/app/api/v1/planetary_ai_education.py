"""
Phase 91: Planetary AI Education & Human Capability Amplification REST API Router.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.planetary_ai_education import (
    PlanetaryLearningProfileService,
    PlanetaryAiTutorService,
    PlanetaryStemCoachingService,
    PlanetaryAssessmentPassportService,
    PlanetaryTeacherWorkforceService,
    PlanetaryKnowledgeRetentionService,
    PlanetaryGovernancePrivacyService,
)

router = APIRouter(prefix="/human-amplification", tags=["Planetary AI Education OS"])

class TutorSessionRequest(BaseModel):
    concept: str
    mode: str = "SOCRATIC" # SOCRATIC, DIRECT_INSTRUCTION, ANALOGY, WORKED_SOLUTION

class HintLadderRequest(BaseModel):
    problem_id: str
    level: int = 1

class LessonPlanRequest(BaseModel):
    topic: str
    level: str = "ADVANCED"

class KnowledgeCaptureRequest(BaseModel):
    expert_name: str
    domain: str

@router.get("/profiles")
def get_learning_profile(user_id: str = Query("user-exec-01", description="User ID")):
    """Get universal learning profile and skill heatmap."""
    return PlanetaryLearningProfileService.get_learning_profile(user_id)

@router.get("/skills/graph")
def get_skill_graph():
    """Get global skill graph connected to Phase 90 Knowledge Graph."""
    return {"skill_graph": PlanetaryLearningProfileService.get_skill_graph()}

@router.post("/tutor/session")
def start_tutor_session(req: TutorSessionRequest):
    """Start adaptive AI Tutor session (Socratic, Direct, Analogy modes)."""
    return PlanetaryAiTutorService.start_tutor_session(req.concept, req.mode)

@router.post("/stem/hint-ladder")
def generate_hint_ladder(req: HintLadderRequest):
    """Generate progressive hint ladder and worked solutions."""
    return PlanetaryStemCoachingService.generate_hint_ladder(req.problem_id, req.level)

@router.get("/passports")
def get_competency_passports(user_id: str = Query("user-exec-01", description="User ID")):
    """List verifiable competency passports and proof of demonstrated skills."""
    return {"passports": PlanetaryAssessmentPassportService.get_competency_passports(user_id)}

@router.post("/teacher/lesson-plan")
def generate_lesson_plan(req: LessonPlanRequest):
    """Generate educator copilot lesson plan and differentiation levels."""
    return PlanetaryTeacherWorkforceService.generate_lesson_plan(req.topic, req.level)

@router.get("/workforce/reskilling")
def get_workforce_reskilling_map(org_id: str = Query("org-uzaii-hq", description="Organization ID")):
    """Get workforce reskilling map and future skills forecasting."""
    return PlanetaryTeacherWorkforceService.get_workforce_reskilling_map(org_id)

@router.get("/knowledge-retention/rag")
def get_personal_rag_sources(user_id: str = Query("user-exec-01", description="User ID")):
    """List personal RAG learning materials."""
    return {"sources": PlanetaryKnowledgeRetentionService.get_personal_rag_sources(user_id)}

@router.post("/knowledge-retention/capture")
def capture_expert_knowledge(req: KnowledgeCaptureRequest):
    """Capture expert institutional knowledge before retirement/succession."""
    return PlanetaryKnowledgeRetentionService.capture_expert_knowledge(req.expert_name, req.domain)

@router.get("/governance/privacy-status")
def get_privacy_controls_status():
    """Get educational privacy, minor safety controls, and disclosure status."""
    return PlanetaryGovernancePrivacyService.get_privacy_controls_status()

@router.get("/governance/audit-trail")
def get_audit_trail():
    """List immutable educational governance audit trail."""
    return {"audits": PlanetaryGovernancePrivacyService.get_audit_trail()}
