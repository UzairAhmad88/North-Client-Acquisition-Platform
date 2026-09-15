"""Unit and Integration Tests for Phase 37: Unified Notification, Communication, Inbox & Real-Time Collaboration Infrastructure."""

import uuid
from datetime import datetime, time, timedelta, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.communication.audience import AudienceResolver
from app.communication.base import (
    CommunicationType,
    ConversationType,
    DeliveryChannel,
    DeliveryPayload,
    DeliveryStatus,
    InboxState,
    MessageVisibility,
    NotificationPriority,
)
from app.communication.deduplication import DeduplicationEngine
from app.communication.engine import CommunicationEngine
from app.communication.policies import CommunicationPolicyEngine, QuietHoursPolicy
from app.messaging.conversations import MessagingManager
from app.models.base import Base
from app.models.communication import (
    CommunicationAuditRecord,
    CommunicationDeliveryRecord,
    ConversationAttachmentRecord,
    ConversationMemberRecord,
    ConversationMessageRecord,
    ConversationMessageVersionRecord,
    ConversationRecord,
    InboxItemRecord,
    NotificationPreferenceRecord,
    NotificationRecord,
    NotificationTemplateRecord,
    RealtimeSubscriptionRecord,
)
from app.notifications.service import NotificationManager
from app.realtime.gateway import RealtimeGateway


# Set up SQLite in-memory database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# =============================================================================
# 1. Policy & Quiet Hours Tests
# =============================================================================

def test_quiet_hours_policy_normal_vs_security_bypass():
    """Verify that normal notifications respect quiet hours while CRITICAL / SECURITY bypasses it."""
    policy = QuietHoursPolicy(enabled=True, start_hour=22, start_minute=0, end_hour=7, end_minute=0)

    test_time_inside = datetime(2026, 9, 9, 23, 30, tzinfo=timezone.utc)
    test_time_outside = datetime(2026, 9, 9, 14, 0, tzinfo=timezone.utc)

    assert policy.is_in_quiet_hours(test_time_inside) is True
    assert policy.is_in_quiet_hours(test_time_outside) is False

    engine = CommunicationPolicyEngine()

    # Normal priority during quiet hours -> Suppressed / Delayed
    suppress, reason = engine.should_suppress_for_quiet_hours(
        priority=NotificationPriority.NORMAL,
        category=CommunicationType.OPERATIONAL,
        quiet_hours=policy,
        now=test_time_inside,
    )
    assert suppress is True
    assert reason == "DELAYED_DUE_TO_QUIET_HOURS"

    # Critical security during quiet hours -> NEVER suppressed (Guardrail)
    suppress_crit, reason_crit = engine.should_suppress_for_quiet_hours(
        priority=NotificationPriority.CRITICAL,
        category=CommunicationType.SECURITY,
        quiet_hours=policy,
        now=test_time_inside,
    )
    assert suppress_crit is False
    assert "BYPASS_MANDATORY_SECURITY_OR_CRITICAL" in reason_crit


def test_mandatory_notification_determination():
    """Verify that security category or critical priority are mandatory notifications."""
    assert CommunicationPolicyEngine.is_mandatory_notification(
        CommunicationType.SECURITY, NotificationPriority.NORMAL
    ) is True

    assert CommunicationPolicyEngine.is_mandatory_notification(
        CommunicationType.OPERATIONAL, NotificationPriority.CRITICAL
    ) is True

    assert CommunicationPolicyEngine.is_mandatory_notification(
        CommunicationType.OPERATIONAL, NotificationPriority.NORMAL
    ) is False


# =============================================================================
# 2. Deduplication & Idempotency Tests
# =============================================================================

