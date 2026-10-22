# ==============================================================================
# File: .//Description-of-file/validate_url.md
# Overview: Validates and sanitizes YouTube URLs to prevent SSRF and injection.
# ==============================================================================

import re
from urllib.parse import urlparse
from config import ALLOWED_DOMAINS, ALLOWED_SCHEMES


def validate_url(url: str) -> str:
    """
    Validates that a URL is a legitimate YouTube link and returns the cleaned URL.
    Raises ValueError if invalid or targeting disallowed destinations.
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string.")

    cleaned_url = url.strip()
    parsed = urlparse(cleaned_url)

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only HTTPS/HTTP are permitted.")

    hostname = (parsed.hostname or "").lower()

    if not hostname:
        raise ValueError("URL has no hostname.")

    # Prevent loopback, local network, and private addresses
    disallowed_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "169.254.169.254"}
    if hostname in disallowed_hosts or hostname.startswith("192.168.") or hostname.startswith("10."):
        raise ValueError("Disallowed network destination.")

    # Match allowed domain patterns
    is_allowed = False
    for allowed in ALLOWED_DOMAINS:
        if hostname == allowed or hostname.endswith("." + allowed):
            is_allowed = True
            break

    if not is_allowed:
        raise ValueError("Only official YouTube URLs are supported (youtube.com, youtu.be).")

    return cleaned_url
