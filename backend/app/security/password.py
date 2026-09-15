"""Password Hashing, Verification, and Policy Validation."""

import hashlib
import hmac
import os
import re
from typing import Tuple

PBKDF2_ITERATIONS = 600_000
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

COMMON_WEAK_PASSWORDS = {
    "password", "password123", "admin123", "welcome123", "letmein", "qwerty12345",
    "12345678", "123456789", "default123", "changeme", "iloveyou", "password1234",
}


def hash_password(password: str) -> str:
    """Hash password securely using PBKDF2-HMAC-SHA256 with random salt."""
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${key.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its stored cryptographic hash."""
    try:
        parts = hashed_password.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        iterations = int(parts[1])
        salt = parts[2]
        expected_hash = parts[3]

        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        )
        return hmac.compare_digest(key.hex(), expected_hash)
    except Exception:
        return False


def validate_password_policy(password: str, user_email: str = "") -> Tuple[bool, str]:
    """Validate password against organizational complexity and safety policy."""
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters."

    if password.lower() in COMMON_WEAK_PASSWORDS:
        return False, "Password is too common and easily guessable."

    if user_email:
        local_part = user_email.split("@")[0].lower()
        if len(local_part) >= 3 and local_part in password.lower():
            return False, "Password cannot contain parts of your email address."

    return True, "Password meets security policy requirements."
