import ipaddress
import socket
from urllib.parse import urlparse

FORBIDDEN_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

BLOCKED_HOSTNAMES = {"localhost", "loopback", "metadata.google.internal"}


class SecurityValidationError(Exception):
    pass


def validate_url_security(url: str) -> str:
    if not url or not isinstance(url, str):
        raise SecurityValidationError("Invalid URL format")

    cleaned_url = url.strip()
    parsed = urlparse(cleaned_url)

    if parsed.scheme.lower() not in ("http", "https"):
        raise SecurityValidationError(
            f"Blocked scheme: '{parsed.scheme}'. Only 'http' and 'https' are allowed."
        )

    hostname = parsed.hostname
    if not hostname:
        raise SecurityValidationError("URL must contain a valid hostname")

    if hostname.lower() in BLOCKED_HOSTNAMES:
        raise SecurityValidationError(f"Target hostname '{hostname}' is blocked")

    # Resolve IP address to detect internal/private/loopback SSRF targets
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        for res in addr_info:
            ip_str = res[4][0]
            try:
                ip_obj = ipaddress.ip_address(ip_str)
                for net in FORBIDDEN_NETWORKS:
                    if ip_obj in net:
                        raise SecurityValidationError(
                            f"SSRF Protection: Hostname '{hostname}' resolves to private/blocked IP '{ip_str}'"
                        )
            except ValueError:
                continue
    except socket.gaierror:
        raise SecurityValidationError(f"Could not resolve hostname '{hostname}'")

    return cleaned_url
