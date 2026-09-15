"""FastAPI endpoints for Global Command Palette and Safe Command Execution."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.command.service import GlobalCommandService
from app.models.user import User
from app.repositories.search import SearchRepository
from app.schemas.search import (
    CommandDefinitionSchema,
    CommandExecuteRequest,
    CommandParseRequest,
    CommandResponseSchema,
    CommandValidateRequest,
)

router = APIRouter(prefix="/command", tags=["Command Palette"])
_global_command_service = GlobalCommandService()


@router.get("/registry", response_model=List[CommandDefinitionSchema], summary="List Registered Commands")
def list_commands(
    current_user: User = Depends(get_current_active_user),
):
    """List all available command definitions and required permissions."""
    return _global_command_service.list_registered_commands()


@router.post("/parse", response_model=Optional[CommandResponseSchema], summary="Parse Natural Language Command")
def parse_command(
    request: CommandParseRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Parse text into a structured CommandObject."""
    cmd = _global_command_service.parse_command(request.text)
    if not cmd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not match command intent from input text",
        )
    return cmd


@router.post("/validate", summary="Validate Command Parameters")
def validate_command(
    request: CommandValidateRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Verify parameters conformance before confirmation or execution."""
    return _global_command_service.validate_command(
        command_id=request.command_id,
        parameters=request.parameters,
    )


@router.post("/execute", response_model=CommandResponseSchema, summary="Safely Execute Command")
def execute_command(
    request: CommandExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Execute command enforcing role authorization and human approval gates."""
    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    user_permissions = set(getattr(current_user, "permissions", []))

    try:
        result = _global_command_service.execute_command(
            command_id=request.command_id,
            parameters=request.parameters,
            user_id=str(current_user.id),
            tenant_id=str(current_user.tenant_id),
            user_permissions=user_permissions,
            is_client=is_client,
            has_confirmation=request.has_confirmation,
            has_approval=request.has_approval,
        )

        # Log command execution audit
        repo = SearchRepository(db)
        repo.log_command_execution(
            tenant_id=str(current_user.tenant_id),
            user_id=str(current_user.id),
            command_id=result["command_id"],
            category=result["category"],
            risk_level=result["risk_level"],
            status=result["status"],
            parameters_json=result["parameters"],
            result_json=result.get("execution_result") or {},
        )

        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
