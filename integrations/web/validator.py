from urllib.parse import urlparse, urlunparse

from integrations.web.security import SecurityValidationError, validate_url_security


class URLValidator:
    DEFAULT_TIMEOUT_SECONDS = 15
    MAX_RESPONSE_BYTES = 5_000_000  # 5 MB
    MAX_REDIRECTS = 3

    @staticmethod
    def sanitize_and_validate(url: str) -> str:
        validated_url = validate_url_security(url)
        parsed = urlparse(validated_url)

        # Normalize scheme & netloc to lowercase
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Reconstruct canonical URL
        normalized = urlunparse(
            (scheme, netloc, parsed.path, parsed.params, parsed.query, "")
        )
        return normalized

    @staticmethod
    def is_safe_url(url: str) -> bool:
        try:
            URLValidator.sanitize_and_validate(url)
            return True
        except SecurityValidationError:
            return False