def test_deduplication_engine_key_and_time_window():
    """Verify deduplication key generation and window-based duplicate prevention."""
    engine = DeduplicationEngine()
    event_type = "invoice.overdue"
    resource_id = "inv-101"
    recipient_id = "usr-88"

    key = engine.generate_deduplication_key(event_type, resource_id, recipient_id)
    assert key == "invoice.overdue:inv-101:usr-88"

    # Existing deliveries within threshold
    now = datetime(2026, 9, 9, 12, 0, tzinfo=timezone.utc)
    recent_deliveries = [
        {
            "id": "del-1",
            "deduplication_key": key,
            "created_at": (now - timedelta(minutes=10)).isoformat(),
        }
    ]

    is_dup, dup_id = engine.should_deduplicate(key, recent_deliveries, window_minutes=60, now=now)
    assert is_dup is True
    assert dup_id == "del-1"

    # Beyond window -> not duplicate
    is_dup_old, _ = engine.should_deduplicate(key, recent_deliveries, window_minutes=5, now=now)
    assert is_dup_old is False


# =============================================================================
# 3. Audience Resolution & Tenant Filtering Tests
# =============================================================================

def test_audience_resolver_explicit_and_group():
    """Test resolving explicit user IDs and tenant-scoped groups."""
    resolver = AudienceResolver()
    tenant_id = "tenant-001"
    u1, u2 = "u1", "u2"

    resolved = resolver.resolve_recipients(
        tenant_id=tenant_id,
        explicit_recipients=[u1, u2],
        project_members=[{"tenant_id": tenant_id, "user_id": u1}],
        visibility=MessageVisibility.INTERNAL,
    )
    assert len(resolved) == 2
    assert u1 in resolved
    assert u2 in resolved

    # Client user resolution with CLIENT_VISIBLE
    client_res = resolver.resolve_recipients(
        tenant_id=tenant_id,
        client_users=[{"tenant_id": tenant_id, "user_id": "client_1"}],
        visibility=MessageVisibility.CLIENT_VISIBLE,
    )
    assert "client_1" in client_res

    # Client user resolution with INTERNAL -> client user must NOT be included
    internal_res = resolver.resolve_recipients(
        tenant_id=tenant_id,
        client_users=[{"tenant_id": tenant_id, "user_id": "client_1"}],
        visibility=MessageVisibility.INTERNAL,
    )
    assert "client_1" not in internal_res


def test_tenant_boundary_filter():
    """Verify filter_by_tenant strips entities belonging to foreign tenants."""
    mixed = [
        {"id": "rec-1", "tenant_id": "tenant-A"},
        {"id": "rec-2", "tenant_id": "tenant-B"},
    ]
    filtered = AudienceResolver.filter_by_tenant(mixed, "tenant-A")
    assert len(filtered) == 1
    assert filtered[0]["id"] == "rec-1"


# =============================================================================
# 4. Client Visibility Boundary & Internal Notes Tests
# =============================================================================

def test_client_visibility_boundary_filtering():
    """Verify internal notes are strictly filtered from client-facing message feeds."""
    messages = [
        MessagingManager.create_message(
            conversation_id="conv-1",
            sender_id="usr-1",
            content="Hello client, here is the weekly status.",
            visibility=MessageVisibility.CLIENT_VISIBLE,
        ),
        MessagingManager.create_message(
            conversation_id="conv-1",
            sender_id="usr-1",
            content="INTERNAL: Client requested a change in scope, schedule internal alignment.",
            visibility=MessageVisibility.INTERNAL,
        ),
        MessagingManager.create_message(
            conversation_id="conv-1",
            sender_id="usr-1",
            content="RESTRICTED: Sensitive commercial discussion.",
            visibility=MessageVisibility.RESTRICTED,
        ),
    ]

    assert len(messages) == 3

    client_visible = MessagingManager.filter_messages_for_client(messages)
    assert len(client_visible) == 1
    assert client_visible[0]["content"] == "Hello client, here is the weekly status."
    assert client_visible[0]["visibility"] == MessageVisibility.CLIENT_VISIBLE.value


# =============================================================================
# 5. Message Editing & Version History Tests
# =============================================================================

