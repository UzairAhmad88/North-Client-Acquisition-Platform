# Authentication Foundation Guide

## Architecture Overview
The **Uzaii Develop By North's** authentication subsystem enforces a standards-based, secure identity boundary.

```text
Unauthenticated Client
        │  (POST /api/v1/auth/login)
        ▼
   FastAPI Backend
        │  (PBKDF2-HMAC-SHA256 verification & email normalization)
        ▼
   JWT Access Token Issued (HS256)
        │
        ▼
Authenticated API Requests (Bearer Token)
        │  (Depends(get_current_user))
        ▼
   Protected Resources
```

## Security Specifications

### Password Hashing
- **Algorithm**: PBKDF2-HMAC-SHA256
- **Iterations**: 600,000
- **Salt**: 16-byte cryptographically secure random salt (`os.urandom(16)`)
- **Format**: `pbkdf2_sha256$600000$<salt>$<hash>`
- **Verification**: Constant-time string comparison via `hmac.compare_digest`.

### Identity Normalization
- All user emails are normalized via `email.strip().lower()` before lookup, registration, or authentication to prevent identity duplicates and case-folding bypasses.

### JWT Access Tokens
- **Algorithm**: HS256
- **Signing Secret**: Configured via `settings.secret_key`
- **Claims**: `sub` (User UUID), `role` (Role string), `iat` (Issued at), `exp` (Expiration timestamp)
- **Token Expiration**: Default 24 hours (1,440 minutes).

## Database Schema (`users` Table)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY CONSTRAINT pk_users DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL CONSTRAINT uq_users_email UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    role VARCHAR(50) NOT NULL DEFAULT 'MEMBER',
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE UNIQUE INDEX ix_users_email ON users(email);
```

## API Endpoints (`/api/v1/auth`)

| Method | Route | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Registers a new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticates user & issues JWT token | No |
| `POST` | `/api/v1/auth/logout` | Client logout & token clearing | No |
| `GET` | `/api/v1/auth/me` | Fetches authenticated user identity | Yes |
| `GET` | `/api/v1/auth/protected` | Test endpoint verifying protected route access | Yes |

### Error Response Codes
- `AUTH_REQUIRED` (401): Missing, expired, or malformed authentication token
- `FORBIDDEN` (403): Account is inactive (`is_active = false`)
- `DUPLICATE_ACCOUNT` (400): Email is already registered
- `VALIDATION_ERROR` (422): Malformed input payload or weak password (<8 characters)

## Backend Dependencies (`app.api.deps`)
- `get_current_user`: Resolves JWT token from `Authorization: Bearer <token>` header, verifies signature and expiration, and fetches user from `UserRepository`.
- `get_current_active_user`: Ensures `user.is_active` is true.

## Frontend Integration
- **Auth Provider**: `frontend/lib/auth/auth-context.tsx` provides `user`, `token`, `login()`, `logout()`, and `isLoading`.
- **API Client**: `frontend/lib/api/client.ts` automatically attaches `Authorization: Bearer <token>` to requests when available.
- **Login UI**: `frontend/app/(auth)/login/page.tsx` features a calm, humanic sign-in form with error feedback and loading state.
- **Route Guard**: `frontend/app/(dashboard)/layout.tsx` checks authentication state and redirects unauthenticated users to `/login`.
