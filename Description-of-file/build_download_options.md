# Description: build_download_options.py

## Overview
Constructs a sanitized options dictionary for `yt-dlp` based on requested audio/video format, quality level, output naming templates, and progress hooks.

## Exports & Functions
- `build_download_options(...) -> Dict[str, Any]`
  - **Description**: Configures format selection strings, postprocessors, output templates, and file naming rules.
  - **Parameters**:
    - `job_id`: Unique identifier for the download job.
    - `output_dir`: Target path for media storage (defaults to `DOWNLOADS_DIR`).
    - `audio_only`: Boolean flag indicating audio-only extraction.
    - `audio_format`: Output audio format (`mp3`, `m4a`, `wav`, `flac`).
    - `audio_bitrate`: Target audio bitrate string.
    - `video_format`: Output video container (`mp4`, `mkv`).
    - `video_quality`: Maximum video resolution height or `"best"`.
    - `progress_hook`: Callback function invoked by `yt-dlp` on progress events.
  - **Returns**: Dictionary formatted for `yt_dlp.YoutubeDL`.

## Dependencies & Data Flow
- **Imports**: `config.COOKIES_FILE`, `config.DOWNLOADS_DIR`, `config.SUPPORTED_AUDIO_FORMATS`, `config.SUPPORTED_VIDEO_FORMATS`.
- **Invoked By**: `execute_download.py`.
- **Data Flow**: High-level job specifications -> validated `yt-dlp` configuration dictionary with `android`/`ios` client rotation.
