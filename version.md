# Project Version History

## [Unreleased] - 2026-10-22

### Added
- Modular YouTube downloader application using FastAPI and yt-dlp.
- Function-per-file architecture with dedicated `Description-of-file/` technical references.
- Real-time download progress tracking with Server-Sent Events (SSE).
- Support for video quality selection (1080p, 720p, 480p, best) and audio-only extraction (MP3, M4A, WAV, FLAC).
- Time range clipping capability via non-shell FFmpeg execution.
- Security enforcement against SSRF, directory traversal, and command injection.
- Modern single-page web interface with responsive dark mode and immediate browser download triggers.
- Cloud deployment configurations for Render (`Dockerfile`, `render.yaml`) and Vercel (`vercel.json`, `asgi.py`).
- Dynamic port and host binding reading `PORT` and `HOST` environment variables.
- Dynamic storage resolution defaulting to `/tmp/downloads` in serverless environments.
