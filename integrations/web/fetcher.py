import httpx

from integrations.web.security import SecurityValidationError, validate_url_security
from integrations.web.validator import URLValidator


class WebFetchError(Exception):
    pass


def fetch_html(
    url: str,
    timeout: int = URLValidator.DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = URLValidator.MAX_RESPONSE_BYTES,
) -> str:
    # 1. SSRF Security check before initiating request
    validated_url = validate_url_security(url)

    headers = {
        "User-Agent": "UzaiiResearchBot/1.0 (+https://norths.agency/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        with httpx.Client(
            timeout=timeout,
            follow_redirects=False,  # Manually inspect redirect URLs for SSRF safety
            headers=headers,
        ) as client:
            current_url = validated_url
            redirect_count = 0

            while redirect_count <= URLValidator.MAX_REDIRECTS:
                response = client.get(current_url)

                if response.is_redirect:
                    redirect_count += 1
                    location = response.headers.get("location")
                    if not location:
                        raise WebFetchError("Redirect header missing")

                    # Handle relative vs absolute redirect URLs
                    if location.startswith("/"):
                        from urllib.parse import urljoin

                        next_url = urljoin(current_url, location)
                    else:
                        next_url = location

                    # Validate redirect target for SSRF safety
                    current_url = validate_url_security(next_url)
                    continue

                response.raise_for_status()

                # Read body content with size cap
                content_length = response.headers.get("content-length")
                if content_length and int(content_length) > max_bytes:
                    raise WebFetchError(
                        f"Response exceeds maximum allowed size of {max_bytes} bytes"
                    )

                body = response.text
                if len(body.encode("utf-8")) > max_bytes:
                    raise WebFetchError(
                        f"Downloaded content exceeds maximum limit of {max_bytes} bytes"
                    )

                return body

            raise WebFetchError(
                f"Exceeded maximum redirects ({URLValidator.MAX_REDIRECTS})"
            )

    except SecurityValidationError as e:
        raise WebFetchError(f"SSRF Security Violation: {e!s}") from e
    except httpx.HTTPError as e:
        raise WebFetchError(f"HTTP fetch error for '{url}': {e!s}") from e
    except Exception as e:
        raise WebFetchError(f"Failed to fetch content from '{url}': {e!s}") from e
