# Session Management & Multi-Factor Step-Up Authentication

## 1. Session Lifecycle & Token Strategy

The platform employs short-lived JWT access tokens backed by persistent database sessions (`user_sessions`):

- **Access Token TTL**: 30 minutes
- **Refresh Token TTL**: 30 days
- **Idle Timeout**: 60 minutes (revoked if no activity within 60 minutes)
- **Absolute Timeout**: 24 hours (forces fresh login after 24 hours)
- **Immediate Revocation**: Modifying user status (e.g. `SUSPENDED`) or clicking "Revoke" instantly invalidates the session token hash.

---

## 2. Step-Up Authentication for High-Risk Actions

Certain critical actions require recent authentication freshness even if a user holds an active session:
- **Contract Signing (`contract.sign`)**
- **Authoritative Price Changing (`price.change`)**
- **AI Model Production Promotion (`ai_model.promote`)**
- **Emergency Kill Switch (`ai_kill_switch.activate`)**
- **Tenant Management (`tenant.manage`)**

### Step-Up Workflow:
1. User requests a sensitive action.
2. The `AuthorizationEngine` identifies `requires_step_up = True`.
3. Client prompts user to re-enter their password (and TOTP if configured) via `POST /api/v1/security/step-up`.
4. The server validates credentials and issues a short-lived `step_up_token` (valid for 15 minutes).
5. The high-risk action executes successfully and logs an audit record.
