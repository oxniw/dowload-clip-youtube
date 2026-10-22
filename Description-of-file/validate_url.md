# Description: validate_url.py

## Overview
Sanitizes and enforces security boundaries on incoming YouTube URLs. Prevents Server-Side Request Forgery (SSRF) and access to internal or unauthorized loopback networks.

## Exports & Functions
- `validate_url(url: str) -> str`
  - **Description**: Validates that an incoming URL string uses permitted schemes (`https`, `http`) and resolves to official YouTube domain names (`youtube.com`, `youtu.be`, etc.). Rejects localhost, RFC1918 private IP ranges, and cloud metadata targets.
  - **Parameters**:
    - `url`: Raw user-provided URL string.
  - **Returns**: Cleaned, verified URL string.
  - **Raises**: `ValueError` if the scheme is missing/disallowed or destination is outside permitted domains.

## Dependencies & Data Flow
- **Imports**: `urllib.parse.urlparse`, `config.ALLOWED_DOMAINS`, `config.ALLOWED_SCHEMES`.
- **Invoked By**: `fetch_video_info.py`, `execute_download.py`, `create_app.py`.
- **Data Flow**: User string input -> URL parsing & domain verification -> safe sanitized URL string.
