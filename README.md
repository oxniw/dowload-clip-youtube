# YouTube Downloader & Clipper

A self-hosted web application for inspecting YouTube videos, downloading custom video resolutions or extracted audio, trimming specific time clips, and monitoring progress in real time.

## Features
- **Video & Audio Downloads**: Download video streams (1080p, 720p, 480p, 360p, Best) or extract audio (MP3, M4A, WAV, FLAC).
- **Time Clipping**: Cut and save specific segments by setting start and end timestamps.
- **Live Progress**: Streams percentage, download speed, and ETA via Server-Sent Events (SSE).
- **Dual Delivery**: Saves completed files to the local `downloads/` directory and triggers an in-browser download.
- **Security Protections**: Prevents SSRF attacks, disallows path traversal outside `downloads/`, and runs FFmpeg subprocesses without shell invocation.

## Requirements
- Python 3.10+
- FFmpeg on system PATH (used for stream merging and clipping)

## Local Installation & Startup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The server binds to `http://127.0.0.1:8000` and automatically opens your web browser.

Optional startup flags:
- `--host <ip>`: Bind to a custom IP address (default: `127.0.0.1`)
- `--port <port>`: Bind to a custom port (default: `8000`)
- `--no-browser`: Start server without launching the browser

---

## Deployment Guide

### Option 1: Render (Recommended for yt-dlp + FFmpeg)

Render provides Docker containers with persistent execution and full system packages, making it ideal for media processing.

1. Push this repository to GitHub or GitLab.
2. Log in to [Render](https://render.com).
3. Click **New +** > **Web Service**.
4. Select your repository.
5. Render detects the [`Dockerfile`](Dockerfile) or [`render.yaml`](render.yaml) automatically:
   - **Environment**: Docker
   - **Health Check Path**: `/api/system-status`
6. Click **Deploy Web Service**.

Render automatically assigns a dynamic port via `$PORT` and binds traffic cleanly.

### Option 2: Vercel

Vercel hosts serverless functions and static assets. The configuration is provided in [`vercel.json`](vercel.json) pointing to [`asgi.py`](asgi.py).

1. Install the Vercel CLI or connect your GitHub repository in the Vercel dashboard:
```bash
npm install -g vercel
vercel
```
2. Follow the interactive prompts to link and deploy.

> **Important Serverless Note**: Vercel serverless functions have a 10-second execution limit on free tiers (max 60s/300s on Pro plans) and a 500MB `/tmp` disk limit. For large video downloads and heavy FFmpeg processing, Render is strongly recommended.

---

## Project Structure
- `main.py`: Entry point for launching the server.
- `asgi.py`: Production ASGI entry point for cloud runners.
- `start_server.py`: Spawns Uvicorn and controls browser launch.
- `create_app.py`: Sets up FastAPI routing, SSE streaming, and file delivery.
- `execute_download.py`: Runs yt-dlp pipelines with progress hooks.
- `clip_media.py`: Cuts media files via FFmpeg.
- `build_download_options.py`: Builds sanitized yt-dlp option dictionaries.
- `progress_tracker.py`: Thread-safe state store for active jobs.
- `parse_time_range.py`: Validates start and end timestamps.
- `fetch_video_info.py`: Inspects video metadata.
- `validate_url.py`: Verifies YouTube domains and guards against SSRF.
- `config.py`: Central settings, paths, and environment variable bindings.
- `static/`: HTML, CSS, and JavaScript for the web dashboard.
- `Description-of-file/`: Dedicated markdown documentation for each module.
- `Dockerfile`: Debian-slim container image bundling Python and FFmpeg.
- `render.yaml`: Infrastructure-as-code blueprint for Render.
- `vercel.json`: Serverless deployment configuration for Vercel.
- `about.md`: Project purpose, architecture, and security constraints.
- `version.md`: Project update logs.
