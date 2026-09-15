"""FastAPI REST & WebSocket endpoints for Phase 37 Unified Communication Infrastructure."""

from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.communication.base import (
    DeliveryChannel,
    DeliveryStatus,
    InboxState,
    NotificationPriority,
)
from app.models.user import User
from app.schemas.communication import (
    BulkUpdateResponse,
    ConversationCreateRequest,
    ConversationDetailResponse,
    ConversationMessageCreateRequest,
    ConversationMessageEditRequest,
    ConversationMessageResponse,
    ConversationResponse,
    DeliveryRecordResponse,
    DeliveryRetryRequest,
    InboxBulkUpdateRequest,
    InboxItemResponse,
    InboxItemUpdateRequest,
    InboxUnreadCountResponse,
    NotificationCreateRequest,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdateRequest,
    NotificationResponse,
)
from app.services.communication import CommunicationService

router = APIRouter(tags=["Communication"])


# =============================================================================
# INBOX ENDPOINTS
# =============================================================================

@router.get(
    "/inbox",
    response_model=List[InboxItemResponse],
    summary="List current user's inbox items",
)
def list_inbox_items(
    state: Optional[InboxState] = Query(None, description="Filter by inbox item state"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    is_pinned: Optional[bool] = Query(None, description="Filter by pinned status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve personal notifications, message items, and alerts for the unified inbox."""
    service = CommunicationService(db)
    return service.list_inbox_items(
        tenant_id=current_user.tenant_id,
        recipient_id=current_user.id,
        state=state,
        is_read=is_read,
        is_pinned=is_pinned,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/inbox/unread-count",
    response_model=InboxUnreadCountResponse,
    summary="Get unread inbox item count",
)
def get_inbox_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Return count of unread items in the current user's inbox."""
    service = CommunicationService(db)
    unread_count = service.get_inbox_unread_count(
        tenant_id=current_user.tenant_id, recipient_id=current_user.id
    )
    return {
        "unread_count": unread_count,
        "tenant_id": current_user.tenant_id,
        "recipient_id": current_user.id,
    }


@router.patch(
    "/inbox/bulk",
    response_model=BulkUpdateResponse,
    summary="Bulk update inbox items",
)
def bulk_update_inbox(
    request: InboxBulkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark multiple inbox items as read, archived, deleted, or snoozed."""
    service = CommunicationService(db)
    return service.bulk_update_inbox(
        tenant_id=current_user.tenant_id,
        recipient_id=current_user.id,
        request=request,
    )


@router.patch(
    "/inbox/{item_id}",
    response_model=InboxItemResponse,
    summary="Update single inbox item state",
)
def update_inbox_item(
    item_id: UUID,
    request: InboxItemUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update read, starred, pinned, or workflow state of a specific inbox item."""
    service = CommunicationService(db)
    item = service.update_inbox_item(
        tenant_id=current_user.tenant_id,
        recipient_id=current_user.id,
        inbox_item_id=item_id,
        request=request,
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inbox item not found or does not belong to user",
        )
    return item


# =============================================================================
# NOTIFICATION ENDPOINTS
# =============================================================================

@router.get(
    "/notifications",
    response_model=List[NotificationResponse],
    summary="List tenant notification records",
)
def list_notifications(
    source_module: Optional[str] = Query(None),
    priority: Optional[NotificationPriority] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Query notification audit history within the current tenant."""
    service = CommunicationService(db)
    return service.list_notifications(
        tenant_id=current_user.tenant_id,
        source_module=source_module,
        priority=priority,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/notifications",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Dispatch a new notification",
)
def create_notification(
    request: NotificationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Dispatch a system, business, or security notification across all configured channels."""
    service = CommunicationService(db)
    return service.create_notification(
        tenant_id=current_user.tenant_id,
        request=request,
        actor_id=current_user.id,
    )


@router.get(
    "/notifications/{notification_id}",
    response_model=NotificationResponse,
    summary="Get single notification record",
)
def get_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Fetch complete notification metadata by ID."""
    service = CommunicationService(db)
    notif = service.get_notification(current_user.tenant_id, notification_id)
    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification record not found",
        )
    return notif


# =============================================================================
# CONVERSATION & MESSAGING ENDPOINTS
# =============================================================================

@router.get(
    "/conversations",
    response_model=List[ConversationResponse],
    summary="List user conversations",
)
def list_conversations(
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[UUID] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List threads and conversations the user has access to."""
    service = CommunicationService(db)
    return service.list_conversations(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/conversations",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conversation thread",
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new unified conversation thread linked to an entity or direct peer."""
    service = CommunicationService(db)
    return service.create_conversation(
        tenant_id=current_user.tenant_id,
        creator_id=current_user.id,
        request=request,
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
    summary="Get conversation thread details and messages",
)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Fetch conversation messages and metadata with client visibility protection."""
    service = CommunicationService(db)
    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    thread = service.get_conversation_details(
        tenant_id=current_user.tenant_id,
        conversation_id=conversation_id,
        user_id=current_user.id,
        is_client_user=is_client,
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or user is not a member",
        )
    return thread


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
    summary="Post message or note to a conversation",
)
def post_conversation_message(
    conversation_id: UUID,
    request: ConversationMessageCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Post a message or internal note to an active conversation thread."""
    service = CommunicationService(db)
    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    try:
        return service.post_message(
            tenant_id=current_user.tenant_id,
            conversation_id=conversation_id,
            sender_id=current_user.id,
            request=request,
            is_client_user=is_client,
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.patch(
    "/conversations/messages/{message_id}",
    response_model=Dict[str, Any],
    summary="Edit conversation message with immutable version snapshot",
)
def edit_conversation_message(
    message_id: UUID,
    request: ConversationMessageEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Edit a message with version tracking for audit compliance."""
    service = CommunicationService(db)
    try:
        return service.edit_message(
            tenant_id=current_user.tenant_id,
            message_id=message_id,
            actor_id=current_user.id,
            request=request,
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))


# =============================================================================
# NOTIFICATION PREFERENCES ENDPOINTS
# =============================================================================

@router.get(
    "/notification-preferences",
    response_model=List[NotificationPreferenceResponse],
    summary="List current user's notification preferences",
)
def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve notification channel and quiet hour preferences per notification type."""
    service = CommunicationService(db)
    return service.get_user_preferences(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )


@router.put(
    "/notification-preferences",
    response_model=NotificationPreferenceResponse,
    summary="Upsert notification preference for category",
)
def update_user_preference(
    request: NotificationPreferenceUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update delivery channels and quiet hours for a specific notification type."""
    service = CommunicationService(db)
    return service.update_user_preference(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        request=request,
    )


# =============================================================================
# DELIVERY AUDITING & RETRY ENDPOINTS
# =============================================================================

@router.get(
    "/communication/deliveries",
    response_model=List[DeliveryRecordResponse],
    summary="List delivery audit logs",
)
def list_deliveries(
    status_filter: Optional[DeliveryStatus] = Query(None, alias="status"),
    channel: Optional[DeliveryChannel] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Explore multi-channel delivery audit logs with error statuses and retry tracking."""
    service = CommunicationService(db)
    return service.list_deliveries(
        tenant_id=current_user.tenant_id,
        status=status_filter,
        channel=channel,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/communication/deliveries/retry",
    response_model=Dict[str, Any],
    summary="Manually trigger retry for failed/DLQ delivery",
)
def retry_delivery(
    request: DeliveryRetryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retry a failed or dead-letter message delivery."""
    service = CommunicationService(db)
    try:
        return service.retry_delivery(
            tenant_id=current_user.tenant_id,
            request=request,
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


# =============================================================================
# WEBSOCKET REAL-TIME COLLABORATION ENDPOINT
# =============================================================================

@router.websocket("/ws/realtime")
async def websocket_realtime_endpoint(
    websocket: WebSocket,
    tenant_id: UUID = Query(...),
    user_id: UUID = Query(...),
    client_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """WebSocket connection handler for live real-time notifications, presence, and messaging."""
    service = CommunicationService(db)
    gateway = service.realtime_gateway
    connection = await gateway.connect(
        websocket=websocket,
        tenant_id=tenant_id,
        user_id=user_id,
        client_id=client_id,
    )

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            channel = data.get("channel")

            if action == "subscribe" and channel:
                gateway.subscribe(connection, channel)
                await websocket.send_json({"type": "subscribed", "channel": channel})
            elif action == "unsubscribe" and channel:
                gateway.unsubscribe(connection, channel)
                await websocket.send_json({"type": "unsubscribed", "channel": channel})
            elif action == "ping":
                await websocket.send_json({"type": "pong"})
            else:
                await websocket.send_json({"type": "unknown_action", "received": data})
    except WebSocketDisconnect:
        gateway.disconnect(connection)
    except Exception:
        gateway.disconnect(connection)
