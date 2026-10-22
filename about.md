# About This Project

## Purpose
A web-based YouTube video and audio downloader inspired by yt-dlp. It provides a browser interface to inspect video metadata, select desired video resolutions or audio-only formats, trim specific time clips, and monitor download progress in real time.

## Target Audience
Local users and developers who need an intuitive, secure, and self-hosted tool for downloading and clipping YouTube media without relying on ad-heavy third-party websites.

## Technical Architecture & Constraints
- **Language & Runtime**: Python 3.12+
- **Backend Framework**: FastAPI with Starlette and Uvicorn
- **Extraction Engine**: `yt-dlp` Python library behind an isolated adapter layer
- **Media Processing**: System `ffmpeg` called via secure, non-shell subprocess execution
- **Frontend**: Lightweight vanilla HTML5, CSS3, and modern JavaScript (no Node.js build pipeline required)
- **Real-Time Updates**: Server-Sent Events (SSE) streaming progress (percentage, download speed, ETA)
- **Modularity**: Strict function-per-file separation compliant with `/write-script-separated-file-function`
- **Delivery Strategy**: Dual delivery saving media to the local `downloads/` directory while offering direct in-browser download triggers
- **Deployment Targets**: Render (Docker web service with full FFmpeg and unconstrained request execution) and Vercel (`vercel.json` serverless deployment with `/tmp` ephemeral storage).

## Security Boundaries & Rules
- **Input Validation**: Strict domain allowlisting (`youtube.com`, `youtu.be`) and scheme enforcement (`https://`) to prevent SSRF and internal network probing.
- **Path Traversal Protection**: Output filenames and paths are sanitized and strictly locked inside the designated `downloads/` directory.
- **Subprocess Security**: All external commands (e.g., FFmpeg) execute with explicit argument lists without `shell=True`.
- **Resource Constraints**: Maximum clip duration limits and time range bounds checks prevent denial-of-service conditions.

## Explicit Non-Goals
- Multi-user authentication, cloud multi-tenancy, or billing subscriptions.
- Scraping arbitrary non-video web domains.
