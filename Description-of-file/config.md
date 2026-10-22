# Description: config.py

## Overview
Stores application-wide configuration constants, file paths, format whitelists, limits, and server binding defaults. Automatically detects cloud environments like Render and Vercel.

## Exports & Constants
- `BASE_DIR: Path`: Absolute path to the project root directory.
- `DOWNLOADS_DIR: Path`: Target storage directory for downloaded and clipped media files. Falls back to `/tmp/downloads` in serverless environments (`VERCEL`) or respects custom `DOWNLOADS_DIR`.
- `STATIC_DIR: Path`: Directory containing frontend static assets (HTML, CSS, JS).
- `DEFAULT_HOST: str`: Host binding IP (`0.0.0.0` when running under cloud environments with `PORT` or `RENDER`, otherwise `127.0.0.1`).
- `DEFAULT_PORT: int`: Server port reading from the `PORT` environment variable (default: `8000`).
- `ALLOWED_DOMAINS: Tuple[str, ...]`: Whitelist of permitted YouTube domain names to prevent SSRF attacks.
- `ALLOWED_SCHEMES: Tuple[str, ...]`: Whitelist of valid network schemes (`https`, `http`).
- `SUPPORTED_VIDEO_FORMATS: Tuple[str, ...]`: Allowed output video containers (`mp4`, `mkv`).
- `SUPPORTED_AUDIO_FORMATS: Tuple[str, ...]`: Allowed audio codecs (`mp3`, `m4a`, `wav`, `flac`).
- `SUPPORTED_QUALITIES: Tuple[str, ...]`: Supported resolution height filters.
- `MAX_CLIP_DURATION_SECONDS: int`: Hard limit on requested clipping duration (7200 seconds / 2 hours).
- `DEFAULT_AUDIO_BITRATE: str`: Default bitrate for audio extraction (`192k`).

## Dependencies & Data Flow
- **Imports**: `os`, `pathlib.Path`
- **Invoked By**: `validate_url.py`, `build_download_options.py`, `clip_media.py`, `execute_download.py`, `create_app.py`, `start_server.py`, `main.py`.
- **Data Flow**: Reads OS environment variables and supplies static parameters and directory paths across the pipeline.