def test_message_editing_and_version_history():
    """Verify that editing a message updates content and retains version history."""
    msg = MessagingManager.create_message(
        conversation_id="conv-101",
        sender_id="usr-dev",
        content="Initial message draft with a typo.",
        visibility=MessageVisibility.CLIENT_VISIBLE,
    )

    assert msg["version"] == 1
    assert len(msg["history"]) == 1

    # Perform edit
    updated = MessagingManager.edit_message(
        message=msg,
        new_content="Corrected message draft without typos.",
        editor_id="usr-dev",
    )

    assert updated["content"] == "Corrected message draft without typos."
    assert updated["version"] == 2
    assert updated["edited_at"] is not None
    assert len(updated["history"]) == 2
    assert updated["history"][0]["content"] == "Initial message draft with a typo."
    assert updated["history"][1]["content"] == "Corrected message draft without typos."


# =============================================================================
# 6. Reading != Approval Guardrail Tests
# =============================================================================

def test_inbox_item_state_transition_read_not_approved():
    """Verify transitioning inbox item state to READ updates timestamps but does not authorize actions."""
    item = NotificationManager.create_inbox_item(
        recipient_id="usr-mgr",
        tenant_id="tenant-1",
        title="Pending Approval: Deployment Plan",
        body="Review deployment plan for Phase 37.",
        category=CommunicationType.APPROVAL,
        priority=NotificationPriority.HIGH,
        action_url="/approvals/plan-37",
        action_type="SIGN_OFF",
    )

    assert item["state"] == InboxState.UNREAD.value
    assert item["read_at"] is None

    # Mark as READ
    read_item = NotificationManager.transition_inbox_state(item, target_state=InboxState.READ)
    assert read_item["state"] == InboxState.READ.value
    assert read_item["read_at"] is not None
    # Action type remains SIGN_OFF (informational), not APPROVED
    assert read_item["action_type"] == "SIGN_OFF"

    # Snooze item
    snooze_time = datetime.now(timezone.utc) + timedelta(hours=4)
    snoozed_item = NotificationManager.transition_inbox_state(
        read_item, target_state=InboxState.SNOOZED, snooze_until=snooze_time
    )
    assert snoozed_item["state"] == InboxState.SNOOZED.value
    assert snoozed_item["snoozed_until"] is not None


# =============================================================================
# 7. Real-Time Gateway & Channel Isolation Tests
# =============================================================================

def test_realtime_gateway_connection_and_channels():
    """Test WebSocket connection lifecycle and tenant-scoped channel subscriptions."""
    gateway = RealtimeGateway()
    conn_id_1 = "conn-1"
    conn_id_2 = "conn-2"
    tenant_A = "tenant-A"
    tenant_B = "tenant-B"

    # Register connections
    gateway.register_connection(conn_id_1, user_id="usr-1", tenant_id=tenant_A)
    gateway.register_connection(conn_id_2, user_id="usr-2", tenant_id=tenant_B)

    # Subscribe conn-1 to tenant-A channel -> Success
    assert gateway.subscribe(conn_id_1, "project:p-101", tenant_id=tenant_A) is True
    # Subscribe conn-1 with mismatched tenant -> Denied (Security guardrail)
    assert gateway.subscribe(conn_id_1, "project:p-202", tenant_id="tenant-other") is False

    # Check active subscribers for project:p-101
    subs = gateway.get_channel_subscribers("project:p-101")
    assert conn_id_1 in subs
    assert conn_id_2 not in subs

    # Unregister connection
    gateway.unregister_connection(conn_id_1)
    subs_after = gateway.get_channel_subscribers("project:p-101")
    assert conn_id_1 not in subs_after


# =============================================================================
# 8. External Communication Guardrail & Engine Tests
# =============================================================================

