# Description: clip_media.py

## Overview
Executes video and audio trimming through FFmpeg using non-shell subprocess execution. Applies fast stream copying with automatic fallback to re-encoding.

## Exports & Functions
- `clip_media(source_path: Path | str, start_seconds: Optional[float] = None, end_seconds: Optional[float] = None) -> Path`
  - **Description**: Verifies that the source file is located within `DOWNLOADS_DIR` to prevent path traversal attacks. Trims the file according to start and end timestamps and removes the unclipped source file upon successful completion.
  - **Parameters**:
    - `source_path`: Path to downloaded media file.
    - `start_seconds`: Clipping offset in seconds.
    - `end_seconds`: Clipping endpoint in seconds.
  - **Returns**: `Path` pointing to the clipped media file.
  - **Raises**: `ValueError` if path escapes downloads directory, `FileNotFoundError` if source file does not exist.

## Dependencies & Data Flow
- **Imports**: `subprocess`, `pathlib.Path`, `config.DOWNLOADS_DIR`.
- **Invoked By**: `execute_download.py`.
- **Data Flow**: Downloaded file + time bounds -> `ffmpeg` subprocess -> trimmed media file.
