# ==============================================================================
# File: .//Description-of-file/start_server.md
# Overview: Launches the Uvicorn web server and triggers the default web browser.
# ==============================================================================

import os
import threading
import time
import webbrowser
import uvicorn
from config import DEFAULT_HOST, DEFAULT_PORT
from create_app import create_app


def open_browser_delayed(url: str, delay_seconds: float = 1.0):
    """Waits for server initialization before launching browser."""
    time.sleep(delay_seconds)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def start_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    auto_open: bool = True,
):
    """
    Spawns the local web application server.
    """
    app = create_app()
    server_url = f"http://{host}:{port}"

    # Do not attempt to open browser on headless/cloud deployment platforms
    is_cloud_env = bool(os.environ.get("RENDER") or os.environ.get("PORT") or os.environ.get("VERCEL"))
    if auto_open and not is_cloud_env:
        threading.Thread(
            target=open_browser_delayed,
            args=(server_url, 1.2),
            daemon=True,
        ).start()

    print(f"\n=======================================================")
    print(f" YouTube Downloader & Clipper running at: {server_url}")
    print(f"=======================================================\n")

    uvicorn.run(app, host=host, port=port, log_level="info")
