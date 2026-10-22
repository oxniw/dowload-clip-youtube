# ==============================================================================
# File: .//Description-of-file/asgi.md
# Overview: ASGI entry point exposing the FastAPI application instance.
# ==============================================================================

from create_app import create_app

# Application instance consumed by ASGI servers (Uvicorn, Gunicorn, Vercel)
app = create_app()
