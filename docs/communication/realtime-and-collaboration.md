# Real-Time Collaboration & WebSocket Gateway

## 1. WebSocket Infrastructure

The Realtime Gateway provides low-latency bi-directional messaging, collaborative presence tracking, and event broadcasting across tenant-scoped channels.

### Channel Hierarchy
- `user:{user_id}`: Targeted directly to an authenticated user connection across all their active browser tabs.
- `tenant:{tenant_id}`: Broadcasts tenant-wide alerts, system notifications, and organization announcements.
- `project:{project_id}` / `conversation:{conv_id}`: Scoped collaboration channels for live typing indicators and instant message delivery.

---

## 2. Tenant Isolation Enforcement

Connections cannot subscribe to channels outside their authenticated tenant. If a client attempts to join `project:proj-999` with a mismatched tenant token, the subscription is rejected immediately at the gateway layer.
