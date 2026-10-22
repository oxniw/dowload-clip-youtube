# ==============================================================================
# File: .//Description-of-file/create_app.md
# Overview: Instantiates and configures the FastAPI web application and API routes.
# ==============================================================================

import asyncio
import json
import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from config import COOKIES_FILE, DOWNLOADS_DIR, STATIC_DIR
from execute_download import execute_download
from fetch_video_info import fetch_video_info
from parse_time_range import parse_time_range
from progress_tracker import tracker
from validate_url import validate_url


class InfoRequest(BaseModel):
    url: str = Field(..., description="YouTube video URL")


class DownloadRequest(BaseModel):
    url: str
    audio_only: bool = False
    audio_format: str = "mp3"
    audio_bitrate: str = "192k"
    video_format: str = "mp4"
    video_quality: str = "best"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_duration: Optional[float] = None


class CookiePayload(BaseModel):
    content: str


def create_app() -> FastAPI:
    """
    Creates and wires the FastAPI application.
    """
    app = FastAPI(title="YouTube Downloader & Clipper", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/system-status")
    def get_system_status():
        ffmpeg_path = shutil.which("ffmpeg")
        has_cookies = COOKIES_FILE.exists() and COOKIES_FILE.stat().st_size > 0
        return {
            "ffmpeg_available": bool(ffmpeg_path),
            "ffmpeg_path": ffmpeg_path or "Not found",
            "cookies_configured": has_cookies,
            "downloads_dir": str(DOWNLOADS_DIR),
        }

    @app.get("/api/cookies/status")
    def api_cookie_status():
        exists = COOKIES_FILE.exists() and COOKIES_FILE.stat().st_size > 0
        return {
            "configured": exists,
            "size_bytes": COOKIES_FILE.stat().st_size if exists else 0,
        }

    @app.post("/api/cookies")
    def api_save_cookies(payload: CookiePayload):
        text = payload.content.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Cookie content cannot be empty.")
        COOKIES_FILE.write_text(text, encoding="utf-8")
        return {"success": True, "message": "Cookies saved successfully."}

    @app.delete("/api/cookies")
    def api_delete_cookies():
        if COOKIES_FILE.exists():
            COOKIES_FILE.unlink()
        return {"success": True, "message": "Cookies deleted."}

    @app.post("/api/info")
    def api_video_info(payload: InfoRequest):
        try:
            info = fetch_video_info(payload.url)
            return {"success": True, "data": info}
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Failed to fetch video details: {err}")

    @app.post("/api/download")
    def api_start_download(payload: DownloadRequest, background_tasks: BackgroundTasks):
        try:
            clean_url = validate_url(payload.url)
            start_sec, end_sec = parse_time_range(
                payload.start_time, payload.end_time, payload.total_duration
            )
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

        job_id = uuid.uuid4().hex[:12]
        tracker.create_job(job_id)

        # Run download in background thread
        background_tasks.add_task(
            execute_download,
            job_id=job_id,
            url=clean_url,
            audio_only=payload.audio_only,
            audio_format=payload.audio_format,
            audio_bitrate=payload.audio_bitrate,
            video_format=payload.video_format,
            video_quality=payload.video_quality,
            start_seconds=start_sec,
            end_seconds=end_sec,
        )

        return {"success": True, "job_id": job_id}

    @app.get("/api/progress/{job_id}")
    def api_get_progress(job_id: str):
        job = tracker.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job.to_dict()

    @app.get("/api/progress/{job_id}/stream")
    async def api_stream_progress(job_id: str):
        job = tracker.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        async def event_generator():
            queue: asyncio.Queue = asyncio.Queue()
            tracker.subscribe(job_id, queue)
            # Send initial snapshot immediately
            initial_data = job.to_dict()
            yield f"data: {json.dumps(initial_data)}\n\n"

            try:
                while True:
                    # Timeout after 25 seconds of silence to keep-alive
                    try:
                        update_data = await asyncio.wait_for(queue.get(), timeout=25.0)
                        yield f"data: {json.dumps(update_data)}\n\n"
                        if update_data.get("status") in ("completed", "error"):
                            break
                    except asyncio.TimeoutError:
                        yield f": keepalive\n\n"
            finally:
                tracker.unsubscribe(job_id, queue)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    @app.get("/api/download-file/{job_id}")
    def api_download_file(job_id: str):
        job = tracker.get_job(job_id)
        if not job or not job.file_path:
            raise HTTPException(status_code=404, detail="File not ready or job not found")

        target_file = Path(job.file_path).resolve()
        base_dir = DOWNLOADS_DIR.resolve()

        # Enforce strict path security check
        if not str(target_file).startswith(str(base_dir)) or not target_file.is_file():
            raise HTTPException(status_code=403, detail="Unauthorized file access.")

        # Strip job_id prefix from user-facing download name
        download_name = target_file.name
        if download_name.startswith(f"{job_id}_"):
            download_name = download_name[len(job_id) + 1 :]
        elif download_name.startswith(f"clipped_{job_id}_"):
            download_name = "clipped_" + download_name[len(f"clipped_{job_id}_") :]

        return FileResponse(
            path=str(target_file),
            filename=download_name,
            media_type="application/octet-stream",
        )

    @app.get("/api/list-downloads")
    def api_list_downloads():
        files = []
        for p in DOWNLOADS_DIR.iterdir():
            if p.is_file() and p.name != ".gitkeep":
                files.append(
                    {
                        "filename": p.name,
                        "size_mb": round(p.stat().st_size / (1024 * 1024), 2),
                        "modified": p.stat().st_mtime,
                    }
                )
        files.sort(key=lambda x: x["modified"], reverse=True)
        return {"downloads": files}

    # Mount static frontend
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app
