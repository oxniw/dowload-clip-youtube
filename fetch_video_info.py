# ==============================================================================
# File: .//Description-of-file/fetch_video_info.md
# Overview: Fetches metadata, available formats, and duration for a YouTube video.
# ==============================================================================

from typing import Any, Dict, List
import yt_dlp
from config import COOKIES_FILE
from validate_url import validate_url


def format_duration(seconds: int | float | None) -> str:
    """Formats seconds into HH:MM:SS or MM:SS."""
    if seconds is None or seconds <= 0:
        return "Live / Unknown"
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def fetch_video_info(url: str) -> Dict[str, Any]:
    """
    Extracts non-downloading video metadata using yt-dlp.
    """
    clean_url = validate_url(url)

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "skip_download": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web"]
            }
        },
    }

    if COOKIES_FILE.exists():
        ydl_opts["cookiefile"] = str(COOKIES_FILE)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(clean_url, download=False)
        if not info:
            raise RuntimeError("Could not retrieve metadata for the provided URL.")

        raw_formats = info.get("formats", [])
        available_heights = set()
        for f in raw_formats:
            height = f.get("height")
            if height and height >= 144:
                available_heights.add(height)

        # Ensure standard options are available for selection
        for h in (1080, 720, 480, 360):
            available_heights.add(h)

        sorted_heights = sorted(list(available_heights), reverse=True)

        return {
            "id": str(info.get("id", "")),
            "title": str(info.get("title", "Untitled Video")),
            "uploader": str(info.get("uploader", "Unknown Uploader")),
            "duration": info.get("duration", 0),
            "duration_formatted": format_duration(info.get("duration")),
            "thumbnail": str(info.get("thumbnail", "")),
            "view_count": info.get("view_count", 0),
            "webpage_url": str(info.get("webpage_url", clean_url)),
            "available_resolutions": sorted_heights,
        }
