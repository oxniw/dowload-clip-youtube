# ==============================================================================
# File: .//Description-of-file/clip_media.md
# Overview: Trims media files using non-shell FFmpeg subprocess calls.
# ==============================================================================

import os
import subprocess
from pathlib import Path
from typing import Optional
from config import DOWNLOADS_DIR


def clip_media(
    source_path: Path | str,
    start_seconds: Optional[float] = None,
    end_seconds: Optional[float] = None,
) -> Path:
    """
    Cuts a media file between start_seconds and end_seconds using FFmpeg safely.
    Returns the Path to the trimmed file.
    """
    src = Path(source_path).resolve()
    base_downloads = DOWNLOADS_DIR.resolve()

    # Prevent directory traversal
    if not str(src).startswith(str(base_downloads)):
        raise ValueError("Invalid file location.")

    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    if start_seconds is None and end_seconds is None:
        return src

    trimmed_filename = f"clipped_{src.name}"
    dest = (src.parent / trimmed_filename).resolve()

    cmd = ["ffmpeg", "-y"]

    if start_seconds is not None:
        cmd.extend(["-ss", f"{start_seconds:.3f}"])

    if end_seconds is not None:
        if start_seconds is not None:
            # -t specifies duration from start
            duration = max(0.01, end_seconds - start_seconds)
            cmd.extend(["-t", f"{duration:.3f}"])
        else:
            cmd.extend(["-to", f"{end_seconds:.3f}"])

    cmd.extend(["-i", str(src), "-c", "copy", str(dest)])

    try:
        # Fast stream-copy cut
        subprocess.run(
            cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=180,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # Fallback to re-encoding if stream copy fails on boundary keyframes
        cmd_reencode = ["ffmpeg", "-y"]
        if start_seconds is not None:
            cmd_reencode.extend(["-ss", f"{start_seconds:.3f}"])
        if end_seconds is not None:
            if start_seconds is not None:
                duration = max(0.01, end_seconds - start_seconds)
                cmd_reencode.extend(["-t", f"{duration:.3f}"])
            else:
                cmd_reencode.extend(["-to", f"{end_seconds:.3f}"])

        cmd_reencode.extend(["-i", str(src), str(dest)])
        subprocess.run(
            cmd_reencode,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=300,
        )

    # Clean up the larger uncut source file to save disk space
    try:
        if dest.exists() and dest.stat().st_size > 0:
            if src != dest and src.exists():
                src.unlink()
    except Exception:
        pass

    return dest
