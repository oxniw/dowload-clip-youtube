# ==============================================================================
# File: .//Description-of-file/progress_tracker.md
# Overview: Manages download state, real-time metrics, and SSE notification queues.
# ==============================================================================

import asyncio
import threading
import time
from typing import Any, Dict, Optional


class JobProgress:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = "queued"
        self.percentage = 0.0
        self.speed = "0 KB/s"
        self.eta = "calculating..."
        self.filename = ""
        self.file_path: Optional[str] = None
        self.error_message: Optional[str] = None
        self.updated_at = time.time()
        self.listeners: list[asyncio.Queue] = []
        self.lock = threading.Lock()

    def to_dict(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "job_id": self.job_id,
                "status": self.status,
                "percentage": round(self.percentage, 1),
                "speed": self.speed,
                "eta": self.eta,
                "filename": self.filename,
                "has_file": bool(self.file_path),
                "error_message": self.error_message,
            }

    def update(
        self,
        status: Optional[str] = None,
        percentage: Optional[float] = None,
        speed: Optional[str] = None,
        eta: Optional[str] = None,
        filename: Optional[str] = None,
        file_path: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        with self.lock:
            if status is not None:
                self.status = status
            if percentage is not None:
                self.percentage = min(100.0, max(0.0, percentage))
            if speed is not None:
                self.speed = speed
            if eta is not None:
                self.eta = eta
            if filename is not None:
                self.filename = filename
            if file_path is not None:
                self.file_path = file_path
            if error_message is not None:
                self.error_message = error_message
            self.updated_at = time.time()
            data = {
                "job_id": self.job_id,
                "status": self.status,
                "percentage": round(self.percentage, 1),
                "speed": self.speed,
                "eta": self.eta,
                "filename": self.filename,
                "has_file": bool(self.file_path),
                "error_message": self.error_message,
            }

        # Notify any waiting async SSE listeners
        for queue in list(self.listeners):
            try:
                queue.put_nowait(data)
            except Exception:
                pass


class ProgressTracker:
    def __init__(self):
        self._jobs: Dict[str, JobProgress] = {}
        self._lock = threading.Lock()

    def create_job(self, job_id: str) -> JobProgress:
        with self._lock:
            job = JobProgress(job_id)
            self._jobs[job_id] = job
            return job

    def get_job(self, job_id: str) -> Optional[JobProgress]:
        with self._lock:
            return self._jobs.get(job_id)

    def subscribe(self, job_id: str, queue: asyncio.Queue):
        job = self.get_job(job_id)
        if job:
            job.listeners.append(queue)

    def unsubscribe(self, job_id: str, queue: asyncio.Queue):
        job = self.get_job(job_id)
        if job and queue in job.listeners:
            job.listeners.remove(queue)


# Global singleton instance
tracker = ProgressTracker()
