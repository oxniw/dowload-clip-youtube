# Description: progress_tracker.py

## Overview
Provides a thread-safe state store for active download jobs and powers real-time updates via Server-Sent Events (SSE).

## Exports & Classes
- `class JobProgress`: Encapsulates status, percentage, speed, ETA, filename, file path, and asynchronous SSE subscriber queues for an individual download job.
  - `to_dict() -> Dict[str, Any]`: Returns a JSON-serializable snapshot of current progress.
  - `update(...)`: Updates job state metrics under lock and broadcasts changes to all active listener queues.
- `class ProgressTracker`: Registry managing active `JobProgress` instances.
  - `create_job(job_id: str) -> JobProgress`: Allocates and registers a new job.
  - `get_job(job_id: str) -> Optional[JobProgress]`: Retrieves job by ID.
  - `subscribe(job_id: str, queue: asyncio.Queue)`: Adds an async queue listener.
  - `unsubscribe(job_id: str, queue: asyncio.Queue)`: Removes an async queue listener.
- `tracker: ProgressTracker`: Global singleton instance.

## Dependencies & Data Flow
- **Imports**: `asyncio`, `threading`, `time`.
- **Invoked By**: `execute_download.py`, `create_app.py`.
- **Data Flow**: `yt-dlp` download hook updates `JobProgress` -> async queues notify SSE clients in browser.
