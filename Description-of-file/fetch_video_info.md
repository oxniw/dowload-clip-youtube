# Description: fetch_video_info.py

## Overview
Inspects a YouTube video using `yt-dlp` to extract metadata without downloading full video streams.

## Exports & Functions
- `format_duration(seconds: int | float | None) -> str`
  - **Description**: Formats seconds into human-readable `HH:MM:SS` or `MM:SS` notation.
  - **Parameters**:
    - `seconds`: Duration value in seconds.
  - **Returns**: Formatted duration string.
- `fetch_video_info(url: str) -> Dict[str, Any]`
  - **Description**: Extracts title, author, duration, thumbnail URL, view count, and list of available video resolutions.
  - **Parameters**:
    - `url`: Validated YouTube URL.
  - **Returns**: Dictionary with video metadata and resolution heights.

## Dependencies & Data Flow
- **Imports**: `yt_dlp`, `validate_url.validate_url`.
- **Invoked By**: `create_app.py` (`POST /api/info`).
- **Data Flow**: YouTube URL -> `yt_dlp.YoutubeDL` metadata probe -> structured dictionary sent to frontend.
