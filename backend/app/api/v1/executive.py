"""API Endpoints for Executive Overview, Business Health, Briefings, Calendar, and Executive Copilot."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query

from app.business_os.base import BriefingFrequency
from app.business_os.service import BusinessOSPlatformService
from app.schemas.business_os import (
    BusinessCalendarEventResponse,
    BusinessHealthReportResponse,
    CopilotQueryRequest,
    CopilotQueryResponse,
    ExecutiveBriefingResponse,
)

router = APIRouter(prefix="/executive", tags=["executive-command-center"])

_service_instance = BusinessOSPlatformService()


def get_business_os_service() -> BusinessOSPlatformService:
    return _service_instance


@router.get("/overview", response_model=Dict[str, Any])
async def get_executive_overview(
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Dict[str, Any]:
    """Retrieve top-level Executive 360 overview payload."""
    return service.get_executive_360_overview()


@router.get("/health", response_model=BusinessHealthReportResponse)
async def get_business_health(
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Retrieve 10-dimension explainable business health scoring report."""
    return service.get_business_health()


@router.get("/briefings", response_model=ExecutiveBriefingResponse)
async def get_executive_briefing(
    frequency: BriefingFrequency = Query(BriefingFrequency.DAILY),
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Generate or retrieve daily, weekly, or monthly executive briefing."""
    return service.get_briefing(frequency=frequency)


@router.get("/calendar", response_model=List[BusinessCalendarEventResponse])
async def get_business_calendar(
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Retrieve aggregated organization-wide strategic business calendar."""
    return service.get_calendar_events()


@router.post("/assistant/query", response_model=CopilotQueryResponse)
async def query_executive_copilot(
    payload: CopilotQueryRequest,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Natural-language strategic intelligence query with grounded evidence sources."""
    return service.query_copilot(query=payload.query, user_role=payload.user_role)
