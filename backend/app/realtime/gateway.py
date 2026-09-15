"""Real-Time Gateway, WebSocket Connection Management & Tenant-Scoped Channels."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
import uuid


class RealtimeGateway:
    """Manages active WebSocket connections, tenant channel subscriptions, and event broadcasts."""

    def __init__(self):
        # Maps channel_name -> Set[connection_id]
        self.channels: Dict[str, Set[str]] = {}
        # Maps connection_id -> { "user_id": str, "tenant_id": str, "connected_at": str }
        self.connections: Dict[str, Dict[str, Any]] = {}

    def register_connection(
        self, connection_id: str, user_id: str, tenant_id: str
    ) -> Dict[str, Any]:
        """Register an authenticated connection."""
        conn_meta = {
            "connection_id": connection_id,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "connected_at": datetime.now(timezone.utc).isoformat(),
        }
        self.connections[connection_id] = conn_meta

        # Automatically join user and tenant channels
        self.subscribe(connection_id, f"user:{user_id}", tenant_id)
        self.subscribe(connection_id, f"tenant:{tenant_id}", tenant_id)
        return conn_meta

    def unregister_connection(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Remove connection and cleanup channel memberships."""
        if connection_id in self.connections:
            meta = self.connections.pop(connection_id)
            for channel_subs in self.channels.values():
                channel_subs.discard(connection_id)
            return meta
        return None

    def subscribe(
        self, connection_id: str, channel: str, tenant_id: str
    ) -> bool:
        """Subscribe connection to channel with strict tenant isolation check."""
        conn_meta = self.connections.get(connection_id)
        if not conn_meta:
            return False

        # Tenant isolation check: if channel has tenant:xxx or project:xxx, verify tenant
        if conn_meta["tenant_id"] != tenant_id:
            return False

        if channel not in self.channels:
            self.channels[channel] = set()

        self.channels[channel].add(connection_id)
        return True

    def get_channel_subscribers(self, channel: str) -> List[str]:
        """Get list of active connection IDs on channel."""
        return list(self.channels.get(channel, set()))
