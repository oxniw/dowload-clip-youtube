# Description: execute_download.py

## Overview
Coordinates the execution of media downloading via `yt-dlp`, real-time progress callbacks, and post-download clipping via `clip_media`.

## Exports & Functions
- `clean_ansi(text: str) -> str`
  - **Description**: Strips terminal escape codes from raw `yt-dlp` output strings.
  - **Parameters**:
    - `text`: String potentially containing ANSI color characters.
  - **Returns**: Clean string.
- `execute_download(...) -> Path`
  - **Description**: Configures hooks, downloads media streams using `yt-dlp`, finds resulting media files, applies time trimming if requested, and finalizes progress tracking.
  - **Parameters**:
    - `job_id`: Unique identifier for the job.
    - `url`: Validated YouTube URL.
    - `audio_only`: Boolean flag for audio extraction.
    - `audio_format`: Output audio format.
    - `audio_bitrate`: Output audio bitrate.
    - `video_format`: Output video container.
    - `video_quality`: Target resolution height.
    - `start_seconds`: Optional clip start offset.
    - `end_seconds`: Optional clip end offset.
  - **Returns**: `Path` pointing to the final completed file.

## Dependencies & Data Flow
- **Imports**: `yt_dlp`, `build_download_options.build_download_options`, `clip_media.clip_media`, `validate_url.validate_url`, `progress_tracker.tracker`, `config.DOWNLOADS_DIR`.
- **Invoked By**: `create_app.py` (via `BackgroundTasks`).
- **Data Flow**: Job parameters -> `yt-dlp` download -> `clip_media` trimming -> file path saved in `JobProgress`.
