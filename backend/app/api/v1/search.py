"""FastAPI endpoints for Global Unified Search, Suggestions, Saved Queries, and Pins."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.repositories.search import SearchRepository
from app.schemas.search import (
    SearchPinCreateRequest,
    SearchPinResponseSchema,
    SearchResponseSchema,
    SearchSavedQueryCreateRequest,
    SearchSavedQueryResponseSchema,
    SearchSuggestionSchema,
)
from app.search.base import SearchEntityType
from app.search.service import GlobalSearchService

router = APIRouter(prefix="/search", tags=["Global Search"])
_global_search_service = GlobalSearchService()


@router.get("", response_model=SearchResponseSchema, summary="Execute Global Unified Search")
def execute_search(
    q: str = Query(..., min_length=1, description="Search query string"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search across all authorized platform entities with tenant isolation and multi-factor ranking."""
    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    role = getattr(current_user, "role", "USER")

    entity_types = None
    if entity_type:
        try:
            entity_types = [SearchEntityType(entity_type.upper())]
        except ValueError:
            pass

    results = _global_search_service.execute_search(
        raw_query=q,
        tenant_id=str(current_user.tenant_id),
        user_id=str(current_user.id),
        is_client=is_client,
        role=role,
        entity_types=entity_types,
        status=status_filter,
        priority=priority,
        limit=limit,
        offset=offset,
    )

    # Log query in audit trail
    repo = SearchRepository(db)
    repo.log_query(
        tenant_id=str(current_user.tenant_id),
        user_id=str(current_user.id),
        query_text=q,
        search_type=results["parsed_query"]["search_type"],
        result_count=results["total_count"],
        latency_ms=results["latency_ms"],
    )

    return results


@router.get("/suggestions", response_model=List[SearchSuggestionSchema], summary="Search Autocomplete Suggestions")
def get_search_suggestions(
    q: str = Query("", description="Query prefix"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve autocomplete suggestions, popular searches, and recent queries."""
    repo = SearchRepository(db)
    recent_audits = repo.list_recent_queries(str(current_user.tenant_id), str(current_user.id), limit=5)
    recent_texts = [r.query_text for r in recent_audits]

    return _global_search_service.get_suggestions(prefix=q, recent_queries=recent_texts)


@router.get("/saved", response_model=List[SearchSavedQueryResponseSchema], summary="List Saved Searches")
def list_saved_searches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve current user's saved searches and filter views."""
    repo = SearchRepository(db)
    return repo.list_saved_queries(str(current_user.tenant_id), str(current_user.id))


@router.post("/saved", response_model=SearchSavedQueryResponseSchema, status_code=status.HTTP_201_CREATED, summary="Create Saved Search")
def create_saved_search(
    request: SearchSavedQueryCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Save a search query and filter view."""
    repo = SearchRepository(db)
    return repo.create_saved_query(
        tenant_id=str(current_user.tenant_id),
        user_id=str(current_user.id),
        name=request.name,
        query_text=request.query_text,
        filters_json=request.filters_json,
        is_pinned=request.is_pinned,
    )


@router.delete("/saved/{saved_id}", summary="Delete Saved Search")
def delete_saved_search(
    saved_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a saved search."""
    repo = SearchRepository(db)
    deleted = repo.delete_saved_query(str(current_user.tenant_id), str(current_user.id), saved_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved search not found")
    return {"status": "SUCCESS", "message": "Saved search deleted"}


@router.get("/pins", response_model=List[SearchPinResponseSchema], summary="List User Pinned Records")
def list_pins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List shortcuts pinned by the user for fast command center access."""
    repo = SearchRepository(db)
    return repo.list_pins(str(current_user.tenant_id), str(current_user.id))


@router.post("/pins", response_model=SearchPinResponseSchema, status_code=status.HTTP_201_CREATED, summary="Create Pin")
def create_pin(
    request: SearchPinCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Pin an entity record."""
    repo = SearchRepository(db)
    return repo.create_pin(
        tenant_id=str(current_user.tenant_id),
        user_id=str(current_user.id),
        entity_type=request.entity_type,
        entity_id=request.entity_id,
        title=request.title,
        action_url=request.action_url,
    )


@router.delete("/pins/{pin_id}", summary="Remove Pin")
def remove_pin(
    pin_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Remove a pinned record."""
    repo = SearchRepository(db)
    deleted = repo.remove_pin(str(current_user.tenant_id), str(current_user.id), pin_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pin not found")
    return {"status": "SUCCESS", "message": "Pin removed"}
