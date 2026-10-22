# ==============================================================================
# File: .//Description-of-file/build_download_options.md
# Overview: Generates yt-dlp option dictionaries based on target format and quality.
# ==============================================================================

from typing import Any, Callable, Dict, Optional
from pathlib import Path
from config import DOWNLOADS_DIR, SUPPORTED_AUDIO_FORMATS, SUPPORTED_VIDEO_FORMATS


def build_download_options(
    job_id: str,
    output_dir: Path = DOWNLOADS_DIR,
    audio_only: bool = False,
    audio_format: str = "mp3",
    audio_bitrate: str = "192k",
    video_format: str = "mp4",
    video_quality: str = "best",
    progress_hook: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """
    Constructs a sanitized dictionary of yt-dlp execution options.
    """
    # Sanitize output filename template
    safe_outtmpl = str(output_dir / f"{job_id}_%(title).100B.%(ext)s")

    opts: Dict[str, Any] = {
        "outtmpl": safe_outtmpl,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
        "windowsfilenames": True,
        "noplaylist": True,
    }

    if progress_hook:
        opts["progress_hooks"] = [progress_hook]

    if audio_only:
        selected_audio = audio_format.lower() if audio_format.lower() in SUPPORTED_AUDIO_FORMATS else "mp3"
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": selected_audio,
                "preferredquality": audio_bitrate.replace("k", ""),
            }
        ]
    else:
        selected_container = video_format.lower() if video_format.lower() in SUPPORTED_VIDEO_FORMATS else "mp4"

        if video_quality in ("best", "", None):
            format_spec = f"bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
        else:
            try:
                height = int(video_quality)
                format_spec = (
                    f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/"
                    f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
                )
            except ValueError:
                format_spec = "bestvideo+bestaudio/best"

        opts["format"] = format_spec
        opts["merge_output_format"] = selected_container

    return opts
