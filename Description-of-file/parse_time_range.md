# Description: parse_time_range.py

## Overview
Parses and validates time range strings for video clipping operations. Enforces chronological order and limits against maximum duration thresholds.

## Exports & Functions
- `time_to_seconds(val: Optional[str | int | float]) -> Optional[float]`
  - **Description**: Converts time notations (`HH:MM:SS`, `MM:SS`, or second values) into total float seconds.
  - **Parameters**:
    - `val`: Raw timestamp input.
  - **Returns**: Float seconds or `None` if input is empty.
- `parse_time_range(start: Optional[str | int | float], end: Optional[str | int | float], total_duration: Optional[float] = None) -> Tuple[Optional[float], Optional[float]]`
  - **Description**: Validates that start time is non-negative, end time exceeds start time, clip duration is within allowed limits, and start time does not exceed total video length.
  - **Parameters**:
    - `start`: Start timestamp.
    - `end`: End timestamp.
    - `total_duration`: Total length of the video in seconds.
  - **Returns**: Validated tuple of `(start_seconds, end_seconds)`.

## Dependencies & Data Flow
- **Imports**: `config.MAX_CLIP_DURATION_SECONDS`.
- **Invoked By**: `create_app.py` (`POST /api/download`).
- **Data Flow**: User string timestamps -> validation logic -> numeric bounds passed to download/clip worker.
