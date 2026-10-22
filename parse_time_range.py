# ==============================================================================
# File: .//Description-of-file/parse_time_range.md
# Overview: Parses and validates start and end timestamps for clipping operations.
# ==============================================================================

from typing import Optional, Tuple
from config import MAX_CLIP_DURATION_SECONDS


def time_to_seconds(val: Optional[str | int | float]) -> Optional[float]:
    """
    Converts HH:MM:SS, MM:SS, or second numbers into total float seconds.
    """
    if val is None:
        return None

    if isinstance(val, (int, float)):
        return max(0.0, float(val))

    val_str = str(val).strip()
    if not val_str:
        return None

    # Match numeric float/int directly
    try:
        sec = float(val_str)
        return max(0.0, sec)
    except ValueError:
        pass

    # Match colon-separated notation
    parts = val_str.split(":")
    if len(parts) > 3 or len(parts) == 0:
        raise ValueError(f"Invalid timestamp format '{val_str}'. Use HH:MM:SS or MM:SS.")

    try:
        numeric_parts = [float(p) for p in parts]
    except ValueError:
        raise ValueError(f"Timestamp contains non-numeric parts: '{val_str}'.")

    if len(numeric_parts) == 3:
        hours, minutes, seconds = numeric_parts
        total = hours * 3600 + minutes * 60 + seconds
    elif len(numeric_parts) == 2:
        minutes, seconds = numeric_parts
        total = minutes * 60 + seconds
    else:
        total = numeric_parts[0]

    return max(0.0, total)


def parse_time_range(
    start: Optional[str | int | float],
    end: Optional[str | int | float],
    total_duration: Optional[float] = None,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Validates clipping boundaries against maximum constraints and video length.
    """
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)

    if start_sec is not None and end_sec is not None:
        if end_sec <= start_sec:
            raise ValueError(f"End time ({end_sec}s) must be greater than start time ({start_sec}s).")
        duration = end_sec - start_sec
        if duration > MAX_CLIP_DURATION_SECONDS:
            raise ValueError(
                f"Requested clip duration ({duration}s) exceeds maximum allowed limit ({MAX_CLIP_DURATION_SECONDS}s)."
            )

    if total_duration and total_duration > 0:
        if start_sec is not None and start_sec >= total_duration:
            raise ValueError(f"Start time ({start_sec}s) exceeds total video duration ({total_duration}s).")

    return start_sec, end_sec
