# Description: create_app.py

## Overview
Initializes the FastAPI application, mounts API routes, configures CORS, and serves static frontend assets.

## Exports & Functions
- `create_app() -> FastAPI`
  - **Description**: Factory function returning the fully configured FastAPI web application.
  - **Routes Exposed**:
    - `GET /api/system-status`: Reports FFmpeg availability, cookie status, and storage directory.
    - `GET /api/cookies/status`: Reports whether cookies are configured and file size.
    - `POST /api/cookies`: Saves YouTube authentication cookies to disk.
    - `DELETE /api/cookies`: Clears configured cookies.
    - `POST /api/info`: Fetches video metadata and available qualities for preview.
    - `POST /api/download`: Validates parameters and triggers background download.
    - `GET /api/progress/{job_id}`: Returns immediate JSON progress snapshot.
    - `GET /api/progress/{job_id}/stream`: Server-Sent Events (SSE) live progress stream.
    - `GET /api/download-file/{job_id}`: Streams completed media file to browser.
    - `GET /api/list-downloads`: Lists files in `downloads/` directory.
    - `GET /`: Mounts `static/` directory with `index.html`.

## Dependencies & Data Flow
- **Imports**: `fastapi`, `pydantic`, `config`, `execute_download`, `fetch_video_info`, `parse_time_range`, `progress_tracker`, `validate_url`.
- **Invoked By**: `start_server.py`.
- **Data Flow**: HTTP/SSE requests from browser -> validation & routing -> backend services -> HTTP/SSE responses.
