# ==============================================================================
# File: .//Description-of-file/config.md
# Overview: Central configuration constants and file paths for the downloader.
# ==============================================================================

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent

# Support serverless read-only filesystems (Vercel uses /tmp) and custom paths
custom_downloads = os.environ.get("DOWNLOADS_DIR")
if custom_downloads:
    DOWNLOADS_DIR = Path(custom_downloads).resolve()
elif os.environ.get("VERCEL"):
    DOWNLOADS_DIR = Path("/tmp/downloads")
else:
    DOWNLOADS_DIR = BASE_DIR / "downloads"

STATIC_DIR = BASE_DIR / "static"
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Server Defaults with Environment Override for Render and Cloud Hosts
DEFAULT_HOST = os.environ.get("HOST", "0.0.0.0" if (os.environ.get("RENDER") or os.environ.get("PORT")) else "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("PORT", 8000))

# Security & Validation
ALLOWED_DOMAINS = (
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "music.youtube.com",
)

ALLOWED_SCHEMES = ("https", "http")

# Format Options
COOKIES_FILE = BASE_DIR / "cookies.txt"
SUPPORTED_VIDEO_FORMATS = ("mp4", "mkv")
SUPPORTED_AUDIO_FORMATS = ("mp3", "m4a", "wav", "flac")
SUPPORTED_QUALITIES = ("best", "1080", "720", "480", "360")

# Processing Limits
MAX_CLIP_DURATION_SECONDS = 7200  # 2 hours maximum per clip
DEFAULT_AUDIO_BITRATE = "192k"
PROGRESS_CLEANUP_SECONDS = 3600