def test_communication_engine_dispatch_and_external_guardrails():
    """Verify CommunicationEngine event transformation and external outbound approval check."""
    engine = CommunicationEngine()
    tenant_id = "tenant-001"
    recipients = ["usr-1", "usr-2"]

    # 1. Process event notification
    deliveries = engine.process_event_notification(
        event_type="build.completed",
        tenant_id=tenant_id,
        recipients=recipients,
        title="Build #42 Passed",
        message="All tests passed successfully.",
        category=CommunicationType.OPERATIONAL,
        priority=NotificationPriority.NORMAL,
        channels=[DeliveryChannel.IN_APP, DeliveryChannel.EMAIL],
        resource_id="build-42",
    )

    assert len(deliveries) == 4  # 2 recipients x 2 channels

    # 2. Validate external communication guardrails
    # External email without human approval -> BLOCKED
    assert engine.validate_external_communication_boundary(
        channel=DeliveryChannel.EMAIL,
        is_external=True,
        has_human_approval=False,
        risk_level="LOW",
    ) is False

    # External email with human approval and low risk -> PERMITTED
    assert engine.validate_external_communication_boundary(
        channel=DeliveryChannel.EMAIL,
        is_external=True,
        has_human_approval=True,
        risk_level="LOW",
    ) is True

    # External email with high risk -> BLOCKED
    assert engine.validate_external_communication_boundary(
        channel=DeliveryChannel.EMAIL,
        is_external=True,
        has_human_approval=True,
        risk_level="HIGH_RISK",
    ) is False


# =============================================================================
# 9. Database ORM Models & Relationships Tests
# =============================================================================

def test_communication_orm_models_persistence(db_session):
    """Verify ORM models for notifications, inbox, conversations, and deliveries save and retrieve cleanly."""
    tenant_id = "tenant-001"
    user_id = "usr-001"

    # 1. Notification record
    notif = NotificationRecord(
        tenant_id=tenant_id,
        recipient_id=user_id,
        category=CommunicationType.SECURITY.value,
        priority=NotificationPriority.CRITICAL.value,
        title="Security Alert: Anomalous Login",
        body="Login from unfamiliar IP address detected.",
        status=DeliveryStatus.DELIVERED.value,
    )
    db_session.add(notif)
    db_session.commit()
    db_session.refresh(notif)
    assert notif.id is not None
    assert notif.category == "SECURITY"

    # 2. Inbox item
    inbox_item = InboxItemRecord(
        tenant_id=tenant_id,
        recipient_id=user_id,
        notification_id=str(notif.id),
        category=CommunicationType.SECURITY.value,
        title="Security Alert",
        body="Anomalous Login",
        priority=NotificationPriority.CRITICAL.value,
        state=InboxState.UNREAD.value,
    )
    db_session.add(inbox_item)
    db_session.commit()
    db_session.refresh(inbox_item)
    assert inbox_item.id is not None
    assert inbox_item.state == "UNREAD"

    # 3. Conversation & Message
    conv = ConversationRecord(
        tenant_id=tenant_id,
        title="Incident-101 Response Thread",
        conversation_type=ConversationType.SYSTEM.value,
        created_by=user_id,
        status="ACTIVE",
    )
    db_session.add(conv)
    db_session.commit()
    db_session.refresh(conv)

    msg = ConversationMessageRecord(
        conversation_id=conv.id,
        sender_id=user_id,
        content="Session revoked and MFA reset enforced.",
        visibility=MessageVisibility.INTERNAL.value,
    )
    db_session.add(msg)
    db_session.commit()
    db_session.refresh(msg)
    assert msg.id is not None
    assert msg.visibility == "INTERNAL"

    # 4. Delivery record
    delivery = CommunicationDeliveryRecord(
        tenant_id=tenant_id,
        recipient_id=user_id,
        channel=DeliveryChannel.IN_APP.value,
        status=DeliveryStatus.DELIVERED.value,
    )
    db_session.add(delivery)
    db_session.commit()
    db_session.refresh(delivery)
    assert delivery.id is not None
    assert delivery.status == "DELIVERED"
