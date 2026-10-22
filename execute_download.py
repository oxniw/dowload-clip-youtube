# ==============================================================================
# File: .//Description-of-file/execute_download.md
# Overview: Orchestrates yt-dlp execution, progress hooking, and post-clipping.
# ==============================================================================

import re
from pathlib import Path
from typing import Optional
import yt_dlp
from build_download_options import build_download_options
from clip_media import clip_media
from config import DOWNLOADS_DIR
from progress_tracker import tracker
from validate_url import validate_url


def clean_ansi(text: str) -> str:
    """Strips terminal ANSI color codes from progress strings."""
    return re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", text).strip()


def execute_download(
    job_id: str,
    url: str,
    audio_only: bool = False,
    audio_format: str = "mp3",
    audio_bitrate: str = "192k",
    video_format: str = "mp4",
    video_quality: str = "best",
    start_seconds: Optional[float] = None,
    end_seconds: Optional[float] = None,
) -> Path:
    """
    Executes media download using yt-dlp and optional clipping via FFmpeg.
    """
    clean_url = validate_url(url)
    job = tracker.get_job(job_id)
    if not job:
        job = tracker.create_job(job_id)

    job.update(status="downloading", percentage=1.0)

    def hook(d: dict):
        status = d.get("status")
        if status == "downloading":
            raw_percent = d.get("_percent_str", "0%")
            clean_percent_str = clean_ansi(raw_percent).replace("%", "")
            try:
                percent = float(clean_percent_str)
            except ValueError:
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                percent = (downloaded / total * 100) if total > 0 else 0.0

            raw_speed = clean_ansi(str(d.get("_speed_str", "N/A")))
            raw_eta = clean_ansi(str(d.get("_eta_str", "N/A")))
            filename = Path(d.get("filename", "")).name

            job.update(
                status="downloading",
                percentage=percent,
                speed=raw_speed,
                eta=raw_eta,
                filename=filename,
            )
        elif status == "finished":
            job.update(status="processing", percentage=95.0, speed="Finalizing", eta="0s")

    opts = build_download_options(
        job_id=job_id,
        output_dir=DOWNLOADS_DIR,
        audio_only=audio_only,
        audio_format=audio_format,
        audio_bitrate=audio_bitrate,
        video_format=video_format,
        video_quality=video_quality,
        progress_hook=hook,
    )

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([clean_url])

        # Locate the downloaded file starting with job_id
        matched_files = list(DOWNLOADS_DIR.glob(f"{job_id}_*"))
        if not matched_files:
            raise FileNotFoundError("Output file could not be located after download.")

        # Sort by modification time to pick the newest resulting file
        downloaded_file = max(matched_files, key=lambda f: f.stat().st_mtime)

        # Apply clipping if requested
        if start_seconds is not None or end_seconds is not None:
            job.update(status="processing", percentage=98.0, speed="Clipping media...")
            downloaded_file = clip_media(downloaded_file, start_seconds, end_seconds)

        job.update(
            status="completed",
            percentage=100.0,
            speed="Done",
            eta="0s",
            filename=downloaded_file.name,
            file_path=str(downloaded_file),
        )
        return downloaded_file

    except Exception as exc:
        job.update(status="error", error_message=str(exc))
        raise exc
