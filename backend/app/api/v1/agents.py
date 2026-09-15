import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from agents.core.registry import global_registry
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.agent import (
    AgentRunCreateRequest,
    AgentRunDetailRead,
    AgentRunRead,
    AgentSpecRead,
)
from app.schemas.common import DataResponse, PaginatedResponse, PaginationMeta
from app.services.agents import AgentRuntimeService

router = APIRouter(tags=["Agent Core Runtime"])

agent_service = AgentRuntimeService()


@router.get("/agents", response_model=DataResponse[List[AgentSpecRead]])
def list_registered_agents(
    current_user: User = Depends(get_current_user),
):
    """List specifications for all registered AI agents in the runtime."""
    specs = global_registry.list_agents()
    return DataResponse(data=[AgentSpecRead.model_validate(s) for s in specs])


@router.get("/agents/{name}", response_model=DataResponse[AgentSpecRead])
def get_agent_spec(
    name: str,
    current_user: User = Depends(get_current_user),
):
    """Get specification for a single registered agent."""
    agent = global_registry.get(name)
    spec = {
        "name": agent.name,
        "version": agent.version,
        "description": agent.description,
        "enabled": agent.enabled,
        "permissions": sorted(list(agent.permissions)),
        "max_steps": agent.max_steps,
        "max_tool_calls": agent.max_tool_calls,
        "max_runtime_seconds": agent.max_runtime_seconds,
    }
    return DataResponse(data=AgentSpecRead.model_validate(spec))


@router.get("/agent-runs", response_model=PaginatedResponse[AgentRunRead])
def list_agent_runs(
    lead_id: Optional[uuid.UUID] = Query(default=None, description="Filter by lead ID"),
    status: Optional[str] = Query(default=None, description="Filter by run status"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List agent execution runs with filtering and pagination."""
    items, total = agent_service.list_runs(db, lead_id=lead_id, status=status, limit=limit, page=page)
    formatted = [AgentRunRead.model_validate(r) for r in items]
    return PaginatedResponse(
        data=formatted,
        pagination=PaginationMeta(
            total=total,
            page=page,
            page_size=limit,
            total_pages=(total + limit - 1) // limit if limit > 0 else 1,
        ),
    )


@router.get("/agent-runs/{id}", response_model=DataResponse[AgentRunDetailRead])
def get_agent_run_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed agent execution run trace with events timeline."""
    run = agent_service.get_run(db, id)
    return DataResponse(data=AgentRunDetailRead.model_validate(run))


@router.post("/agent-runs/{id}/cancel", response_model=DataResponse[AgentRunRead])
def cancel_agent_run(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cancel an active agent execution run."""
    run = agent_service.cancel_run(db, id)
    return DataResponse(data=AgentRunRead.model_validate(run))


@router.post("/agent-runs", response_model=DataResponse[AgentRunRead])
def trigger_agent_run(
    body: AgentRunCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger an authorized agent execution run."""
    run = agent_service.trigger_agent_run(
        db,
        agent_name=body.agent_name,
        user_id=current_user.id,
        lead_id=body.lead_id,
        business_id=body.business_id,
        input_data=body.input_data,
    )
    return DataResponse(data=AgentRunRead.model_validate(run))
